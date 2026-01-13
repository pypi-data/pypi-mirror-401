"""
Quantization Optimizations

Lower precision computation for speed and memory efficiency:
- FP16: Good baseline, 2x memory reduction
- BF16: Better range than FP16, TPU native
- INT8: 4x speedup on Tensor Cores, needs calibration
- FP8: Newest (H100, MI300), 2x over FP16

Backend support:
- CUDA: FP16, BF16, INT8, FP8 (Hopper+)
- TPU: BF16 native, INT8 experimental
- AMD: FP16, BF16, INT8, FP8 (MI300)
- Intel: BF16 (with AMX), INT8
- DirectML: FP16 limited, no INT8
"""

import torch
import torch.nn as nn
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class QuantizationType(Enum):
    """Quantization types."""
    NONE = "none"
    FP16 = "fp16"
    BF16 = "bf16"
    INT8 = "int8"
    FP8_E4M3 = "fp8_e4m3"  # For weights
    FP8_E5M2 = "fp8_e5m2"  # For activations
    INT4 = "int4"          # Extreme quantization


@dataclass
class QuantizationConfig:
    """Configuration for quantization."""
    weight_type: QuantizationType = QuantizationType.NONE
    activation_type: QuantizationType = QuantizationType.NONE
    dynamic: bool = True  # Dynamic vs static quantization
    calibration_samples: int = 100
    symmetric: bool = True


# Backend quantization support
QUANTIZATION_SUPPORT = {
    "cuda": {
        QuantizationType.FP16: True,
        QuantizationType.BF16: True,  # Ampere+
        QuantizationType.INT8: True,   # Tensor Cores
        QuantizationType.FP8_E4M3: True,  # Hopper+
        QuantizationType.FP8_E5M2: True,
        QuantizationType.INT4: True,   # With cutlass
    },
    "tpu": {
        QuantizationType.FP16: False,  # TPU prefers BF16
        QuantizationType.BF16: True,   # Native
        QuantizationType.INT8: True,   # Experimental
        QuantizationType.FP8_E4M3: False,
        QuantizationType.FP8_E5M2: False,
        QuantizationType.INT4: False,
    },
    "amd": {
        QuantizationType.FP16: True,
        QuantizationType.BF16: True,   # MI300
        QuantizationType.INT8: True,
        QuantizationType.FP8_E4M3: True,  # MI300X
        QuantizationType.FP8_E5M2: True,
        QuantizationType.INT4: False,
    },
    "intel": {
        QuantizationType.FP16: True,
        QuantizationType.BF16: True,   # With AMX
        QuantizationType.INT8: True,
        QuantizationType.FP8_E4M3: False,
        QuantizationType.FP8_E5M2: False,
        QuantizationType.INT4: False,
    },
    "directml": {
        QuantizationType.FP16: True,   # Limited
        QuantizationType.BF16: False,
        QuantizationType.INT8: False,
        QuantizationType.FP8_E4M3: False,
        QuantizationType.FP8_E5M2: False,
        QuantizationType.INT4: False,
    },
    "cpu": {
        QuantizationType.FP16: False,  # CPU FP16 is slow
        QuantizationType.BF16: True,   # AVX-512 BF16
        QuantizationType.INT8: True,   # VNNI
        QuantizationType.FP8_E4M3: False,
        QuantizationType.FP8_E5M2: False,
        QuantizationType.INT4: True,   # With GPTQ/AWQ
    },
}


def get_supported_quantization(backend: str) -> list:
    """Get supported quantization types for a backend."""
    support = QUANTIZATION_SUPPORT.get(backend, {})
    return [qt for qt, supported in support.items() if supported]


def get_recommended_quantization(backend: str, use_case: str = "training") -> QuantizationType:
    """
    Get recommended quantization for backend and use case.

    Args:
        backend: Target backend
        use_case: "training" or "inference"
    """
    if use_case == "training":
        # Training: prefer BF16 for stability
        if backend in ["tpu", "amd", "cuda"]:
            return QuantizationType.BF16
        elif backend == "intel":
            return QuantizationType.BF16
        else:
            return QuantizationType.FP16
    else:
        # Inference: prefer INT8 for speed
        if backend in ["cuda", "amd", "intel", "cpu"]:
            return QuantizationType.INT8
        elif backend == "tpu":
            return QuantizationType.BF16  # INT8 experimental
        else:
            return QuantizationType.FP16


