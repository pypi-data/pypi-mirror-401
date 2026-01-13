"""
Batching strategies for high-throughput inference.

Supports:
- Static batching (fixed batch size)
- Dynamic batching (variable batch size with padding)
- Continuous batching (in-flight batching like vLLM)
"""

import torch
import torch.nn as nn
from typing import Optional, List, Dict, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import threading
from queue import Queue, Empty
import heapq


class BatchingStrategy(Enum):
    """Batching strategies."""
    STATIC = "static"        # Fixed batch size, wait for full batch
    DYNAMIC = "dynamic"      # Variable size, pad sequences
    CONTINUOUS = "continuous" # In-flight batching (vLLM-style)


@dataclass
class BatchingConfig:
    """Configuration for batching."""
    strategy: BatchingStrategy = BatchingStrategy.DYNAMIC

    # Batch limits
    max_batch_size: int = 32
    max_tokens_per_batch: int = 4096  # For continuous batching

    # Timing
    max_wait_ms: float = 50.0  # Max time to wait for more requests

    # Padding
    pad_token_id: int = 0

    # Priority
    use_priority_queue: bool = False


@dataclass
class InferenceRequest:
    """A single inference request."""
    request_id: str
    input_ids: List[int]
    max_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9
    priority: int = 0  # Higher = more priority

    # State
    generated_ids: List[int] = field(default_factory=list)
    is_complete: bool = False
    start_time: float = field(default_factory=time.perf_counter)

    def __lt__(self, other):
        """For priority queue ordering."""
        return self.priority > other.priority  # Higher priority first


@dataclass
class BatchResult:
    """Result of a batched inference step."""
    request_ids: List[str]
    next_tokens: torch.Tensor
    finished: List[str]


class BatchScheduler:
    """
    Schedules requests into efficient batches.

    Implements multiple batching strategies for different use cases.
    """

    def __init__(self, config: Optional[BatchingConfig] = None):
        self.config = config or BatchingConfig()

        # Request queue
        if self.config.use_priority_queue:
            self.queue: List[InferenceRequest] = []  # heapq
        else:
            self.queue: Queue = Queue()

        # Active requests (for continuous batching)
        self.active_requests: Dict[str, InferenceRequest] = {}

        # Lock for thread safety
        self._lock = threading.Lock()

        # Stats
        self.stats = {
            "requests_processed": 0,
            "batches_processed": 0,
            "total_tokens": 0,
            "avg_batch_size": 0.0,
        }

    def add_request(self, request: InferenceRequest):
        """Add a request to the queue."""
        with self._lock:
            if self.config.use_priority_queue:
                heapq.heappush(self.queue, request)
            else:
                self.queue.put(request)

    def get_batch(self) -> Optional[List[InferenceRequest]]:
        """
        Get the next batch of requests.

        Returns:
            List of requests to process, or None if queue is empty
        """
        with self._lock:
            if self.config.strategy == BatchingStrategy.STATIC:
                return self._get_static_batch()
            elif self.config.strategy == BatchingStrategy.DYNAMIC:
                return self._get_dynamic_batch()
            else:  # CONTINUOUS
                return self._get_continuous_batch()

    def _get_static_batch(self) -> Optional[List[InferenceRequest]]:
        """Get a fixed-size batch."""
        batch = []

        while len(batch) < self.config.max_batch_size:
            try:
                if self.config.use_priority_queue and self.queue:
                    request = heapq.heappop(self.queue)
                else:
                    request = self.queue.get_nowait()
                batch.append(request)
            except Empty:
                break

        return batch if batch else None

    def _get_dynamic_batch(self) -> Optional[List[InferenceRequest]]:
        """Get a dynamic batch with timeout."""
        batch = []
        start_time = time.perf_counter()
        max_wait_sec = self.config.max_wait_ms / 1000.0

        while len(batch) < self.config.max_batch_size:
            elapsed = time.perf_counter() - start_time
            if elapsed > max_wait_sec and batch:
                break

            remaining_wait = max(0, max_wait_sec - elapsed)

            try:
                if self.config.use_priority_queue:
                    if self.queue:
                        request = heapq.heappop(self.queue)
                        batch.append(request)
                    elif not batch:
                        return None
                    else:
                        break
                else:
                    request = self.queue.get(timeout=remaining_wait)
                    batch.append(request)
            except Empty:
                break

        return batch if batch else None

    def _get_continuous_batch(self) -> Optional[List[InferenceRequest]]:
        """Get batch for continuous batching (including active requests)."""
        batch = []
        total_tokens = 0

        # First, include active requests
        for req_id, request in list(self.active_requests.items()):
            if not request.is_complete:
                seq_len = len(request.input_ids) + len(request.generated_ids)
                if total_tokens + seq_len <= self.config.max_tokens_per_batch:
                    batch.append(request)
                    total_tokens += seq_len

        # Then add new requests
        while (len(batch) < self.config.max_batch_size and
               total_tokens < self.config.max_tokens_per_batch):
            try:
                if self.config.use_priority_queue:
                    if not self.queue:
                        break
                    request = heapq.heappop(self.queue)
                else:
                    request = self.queue.get_nowait()

                seq_len = len(request.input_ids)
                if total_tokens + seq_len <= self.config.max_tokens_per_batch:
                    batch.append(request)
                    self.active_requests[request.request_id] = request
                    total_tokens += seq_len
                else:
                    # Put back if doesn't fit
                    if self.config.use_priority_queue:
                        heapq.heappush(self.queue, request)
                    else:
                        self.queue.put(request)
                    break
            except Empty:
                break

        return batch if batch else None

    def mark_complete(self, request_id: str):
        """Mark a request as complete (for continuous batching)."""
        with self._lock:
            if request_id in self.active_requests:
                self.active_requests[request_id].is_complete = True
                del self.active_requests[request_id]

    def update_stats(self, batch_size: int, tokens: int):
        """Update statistics."""
        self.stats["requests_processed"] += batch_size
        self.stats["batches_processed"] += 1
        self.stats["total_tokens"] += tokens
        self.stats["avg_batch_size"] = (
            self.stats["requests_processed"] /
            max(1, self.stats["batches_processed"])
        )


