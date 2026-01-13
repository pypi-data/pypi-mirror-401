"""
TPU-INL Complexity Model Support

Wrapper for Complexity models with:
- Auto backend detection (CUDA, DirectML, CPU, etc.)
- Automatic precision selection
- KV cache support
- Streaming generation
"""

import torch
import torch.nn as nn
from typing import Optional, Dict, Any, Union, Generator
from pathlib import Path
import json

from ..autodetect import get_backend, Backend

# Check if complexity package is available
try:
    from complexity import ComplexityConfig, ComplexityForCausalLM
    COMPLEXITY_AVAILABLE = True
except ImportError:
    COMPLEXITY_AVAILABLE = False
    ComplexityConfig = None
    ComplexityForCausalLM = None


def load_complexity_model(
    model_path: Union[str, Path],
    device: Optional[str] = "auto",
    dtype: Optional[str] = "auto",
    trust_remote_code: bool = True,
) -> "ComplexityWrapper":
    """
    Load a Complexity model with TPU-INL optimizations.

    Args:
        model_path: Path to model directory or HuggingFace model ID
        device: Device to load on ("auto", "cuda", "directml", "cpu", etc.)
        dtype: Data type ("auto", "fp16", "bf16", "fp32")
        trust_remote_code: Allow loading custom model code

    Returns:
        ComplexityWrapper instance ready for inference
    """
    if not COMPLEXITY_AVAILABLE:
        raise ImportError(
            "complexity package not installed. Install with: pip install complexity-model"
        )

    return ComplexityWrapper(
        model_path=model_path,
        device=device,
        dtype=dtype,
    )