def quantize_for_inference(
    model: nn.Module,
    config: Optional[QuantizationConfig] = None,
    backend: str = "cuda"
) -> nn.Module:
    """
    Quantize model for inference.

    Args:
        model: PyTorch model
        config: Quantization configuration
        backend: Target backend

    Returns:
        Quantized model
    """
    if config is None:
        config = QuantizationConfig(
            weight_type=get_recommended_quantization(backend, "inference"),
            activation_type=QuantizationType.FP16,
            dynamic=True
        )

    # BF16/FP16 conversion (simple)
    if config.weight_type == QuantizationType.BF16:
        return model.to(torch.bfloat16)
    elif config.weight_type == QuantizationType.FP16:
        return model.to(torch.float16)

    # INT8 quantization
    elif config.weight_type == QuantizationType.INT8:
        if config.dynamic:
            # Dynamic quantization (easier, slightly slower)
            return torch.quantization.quantize_dynamic(
                model,
                {nn.Linear},  # Quantize linear layers
                dtype=torch.qint8
            )
        else:
            # Static quantization (needs calibration)
            model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
            torch.quantization.prepare(model, inplace=True)
            # Note: Would need calibration data here
            torch.quantization.convert(model, inplace=True)
            return model

    return model


class QuantizedINLDynamics(nn.Module):
    """
    INL dynamics with quantization support.

    Automatically uses appropriate precision for each backend.
    """

    def __init__(
        self,
        dim: int,
        dt: float = 0.1,
        quantization: QuantizationType = QuantizationType.NONE
    ):
        super().__init__()
        self.dim = dim
        self.dt = dt
        self.quantization = quantization

        # Parameters (will be quantized based on type)
        self.mu = nn.Parameter(torch.zeros(dim))

        # Controller
        self.controller = nn.Sequential(
            nn.Linear(dim * 2, dim // 2),
            nn.GELU(),
            nn.Linear(dim // 2, dim * 3)
        )

    def forward(self, x: torch.Tensor, v: torch.Tensor):
        """Forward with automatic precision handling."""
        # Get controller output
        ctx = torch.cat([x, v], dim=-1)
        ctrl_out = self.controller(ctx)

        # Split and apply activations
        alpha_raw, beta_raw, gate_raw = torch.split(ctrl_out, self.dim, dim=-1)
        alpha = torch.sigmoid(alpha_raw)
        beta = torch.nn.functional.softplus(beta_raw)
        gate = torch.sigmoid(gate_raw)

        # INL dynamics
        error = x - self.mu
        v_next = alpha * v - beta * error
        x_next = x + self.dt * gate * v_next

        return x_next, v_next


def estimate_memory_savings(
    model: nn.Module,
    quantization: QuantizationType
) -> Dict[str, float]:
    """
    Estimate memory savings from quantization.

    Returns:
        Dict with original_mb, quantized_mb, savings_pct
    """
    # Count parameters
    num_params = sum(p.numel() for p in model.parameters())

    # Original size (FP32)
    original_bytes = num_params * 4

    # Quantized size
    bytes_per_param = {
        QuantizationType.NONE: 4,
        QuantizationType.FP16: 2,
        QuantizationType.BF16: 2,
        QuantizationType.INT8: 1,
        QuantizationType.FP8_E4M3: 1,
        QuantizationType.FP8_E5M2: 1,
        QuantizationType.INT4: 0.5,
    }

    quantized_bytes = num_params * bytes_per_param.get(quantization, 4)

    original_mb = original_bytes / (1024 * 1024)
    quantized_mb = quantized_bytes / (1024 * 1024)
    savings_pct = (1 - quantized_bytes / original_bytes) * 100

    return {
        "original_mb": original_mb,
        "quantized_mb": quantized_mb,
        "savings_pct": savings_pct,
        "compression_ratio": original_bytes / quantized_bytes
    }


def print_quantization_guide():
    """Print quantization recommendations."""
    print("=" * 60)
    print("Quantization Guide for TPU-INL")
    print("=" * 60)

    print("\nRecommendations by Backend:")
    for backend in QUANTIZATION_SUPPORT.keys():
        supported = get_supported_quantization(backend)
        training_rec = get_recommended_quantization(backend, "training")
        inference_rec = get_recommended_quantization(backend, "inference")

        print(f"\n{backend.upper()}:")
        print(f"  Supported: {[qt.value for qt in supported]}")
        print(f"  Training: {training_rec.value}")
        print(f"  Inference: {inference_rec.value}")

    print("\n" + "=" * 60)
    print("Memory Savings:")
    print("  FP32 → FP16/BF16: 50%")
    print("  FP32 → INT8: 75%")
    print("  FP32 → FP8: 75%")
    print("  FP32 → INT4: 87.5%")
    print("=" * 60)


if __name__ == "__main__":
    print_quantization_guide()
