"""
MoE (Mixture of Experts) Routing Operations

Cross-platform MoE routing with automatic backend selection.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional


class MoERouter(nn.Module):
    """
    Mixture of Experts Router.

    Supports top-k routing with load balancing.
    """

    def __init__(
        self,
        hidden_size: int,
        num_experts: int,
        top_k: int = 2,
        capacity_factor: float = 1.25,
        use_aux_loss: bool = True,
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_experts = num_experts
        self.top_k = top_k
        self.capacity_factor = capacity_factor
        self.use_aux_loss = use_aux_loss

        # Router gate
        self.gate = nn.Linear(hidden_size, num_experts, bias=False)

    def forward(
        self,
        hidden_states: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, Optional[torch.Tensor]]:
        """
        Route tokens to experts.

        Args:
            hidden_states: [batch, seq_len, hidden_size]

        Returns:
            routing_weights: [batch, seq_len, top_k]
            selected_experts: [batch, seq_len, top_k]
            aux_loss: Load balancing loss (if use_aux_loss)
        """
        batch_size, seq_len, _ = hidden_states.shape

        # Compute router logits
        router_logits = self.gate(hidden_states)  # [batch, seq_len, num_experts]

        # Get top-k experts
        routing_weights, selected_experts = torch.topk(
            router_logits, self.top_k, dim=-1
        )
        routing_weights = F.softmax(routing_weights, dim=-1)

        # Compute auxiliary loss for load balancing
        aux_loss = None
        if self.use_aux_loss and self.training:
            # Router probability distribution
            router_probs = F.softmax(router_logits, dim=-1)

            # Fraction of tokens routed to each expert
            tokens_per_expert = router_probs.mean(dim=[0, 1])

            # Load balancing loss (encourage uniform distribution)
            aux_loss = self.num_experts * (tokens_per_expert ** 2).sum()

        return routing_weights, selected_experts, aux_loss


def moe_dispatch(
    hidden_states: torch.Tensor,
    routing_weights: torch.Tensor,
    selected_experts: torch.Tensor,
    num_experts: int,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Dispatch tokens to their selected experts.

    Args:
        hidden_states: [batch, seq_len, hidden_size]
        routing_weights: [batch, seq_len, top_k]
        selected_experts: [batch, seq_len, top_k]
        num_experts: Total number of experts

    Returns:
        dispatched: List of tensors for each expert
        indices: Indices for recombining
    """
    batch_size, seq_len, hidden_size = hidden_states.shape
    top_k = selected_experts.shape[-1]

    # Flatten for easier processing
    flat_hidden = hidden_states.view(-1, hidden_size)
    flat_experts = selected_experts.view(-1, top_k)
    flat_weights = routing_weights.view(-1, top_k)

    # Create dispatch tensors for each expert
    expert_inputs = []
    expert_indices = []

    for expert_idx in range(num_experts):
        # Find tokens assigned to this expert
        mask = (flat_experts == expert_idx).any(dim=-1)
        indices = torch.where(mask)[0]

        if len(indices) > 0:
            expert_inputs.append(flat_hidden[indices])
            expert_indices.append(indices)
        else:
            expert_inputs.append(torch.zeros(0, hidden_size, device=hidden_states.device))
            expert_indices.append(torch.zeros(0, dtype=torch.long, device=hidden_states.device))

    return expert_inputs, expert_indices


def moe_combine(
    expert_outputs: list,
    expert_indices: list,
    routing_weights: torch.Tensor,
    selected_experts: torch.Tensor,
    output_shape: Tuple[int, ...],
) -> torch.Tensor:
    """
    Combine expert outputs back into original sequence.

    Args:
        expert_outputs: List of outputs from each expert
        expert_indices: Indices for each expert's tokens
        routing_weights: [batch, seq_len, top_k]
        selected_experts: [batch, seq_len, top_k]
        output_shape: Shape of output tensor

    Returns:
        combined: [batch, seq_len, hidden_size]
    """
    batch_size, seq_len, hidden_size = output_shape
    device = routing_weights.device

    # Initialize output
    combined = torch.zeros(batch_size * seq_len, hidden_size, device=device)

    flat_experts = selected_experts.view(-1, selected_experts.shape[-1])
    flat_weights = routing_weights.view(-1, routing_weights.shape[-1])

    # Add contributions from each expert
    for expert_idx, (outputs, indices) in enumerate(zip(expert_outputs, expert_indices)):
        if len(indices) == 0:
            continue

        # Get weights for this expert
        expert_mask = (flat_experts[indices] == expert_idx)
        weights = (flat_weights[indices] * expert_mask.float()).sum(dim=-1, keepdim=True)

        # Weighted add
        combined[indices] += outputs * weights

    return combined.view(batch_size, seq_len, hidden_size)
