"""
Memory Layout Optimizations

Different hardware prefers different tensor memory layouts:
- NVIDIA: NCHW (channels first) for cuDNN, but NHWC also good
- TPU: NHWC (channels last) strongly preferred
- AMD: Both work, NHWC slightly better on newer cards
- Intel: NHWC preferred for oneDNN
- CPU: Depends on BLAS library

For INL dynamics (not convolutions), layout is less critical
but stride patterns still matter for memory coalescing.
"""

import torch
import torch.nn as nn
from typing import Optional, Union
from enum import Enum
from dataclasses import dataclass


class MemoryFormat(Enum):
    """Tensor memory formats."""
    CONTIGUOUS = "contiguous"      # Standard row-major
    CHANNELS_LAST = "channels_last"  # NHWC for 4D tensors
    CHANNELS_LAST_3D = "channels_last_3d"  # NDHWC for 5D
    PRESERVE = "preserve"          # Keep existing format


@dataclass
class LayoutRecommendation:
    """Recommended memory layout for a backend."""
    backend: str
    format: MemoryFormat
    reason: str


# Backend-specific recommendations
LAYOUT_RECOMMENDATIONS = {
    "cuda": LayoutRecommendation(
        backend="cuda",
        format=MemoryFormat.CONTIGUOUS,
        reason="cuDNN handles both, contiguous is safer"
    ),
    "tpu": LayoutRecommendation(
        backend="tpu",
        format=MemoryFormat.CHANNELS_LAST,
        reason="TPU XLA strongly prefers NHWC layout"
    ),
    "amd": LayoutRecommendation(
        backend="amd",
        format=MemoryFormat.CHANNELS_LAST,
        reason="MIOpen prefers NHWC on MI300"
    ),
    "intel": LayoutRecommendation(
        backend="intel",
        format=MemoryFormat.CHANNELS_LAST,
        reason="oneDNN optimized for NHWC"
    ),
    "directml": LayoutRecommendation(
        backend="directml",
        format=MemoryFormat.CONTIGUOUS,
        reason="DirectML handles conversion internally"
    ),
    "cpu": LayoutRecommendation(
        backend="cpu",
        format=MemoryFormat.CHANNELS_LAST,
        reason="oneDNN CPU backend prefers NHWC"
    ),
}


def get_recommended_format(backend: str) -> MemoryFormat:
    """Get recommended memory format for a backend."""
    rec = LAYOUT_RECOMMENDATIONS.get(backend)
    if rec:
        return rec.format
    return MemoryFormat.CONTIGUOUS


def optimize_memory_layout(
    tensor: torch.Tensor,
    format: MemoryFormat = MemoryFormat.CONTIGUOUS,
    backend: Optional[str] = None
) -> torch.Tensor:
    """
    Optimize tensor memory layout for target backend.

    Args:
        tensor: Input tensor
        format: Target memory format
        backend: Target backend (uses format if None)

    Returns:
        Tensor with optimized layout
    """
    # Get format from backend if not specified
    if format == MemoryFormat.PRESERVE:
        return tensor

    if backend and format == MemoryFormat.CONTIGUOUS:
        format = get_recommended_format(backend)

    # Apply format
    if format == MemoryFormat.CONTIGUOUS:
        return tensor.contiguous()
    elif format == MemoryFormat.CHANNELS_LAST:
        if tensor.dim() == 4:
            return tensor.to(memory_format=torch.channels_last)
        return tensor.contiguous()
    elif format == MemoryFormat.CHANNELS_LAST_3D:
        if tensor.dim() == 5:
            return tensor.to(memory_format=torch.channels_last_3d)
        return tensor.contiguous()

    return tensor


