"""
AMD Backend - ROCm/HIP + Triton

Optimized INL dynamics for AMD GPUs (MI250X, MI300X, etc.) using:
- ROCm (AMD's CUDA equivalent)
- Triton with ROCm backend
- HIP for direct GPU programming

AMD GPUs are increasingly used in HPC (Frontier supercomputer uses MI250X).
"""

import torch
import torch.nn.functional as F
from typing import Tuple
from dataclasses import dataclass

# Check for AMD GPU (ROCm)
HAS_ROCM = False
try:
    if torch.cuda.is_available():
        # Check if it's AMD (ROCm reports as CUDA but with AMD device)
        device_name = torch.cuda.get_device_name(0).lower()
        HAS_ROCM = any(x in device_name for x in ['amd', 'radeon', 'mi250', 'mi300', 'instinct'])
except Exception:
    pass

# Triton works on ROCm too (with some limitations)
HAS_TRITON_ROCM = False
try:
    import triton
    import triton.language as tl
    # Check if Triton has ROCm support
    if HAS_ROCM:
        HAS_TRITON_ROCM = True
except ImportError:
    triton = None
    tl = None


if HAS_TRITON_ROCM:
    # =========================================================================
    # TRITON KERNELS FOR AMD (ROCm)
    # =========================================================================
    # Note: Triton kernels are mostly portable between CUDA and ROCm
    # Some features may differ (warp size: NVIDIA=32, AMD=64)

    @triton.jit
    def _rocm_fused_inl_dynamics_kernel(
        # Inputs
        x_ptr, v_ptr, mu_ptr,
        alpha_ptr, beta_ptr, gate_ptr,
        # Outputs
        x_out_ptr, v_out_ptr,
        # Scalars
        dt,
        n_elements,
        # Block size (AMD wavefront = 64, so use multiples of 64)
        BLOCK_SIZE: tl.constexpr
    ):
        """
        Fused INL dynamics kernel for AMD GPUs.

        Same algorithm as CUDA, but tuned for AMD's wavefront size (64 vs 32).
        """
        pid = tl.program_id(0)
        block_start = pid * BLOCK_SIZE
        offsets = block_start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < n_elements

        # Load inputs (coalesced for HBM bandwidth)
        x = tl.load(x_ptr + offsets, mask=mask, other=0.0)
        v = tl.load(v_ptr + offsets, mask=mask, other=0.0)
        mu = tl.load(mu_ptr + offsets, mask=mask, other=0.0)
        alpha = tl.load(alpha_ptr + offsets, mask=mask, other=0.0)
        beta = tl.load(beta_ptr + offsets, mask=mask, other=0.0)
        gate = tl.load(gate_ptr + offsets, mask=mask, other=0.0)

        # Fused computation
        error = x - mu
        v_next = alpha * v - beta * error
        x_next = x + dt * gate * v_next

        # Store outputs
        tl.store(x_out_ptr + offsets, x_next, mask=mask)
        tl.store(v_out_ptr + offsets, v_next, mask=mask)


