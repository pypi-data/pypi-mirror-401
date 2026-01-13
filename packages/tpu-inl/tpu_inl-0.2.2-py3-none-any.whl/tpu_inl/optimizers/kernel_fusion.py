"""
Kernel Fusion Optimizations

Techniques for fusing multiple operations into single kernels
to reduce memory bandwidth and kernel launch overhead.

Different backends need different fusion strategies:
- CUDA: Triton @jit with explicit fusion
- TPU: XLA auto-fusion (just write clean code)
- AMD: Triton ROCm (similar to CUDA)
- Intel: oneDNN graph fusion
- DirectML: DX12 compute shader fusion (limited)
"""

import torch
import torch.nn as nn
from typing import Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class FusionStrategy(Enum):
    """Available fusion strategies."""
    NONE = "none"              # No fusion
    TORCH_COMPILE = "compile"  # torch.compile inductor
    TRITON = "triton"          # Custom Triton kernels
    XLA = "xla"                # JAX/XLA auto-fusion
    ONEDNN = "onednn"          # Intel oneDNN fusion


@dataclass
class FusedOps:
    """
    Registry of fused operations.

    Track which ops can be fused together for each backend.
    """

    # INL dynamics fusion candidates
    INL_DYNAMICS = [
        "sub",      # error = x - mu
        "mul",      # alpha * v
        "mul",      # beta * error
        "sub",      # alpha*v - beta*error
        "mul",      # gate * v_next
        "mul",      # dt * gate * v_next
        "add",      # x + dt * gate * v_next
    ]

    # MoE fusion candidates
    MOE_DISPATCH = [
        "softmax",  # router probs
        "topk",     # expert selection
        "div",      # normalize weights
        "expand",   # expand inputs
    ]

    MOE_COMBINE = [
        "mul",      # weight * output
        "sum",      # aggregate
    ]

    @staticmethod
    def count_ops_fused(op_list: list) -> int:
        """Count how many ops are fused."""
        return len(op_list)

    @staticmethod
    def estimate_speedup(num_ops: int) -> float:
        """Estimate speedup from fusing N ops into 1."""
        # Rough estimate: each kernel launch ~5-10us
        # Memory bandwidth is usually the bottleneck
        # Fusion can give 2-5x speedup depending on ops
        return min(num_ops * 0.5, 5.0)


def apply_kernel_fusion(
    module: nn.Module,
    strategy: FusionStrategy = FusionStrategy.TORCH_COMPILE,
    backend: Optional[str] = None
) -> nn.Module:
    """
    Apply kernel fusion optimizations to a module.

    Args:
        module: PyTorch module to optimize
        strategy: Fusion strategy to use
        backend: Target backend (auto-detected if None)

    Returns:
        Optimized module
    """
    if strategy == FusionStrategy.NONE:
        return module

    elif strategy == FusionStrategy.TORCH_COMPILE:
        # Use PyTorch 2.0+ compile with inductor
        try:
            return torch.compile(module, mode="reduce-overhead")
        except Exception as e:
            print(f"torch.compile failed: {e}, returning original module")
            return module

    elif strategy == FusionStrategy.TRITON:
        # Custom Triton kernels are applied at op level, not module level
        # This just marks the module for Triton usage
        module._use_triton = True
        return module

    elif strategy == FusionStrategy.XLA:
        # For JAX/XLA, fusion is automatic
        # This is a no-op for PyTorch modules
        return module

    elif strategy == FusionStrategy.ONEDNN:
        # Intel oneDNN fusion via IPEX
        try:
            import intel_extension_for_pytorch as ipex
            return ipex.optimize(module)
        except ImportError:
            print("IPEX not available, returning original module")
            return module

    return module


class FusedINLDynamics(nn.Module):
    """
    Fused INL dynamics as a single operation.

    Instead of:
        error = x - mu
        v_next = alpha * v - beta * error
        x_next = x + dt * gate * v_next

    This computes everything in one fused kernel.
    """

    def __init__(self, dim: int, dt: float = 0.1):
        super().__init__()
        self.dim = dim
        self.dt = dt
        self.mu = nn.Parameter(torch.zeros(dim))

    def forward(
        self,
        x: torch.Tensor,
        v: torch.Tensor,
        alpha: torch.Tensor,
        beta: torch.Tensor,
        gate: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Fused forward pass."""
        # Try to use backend-specific fusion
        if hasattr(self, '_use_triton') and self._use_triton:
            from ..backends.cuda import CUDABackend
            return CUDABackend.inl_dynamics(
                x, v, self.mu, alpha, beta, gate, self.dt
            )

        # Default: let torch.compile handle fusion
        error = x - self.mu
        v_next = alpha * v - beta * error
        x_next = x + self.dt * gate * v_next
        return x_next, v_next


class FusedMoEDispatch(nn.Module):
    """
    Fused MoE dispatch operation.

    Combines softmax + topk + normalization + expansion.
    """

    def __init__(self, num_experts: int, top_k: int = 2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k

    def forward(
        self,
        x: torch.Tensor,
        router_logits: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Fused dispatch.

        Returns:
            expanded_x: [batch * top_k, dim]
            expert_indices: [batch * top_k]
            expert_weights: [batch * top_k]
        """
        # Fused softmax + topk
        router_probs = torch.softmax(router_logits, dim=-1)
        top_k_probs, top_k_indices = torch.topk(router_probs, self.top_k, dim=-1)

        # Fused normalize + expand
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)

        batch_size, dim = x.shape
        expanded_x = x.unsqueeze(1).expand(-1, self.top_k, -1).reshape(-1, dim)
        expert_indices = top_k_indices.reshape(-1)
        expert_weights = top_k_probs.reshape(-1)

        return expanded_x, expert_indices, expert_weights


def benchmark_fusion(batch_size: int = 4096, dim: int = 1024, n_iter: int = 100):
    """Benchmark fused vs unfused operations."""
    import time

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    x = torch.randn(batch_size, dim, device=device)
    v = torch.randn(batch_size, dim, device=device)
    mu = torch.randn(dim, device=device)
    alpha = torch.sigmoid(torch.randn(batch_size, dim, device=device))
    beta = torch.nn.functional.softplus(torch.randn(batch_size, dim, device=device))
    gate = torch.sigmoid(torch.randn(batch_size, dim, device=device))
    dt = 0.1

    # Unfused version
    def unfused():
        error = x - mu
        v_next = alpha * v - beta * error
        x_next = x + dt * gate * v_next
        return x_next, v_next

    # Compiled version
    fused = torch.compile(unfused, mode="reduce-overhead")

    # Warmup
    for _ in range(10):
        unfused()
        fused()

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    # Benchmark unfused
    start = time.perf_counter()
    for _ in range(n_iter):
        unfused()
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    unfused_time = (time.perf_counter() - start) / n_iter * 1000

    # Benchmark fused
    start = time.perf_counter()
    for _ in range(n_iter):
        fused()
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    fused_time = (time.perf_counter() - start) / n_iter * 1000

    print(f"Kernel Fusion Benchmark (batch={batch_size}, dim={dim})")
    print(f"  Unfused:  {unfused_time:.3f} ms")
    print(f"  Fused:    {fused_time:.3f} ms")
    print(f"  Speedup:  {unfused_time / fused_time:.2f}x")

    return unfused_time, fused_time


if __name__ == "__main__":
    benchmark_fusion()
