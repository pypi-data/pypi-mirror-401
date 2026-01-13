"""
Work scheduling optimizations for parallel execution.

Handles:
- Optimal parallelism across devices (multi-GPU, multi-TPU)
- Pipeline parallelism for large models
- Tensor parallelism for wide models
- Expert parallelism for MoE
"""

import torch
import torch.nn as nn
from typing import Optional, List, Dict, Any, Tuple, Callable
from dataclasses import dataclass
from enum import Enum
import threading
from queue import Queue


class ParallelismType(Enum):
    """Types of parallelism."""
    DATA = "data"          # Same model, different data (DDP)
    TENSOR = "tensor"      # Split layers across devices (Megatron-style)
    PIPELINE = "pipeline"  # Split layers sequentially
    EXPERT = "expert"      # MoE expert parallelism
    SEQUENCE = "sequence"  # Split sequence dimension (long context)


@dataclass
class SchedulingConfig:
    """Configuration for work scheduling."""
    # Parallelism
    parallelism: ParallelismType = ParallelismType.DATA
    num_devices: int = 1

    # Pipeline
    num_microbatches: int = 4
    pipeline_chunks: int = 4

    # Tensor parallel
    tensor_parallel_size: int = 1

    # Expert parallel
    expert_parallel_size: int = 1

    # Memory
    gradient_checkpointing: bool = False
    offload_to_cpu: bool = False


