"""
TPU-INL Inference Engine

Cross-platform inference engine with automatic backend selection
and optimization for real-time applications.
"""

import torch
import torch.nn as nn
from typing import Optional, Dict, Any, List, Union, Generator
from dataclasses import dataclass, field
from enum import Enum
import time

from ..autodetect import get_backend, Backend


class GenerationMode(Enum):
    """Text generation modes."""
    GREEDY = "greedy"
    SAMPLING = "sampling"
    BEAM_SEARCH = "beam_search"
    CONTRASTIVE = "contrastive"


@dataclass
class EngineConfig:
    """Inference engine configuration."""
    # Backend
    backend: str = "auto"  # "auto", "cuda", "tpu", "amd", "intel", "directml", "cpu"

    # Precision
    dtype: str = "auto"  # "auto", "fp32", "fp16", "bf16", "int8"

    # Memory
    max_batch_size: int = 32
    max_sequence_length: int = 4096
    use_kv_cache: bool = True
    use_paged_attention: bool = False

    # Performance
    use_torch_compile: bool = True
    use_cuda_graphs: bool = True  # CUDA only
    warmup_steps: int = 3

    # Generation
    default_max_tokens: int = 256
    default_temperature: float = 0.7
    default_top_p: float = 0.9
    default_top_k: int = 50


@dataclass
class GenerationConfig:
    """Configuration for a single generation request."""
    max_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    stop_sequences: List[str] = field(default_factory=list)
    mode: GenerationMode = GenerationMode.SAMPLING


