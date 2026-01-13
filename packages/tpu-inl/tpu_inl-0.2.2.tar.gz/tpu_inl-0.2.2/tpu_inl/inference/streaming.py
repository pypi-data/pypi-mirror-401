"""
Streaming inference for real-time token generation.

Supports:
- Token-by-token streaming
- Sentence/chunk streaming
- Server-Sent Events (SSE) compatible output
- Multi-client session management
"""

import torch
import torch.nn as nn
from typing import Optional, Generator, Callable, Any, Dict, List
from dataclasses import dataclass, field
from enum import Enum
import time
import asyncio
from queue import Queue
import threading


class StreamingMode(Enum):
    """Streaming output modes."""
    TOKEN = "token"          # Emit each token
    WORD = "word"            # Emit complete words
    SENTENCE = "sentence"    # Emit complete sentences
    CHUNK = "chunk"          # Emit fixed-size chunks


@dataclass
class StreamingConfig:
    """Configuration for streaming generation."""
    mode: StreamingMode = StreamingMode.TOKEN
    chunk_size: int = 10  # For CHUNK mode

    # Buffering
    buffer_size: int = 1  # Tokens to buffer before emitting

    # Timing
    min_interval_ms: float = 0.0  # Minimum time between emissions

    # Callbacks
    on_token: Optional[Callable[[str], None]] = None
    on_finish: Optional[Callable[[str], None]] = None
    on_error: Optional[Callable[[Exception], None]] = None


@dataclass
class StreamingStats:
    """Statistics for a streaming session."""
    tokens_generated: int = 0
    chunks_emitted: int = 0
    total_time: float = 0.0
    first_token_time: float = 0.0

    @property
    def tokens_per_second(self) -> float:
        if self.total_time > 0:
            return self.tokens_generated / self.total_time
        return 0.0

    @property
    def time_to_first_token_ms(self) -> float:
        return self.first_token_time * 1000


class StreamingSession:
    """
    Manages a single streaming generation session.

    Handles buffering, chunking, and output formatting.
    """

    def __init__(
        self,
        session_id: str,
        tokenizer: Any,
        config: Optional[StreamingConfig] = None
    ):
        self.session_id = session_id
        self.tokenizer = tokenizer
        self.config = config or StreamingConfig()

        # State
        self.buffer: List[int] = []
        self.output_text = ""
        self.is_active = True
        self.stats = StreamingStats()

        # For word/sentence detection
        self._partial_text = ""

        # Timing
        self._start_time: Optional[float] = None
        self._last_emit_time: float = 0.0

    def add_token(self, token_id: int) -> Optional[str]:
        """
        Add a generated token and potentially emit output.

        Returns:
            Text to emit, or None if buffering
        """
        if not self.is_active:
            return None

        # Record timing
        current_time = time.perf_counter()
        if self._start_time is None:
            self._start_time = current_time

        if self.stats.tokens_generated == 0:
            self.stats.first_token_time = current_time - self._start_time

        self.stats.tokens_generated += 1
        self.buffer.append(token_id)

        # Check emission based on mode
        emission = self._check_emission()

        if emission:
            self.stats.chunks_emitted += 1
            self._last_emit_time = current_time
            self.output_text += emission

            if self.config.on_token:
                self.config.on_token(emission)

        return emission

    def _check_emission(self) -> Optional[str]:
        """Check if we should emit based on mode and config."""
        if len(self.buffer) < self.config.buffer_size:
            return None

        # Respect minimum interval
        if self.config.min_interval_ms > 0:
            elapsed = (time.perf_counter() - self._last_emit_time) * 1000
            if elapsed < self.config.min_interval_ms:
                return None

        if self.config.mode == StreamingMode.TOKEN:
            return self._emit_tokens()

        elif self.config.mode == StreamingMode.WORD:
            return self._emit_word()

        elif self.config.mode == StreamingMode.SENTENCE:
            return self._emit_sentence()

        elif self.config.mode == StreamingMode.CHUNK:
            if len(self.buffer) >= self.config.chunk_size:
                return self._emit_tokens()
            return None

        return None

    def _emit_tokens(self) -> str:
        """Emit all buffered tokens."""
        if not self.buffer:
            return ""
        text = self.tokenizer.decode(self.buffer)
        self.buffer.clear()
        return text

    def _emit_word(self) -> Optional[str]:
        """Emit if we have a complete word."""
        text = self.tokenizer.decode(self.buffer)
        self._partial_text += text
        self.buffer.clear()

        # Check for word boundary (space)
        if ' ' in self._partial_text or '\n' in self._partial_text:
            # Find last word boundary
            for sep in [' ', '\n']:
                if sep in self._partial_text:
                    idx = self._partial_text.rfind(sep)
                    emission = self._partial_text[:idx + 1]
                    self._partial_text = self._partial_text[idx + 1:]
                    return emission

        return None

    def _emit_sentence(self) -> Optional[str]:
        """Emit if we have a complete sentence."""
        text = self.tokenizer.decode(self.buffer)
        self._partial_text += text
        self.buffer.clear()

        # Check for sentence boundary
        for end_char in ['.', '!', '?', '\n']:
            if end_char in self._partial_text:
                idx = self._partial_text.rfind(end_char)
                emission = self._partial_text[:idx + 1]
                self._partial_text = self._partial_text[idx + 1:]
                return emission

        return None

    def finish(self) -> str:
        """Finish streaming and return any remaining text."""
        self.is_active = False
        self.stats.total_time = time.perf_counter() - (self._start_time or time.perf_counter())

        # Emit remaining buffer
        remaining = ""
        if self.buffer:
            remaining = self.tokenizer.decode(self.buffer)
            self.buffer.clear()

        # Add any partial text
        remaining += self._partial_text
        self._partial_text = ""

        if remaining:
            self.output_text += remaining

        if self.config.on_finish:
            self.config.on_finish(self.output_text)

        return remaining

    def cancel(self):
        """Cancel the streaming session."""
        self.is_active = False

    def get_full_output(self) -> str:
        """Get the complete generated text so far."""
        return self.output_text


