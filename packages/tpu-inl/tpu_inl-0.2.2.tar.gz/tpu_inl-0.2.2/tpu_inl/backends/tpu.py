"""
TPU Backend - JAX/Pallas

Optimized INL dynamics for Google TPUs using:
- JAX for automatic XLA compilation
- Pallas for custom TPU kernels (like Triton for GPUs)
- pjit/pmap for multi-TPU parallelism

This is the key backend for large-scale from-scratch training on TPU pods.
"""

from typing import Tuple, Optional, Callable
from dataclasses import dataclass

# Try to import JAX
try:
    import jax
    import jax.numpy as jnp
    from jax import lax
    HAS_JAX = True
except ImportError:
    HAS_JAX = False
    jax = None
    jnp = None
    lax = None

# Try to import Pallas (JAX's Triton equivalent)
try:
    from jax.experimental import pallas as pl
    HAS_PALLAS = True
except ImportError:
    HAS_PALLAS = False
    pl = None


if HAS_JAX:
    # =========================================================================
    # JAX IMPLEMENTATIONS
    # =========================================================================

    @jax.jit
    def _jax_inl_dynamics(
        x: jnp.ndarray,
        v: jnp.ndarray,
        mu: jnp.ndarray,
        alpha: jnp.ndarray,
        beta: jnp.ndarray,
        gate: jnp.ndarray,
        dt: float
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        """
        JAX-compiled INL dynamics.

        XLA will automatically fuse these ops into an efficient kernel.
        """
        error = x - mu
        v_next = alpha * v - beta * error
        x_next = x + dt * gate * v_next
        return x_next, v_next

    @jax.jit
    def _jax_inl_dynamics_scan(
        carry: Tuple[jnp.ndarray, jnp.ndarray],
        step_inputs: Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray],
        mu: jnp.ndarray,
        dt: float
    ) -> Tuple[Tuple[jnp.ndarray, jnp.ndarray], None]:
        """
        Single step for lax.scan-based iteration.

        More efficient than Python loop for multiple steps.
        """
        x, v = carry
        alpha, beta, gate = step_inputs
        x_next, v_next = _jax_inl_dynamics(x, v, mu, alpha, beta, gate, dt)
        return (x_next, v_next), None

    def _jax_inl_n_steps(
        x: jnp.ndarray,
        v: jnp.ndarray,
        mu: jnp.ndarray,
        alphas: jnp.ndarray,  # [n_steps, ...]
        betas: jnp.ndarray,
        gates: jnp.ndarray,
        dt: float
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        """
        Run n steps of INL dynamics efficiently using lax.scan.

        Args:
            x, v: Initial state [batch, dim]
            mu: Equilibrium [dim]
            alphas, betas, gates: Per-step parameters [n_steps, batch, dim]
            dt: Time step

        Returns:
            Final x, v
        """
        def scan_fn(carry, inputs):
            x, v = carry
            alpha, beta, gate = inputs
            error = x - mu
            v_next = alpha * v - beta * error
            x_next = x + dt * gate * v_next
            return (x_next, v_next), None

        (x_final, v_final), _ = lax.scan(
            scan_fn,
            (x, v),
            (alphas, betas, gates)
        )
        return x_final, v_final

    @jax.jit
    def _jax_moe_dispatch(
        x: jnp.ndarray,
        router_logits: jnp.ndarray,
        top_k: int
    ) -> Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray]:
        """
        MoE dispatch in JAX.

        Uses jax.lax.top_k for efficient top-k selection on TPU.
        """
        # Softmax routing
        router_probs = jax.nn.softmax(router_logits, axis=-1)

        # Top-k selection
        top_k_probs, top_k_indices = lax.top_k(router_probs, top_k)

        # Normalize
        top_k_probs = top_k_probs / top_k_probs.sum(axis=-1, keepdims=True)

        # Expand
        batch_size, dim = x.shape
        expanded_x = jnp.repeat(x[:, None, :], top_k, axis=1).reshape(-1, dim)
        expert_indices = top_k_indices.reshape(-1)
        expert_weights = top_k_probs.reshape(-1)

        return expanded_x, expert_indices, expert_weights

    @jax.jit
    def _jax_moe_combine(
        expert_outputs: jnp.ndarray,
        expert_weights: jnp.ndarray,
        batch_size: int,
        top_k: int
    ) -> jnp.ndarray:
        """MoE combine in JAX."""
        dim = expert_outputs.shape[-1]
        weighted = expert_outputs * expert_weights[:, None]
        weighted = weighted.reshape(batch_size, top_k, dim)
        return weighted.sum(axis=1)

    @jax.jit
    def _jax_batched_expert_forward(
        ctx: jnp.ndarray,
        expert_indices: jnp.ndarray,
        expert_w1: jnp.ndarray,
        expert_b1: jnp.ndarray,
        expert_w2: jnp.ndarray,
        expert_b2: jnp.ndarray
    ) -> jnp.ndarray:
        """
        Batched expert MLP forward in JAX.

        Uses vmap for efficient batched computation on TPU.
        """
        # Gather weights
        w1 = expert_w1[expert_indices]  # [n, in, hidden]
        b1 = expert_b1[expert_indices]  # [n, hidden]
        w2 = expert_w2[expert_indices]  # [n, hidden, out]
        b2 = expert_b2[expert_indices]  # [n, out]

        # Layer 1
        hidden = jnp.einsum('ni,nih->nh', ctx, w1) + b1
        hidden = jax.nn.gelu(hidden)

        # Layer 2
        out = jnp.einsum('nh,nho->no', hidden, w2) + b2

        return out


