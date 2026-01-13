"""
TPU-INL: Cross-Platform Integrator Neuron Layer Acceleration

Unified API for INL dynamics across:
- TPU (JAX/Pallas)
- GPU (Triton/CUDA)
- DirectML (Windows GPU)
- CPU (PyTorch fallback)

Usage:
    from tpu_inl import inl_dynamics, MoEIntegrator, get_backend

    # Auto-detects best backend
    x_next, v_next = inl_dynamics(x, v, mu, alpha, beta, gate, dt)

    # Check which backend is active
    print(f"Using backend: {get_backend()}")

    # Load Complexity model with auto-acceleration
    from tpu_inl.models import load_complexity_model
    model = load_complexity_model("Pacific-Prime/complexity-tiny")
    output = model.generate("Hello, how are you?")

Author: Boris Peyriguere / Pacific Prime
"""

__version__ = "0.2.2"

from .autodetect import get_backend, set_backend, Backend
from .ops.inl_dynamics import inl_dynamics, inl_dynamics_step
from .ops.moe_routing import MoERouter, moe_dispatch, moe_combine
from .ops.fused_ops import fused_inl_moe, FusedINLLayer

# Model loaders
from .models import load_complexity_model, ComplexityWrapper, COMPLEXITY_AVAILABLE

__all__ = [
    # Backend detection
    "get_backend",
    "set_backend",
    "Backend",
    # INL dynamics
    "inl_dynamics",
    "inl_dynamics_step",
    # MoE routing
    "MoERouter",
    "moe_dispatch",
    "moe_combine",
    # Fused operations
    "fused_inl_moe",
    "FusedINLLayer",
    # Model loaders
    "load_complexity_model",
    "ComplexityWrapper",
    "COMPLEXITY_AVAILABLE",
]
