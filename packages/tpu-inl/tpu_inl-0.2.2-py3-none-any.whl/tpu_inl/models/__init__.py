"""
TPU-INL Model Support

Provides unified loading and inference for supported model architectures:
- Complexity (Token-Routed MLP with MoE)
- INL-LLM v3 (Integrator Neuron Layer)
"""

from .complexity import (
    load_complexity_model,
    ComplexityWrapper,
    COMPLEXITY_AVAILABLE,
)

__all__ = [
    "load_complexity_model",
    "ComplexityWrapper",
    "COMPLEXITY_AVAILABLE",
]