@dataclass
class AMDBackend:
    """
    AMD backend using ROCm/Triton.

    Supports:
    - AMD Instinct MI250X (used in Frontier, LUMI)
    - AMD Instinct MI300X (latest generation)
    - Consumer Radeon (limited ROCm support)
    """

    name: str = "amd"
    has_rocm: bool = HAS_ROCM
    has_triton: bool = HAS_TRITON_ROCM

    @staticmethod
    def is_available() -> bool:
        """Check if AMD GPU is available."""
        return HAS_ROCM

    @staticmethod
    def get_device_info() -> dict:
        """Get AMD GPU info."""
        if not HAS_ROCM:
            return {"available": False}

        return {
            "available": True,
            "device_name": torch.cuda.get_device_name(0),
            "memory_gb": torch.cuda.get_device_properties(0).total_memory / 1e9,
            "triton_available": HAS_TRITON_ROCM,
            # AMD MI250X has 128GB HBM2e, MI300X has 192GB HBM3
        }

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
        Compute INL dynamics on AMD GPU.

        Uses Triton with ROCm backend if available, else PyTorch.
        """
        if not HAS_TRITON_ROCM or not x.is_cuda:
            # PyTorch fallback (still runs on ROCm via HIP)
            error = x - mu
            v_next = alpha * v - beta * error
            x_next = x + dt * gate * v_next
            return x_next, v_next

        # Use Triton kernel
        original_shape = x.shape
        x_flat = x.contiguous().view(-1)
        v_flat = v.contiguous().view(-1)

        # Broadcast mu
        if mu.dim() == 1 and x.dim() > 1:
            mu_expanded = mu.unsqueeze(0).expand(original_shape).contiguous().view(-1)
        else:
            mu_expanded = mu.contiguous().view(-1)

        alpha_flat = alpha.contiguous().view(-1)
        beta_flat = beta.contiguous().view(-1)
        gate_flat = gate.contiguous().view(-1)

        n_elements = x_flat.numel()

        # Allocate outputs
        x_out = torch.empty_like(x_flat)
        v_out = torch.empty_like(v_flat)

        # Launch kernel (AMD wavefront = 64, so use 1024 or 2048)
        BLOCK_SIZE = 1024
        grid = (triton.cdiv(n_elements, BLOCK_SIZE),)

        _rocm_fused_inl_dynamics_kernel[grid](
            x_flat, v_flat, mu_expanded,
            alpha_flat, beta_flat, gate_flat,
            x_out, v_out,
            dt,
            n_elements,
            BLOCK_SIZE=BLOCK_SIZE
        )

        return x_out.view(original_shape), v_out.view(original_shape)

    @staticmethod
    def moe_dispatch(
        x: torch.Tensor,
        router_logits: torch.Tensor,
        top_k: int = 2
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """MoE dispatch on AMD GPU."""
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
        """MoE combine on AMD GPU."""
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
        """Batched expert forward on AMD GPU."""
        # Gather weights
        w1 = expert_w1[expert_indices]
        b1 = expert_b1[expert_indices]
        w2 = expert_w2[expert_indices]
        b2 = expert_b2[expert_indices]

        # Two-layer MLP (uses ROCm BLAS under the hood)
        hidden = torch.bmm(ctx.unsqueeze(1), w1).squeeze(1) + b1
        hidden = F.gelu(hidden)
        out = torch.bmm(hidden.unsqueeze(1), w2).squeeze(1) + b2

        return out


def benchmark_amd_backend(batch_size: int = 4096, dim: int = 1024, n_iter: int = 100):
    """Benchmark AMD backend."""
    if not HAS_ROCM:
        print("AMD GPU (ROCm) not available")
        return

    import time

    device = torch.device("cuda")  # ROCm uses "cuda" device string

    x = torch.randn(batch_size, dim, device=device)
    v = torch.randn(batch_size, dim, device=device)
    mu = torch.randn(dim, device=device)
    alpha = torch.sigmoid(torch.randn(batch_size, dim, device=device))
    beta = F.softplus(torch.randn(batch_size, dim, device=device))
    gate = torch.sigmoid(torch.randn(batch_size, dim, device=device))
    dt = 0.1

    # Warmup
    for _ in range(10):
        _ = AMDBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)
    torch.cuda.synchronize()

    # Benchmark
    start = time.perf_counter()
    for _ in range(n_iter):
        x_next, v_next = AMDBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)
    torch.cuda.synchronize()
    elapsed = (time.perf_counter() - start) / n_iter * 1000

    info = AMDBackend.get_device_info()
    print(f"AMD Backend Benchmark (batch={batch_size}, dim={dim})")
    print(f"  Device: {info['device_name']}")
    print(f"  Memory: {info['memory_gb']:.1f} GB")
    print(f"  Triton: {info['triton_available']}")
    print(f"  Time: {elapsed:.3f} ms/step")

    return elapsed


if __name__ == "__main__":
    benchmark_amd_backend()
