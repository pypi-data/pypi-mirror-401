"""
Fused INL Operations

Combines multiple operations into single kernels for efficiency.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple

from .moe_routing import MoERouter, moe_dispatch, moe_combine


class FusedINLLayer(nn.Module):
    """
    Fused INL layer with optional MoE.

    Combines attention, INL dynamics, and MoE into optimized operations.
    """

    def __init__(
        self,
        hidden_size: int,
        num_heads: int,
        feedforward_dim: int,
        num_iterations: int = 2,
        use_moe: bool = False,
        num_experts: int = 4,
        top_k: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.head_dim = hidden_size // num_heads
        self.num_iterations = num_iterations
        self.use_moe = use_moe

        # Attention projections
        self.qkv_proj = nn.Linear(hidden_size, 3 * hidden_size)
        self.out_proj = nn.Linear(hidden_size, hidden_size)

        # INL dynamics
        self.iteration_gate = nn.Linear(hidden_size, hidden_size)
        self.iteration_norm = nn.LayerNorm(hidden_size)

        # Feedforward / MoE
        if use_moe:
            self.router = MoERouter(hidden_size, num_experts, top_k)
            self.experts = nn.ModuleList([
                nn.Sequential(
                    nn.Linear(hidden_size, feedforward_dim),
                    nn.GELU(),
                    nn.Linear(feedforward_dim, hidden_size),
                )
                for _ in range(num_experts)
            ])
        else:
            self.ff = nn.Sequential(
                nn.Linear(hidden_size, feedforward_dim),
                nn.GELU(),
                nn.Linear(feedforward_dim, hidden_size),
            )

        # Norms
        self.attn_norm = nn.LayerNorm(hidden_size)
        self.ff_norm = nn.LayerNorm(hidden_size)

        self.dropout = nn.Dropout(dropout)

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        Forward pass with fused operations.

        Args:
            hidden_states: [batch, seq_len, hidden_size]
            attention_mask: Optional attention mask

        Returns:
            output: [batch, seq_len, hidden_size]
            aux_loss: MoE load balancing loss (if using MoE)
        """
        batch_size, seq_len, _ = hidden_states.shape

        # === Attention ===
        residual = hidden_states
        hidden_states = self.attn_norm(hidden_states)

        # QKV projection
        qkv = self.qkv_proj(hidden_states)
        qkv = qkv.view(batch_size, seq_len, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)  # [3, batch, heads, seq, head_dim]
        q, k, v = qkv[0], qkv[1], qkv[2]

        # Attention with optional mask
        attn_weights = torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        if attention_mask is not None:
            attn_weights = attn_weights + attention_mask
        attn_weights = F.softmax(attn_weights, dim=-1)
        attn_output = torch.matmul(attn_weights, v)

        # Reshape and project
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.view(batch_size, seq_len, self.hidden_size)
        attn_output = self.out_proj(attn_output)
        attn_output = self.dropout(attn_output)

        hidden_states = residual + attn_output

        # === INL Dynamics ===
        for _ in range(self.num_iterations):
            gate = torch.sigmoid(self.iteration_gate(hidden_states))
            hidden_states = hidden_states + gate * self.iteration_norm(hidden_states)

        # === Feedforward / MoE ===
        residual = hidden_states
        hidden_states = self.ff_norm(hidden_states)

        aux_loss = None
        if self.use_moe:
            # Route to experts
            routing_weights, selected_experts, aux_loss = self.router(hidden_states)

            # Dispatch to experts
            expert_inputs, expert_indices = moe_dispatch(
                hidden_states, routing_weights, selected_experts, len(self.experts)
            )

            # Process through experts
            expert_outputs = []
            for expert, inputs in zip(self.experts, expert_inputs):
                if inputs.shape[0] > 0:
                    expert_outputs.append(expert(inputs))
                else:
                    expert_outputs.append(inputs)

            # Combine outputs
            hidden_states = moe_combine(
                expert_outputs, expert_indices,
                routing_weights, selected_experts,
                (batch_size, seq_len, self.hidden_size)
            )
        else:
            hidden_states = self.ff(hidden_states)

        hidden_states = self.dropout(hidden_states)
        hidden_states = residual + hidden_states

        return hidden_states, aux_loss


def fused_inl_moe(
    hidden_states: torch.Tensor,
    router: MoERouter,
    experts: nn.ModuleList,
    norm: nn.LayerNorm,
) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
    """
    Fused INL + MoE operation.

    Args:
        hidden_states: [batch, seq_len, hidden_size]
        router: MoE router module
        experts: List of expert modules
        norm: Layer norm

    Returns:
        output: [batch, seq_len, hidden_size]
        aux_loss: Load balancing loss
    """
    batch_size, seq_len, hidden_size = hidden_states.shape

    # Normalize
    normed = norm(hidden_states)

    # Route
    routing_weights, selected_experts, aux_loss = router(normed)

    # Dispatch
    expert_inputs, expert_indices = moe_dispatch(
        normed, routing_weights, selected_experts, len(experts)
    )

    # Process
    expert_outputs = []
    for expert, inputs in zip(experts, expert_inputs):
        if inputs.shape[0] > 0:
            expert_outputs.append(expert(inputs))
        else:
            expert_outputs.append(inputs)

    # Combine
    output = moe_combine(
        expert_outputs, expert_indices,
        routing_weights, selected_experts,
        (batch_size, seq_len, hidden_size)
    )

    return hidden_states + output, aux_loss