class StreamingEngine:
    """
    Streaming inference engine with session management.

    Supports multiple concurrent streaming sessions.
    """

    def __init__(
        self,
        model: nn.Module,
        tokenizer: Any,
        device: torch.device = None
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device or next(model.parameters()).device

        # Session management
        self.sessions: Dict[str, StreamingSession] = {}
        self._session_counter = 0
        self._lock = threading.Lock()

    def create_session(
        self,
        config: Optional[StreamingConfig] = None
    ) -> str:
        """Create a new streaming session."""
        with self._lock:
            self._session_counter += 1
            session_id = f"stream_{self._session_counter}"
            self.sessions[session_id] = StreamingSession(
                session_id, self.tokenizer, config
            )
            return session_id

    def get_session(self, session_id: str) -> Optional[StreamingSession]:
        """Get a session by ID."""
        return self.sessions.get(session_id)

    def close_session(self, session_id: str) -> Optional[str]:
        """Close a session and return remaining text."""
        session = self.sessions.pop(session_id, None)
        if session:
            return session.finish()
        return None

    def stream_generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        config: Optional[StreamingConfig] = None
    ) -> Generator[str, None, None]:
        """
        Stream-generate text from a prompt.

        Yields text chunks as they're generated.
        """
        session_id = self.create_session(config)
        session = self.sessions[session_id]

        try:
            # Tokenize
            input_ids = self.tokenizer.encode(prompt)
            input_ids = torch.tensor([input_ids], device=self.device)

            with torch.inference_mode():
                for _ in range(max_tokens):
                    if not session.is_active:
                        break

                    # Forward pass
                    logits = self.model(input_ids)
                    next_logits = logits[:, -1, :] / max(temperature, 0.01)

                    # Top-p sampling
                    if top_p < 1.0:
                        sorted_logits, sorted_indices = torch.sort(next_logits, descending=True)
                        cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
                        sorted_indices_to_remove = cumulative_probs > top_p
                        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                        sorted_indices_to_remove[..., 0] = 0
                        indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
                        next_logits[indices_to_remove] = float('-inf')

                    # Sample
                    probs = torch.softmax(next_logits, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1)

                    # Add to session
                    emission = session.add_token(next_token.item())
                    if emission:
                        yield emission

                    # Update input
                    input_ids = torch.cat([input_ids, next_token], dim=1)

                    # Check EOS
                    if next_token.item() == self.tokenizer.eos_token_id:
                        break

        finally:
            # Emit remaining and cleanup
            remaining = self.close_session(session_id)
            if remaining:
                yield remaining

    async def async_stream_generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
        config: Optional[StreamingConfig] = None
    ):
        """
        Async streaming generation for server integration.

        Yields text chunks compatible with SSE.
        """
        for chunk in self.stream_generate(prompt, max_tokens, temperature, config=config):
            yield chunk
            await asyncio.sleep(0)  # Yield to event loop


class SSEFormatter:
    """Format streaming output for Server-Sent Events."""

    @staticmethod
    def format_chunk(text: str, event: str = "token") -> str:
        """Format a text chunk as SSE."""
        return f"event: {event}\ndata: {text}\n\n"

    @staticmethod
    def format_done() -> str:
        """Format end-of-stream marker."""
        return "event: done\ndata: [DONE]\n\n"

    @staticmethod
    def format_error(error: str) -> str:
        """Format an error message."""
        return f"event: error\ndata: {error}\n\n"
