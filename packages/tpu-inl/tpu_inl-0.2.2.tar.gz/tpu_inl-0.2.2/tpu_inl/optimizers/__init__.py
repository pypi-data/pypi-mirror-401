"""
TPU-INL Optimizers

This module contains optimization techniques discovered over time
to close the performance gap between different backends.

Goal: Make TPU, AMD, Intel, DirectML as fast as CUDA+Triton

Categories:
-----------
1. kernel_fusion.py - Fusing multiple ops into one
2. memory_layout.py - Optimal tensor layouts per hardware
3. quantization.py - INT8/FP8 acceleration
4. scheduling.py - Optimal work scheduling
5. autotuning.py - Runtime parameter tuning

Usage:
------
from tpu_inl.optimizers import optimize_for_backend

# Auto-applies best optimizations for current backend
model = optimize_for_backend(model)

Research Notes:
---------------
Keep track of optimization discoveries in OPTIMIZATION_LOG below.
"""

from .kernel_fusion import FusedOps, apply_kernel_fusion, FusionStrategy
from .memory_layout import optimize_memory_layout, MemoryFormat
from .quantization import quantize_for_inference, QuantizationConfig, QuantizationType
from .autotuning import autotune, AutotuneConfig, Autotuner, ParameterSpace
from .scheduling import (
    DeviceScheduler,
    PipelineScheduler,
    TensorParallelizer,
    ExpertParallelizer,
    SequenceParallelizer,
    SchedulingConfig,
    ParallelismType,
    get_optimal_parallelism,
)

__all__ = [
    # Kernel fusion
    "FusedOps",
    "apply_kernel_fusion",
    "FusionStrategy",
    # Memory layout
    "optimize_memory_layout",
    "MemoryFormat",
    # Quantization
    "quantize_for_inference",
    "QuantizationConfig",
    "QuantizationType",
    # Autotuning
    "autotune",
    "AutotuneConfig",
    "Autotuner",
    "ParameterSpace",
    # Scheduling / Parallelism
    "DeviceScheduler",
    "PipelineScheduler",
    "TensorParallelizer",
    "ExpertParallelizer",
    "SequenceParallelizer",
    "SchedulingConfig",
    "ParallelismType",
    "get_optimal_parallelism",
]


# =============================================================================
# OPTIMIZATION LOG
# =============================================================================
# Track discoveries and optimizations over time

OPTIMIZATION_LOG = """
TPU-INL Optimization Log
========================

[2025-01] Initial Release
--------------------------
- CUDA: Triton kernels for INL dynamics (3-5x speedup)
- TPU: JAX @jit compilation (auto-fused by XLA)
- AMD: Triton with ROCm (similar to CUDA)
- Intel: IPEX optimizations
- DirectML: PyTorch ops (no custom kernels yet)

[TODO] Future Optimizations
----------------------------
TPU:
- [ ] Pallas kernels for finer control
- [ ] Custom XLA ops for INL dynamics
- [ ] Multi-TPU sharding strategies

AMD:
- [ ] Tune block sizes for AMD wavefront (64 vs NVIDIA 32)
- [ ] Use WMMA for matrix ops on MI300
- [ ] Profile HBM2e vs HBM3 bandwidth differences

Intel:
- [ ] Intel AMX for BF16 matmul acceleration
- [ ] Custom SYCL kernels for Arc GPUs
- [ ] AVX-512 vectorization for CPU fallback

DirectML:
- [ ] HLSL compute shader custom kernels
- [ ] DirectX 12 Ultimate ray-tracing for sparse ops
- [ ] Xbox Series X/S optimization (same DX12 backend)

General:
- [ ] FP8 quantization (Hopper, Ada, AMD MI300)
- [ ] Sparsity support (2:4 structured sparsity)
- [ ] Flash Attention integration
- [ ] Continuous batching for inference

[Benchmarks]
-------------
Target: Within 20% of CUDA+Triton performance

Hardware          | Status  | Gap vs CUDA
------------------|---------|-------------
NVIDIA H100       | ✓       | Baseline
NVIDIA A100       | ✓       | Baseline
Google TPU v4     | ~       | -10% (XLA overhead)
AMD MI300X        | ~       | -15% (Triton ROCm)
Intel Arc A770    | ?       | TBD
DirectML RTX 4090 | ?       | -40% estimate

Legend: ✓ = On par, ~ = Close, ? = Unknown
"""


def print_optimization_log():
    """Print the optimization log."""
    print(OPTIMIZATION_LOG)


def get_recommendations(backend: str) -> list:
    """Get optimization recommendations for a specific backend."""
    recommendations = {
        "cuda": [
            "Use Triton for custom kernels",
            "Enable bf16 mixed precision",
            "Use torch.compile() for graph optimization",
        ],
        "tpu": [
            "Use @jax.jit for all functions",
            "Prefer static shapes (no dynamic shapes)",
            "Use lax.scan instead of Python loops",
            "Enable bf16 (TPU's native precision)",
        ],
        "amd": [
            "Use Triton with ROCm backend",
            "Tune block sizes for wavefront=64",
            "Enable bf16 (MI300 optimized)",
            "Use hipBLAS for matmuls",
        ],
        "intel": [
            "Use IPEX for automatic optimization",
            "Enable bf16 with AMX (Xeon)",
            "Use torch.xpu for Intel GPUs",
            "Consider oneDNN for primitives",
        ],
        "directml": [
            "Keep batch sizes moderate (DX12 overhead)",
            "Avoid frequent CPU-GPU transfers",
            "Use fp32 (DirectML bf16 limited)",
            "Consider torch.compile() for graph capture",
        ],
        "cpu": [
            "Use IPEX for Intel CPUs",
            "Enable MKL-DNN",
            "Use torch.compile() with inductor",
            "Consider ONNX Runtime for inference",
        ],
    }
    return recommendations.get(backend, ["No specific recommendations"])
