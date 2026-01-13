"""
Cross-platform INL Dynamics

Unified API for INL dynamics that works on TPU, GPU, and CPU.
Automatically dispatches to the best available backend.
"""

from typing import Tuple, Union, Optional
from ..autodetect import get_backend, Backend

# Import backends
from ..backends.cpu import CPUBackend
from ..backends.cuda import CUDABackend
from ..backends.tpu import TPUBackend


def inl_dynamics(
    x,
    v,
    mu,
    alpha,
    beta,
    gate,
    dt: float = 0.1,
    backend: Optional[Backend] = None
) -> Tuple:
    """
    Compute one step of INL dynamics.

    Damped harmonic oscillator:
        error = x - mu
        v_next = alpha * v - beta * error
        x_next = x + dt * gate * v_next

    This is the core computation of Integrator Neurons.

    Args:
        x: State tensor [batch, ..., dim]
        v: Velocity tensor [batch, ..., dim]
        mu: Equilibrium point [dim] (broadcasts)
        alpha: Damping coefficient (0-1, controls momentum)
        beta: Spring constant (controls attraction to mu)
        gate: Output gate (0-1, controls update magnitude)
        dt: Time step (default 0.1)
        backend: Force specific backend (default: auto-detect)

    Returns:
        x_next: Updated state
        v_next: Updated velocity

    Example:
        >>> from tpu_inl import inl_dynamics
        >>> x_next, v_next = inl_dynamics(x, v, mu, alpha, beta, gate)
    """
    if backend is None:
        backend = get_backend()

    if backend == Backend.TPU:
        return TPUBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)
    elif backend == Backend.CUDA:
        return CUDABackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)
    else:
        return CPUBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)


def inl_dynamics_step(
    x,
    v,
    mu,
    controller_output,
    dt: float = 0.1,
    backend: Optional[Backend] = None
) -> Tuple:
    """
    INL dynamics step with controller output.

    Convenience wrapper that splits controller output into alpha, beta, gate.

    Args:
        x: State tensor [batch, ..., dim]
        v: Velocity tensor [batch, ..., dim]
        mu: Equilibrium point [dim]
        controller_output: [batch, ..., 3*dim] containing [alpha, beta, gate]
        dt: Time step
        backend: Force specific backend

    Returns:
        x_next, v_next
    """
    import torch

    dim = x.shape[-1]

    # Split controller output
    alpha_raw = controller_output[..., :dim]
    beta_raw = controller_output[..., dim:2*dim]
    gate_raw = controller_output[..., 2*dim:]

    # Apply activations
    alpha = torch.sigmoid(alpha_raw)
    beta = torch.nn.functional.softplus(beta_raw)
    gate = torch.sigmoid(gate_raw)

    return inl_dynamics(x, v, mu, alpha, beta, gate, dt, backend)


def inl_dynamics_n_steps(
    x,
    v,
    mu,
    controller_fn,
    n_steps: int,
    dt: float = 0.1,
    backend: Optional[Backend] = None
):
    """
    Run INL dynamics for n steps with a controller.

    Args:
        x: Initial state
        v: Initial velocity
        mu: Equilibrium point
        controller_fn: Function (x, v) -> (alpha, beta, gate)
        n_steps: Number of integration steps
        dt: Time step
        backend: Force specific backend

    Returns:
        Final x, v
    """
    if backend is None:
        backend = get_backend()

    # For TPU, we could use lax.scan for better efficiency
    # For now, use simple loop that works on all backends
    for _ in range(n_steps):
        alpha, beta, gate = controller_fn(x, v)
        x, v = inl_dynamics(x, v, mu, alpha, beta, gate, dt, backend)

    return x, v


# ============================================================================
# PyTorch Module Wrapper
# ============================================================================

try:
    import torch
    import torch.nn as nn

    class INLDynamicsLayer(nn.Module):
        """
        PyTorch module for INL dynamics with learnable parameters.

        Cross-platform: works on TPU, GPU, and CPU.
        """

        def __init__(
            self,
            dim: int,
            dt: float = 0.1,
            learnable_mu: bool = True,
            controller_hidden: int = 64
        ):
            super().__init__()
            self.dim = dim
            self.dt = dt

            # Learnable equilibrium
            if learnable_mu:
                self.mu = nn.Parameter(torch.zeros(dim))
            else:
                self.register_buffer('mu', torch.zeros(dim))

            # Controller: (x, v) -> (alpha, beta, gate)
            self.controller = nn.Sequential(
                nn.Linear(dim * 2, controller_hidden),
                nn.GELU(),
                nn.Linear(controller_hidden, dim * 3)
            )

        def forward(self, x: torch.Tensor, v: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
            """
            Forward pass.

            Args:
                x: State [batch, ..., dim]
                v: Velocity [batch, ..., dim]

            Returns:
                x_next, v_next
            """
            # Build context
            ctx = torch.cat([x, v], dim=-1)

            # Get controller output
            ctrl_out = self.controller(ctx)

            # Compute dynamics
            return inl_dynamics_step(x, v, self.mu, ctrl_out, self.dt)

except ImportError:
    INLDynamicsLayer = None
