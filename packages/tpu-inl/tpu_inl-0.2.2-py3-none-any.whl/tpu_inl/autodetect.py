"""
Backend Auto-Detection for TPU-INL

Automatically detects available hardware and selects optimal backend:
1. TPU → JAX/Pallas
2. NVIDIA GPU → Triton/CUDA
3. AMD GPU → ROCm/Triton
4. Intel GPU → oneAPI/XPU
5. DirectML → Windows DX12 (any GPU)
6. CPU → PyTorch fallback

Can be overridden manually with set_backend().
"""

import os
from enum import Enum
from typing import Optional

# Global backend state
_current_backend: Optional["Backend"] = None


class Backend(Enum):
    """Available compute backends."""
    TPU = "tpu"          # Google TPU with JAX/Pallas
    CUDA = "cuda"        # NVIDIA GPU with Triton
    AMD = "amd"          # AMD GPU with ROCm/Triton
    INTEL = "intel"      # Intel GPU/CPU with oneAPI
    DIRECTML = "directml"  # Windows DX12 (any GPU)
    CPU = "cpu"          # PyTorch fallback


def _detect_tpu() -> bool:
    """Check if TPU is available."""
    try:
        import jax
        devices = jax.devices()
        return any(d.platform == "tpu" for d in devices)
    except ImportError:
        return False
    except Exception:
        return False


def _detect_cuda() -> bool:
    """Check if NVIDIA CUDA GPU is available."""
    try:
        import torch
        if not torch.cuda.is_available():
            return False
        # Make sure it's NVIDIA, not AMD ROCm
        device_name = torch.cuda.get_device_name(0).lower()
        return not any(x in device_name for x in ['amd', 'radeon', 'mi250', 'mi300', 'instinct'])
    except ImportError:
        return False
    except Exception:
        return False


def _detect_amd() -> bool:
    """Check if AMD GPU with ROCm is available."""
    try:
        import torch
        if not torch.cuda.is_available():
            return False
        device_name = torch.cuda.get_device_name(0).lower()
        return any(x in device_name for x in ['amd', 'radeon', 'mi250', 'mi300', 'instinct'])
    except Exception:
        return False


def _detect_intel() -> bool:
    """Check if Intel XPU (GPU) or IPEX is available."""
    try:
        import torch
        # Check for Intel XPU
        if hasattr(torch, 'xpu') and torch.xpu.is_available():
            return True
        # Check for IPEX
        import intel_extension_for_pytorch
        return True
    except ImportError:
        return False
    except Exception:
        return False


def _detect_directml() -> bool:
    """Check if DirectML is available (Windows)."""
    try:
        import torch_directml
        return True
    except ImportError:
        return False


def _detect_triton() -> bool:
    """Check if Triton is available for CUDA/ROCm acceleration."""
    try:
        import triton
        return True
    except ImportError:
        return False


def _detect_pallas() -> bool:
    """Check if Pallas (JAX's Triton equivalent) is available."""
    try:
        from jax.experimental import pallas
        return True
    except ImportError:
        return False


def autodetect_backend() -> Backend:
    """
    Auto-detect the best available backend.

    Priority:
    1. TPU (if JAX detects TPU devices)
    2. NVIDIA CUDA (if torch.cuda with NVIDIA)
    3. AMD ROCm (if torch.cuda with AMD)
    4. Intel XPU (if torch.xpu available)
    5. DirectML (if torch-directml installed)
    6. CPU (fallback)
    """
    # Check environment variable override
    env_backend = os.getenv("TPU_INL_BACKEND", "").lower()
    if env_backend:
        backend_map = {
            "tpu": Backend.TPU,
            "cuda": Backend.CUDA,
            "amd": Backend.AMD,
            "intel": Backend.INTEL,
            "directml": Backend.DIRECTML,
            "cpu": Backend.CPU,
        }
        if env_backend in backend_map:
            return backend_map[env_backend]

    # Auto-detect in priority order
    if _detect_tpu():
        return Backend.TPU
    elif _detect_cuda():
        return Backend.CUDA
    elif _detect_amd():
        return Backend.AMD
    elif _detect_intel():
        return Backend.INTEL
    elif _detect_directml():
        return Backend.DIRECTML
    else:
        return Backend.CPU


def get_backend() -> Backend:
    """Get the current active backend."""
    global _current_backend
    if _current_backend is None:
        _current_backend = autodetect_backend()
    return _current_backend


def set_backend(backend: Backend) -> None:
    """
    Manually set the backend.

    Args:
        backend: Backend to use (Backend.TPU, Backend.CUDA, etc.)

    Example:
        >>> from tpu_inl import set_backend, Backend
        >>> set_backend(Backend.DIRECTML)  # Force DirectML on Windows
    """
    global _current_backend
    _current_backend = backend
    print(f"[TPU-INL] Backend set to: {backend.value}")


def get_backend_info() -> dict:
    """Get detailed info about all available backends."""
    return {
        "current": get_backend().value,
        "available": {
            "tpu": _detect_tpu(),
            "cuda": _detect_cuda(),
            "amd": _detect_amd(),
            "intel": _detect_intel(),
            "directml": _detect_directml(),
            "cpu": True,  # Always available
        },
        "accelerators": {
            "triton": _detect_triton(),
            "pallas": _detect_pallas(),
        }
    }


def print_backend_info():
    """Print detailed backend information."""
    info = get_backend_info()
    print("=" * 50)
    print("TPU-INL Backend Information")
    print("=" * 50)
    print(f"Current backend: {info['current'].upper()}")
    print("\nAvailable backends:")
    for name, available in info['available'].items():
        status = "✓" if available else "✗"
        print(f"  {status} {name}")
    print("\nAccelerators:")
    for name, available in info['accelerators'].items():
        status = "✓" if available else "✗"
        print(f"  {status} {name}")
    print("=" * 50)


# Print backend info on import (optional)
if os.getenv("TPU_INL_VERBOSE", "0") == "1":
    print_backend_info()
