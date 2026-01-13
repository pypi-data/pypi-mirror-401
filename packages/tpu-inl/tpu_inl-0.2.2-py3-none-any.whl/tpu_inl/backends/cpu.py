"""
CPU Backend - PyTorch Fallback

Pure PyTorch implementation of INL dynamics.
Used when no accelerator (TPU/GPU) is available.

This is the reference implementation - other backends should produce
identical results (within floating point tolerance).
"""

import torch
import torch.nn.functional as F
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class CPUBackend:
    """CPU backend using pure PyTorch."""

    name: str = "cpu"

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
        Compute INL dynamics step.

        Damped harmonic oscillator:
            error = x - mu
            v_next = alpha * v - beta * error
            x_next = x + dt * gate * v_next

        Args:
            x: State tensor [batch, ..., dim]
            v: Velocity tensor [batch, ..., dim]
            mu: Equilibrium point [dim] or broadcastable
            alpha: Damping coefficient [batch, ..., dim]
            beta: Spring constant [batch, ..., dim]
            gate: Output gate [batch, ..., dim]
            dt: Time step

        Returns:
            x_next, v_next: Updated state and velocity
        """
        error = x - mu
        v_next = alpha * v - beta * error
        x_next = x + dt * gate * v_next
        return x_next, v_next

    @staticmethod
    def inl_dynamics_n_steps(
        x: torch.Tensor,
        v: torch.Tensor,
        mu: torch.Tensor,
        controller_fn,
        n_steps: int,
        dt: float = 0.1
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Run INL dynamics for n steps.

        Args:
            x: Initial state
            v: Initial velocity
            mu: Equilibrium point
            controller_fn: Function (x, v) -> (alpha, beta, gate)
            n_steps: Number of integration steps
            dt: Time step

        Returns:
            Final x, v
        """
        for _ in range(n_steps):
            alpha, beta, gate = controller_fn(x, v)
            x, v = CPUBackend.inl_dynamics(x, v, mu, alpha, beta, gate, dt)
        return x, v

    @staticmethod
    def moe_dispatch(
        x: torch.Tensor,
        router_logits: torch.Tensor,
        top_k: int = 2
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        MoE dispatch - route inputs to experts.

        Args:
            x: Input tensor [batch, dim]
            router_logits: Router scores [batch, num_experts]
            top_k: Number of experts per token

        Returns:
            expanded_x: [batch * top_k, dim]
            expert_indices: [batch * top_k]
            expert_weights: [batch * top_k]
        """
        # Softmax routing
        router_probs = F.softmax(router_logits, dim=-1)

        # Top-k selection
        top_k_probs, top_k_indices = torch.topk(router_probs, top_k, dim=-1)

        # Normalize weights
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)

        # Expand inputs for each expert
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
        """
        MoE combine - aggregate expert outputs.

        Args:
            expert_outputs: [batch * top_k, dim]
            expert_weights: [batch * top_k]
            batch_size: Original batch size
            top_k: Number of experts per token

        Returns:
            combined: [batch, dim]
        """
        dim = expert_outputs.shape[-1]

        # Weight outputs
        weighted = expert_outputs * expert_weights.unsqueeze(-1)

        # Reshape and sum
        weighted = weighted.view(batch_size, top_k, dim)
        combined = weighted.sum(dim=1)

        return combined

    @staticmethod
    def batched_expert_forward(
        ctx: torch.Tensor,
        expert_indices: torch.Tensor,
        expert_w1: torch.Tensor,
        expert_b1: torch.Tensor,
        expert_w2: torch.Tensor,
        expert_b2: torch.Tensor
    ) -> torch.Tensor:
        """
        Batched expert MLP forward.

        Args:
            ctx: Context [n_tokens, ctx_dim]
            expert_indices: Which expert for each token [n_tokens]
            expert_w1: [num_experts, ctx_dim, hidden]
            expert_b1: [num_experts, hidden]
            expert_w2: [num_experts, hidden, out_dim]
            expert_b2: [num_experts, out_dim]

        Returns:
            output: [n_tokens, out_dim]
        """
        # Gather weights for each token's expert
        w1 = expert_w1[expert_indices]  # [n, ctx_dim, hidden]
        b1 = expert_b1[expert_indices]  # [n, hidden]
        w2 = expert_w2[expert_indices]  # [n, hidden, out]
        b2 = expert_b2[expert_indices]  # [n, out]

        # Layer 1: bmm
        hidden = torch.bmm(ctx.unsqueeze(1), w1).squeeze(1) + b1
        hidden = F.gelu(hidden)

        # Layer 2: bmm
        out = torch.bmm(hidden.unsqueeze(1), w2).squeeze(1) + b2

        return out