def optimize_model_layout(
    model: nn.Module,
    format: MemoryFormat = MemoryFormat.CONTIGUOUS
) -> nn.Module:
    """
    Convert model to use optimal memory layout.

    Args:
        model: PyTorch model
        format: Target memory format

    Returns:
        Model with optimized layout
    """
    if format == MemoryFormat.CHANNELS_LAST:
        return model.to(memory_format=torch.channels_last)
    elif format == MemoryFormat.CHANNELS_LAST_3D:
        return model.to(memory_format=torch.channels_last_3d)
    return model


class LayoutOptimizedModule(nn.Module):
    """
    Wrapper that automatically optimizes tensor layouts.

    Usage:
        model = LayoutOptimizedModule(model, backend="tpu")
    """

    def __init__(self, module: nn.Module, backend: str = "cuda"):
        super().__init__()
        self.module = module
        self.backend = backend
        self.format = get_recommended_format(backend)

    def forward(self, *args, **kwargs):
        # Convert inputs to optimal format
        args = tuple(
            optimize_memory_layout(a, self.format) if isinstance(a, torch.Tensor) else a
            for a in args
        )
        kwargs = {
            k: optimize_memory_layout(v, self.format) if isinstance(v, torch.Tensor) else v
            for k, v in kwargs.items()
        }

        return self.module(*args, **kwargs)


def analyze_tensor_layout(tensor: torch.Tensor) -> dict:
    """Analyze tensor memory layout."""
    return {
        "shape": tensor.shape,
        "stride": tensor.stride(),
        "is_contiguous": tensor.is_contiguous(),
        "is_channels_last": tensor.is_contiguous(memory_format=torch.channels_last)
            if tensor.dim() == 4 else False,
        "element_size": tensor.element_size(),
        "storage_offset": tensor.storage_offset(),
        "numel": tensor.numel(),
        "nbytes": tensor.numel() * tensor.element_size(),
    }


def print_layout_analysis(tensor: torch.Tensor, name: str = "tensor"):
    """Print tensor layout analysis."""
    info = analyze_tensor_layout(tensor)
    print(f"\nLayout Analysis: {name}")
    print(f"  Shape: {info['shape']}")
    print(f"  Stride: {info['stride']}")
    print(f"  Contiguous: {info['is_contiguous']}")
    print(f"  Channels Last: {info['is_channels_last']}")
    print(f"  Size: {info['nbytes'] / 1024:.2f} KB")


def benchmark_layout(batch_size: int = 32, channels: int = 1024, height: int = 64, width: int = 64):
    """Benchmark different memory layouts."""
    import time

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Create tensors in different formats
    x_nchw = torch.randn(batch_size, channels, height, width, device=device)
    x_nhwc = x_nchw.to(memory_format=torch.channels_last)

    # Simple operation to benchmark
    def op(x):
        return x * 2 + 1

    # Warmup
    for _ in range(10):
        op(x_nchw)
        op(x_nhwc)

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    n_iter = 100

    # Benchmark NCHW
    start = time.perf_counter()
    for _ in range(n_iter):
        _ = op(x_nchw)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    nchw_time = (time.perf_counter() - start) / n_iter * 1000

    # Benchmark NHWC
    start = time.perf_counter()
    for _ in range(n_iter):
        _ = op(x_nhwc)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    nhwc_time = (time.perf_counter() - start) / n_iter * 1000

    print(f"Memory Layout Benchmark ({batch_size}x{channels}x{height}x{width})")
    print(f"  NCHW (contiguous): {nchw_time:.3f} ms")
    print(f"  NHWC (channels_last): {nhwc_time:.3f} ms")
    print(f"  Faster: {'NHWC' if nhwc_time < nchw_time else 'NCHW'}")

    return nchw_time, nhwc_time


if __name__ == "__main__":
    # Print recommendations
    print("Memory Layout Recommendations:")
    print("=" * 50)
    for backend, rec in LAYOUT_RECOMMENDATIONS.items():
        print(f"  {backend}: {rec.format.value} - {rec.reason}")

    print("\n")
    benchmark_layout()
