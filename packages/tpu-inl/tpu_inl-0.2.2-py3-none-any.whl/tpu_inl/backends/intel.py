"""
Intel Backend - oneAPI / Intel Extension for PyTorch

For Intel hardware:
- Intel Arc A-series GPUs (A770, A750, A380)
- Intel Data Center GPUs (Max series, Ponte Vecchio)
- Intel Xe integrated graphics
- Intel CPUs with AVX-512 (optimized CPU path)

Uses Intel Extension for PyTorch (IPEX) for acceleration.
"""

import torch
import torch.nn.functional as F
from typing import Tuple
from dataclasses import dataclass

# Check for Intel Extension for PyTorch
HAS_IPEX = False
HAS_XPU = False

try:
    import intel_extension_for_pytorch as ipex
    HAS_IPEX = True
    # Check for Intel GPU (XPU)
    if hasattr(torch, 'xpu') and torch.xpu.is_available():
        HAS_XPU = True
except ImportError:
    ipex = None


@dataclass
class IntelBackend:
    """
    Intel backend using oneAPI/IPEX.

    Supports:
    - Intel Arc A770/A750/A380 (consumer GPUs)
    - Intel Data Center GPU Max (HPC)
    - Intel Xe integrated graphics
    - Optimized CPU path with AVX-512

    Installation:
        pip install intel-extension-for-pytorch

    For GPU (XPU):
        pip install torch torchvision --index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/
    """

    name: str = "intel"
    has_ipex: bool = HAS_IPEX
    has_xpu: bool = HAS_XPU

    @staticmethod
    def is_available() -> bool:
        """Check if Intel backend is available."""
        return HAS_IPEX

    @staticmethod
    def is_xpu_available() -> bool:
        """Check if Intel GPU (XPU) is available."""
        return HAS_XPU

    @staticmethod
    def get_device():
        """Get Intel XPU device."""
        if HAS_XPU:
            return torch.device("xpu")
        return torch.device("cpu")

    @staticmethod
    def get_device_info() -> dict:
        """Get Intel device info."""
        info = {
            "ipex_available": HAS_IPEX,
            "xpu_available": HAS_XPU,
        }

        if HAS_XPU:
            info.update({
                "device_count": torch.xpu.device_count(),
                "device_name": torch.xpu.get_device_name(0),
                "memory_gb": torch.xpu.get_device_properties(0).total_memory / 1e9,
            })

        if HAS_IPEX:
            info["ipex_version"] = ipex.__version__

        return info

    @staticmethod
    def optimize_model(model: torch.nn.Module, dtype=torch.bfloat16):
        """
        Optimize model for Intel hardware.

        Uses IPEX optimizations:
        - Operator fusion
        - Memory layout optimization
        - BF16 acceleration (if supported)
        """
        if not HAS_IPEX:
            return model

        # IPEX optimization
        model = ipex.optimize(model, dtype=dtype)
        return model

    @staticmethod
    def inl_dynamics(
        x: torch.Tensor,
        v: torch.Tensor,
        mu: torch.Tensor,
        alpha: torch.Tensor,
        beta: torch.Tensor,
        gate: torch.Tensor,
        dt: float = 0.1
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Compute INL dynamics on Intel hardware.

        IPEX automatically optimizes these ops for:
        - Intel GPUs (XPU): Uses oneAPI Level Zero
        - Intel CPUs: Uses AVX-512/AMX instructions
        """
        # Standard computation - IPEX handles optimization
        error = x - mu
        v_next = alpha * v - beta * error
        x_next = x + dt * gate * v_next
        return x_next, v_next

    @staticmethod
    def moe_dispatch(
        x: torch.Tensor,
        router_logits: torch.Tensor,
        top_k: int = 2
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """MoE dispatch on Intel."""
        router_probs = F.softmax(router_logits, dim=-1)
        top_k_probs, top_k_indices = torch.topk(router_probs, top_k, dim=-1)
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)

        batch_size, dim = x.shape
        expanded_x = x.unsqueeze(1).expand(-1, top_k, -1).reshape(-1, dim)
        expert_indices = top_k_indices.reshape(-1)
        expert_weights = top_k_probs.reshape(-1)

        return expanded_x, expert_indices, expert_weights

    @staticmethod
    def moe_combine(
        expert_outputs: torch.Tensor,
        expert_weights: torch.Tensor,
        batch_size: int,
        top_k: int
    ) -> torch.Tensor:
        """MoE combine on Intel."""
        dim = expert_outputs.shape[-1]
        weighted = expert_outputs * expert_weights.unsqueeze(-1)
        weighted = weighted.view(batch_size, top_k, dim)
        return weighted.sum(dim=1)

    @staticmethod
    def batched_expert_forward(
        ctx: torch.Tensor,
        expert_indices: torch.Tensor,
        expert_w1: torch.Tensor,
        expert_b1: torch.Tensor,
        expert_w2: torch.Tensor,
        expert_b2: torch.Tensor
    ) -> torch.Tensor:
        """Batched expert forward on Intel."""
        w1 = expert_w1[expert_indices]
        b1 = expert_b1[expert_indices]
        w2 = expert_w2[expert_indices]
        b2 = expert_b2[expert_indices]

        hidden = torch.bmm(ctx.unsqueeze(1), w1).squeeze(1) + b1
        hidden = F.gelu(hidden)
        out = torch.bmm(hidden.unsqueeze(1), w2).squeeze(1) + b2

        return out


def benchmark_intel_backend(batch_size: int = 2048, dim: int = 1024, n_iter: int = 100):
    """Benchmark Intel backend."""
    import time

    # Use XPU if available, else CPU with IPEX
    if HAS_XPU:
        device = torch.device("xpu")
        print("Using Intel XPU (GPU)")
    else:
        device = torch.device("cpu")
        print("Using Intel CPU with IPEX optimizations")

    x = torch.randn(batch_size, dim, device=device)
    v = torch.randn(batch_size, dim, device=device)
    mu = torch.randn(dim, device=device)
    alpha = torch.sigmoid(torch.randn(batch_size, dim, device=device))
    beta = F.softplus(torch.randn(batch_size, dim, device=device))
    gate = torch.sigmoid(torch.randn(batch_size, dim, device=device))
    dt = 0.1

    # Warmup
    for _ in range(10):
        _ = IntelBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)

    if HAS_XPU:
        torch.xpu.synchronize()

    # Benchmark
    start = time.perf_counter()
    for _ in range(n_iter):
        x_next, v_next = IntelBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)

    if HAS_XPU:
        torch.xpu.synchronize()

    elapsed = (time.perf_counter() - start) / n_iter * 1000

    info = IntelBackend.get_device_info()
    print(f"Intel Backend Benchmark (batch={batch_size}, dim={dim})")
    print(f"  IPEX: {info['ipex_available']}, XPU: {info['xpu_available']}")
    if 'device_name' in info:
        print(f"  Device: {info['device_name']}")
    print(f"  Time: {elapsed:.3f} ms/step")

    return elapsed


# Setup guide
SETUP_GUIDE = """
Intel Backend Setup Guide
=========================

For Intel GPUs (Arc A770, A750, etc.):
--------------------------------------
1. Install Intel GPU drivers
2. Install PyTorch with XPU support:
   pip install torch torchvision --index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/

For Intel CPUs (optimized):
---------------------------
pip install intel-extension-for-pytorch

Usage:
------
from tpu_inl import inl_dynamics, set_backend, Backend
set_backend(Backend.INTEL)

# Auto-uses XPU if available, else optimized CPU
x_next, v_next = inl_dynamics(x, v, mu, alpha, beta, gate)

Supported Hardware:
- Intel Arc A770/A750/A580/A380 (16GB/8GB/8GB/6GB VRAM)
- Intel Data Center GPU Max (48GB+ HBM)
- Intel Core CPUs with AVX-512 (13th/14th gen)
- Intel Xeon CPUs with AMX
"""


if __name__ == "__main__":
    print(SETUP_GUIDE)
    if HAS_IPEX:
        benchmark_intel_backend()
    else:
        print("\nInstall: pip install intel-extension-for-pytorch")