if HAS_PALLAS:
    # =========================================================================
    # PALLAS KERNELS (TPU's Triton equivalent)
    # =========================================================================

    def _pallas_inl_dynamics_kernel(
        x_ref, v_ref, mu_ref, alpha_ref, beta_ref, gate_ref,
        x_out_ref, v_out_ref,
        dt: float
    ):
        """
        Pallas kernel for fused INL dynamics on TPU.

        Similar to Triton but targets TPU's systolic array.
        """
        # Load from HBM to VMEM
        x = x_ref[...]
        v = v_ref[...]
        mu = mu_ref[...]
        alpha = alpha_ref[...]
        beta = beta_ref[...]
        gate = gate_ref[...]

        # Compute (fused in TPU's vector unit)
        error = x - mu
        v_next = alpha * v - beta * error
        x_next = x + dt * gate * v_next

        # Store back to HBM
        x_out_ref[...] = x_next
        v_out_ref[...] = v_next


@dataclass
class TPUBackend:
    """TPU backend using JAX/Pallas."""

    name: str = "tpu"
    has_jax: bool = HAS_JAX
    has_pallas: bool = HAS_PALLAS

    @staticmethod
    def inl_dynamics(
        x,  # Can be jnp.ndarray or torch.Tensor
        v,
        mu,
        alpha,
        beta,
        gate,
        dt: float = 0.1
    ):
        """
        Compute INL dynamics on TPU.

        Accepts both JAX arrays and PyTorch tensors (auto-converts).
        """
        if not HAS_JAX:
            raise RuntimeError("JAX not available for TPU backend")

        # Convert from PyTorch if needed
        is_torch = False
        try:
            import torch
            if isinstance(x, torch.Tensor):
                is_torch = True
                x = jnp.array(x.cpu().numpy())
                v = jnp.array(v.cpu().numpy())
                mu = jnp.array(mu.cpu().numpy())
                alpha = jnp.array(alpha.cpu().numpy())
                beta = jnp.array(beta.cpu().numpy())
                gate = jnp.array(gate.cpu().numpy())
        except ImportError:
            pass

        # Compute
        x_next, v_next = _jax_inl_dynamics(x, v, mu, alpha, beta, gate, dt)

        # Convert back to PyTorch if needed
        if is_torch:
            import torch
            x_next = torch.from_numpy(jax.device_get(x_next))
            v_next = torch.from_numpy(jax.device_get(v_next))

        return x_next, v_next

    @staticmethod
    def inl_dynamics_n_steps(
        x, v, mu, alphas, betas, gates, dt: float = 0.1
    ):
        """Run n steps efficiently using lax.scan."""
        if not HAS_JAX:
            raise RuntimeError("JAX not available")
        return _jax_inl_n_steps(x, v, mu, alphas, betas, gates, dt)

    @staticmethod
    def moe_dispatch(x, router_logits, top_k: int = 2):
        """MoE dispatch on TPU."""
        if not HAS_JAX:
            raise RuntimeError("JAX not available")
        return _jax_moe_dispatch(x, router_logits, top_k)

    @staticmethod
    def moe_combine(expert_outputs, expert_weights, batch_size: int, top_k: int):
        """MoE combine on TPU."""
        if not HAS_JAX:
            raise RuntimeError("JAX not available")
        return _jax_moe_combine(expert_outputs, expert_weights, batch_size, top_k)

    @staticmethod
    def batched_expert_forward(
        ctx, expert_indices, expert_w1, expert_b1, expert_w2, expert_b2
    ):
        """Batched expert forward on TPU."""
        if not HAS_JAX:
            raise RuntimeError("JAX not available")
        return _jax_batched_expert_forward(
            ctx, expert_indices, expert_w1, expert_b1, expert_w2, expert_b2
        )


def benchmark_tpu_backend(batch_size: int = 4096, dim: int = 1024, n_iter: int = 100):
    """Benchmark TPU backend."""
    if not HAS_JAX:
        print("JAX not available")
        return

    import time

    # Create test data
    key = jax.random.PRNGKey(42)
    keys = jax.random.split(key, 6)

    x = jax.random.normal(keys[0], (batch_size, dim))
    v = jax.random.normal(keys[1], (batch_size, dim))
    mu = jax.random.normal(keys[2], (dim,))
    alpha = jax.nn.sigmoid(jax.random.normal(keys[3], (batch_size, dim)))
    beta = jax.nn.softplus(jax.random.normal(keys[4], (batch_size, dim)))
    gate = jax.nn.sigmoid(jax.random.normal(keys[5], (batch_size, dim)))
    dt = 0.1

    # Warmup
    for _ in range(10):
        _ = TPUBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)
    jax.block_until_ready(x)

    # Benchmark
    start = time.perf_counter()
    for _ in range(n_iter):
        x_next, v_next = TPUBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)
    jax.block_until_ready(x_next)
    elapsed = (time.perf_counter() - start) / n_iter * 1000

    devices = jax.devices()
    device_type = devices[0].platform if devices else "unknown"

    print(f"TPU Backend Benchmark (batch={batch_size}, dim={dim})")
    print(f"  Device: {device_type}")
    print(f"  Time: {elapsed:.3f} ms/step")

    return elapsed


if __name__ == "__main__":
    benchmark_tpu_backend()