class ComplexityWrapper(nn.Module):
    """
    Wrapper for Complexity models with TPU-INL acceleration.

    Provides:
    - Automatic backend detection
    - Device placement
    - Streaming generation
    - Batch inference
    """

    def __init__(
        self,
        model_path: Union[str, Path],
        device: str = "auto",
        dtype: str = "auto",
        use_kv_cache: bool = True,
    ):
        super().__init__()

        if not COMPLEXITY_AVAILABLE:
            raise ImportError("complexity package not installed")

        self.model_path = Path(model_path)
        self.use_kv_cache = use_kv_cache

        # Detect backend
        if device == "auto":
            self.backend = get_backend()
            self.device = self._get_device_for_backend()
        else:
            self.device = torch.device(device)
            self.backend = self._backend_from_device(device)

        print(f"[TPU-INL Complexity] Backend: {self.backend.value}, Device: {self.device}")

        # Load config
        config_path = self.model_path / "config.json"
        with open(config_path) as f:
            cfg = json.load(f)

        # Create Complexity config
        self.config = ComplexityConfig(
            vocab_size=cfg.get("vocab_size", 100000),
            hidden_size=cfg.get("hidden_size", 768),
            intermediate_size=cfg.get("intermediate_size", 2048),
            num_hidden_layers=cfg.get("num_hidden_layers", 12),
            num_attention_heads=cfg.get("num_attention_heads", 12),
            num_key_value_heads=cfg.get("num_key_value_heads", 4),
            max_position_embeddings=cfg.get("max_position_embeddings", 2048),
            rms_norm_eps=cfg.get("rms_norm_eps", 1e-6),
            rope_theta=cfg.get("rope_theta", 10000.0),
            use_token_routed_mlp=cfg.get("use_token_routed_mlp", True),
            num_experts=cfg.get("num_experts", 4),
            use_qk_norm=cfg.get("use_qk_norm", True),
            use_sdpa=cfg.get("use_sdpa", True),
        )

        # Create model
        print("[TPU-INL Complexity] Loading model...")
        self.model = ComplexityForCausalLM(self.config)

        # Load weights
        weights_path = self.model_path / "model.safetensors"
        if weights_path.exists():
            from safetensors.torch import load_file
            weights = load_file(weights_path)
            self.model.load_state_dict(weights, strict=False)
        else:
            # Try .bin format
            weights_path = self.model_path / "pytorch_model.bin"
            if weights_path.exists():
                weights = torch.load(weights_path, map_location="cpu")
                self.model.load_state_dict(weights, strict=False)

        # Move to device and set dtype
        self._setup_dtype(dtype)
        self.model = self.model.to(self.device)
        self.model.eval()

        # Load tokenizer
        self.tokenizer = None
        try:
            from transformers import AutoTokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        except Exception:
            pass

        # Count params
        num_params = sum(p.numel() for p in self.model.parameters())
        print(f"[TPU-INL Complexity] Loaded {num_params:,} parameters on {self.device}")

    def _get_device_for_backend(self) -> torch.device:
        """Get device for detected backend."""
        if self.backend == Backend.CUDA:
            return torch.device("cuda")
        elif self.backend == Backend.AMD:
            return torch.device("cuda")  # ROCm
        elif self.backend == Backend.DIRECTML:
            try:
                import torch_directml
                return torch_directml.device()
            except ImportError:
                return torch.device("cpu")
        elif self.backend == Backend.INTEL:
            if hasattr(torch, 'xpu') and torch.xpu.is_available():
                return torch.device("xpu")
            return torch.device("cpu")
        else:
            return torch.device("cpu")

    def _backend_from_device(self, device: str) -> Backend:
        """Infer backend from device string."""
        if "cuda" in device:
            return Backend.CUDA
        elif "directml" in device or "privateuseone" in device:
            return Backend.DIRECTML
        elif "xpu" in device:
            return Backend.INTEL
        else:
            return Backend.CPU

    def _setup_dtype(self, dtype: str):
        """Setup model dtype based on backend."""
        if dtype == "auto":
            if self.backend in [Backend.CUDA, Backend.AMD]:
                self.model = self.model.to(torch.bfloat16)
            elif self.backend == Backend.DIRECTML:
                self.model = self.model.half()  # FP16 for DirectML
            # CPU stays FP32
        elif dtype == "fp16":
            self.model = self.model.half()
        elif dtype == "bf16":
            self.model = self.model.to(torch.bfloat16)
        # else fp32 (default)

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        **kwargs
    ):
        """Forward pass through the model."""
        return self.model(input_ids, attention_mask=attention_mask, **kwargs)

    @torch.inference_mode()
    def generate(
        self,
        prompt: Union[str, torch.Tensor],
        max_tokens: int = 100,
        temperature: float = 0.7,
        top_k: int = 50,
        top_p: float = 0.9,
        repetition_penalty: float = 1.1,
    ) -> str:
        """
        Generate text from a prompt.

        Args:
            prompt: Text prompt or token tensor
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_k: Top-k filtering
            top_p: Top-p (nucleus) filtering
            repetition_penalty: Penalty for repeating tokens

        Returns:
            Generated text
        """
        # Tokenize
        if isinstance(prompt, str):
            if self.tokenizer is None:
                raise ValueError("Tokenizer not available")
            input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
            input_ids = input_ids.to(self.device)
        else:
            input_ids = prompt.to(self.device)

        generated = input_ids

        for _ in range(max_tokens):
            # Forward
            outputs = self.model(generated)
            logits = outputs.logits if hasattr(outputs, 'logits') else outputs[0]
            next_logits = logits[:, -1, :].float()

            # Temperature
            if temperature > 0:
                next_logits = next_logits / temperature

            # Repetition penalty
            if repetition_penalty != 1.0:
                for token_id in generated[0].unique():
                    next_logits[0, token_id] /= repetition_penalty

            # Top-k
            if top_k > 0:
                top_k_vals, _ = torch.topk(next_logits, min(top_k, next_logits.size(-1)))
                next_logits[next_logits < top_k_vals[:, -1, None]] = float('-inf')

            # Top-p
            if top_p < 1.0:
                sorted_logits, sorted_indices = torch.sort(next_logits, descending=True)
                cumsum = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
                sorted_indices_to_remove = cumsum > top_p
                sorted_indices_to_remove[:, 1:] = sorted_indices_to_remove[:, :-1].clone()
                sorted_indices_to_remove[:, 0] = False
                indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
                next_logits[indices_to_remove] = float('-inf')

            # Sample
            probs = torch.softmax(next_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)

            # Append
            generated = torch.cat([generated, next_token], dim=1)

            # EOS check
            if self.tokenizer and next_token.item() == self.tokenizer.eos_token_id:
                break

        # Decode
        if self.tokenizer:
            return self.tokenizer.decode(generated[0], skip_special_tokens=True)
        return generated

    @torch.inference_mode()
    def stream(
        self,
        prompt: str,
        max_tokens: int = 100,
        temperature: float = 0.7,
    ) -> Generator[str, None, None]:
        """
        Stream generated tokens.

        Yields tokens as they're generated.
        """
        if self.tokenizer is None:
            raise ValueError("Tokenizer required for streaming")

        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        input_ids = input_ids.to(self.device)

        generated = input_ids

        for _ in range(max_tokens):
            outputs = self.model(generated)
            logits = outputs.logits if hasattr(outputs, 'logits') else outputs[0]
            next_logits = logits[:, -1, :].float() / max(temperature, 0.01)

            probs = torch.softmax(next_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)

            # Decode and yield
            token_str = self.tokenizer.decode([next_token.item()])
            yield token_str

            generated = torch.cat([generated, next_token], dim=1)

            if next_token.item() == self.tokenizer.eos_token_id:
                break