class ContinuousBatcher:
    """
    Continuous batching engine for maximum throughput.

    Implements in-flight batching similar to vLLM, where new requests
    can join a batch while others are still generating.
    """

    def __init__(
        self,
        model: nn.Module,
        tokenizer: Any,
        config: Optional[BatchingConfig] = None,
        device: torch.device = None
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.config = config or BatchingConfig(strategy=BatchingStrategy.CONTINUOUS)
        self.device = device or next(model.parameters()).device

        self.scheduler = BatchScheduler(self.config)

        # Request completion callbacks
        self.callbacks: Dict[str, Callable[[str], None]] = {}

        # Running state
        self.is_running = False
        self._thread: Optional[threading.Thread] = None

    def submit(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
        callback: Optional[Callable[[str], None]] = None,
        priority: int = 0
    ) -> str:
        """
        Submit a generation request.

        Args:
            prompt: Input text
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            callback: Optional callback when complete
            priority: Request priority (higher = sooner)

        Returns:
            Request ID
        """
        import uuid
        request_id = str(uuid.uuid4())[:8]

        input_ids = self.tokenizer.encode(prompt)
        request = InferenceRequest(
            request_id=request_id,
            input_ids=input_ids,
            max_tokens=max_tokens,
            temperature=temperature,
            priority=priority
        )

        if callback:
            self.callbacks[request_id] = callback

        self.scheduler.add_request(request)
        return request_id

    def start(self):
        """Start the continuous batching loop."""
        if self.is_running:
            return

        self.is_running = True
        self._thread = threading.Thread(target=self._batch_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the batching loop."""
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=5.0)

    def _batch_loop(self):
        """Main batching loop."""
        while self.is_running:
            batch = self.scheduler.get_batch()

            if not batch:
                time.sleep(0.001)  # Small sleep when idle
                continue

            self._process_batch(batch)

    def _process_batch(self, batch: List[InferenceRequest]):
        """Process a batch of requests."""
        # Prepare inputs with padding
        max_len = max(len(r.input_ids) + len(r.generated_ids) for r in batch)

        input_ids_list = []
        attention_mask_list = []

        for request in batch:
            ids = request.input_ids + request.generated_ids
            padding = max_len - len(ids)

            # Left padding for generation
            padded_ids = [self.config.pad_token_id] * padding + ids
            mask = [0] * padding + [1] * len(ids)

            input_ids_list.append(padded_ids)
            attention_mask_list.append(mask)

        input_ids = torch.tensor(input_ids_list, device=self.device)
        attention_mask = torch.tensor(attention_mask_list, device=self.device)

        # Forward pass
        with torch.inference_mode():
            logits = self.model(input_ids, attention_mask=attention_mask)

        # Sample next tokens for each request
        finished_ids = []

        for i, request in enumerate(batch):
            next_logits = logits[i, -1, :] / max(request.temperature, 0.01)

            # Sample
            probs = torch.softmax(next_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1).item()

            request.generated_ids.append(next_token)

            # Check completion
            is_eos = next_token == getattr(self.tokenizer, 'eos_token_id', 2)
            reached_max = len(request.generated_ids) >= request.max_tokens

            if is_eos or reached_max:
                finished_ids.append(request.request_id)
                self._complete_request(request)

        # Update scheduler
        for req_id in finished_ids:
            self.scheduler.mark_complete(req_id)

        self.scheduler.update_stats(len(batch), sum(len(r.generated_ids) for r in batch))

    def _complete_request(self, request: InferenceRequest):
        """Handle request completion."""
        output_text = self.tokenizer.decode(request.generated_ids)

        if request.request_id in self.callbacks:
            try:
                self.callbacks[request.request_id](output_text)
            except Exception as e:
                print(f"Callback error for {request.request_id}: {e}")
            finally:
                del self.callbacks[request.request_id]

    def get_stats(self) -> Dict[str, Any]:
        """Get batching statistics."""
        return {
            **self.scheduler.stats,
            "active_requests": len(self.scheduler.active_requests),
            "queue_size": (
                len(self.scheduler.queue) if isinstance(self.scheduler.queue, list)
                else self.scheduler.queue.qsize()
            )
        }


def pad_batch(
    sequences: List[List[int]],
    pad_token_id: int = 0,
    max_length: Optional[int] = None,
    left_pad: bool = True
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Pad a batch of sequences.

    Args:
        sequences: List of token ID lists
        pad_token_id: Token ID for padding
        max_length: Maximum length (default: longest sequence)
        left_pad: Whether to left-pad (for generation) or right-pad

    Returns:
        Padded input IDs and attention mask tensors
    """
    if max_length is None:
        max_length = max(len(seq) for seq in sequences)

    input_ids = []
    attention_mask = []

    for seq in sequences:
        padding_length = max_length - len(seq)

        if left_pad:
            padded = [pad_token_id] * padding_length + seq
            mask = [0] * padding_length + [1] * len(seq)
        else:
            padded = seq + [pad_token_id] * padding_length
            mask = [1] * len(seq) + [0] * padding_length

        input_ids.append(padded)
        attention_mask.append(mask)

    return torch.tensor(input_ids), torch.tensor(attention_mask)