class InferenceEngine:
    """
    Cross-platform inference engine for INL models.

    Automatically selects the best backend and applies optimizations.
    Supports both batch and streaming inference.
    """

    def __init__(
        self,
        model: nn.Module,
        tokenizer: Any = None,
        config: Optional[EngineConfig] = None
    ):
        self.config = config or EngineConfig()
        self.tokenizer = tokenizer

        # Detect backend
        if self.config.backend == "auto":
            self.backend = get_backend()
        else:
            self.backend = Backend(self.config.backend)

        # Setup device
        self.device = self._get_device()
        print(f"[TPU-INL Engine] Backend: {self.backend.value}, Device: {self.device}")

        # Setup model
        self.model = self._prepare_model(model)

        # Initialize KV cache if enabled
        self.kv_cache = None
        if self.config.use_kv_cache:
            from .kv_cache import KVCache
            self.kv_cache = KVCache(
                max_batch_size=self.config.max_batch_size,
                max_seq_len=self.config.max_sequence_length,
                device=self.device
            )

        # Warmup
        if self.config.warmup_steps > 0:
            self._warmup()

        # Stats
        self.stats = {
            "total_tokens": 0,
            "total_time": 0.0,
            "requests": 0,
        }

    def _get_device(self) -> torch.device:
        """Get device for current backend."""
        if self.backend == Backend.CUDA:
            return torch.device("cuda")
        elif self.backend == Backend.AMD:
            return torch.device("cuda")  # ROCm uses cuda device
        elif self.backend == Backend.INTEL:
            if hasattr(torch, 'xpu') and torch.xpu.is_available():
                return torch.device("xpu")
            return torch.device("cpu")
        elif self.backend == Backend.DIRECTML:
            try:
                import torch_directml
                return torch_directml.device()
            except ImportError:
                return torch.device("cpu")
        elif self.backend == Backend.TPU:
            # For TPU, we use JAX, but PyTorch model stays on CPU
            # JAX handles TPU placement
            return torch.device("cpu")
        else:
            return torch.device("cpu")

    def _prepare_model(self, model: nn.Module) -> nn.Module:
        """Prepare model for inference."""
        model = model.to(self.device)
        model.eval()

        # Apply dtype
        if self.config.dtype == "auto":
            if self.backend in [Backend.CUDA, Backend.AMD]:
                model = model.to(torch.bfloat16)
            elif self.backend == Backend.TPU:
                model = model.to(torch.bfloat16)
            # DirectML and CPU stay FP32
        elif self.config.dtype == "fp16":
            model = model.half()
        elif self.config.dtype == "bf16":
            model = model.to(torch.bfloat16)
        elif self.config.dtype == "int8":
            model = torch.quantization.quantize_dynamic(
                model, {nn.Linear}, dtype=torch.qint8
            )

        # Apply torch.compile if enabled
        if self.config.use_torch_compile and self.backend != Backend.TPU:
            try:
                model = torch.compile(model, mode="reduce-overhead")
                print("[TPU-INL Engine] torch.compile enabled")
            except Exception as e:
                print(f"[TPU-INL Engine] torch.compile failed: {e}")

        return model

    def _warmup(self):
        """Warmup the model for consistent performance."""
        print(f"[TPU-INL Engine] Warming up ({self.config.warmup_steps} steps)...")

        # Create dummy input
        dummy_input = torch.randint(
            0, 1000, (1, 32), device=self.device
        )

        with torch.no_grad():
            for _ in range(self.config.warmup_steps):
                try:
                    _ = self.model(dummy_input)
                except Exception:
                    # Model might have different signature
                    break

        if self.device.type == "cuda":
            torch.cuda.synchronize()

        print("[TPU-INL Engine] Warmup complete")

    @torch.inference_mode()
    def generate(
        self,
        prompt: Union[str, torch.Tensor, List[int]],
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> Union[str, torch.Tensor]:
        """
        Generate text from a prompt.

        Args:
            prompt: Text prompt, token IDs, or tensor
            config: Generation configuration
            **kwargs: Override config parameters

        Returns:
            Generated text or tokens
        """
        config = config or GenerationConfig(**kwargs)

        # Tokenize if string
        if isinstance(prompt, str):
            if self.tokenizer is None:
                raise ValueError("Tokenizer required for string prompts")
            input_ids = self.tokenizer.encode(prompt)
            input_ids = torch.tensor([input_ids], device=self.device)
            return_string = True
        elif isinstance(prompt, list):
            input_ids = torch.tensor([prompt], device=self.device)
            return_string = False
        else:
            input_ids = prompt.to(self.device)
            return_string = False

        start_time = time.perf_counter()

        # Generate tokens
        generated = self._generate_tokens(input_ids, config)

        elapsed = time.perf_counter() - start_time

        # Update stats
        num_new_tokens = generated.shape[1] - input_ids.shape[1]
        self.stats["total_tokens"] += num_new_tokens
        self.stats["total_time"] += elapsed
        self.stats["requests"] += 1

        # Decode if needed
        if return_string:
            return self.tokenizer.decode(generated[0].tolist())
        return generated

    def _generate_tokens(
        self,
        input_ids: torch.Tensor,
        config: GenerationConfig
    ) -> torch.Tensor:
        """Core token generation loop."""
        batch_size, seq_len = input_ids.shape
        generated = input_ids

        # Reset KV cache
        if self.kv_cache:
            self.kv_cache.reset()

        for _ in range(config.max_tokens):
            # Get model output
            if self.kv_cache and seq_len > 1:
                # Use cached keys/values
                logits = self._forward_with_cache(generated[:, -1:])
            else:
                logits = self.model(generated)

            # Get next token logits
            next_logits = logits[:, -1, :]

            # Apply temperature
            if config.temperature > 0:
                next_logits = next_logits / config.temperature

            # Apply repetition penalty
            if config.repetition_penalty != 1.0:
                for i in range(batch_size):
                    for token_id in generated[i].unique():
                        next_logits[i, token_id] /= config.repetition_penalty

            # Sample next token
            if config.mode == GenerationMode.GREEDY:
                next_token = next_logits.argmax(dim=-1, keepdim=True)
            else:
                # Top-k filtering
                if config.top_k > 0:
                    indices_to_remove = next_logits < torch.topk(next_logits, config.top_k)[0][..., -1, None]
                    next_logits[indices_to_remove] = float('-inf')

                # Top-p filtering
                if config.top_p < 1.0:
                    sorted_logits, sorted_indices = torch.sort(next_logits, descending=True)
                    cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
                    sorted_indices_to_remove = cumulative_probs > config.top_p
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                    sorted_indices_to_remove[..., 0] = 0
                    indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
                    next_logits[indices_to_remove] = float('-inf')

                # Sample
                probs = torch.softmax(next_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)

            # Append
            generated = torch.cat([generated, next_token], dim=1)

            # Check for EOS (assuming token 2 is EOS, adjust for your tokenizer)
            if (next_token == 2).all():
                break

        return generated

    def _forward_with_cache(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Forward pass with KV cache."""
        # This is a simplified version - real implementation depends on model architecture
        return self.model(input_ids)

    def stream(
        self,
        prompt: Union[str, torch.Tensor],
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        Stream generated tokens one at a time.

        Yields tokens as they're generated for real-time display.
        """
        config = config or GenerationConfig(**kwargs)

        # Tokenize
        if isinstance(prompt, str):
            if self.tokenizer is None:
                raise ValueError("Tokenizer required for streaming")
            input_ids = self.tokenizer.encode(prompt)
            input_ids = torch.tensor([input_ids], device=self.device)
        else:
            input_ids = prompt.to(self.device)

        generated = input_ids

        if self.kv_cache:
            self.kv_cache.reset()

        with torch.inference_mode():
            for _ in range(config.max_tokens):
                logits = self.model(generated)
                next_logits = logits[:, -1, :] / max(config.temperature, 0.01)

                # Sample
                probs = torch.softmax(next_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)

                # Decode and yield
                token_str = self.tokenizer.decode([next_token.item()])
                yield token_str

                # Append
                generated = torch.cat([generated, next_token], dim=1)

                # Check EOS
                if next_token.item() == 2:  # EOS token
                    break

    def get_stats(self) -> Dict[str, Any]:
        """Get inference statistics."""
        stats = self.stats.copy()
        if stats["total_time"] > 0:
            stats["tokens_per_second"] = stats["total_tokens"] / stats["total_time"]
        else:
            stats["tokens_per_second"] = 0
        return stats

    def reset_stats(self):
        """Reset statistics."""
        self.stats = {"total_tokens": 0, "total_time": 0.0, "requests": 0}


def benchmark_engine(model: nn.Module, tokenizer: Any = None, prompt: str = "Hello, how are you?"):
    """Benchmark inference engine across backends."""
    from ..autodetect import get_backend_info

    print("=" * 60)
    print("TPU-INL Inference Engine Benchmark")
    print("=" * 60)

    info = get_backend_info()
    print(f"\nBackend Info:")
    for k, v in info.items():
        print(f"  {k}: {v}")

    # Create engine
    engine = InferenceEngine(model, tokenizer)

    # Benchmark
    print(f"\nBenchmarking with prompt: '{prompt}'")

    n_runs = 10
    times = []

    for i in range(n_runs):
        start = time.perf_counter()
        if tokenizer:
            _ = engine.generate(prompt, max_tokens=50)
        else:
            dummy = torch.randint(0, 1000, (1, 32), device=engine.device)
            _ = engine.generate(dummy, max_tokens=50)
        times.append(time.perf_counter() - start)

    avg_time = sum(times) / len(times)
    stats = engine.get_stats()

    print(f"\nResults:")
    print(f"  Avg time per request: {avg_time*1000:.2f} ms")
    print(f"  Tokens/second: {stats['tokens_per_second']:.1f}")
    print("=" * 60)
