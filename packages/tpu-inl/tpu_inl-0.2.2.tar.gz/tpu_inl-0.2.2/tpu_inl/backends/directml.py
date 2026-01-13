"""
DirectML Backend - Windows GPU without CUDA

For Windows users with:
- NVIDIA RTX without CUDA Toolkit installed
- AMD Radeon (consumer cards without ROCm)
- Intel Arc/Iris

DirectML provides GPU acceleration via DirectX 12.
Works with torch-directml package.

Limitations:
- Slower than native CUDA/ROCm
- No custom kernels (uses PyTorch ops)
- But: Works on any Windows GPU with DX12 support!
"""

import torch
import torch.nn.functional as F
from typing import Tuple, Optional
from dataclasses import dataclass

# Check for DirectML
HAS_DIRECTML = False
DIRECTML_DEVICE = None

try:
    import torch_directml
    HAS_DIRECTML = True
    DIRECTML_DEVICE = torch_directml.device()
except ImportError:
    torch_directml = None


@dataclass
class DirectMLBackend:
    """
    DirectML backend for Windows GPUs.

    Works with any DirectX 12 compatible GPU:
    - NVIDIA GeForce RTX 2000/3000/4000 series
    - AMD Radeon RX 5000/6000/7000 series
    - Intel Arc A-series

    Installation:
        pip install torch-directml

    Note: No custom kernels available, uses PyTorch ops
    which DirectML translates to DX12 compute shaders.
    """

    name: str = "directml"
    has_directml: bool = HAS_DIRECTML

    @staticmethod
    def is_available() -> bool:
        """Check if DirectML is available."""
        return HAS_DIRECTML

    @staticmethod
    def get_device():
        """Get DirectML device for tensor allocation."""
        if not HAS_DIRECTML:
            raise RuntimeError("DirectML not available. Install: pip install torch-directml")
        return DIRECTML_DEVICE

    @staticmethod
    def get_device_info() -> dict:
        """Get DirectML device info."""
        if not HAS_DIRECTML:
            return {"available": False}

        try:
            # torch-directml provides device info
            device = torch_directml.device()
            return {
                "available": True,
                "device": str(device),
                "backend": "DirectML (DirectX 12)",
                # Note: DirectML doesn't expose detailed GPU info easily
            }
        except Exception as e:
            return {"available": True, "error": str(e)}

    @staticmethod
    def to_device(tensor: torch.Tensor) -> torch.Tensor:
        """Move tensor to DirectML device."""
        if not HAS_DIRECTML:
            return tensor
        return tensor.to(DIRECTML_DEVICE)

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
        Compute INL dynamics on DirectML.

        Uses standard PyTorch ops (no custom kernels).
        DirectML will translate to DX12 compute shaders.
        """
        # Standard PyTorch computation
        # DirectML handles GPU execution automatically
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
        """MoE dispatch on DirectML."""
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
        """MoE combine on DirectML."""
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
        """Batched expert forward on DirectML."""
        # Gather weights
        w1 = expert_w1[expert_indices]
        b1 = expert_b1[expert_indices]
        w2 = expert_w2[expert_indices]
        b2 = expert_b2[expert_indices]

        # Two-layer MLP
        hidden = torch.bmm(ctx.unsqueeze(1), w1).squeeze(1) + b1
        hidden = F.gelu(hidden)
        out = torch.bmm(hidden.unsqueeze(1), w2).squeeze(1) + b2

        return out


def benchmark_directml_backend(batch_size: int = 1024, dim: int = 512, n_iter: int = 50):
    """
    Benchmark DirectML backend.

    Note: DirectML is slower than native CUDA but allows GPU usage
    on Windows without CUDA toolkit installation.
    """
    if not HAS_DIRECTML:
        print("DirectML not available. Install: pip install torch-directml")
        return

    import time

    device = DirectMLBackend.get_device()
    print(f"DirectML device: {device}")

    x = torch.randn(batch_size, dim).to(device)
    v = torch.randn(batch_size, dim).to(device)
    mu = torch.randn(dim).to(device)
    alpha = torch.sigmoid(torch.randn(batch_size, dim)).to(device)
    beta = F.softplus(torch.randn(batch_size, dim)).to(device)
    gate = torch.sigmoid(torch.randn(batch_size, dim)).to(device)
    dt = 0.1

    # Warmup
    for _ in range(5):
        _ = DirectMLBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)

    # Benchmark
    start = time.perf_counter()
    for _ in range(n_iter):
        x_next, v_next = DirectMLBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)
    elapsed = (time.perf_counter() - start) / n_iter * 1000

    print(f"DirectML Backend Benchmark (batch={batch_size}, dim={dim})")
    print(f"  Time: {elapsed:.3f} ms/step")
    print(f"  Note: DirectML is slower than CUDA but works on any DX12 GPU")

    return elapsed


# Quick setup guide
SETUP_GUIDE = """
DirectML Setup Guide
====================

1. Install torch-directml:
   pip install torch-directml

2. Use in your code:
   import torch
   import torch_directml

   device = torch_directml.device()
   x = torch.randn(32, 512).to(device)

3. For INL:
   from tpu_inl import inl_dynamics, set_backend, Backend
   set_backend(Backend.DIRECTML)

   x_next, v_next = inl_dynamics(x, v, mu, alpha, beta, gate)

Supported GPUs:
- NVIDIA GeForce GTX 10xx, RTX 20xx/30xx/40xx
- AMD Radeon RX 5000/6000/7000
- Intel Arc A-series
- Any GPU with DirectX 12 support

Limitations:
- ~2-5x slower than native CUDA
- No custom kernels
- But works without CUDA toolkit!
"""


if __name__ == "__main__":
    print(SETUP_GUIDE)
    benchmark_directml_backend()
