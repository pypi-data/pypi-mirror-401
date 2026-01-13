"""
Cross-platform INL operations.

These functions automatically dispatch to the best available backend.
"""

from .inl_dynamics import inl_dynamics, inl_dynamics_step
from .moe_routing import MoERouter, moe_dispatch, moe_combine
from .fused_ops import fused_inl_moe, FusedINLLayer

__all__ = [
    "inl_dynamics",
    "inl_dynamics_step",
    "MoERouter",
    "moe_dispatch",
    "moe_combine",
    "fused_inl_moe",
    "FusedINLLayer",
]