class DeviceScheduler:
    """
    Schedules work across multiple devices.
    """

    def __init__(self, config: Optional[SchedulingConfig] = None):
        self.config = config or SchedulingConfig()
        self.devices = self._detect_devices()

    def _detect_devices(self) -> List[torch.device]:
        """Detect available devices."""
        devices = []

        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                devices.append(torch.device(f"cuda:{i}"))
        elif hasattr(torch, 'xpu') and torch.xpu.is_available():
            for i in range(torch.xpu.device_count()):
                devices.append(torch.device(f"xpu:{i}"))
        else:
            devices.append(torch.device("cpu"))

        return devices[:self.config.num_devices] if self.config.num_devices > 0 else devices

    def get_placement(self, layer_idx: int, num_layers: int) -> torch.device:
        """
        Get device placement for a layer.

        Args:
            layer_idx: Layer index
            num_layers: Total number of layers

        Returns:
            Device for this layer
        """
        if len(self.devices) == 1:
            return self.devices[0]

        if self.config.parallelism == ParallelismType.PIPELINE:
            # Distribute layers evenly across devices
            layers_per_device = num_layers // len(self.devices)
            device_idx = min(layer_idx // layers_per_device, len(self.devices) - 1)
            return self.devices[device_idx]

        # Default to first device
        return self.devices[0]


class PipelineScheduler:
    """
    Pipeline parallel scheduler for large models.

    Implements 1F1B (one forward, one backward) schedule for
    efficient pipeline utilization.
    """

    def __init__(
        self,
        num_stages: int,
        num_microbatches: int,
        schedule: str = "1f1b"
    ):
        self.num_stages = num_stages
        self.num_microbatches = num_microbatches
        self.schedule = schedule

        # Compute schedule
        self.forward_schedule = []
        self.backward_schedule = []
        self._compute_schedule()

    def _compute_schedule(self):
        """Compute forward/backward schedule."""
        if self.schedule == "1f1b":
            self._compute_1f1b_schedule()
        elif self.schedule == "gpipe":
            self._compute_gpipe_schedule()
        else:
            raise ValueError(f"Unknown schedule: {self.schedule}")

    def _compute_1f1b_schedule(self):
        """
        Compute 1F1B schedule.

        Warmup phase: fill pipeline
        Steady state: 1 forward, 1 backward per step
        Cooldown: drain pipeline
        """
        # Warmup: forward passes to fill pipeline
        for mb in range(min(self.num_stages, self.num_microbatches)):
            self.forward_schedule.append(mb)

        # Steady state: interleaved forward/backward
        for mb in range(self.num_stages, self.num_microbatches):
            self.forward_schedule.append(mb)
            self.backward_schedule.append(mb - self.num_stages)

        # Cooldown: drain remaining backwards
        for mb in range(self.num_microbatches - self.num_stages, self.num_microbatches):
            self.backward_schedule.append(mb)

    def _compute_gpipe_schedule(self):
        """
        Compute GPipe schedule.

        All forwards first, then all backwards.
        Simple but has bubble (idle time).
        """
        self.forward_schedule = list(range(self.num_microbatches))
        self.backward_schedule = list(range(self.num_microbatches))

    def get_bubble_ratio(self) -> float:
        """
        Calculate pipeline bubble ratio.

        Bubble = idle time / total time
        """
        # For 1F1B: bubble = (num_stages - 1) / num_microbatches
        if self.schedule == "1f1b":
            return (self.num_stages - 1) / self.num_microbatches
        else:  # GPipe
            return (self.num_stages - 1) / (self.num_stages + self.num_microbatches - 1)


class TensorParallelizer:
    """
    Tensor parallelism for splitting layers across devices.

    Megatron-style column/row parallelism for linear layers.
    """

    def __init__(self, world_size: int, rank: int):
        self.world_size = world_size
        self.rank = rank

    def column_parallel_linear(
        self,
        weight: torch.Tensor,
        bias: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        Split linear layer column-wise (output dim).

        A @ W^T -> [A @ W_0^T, A @ W_1^T, ...]
        Each device gets 1/world_size of output features.
        """
        out_features = weight.shape[0]
        features_per_rank = out_features // self.world_size

        start = self.rank * features_per_rank
        end = start + features_per_rank

        weight_shard = weight[start:end]
        bias_shard = bias[start:end] if bias is not None else None

        return weight_shard, bias_shard

    def row_parallel_linear(
        self,
        weight: torch.Tensor,
        bias: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        Split linear layer row-wise (input dim).

        [A_0, A_1, ...] @ [W_0; W_1; ...]^T
        Each device gets 1/world_size of input features.
        Requires all-reduce at output.
        """
        in_features = weight.shape[1]
        features_per_rank = in_features // self.world_size

        start = self.rank * features_per_rank
        end = start + features_per_rank

        weight_shard = weight[:, start:end]
        # Bias only on rank 0 (or after all-reduce)
        bias_shard = bias if self.rank == 0 and bias is not None else None

        return weight_shard, bias_shard


class ExpertParallelizer:
    """
    Expert parallelism for MoE models.

    Distributes experts across devices and handles routing.
    """

    def __init__(
        self,
        num_experts: int,
        world_size: int,
        rank: int
    ):
        self.num_experts = num_experts
        self.world_size = world_size
        self.rank = rank

        # Calculate experts per device
        self.experts_per_rank = num_experts // world_size
        self.local_expert_start = rank * self.experts_per_rank
        self.local_expert_end = self.local_expert_start + self.experts_per_rank

    def get_local_experts(self) -> List[int]:
        """Get expert indices assigned to this rank."""
        return list(range(self.local_expert_start, self.local_expert_end))

    def route_tokens(
        self,
        tokens: torch.Tensor,
        expert_indices: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Route tokens to local experts.

        Args:
            tokens: Token embeddings [batch, seq, dim]
            expert_indices: Expert assignment [batch, seq]

        Returns:
            Local tokens and their indices
        """
        # Flatten
        flat_tokens = tokens.view(-1, tokens.shape[-1])
        flat_indices = expert_indices.view(-1)

        # Filter to local experts
        local_mask = (flat_indices >= self.local_expert_start) & \
                     (flat_indices < self.local_expert_end)

        local_tokens = flat_tokens[local_mask]
        local_expert_ids = flat_indices[local_mask] - self.local_expert_start

        return local_tokens, local_expert_ids

    def all_to_all_dispatch(
        self,
        tokens: torch.Tensor,
        expert_indices: torch.Tensor,
        group: Optional[Any] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        All-to-all dispatch for expert parallelism.

        Redistributes tokens so each device only processes its experts.
        """
        if group is None and torch.distributed.is_initialized():
            group = torch.distributed.group.WORLD

        # Simplified version - full implementation would use all_to_all
        return self.route_tokens(tokens, expert_indices)


class SequenceParallelizer:
    """
    Sequence parallelism for long context.

    Splits sequence dimension across devices.
    Used with Ring Attention for linear scaling with context length.
    """

    def __init__(self, world_size: int, rank: int):
        self.world_size = world_size
        self.rank = rank

    def split_sequence(
        self,
        hidden_states: torch.Tensor
    ) -> torch.Tensor:
        """
        Split sequence across devices.

        Args:
            hidden_states: [batch, seq, dim]

        Returns:
            Local sequence shard [batch, seq/world_size, dim]
        """
        batch, seq, dim = hidden_states.shape
        chunk_size = seq // self.world_size

        start = self.rank * chunk_size
        end = start + chunk_size

        return hidden_states[:, start:end, :]

    def gather_sequence(
        self,
        local_hidden: torch.Tensor,
        group: Optional[Any] = None
    ) -> torch.Tensor:
        """
        Gather sequence shards from all devices.

        Args:
            local_hidden: Local sequence shard [batch, seq/world_size, dim]

        Returns:
            Full sequence [batch, seq, dim]
        """
        if not torch.distributed.is_initialized():
            return local_hidden

        # All-gather along sequence dimension
        gathered = [torch.zeros_like(local_hidden) for _ in range(self.world_size)]
        torch.distributed.all_gather(gathered, local_hidden, group=group)

        return torch.cat(gathered, dim=1)


def get_optimal_parallelism(
    model_size_params: int,
    num_devices: int,
    memory_per_device_gb: float
) -> SchedulingConfig:
    """
    Recommend optimal parallelism strategy based on model and hardware.

    Args:
        model_size_params: Number of model parameters
        num_devices: Number of available devices
        memory_per_device_gb: GPU memory per device

    Returns:
        Recommended SchedulingConfig
    """
    config = SchedulingConfig(num_devices=num_devices)

    # Estimate memory requirement (rough: 4 bytes per param for fp32)
    model_memory_gb = model_size_params * 4 / 1e9

    # If model fits on one device, use data parallelism
    if model_memory_gb < memory_per_device_gb * 0.7:  # 70% threshold
        config.parallelism = ParallelismType.DATA
        return config

    # If model needs 2-4x more memory, use tensor parallelism
    if model_memory_gb < memory_per_device_gb * num_devices * 0.7:
        config.parallelism = ParallelismType.TENSOR
        config.tensor_parallel_size = min(
            num_devices,
            int(model_memory_gb / (memory_per_device_gb * 0.5)) + 1
        )
        return config

    # For very large models, use pipeline parallelism
    config.parallelism = ParallelismType.PIPELINE
    config.gradient_checkpointing = True
    return config
