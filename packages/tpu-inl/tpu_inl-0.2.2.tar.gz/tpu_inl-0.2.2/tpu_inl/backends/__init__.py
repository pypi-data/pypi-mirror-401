"""
Backend implementations for TPU-INL.

Each backend provides the same API but optimized for different hardware:
- cuda.py: Triton kernels for NVIDIA GPUs
- tpu.py: JAX/Pallas for Google TPUs
- amd.py: ROCm/Triton for AMD GPUs (MI250X, MI300X)
- directml.py: DirectML for Windows (RTX/Radeon/Intel without CUDA)
- intel.py: Intel oneAPI for Intel Arc/Xe GPUs
- cpu.py: PyTorch fallback for CPU
"""

from .cuda import CUDABackend
from .tpu import TPUBackend
from .amd import AMDBackend
from .directml import DirectMLBackend
from .intel import IntelBackend
from .cpu import CPUBackend

__all__ = [
    "CUDABackend",
    "TPUBackend",
    "AMDBackend",
    "DirectMLBackend",
    "IntelBackend",
    "CPUBackend"
]
