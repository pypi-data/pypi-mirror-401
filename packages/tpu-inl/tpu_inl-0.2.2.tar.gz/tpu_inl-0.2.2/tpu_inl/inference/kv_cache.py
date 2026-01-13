"""
KV Cache implementations for efficient autoregressive generation.

Supports:
- Standard KV Cache (pre-allocated memory)
- Paged KV Cache (memory-efficient for long sequences)
- Multi-backend support (CUDA, TPU, CPU)
"""

import torch
import torch.nn as nn
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass
import math


@dataclass
class CacheConfig:
    """Configuration for KV cache."""
    max_batch_size: int = 32
    max_seq_len: int = 4096
    num_layers: int = 32
    num_heads: int = 32
    head_dim: int = 128
    dtype: torch.dtype = torch.bfloat16

    # Paged attention settings
    page_size: int = 16  # Tokens per page
    max_pages: int = 256  # Maximum pages in pool


class KVCache:
    """
    Standard KV Cache with pre-allocated memory.

    Memory layout: [batch, num_heads, seq_len, head_dim]
    """

    def __init__(
        self,
        max_batch_size: int = 32,
        max_seq_len: int = 4096,
        num_layers: int = 32,
        num_heads: int = 32,
        head_dim: int = 128,
        dtype: torch.dtype = torch.bfloat16,
        device: torch.device = None
    ):
        self.max_batch_size = max_batch_size
        self.max_seq_len = max_seq_len
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.head_dim = head_dim
        self.dtype = dtype
        self.device = device or torch.device("cpu")

        # Pre-allocate cache
        self._allocate_cache()

        # Track current position per batch element
        self.seq_positions = torch.zeros(max_batch_size, dtype=torch.long, device=self.device)

    def _allocate_cache(self):
        """Allocate cache tensors."""
        cache_shape = (
            self.num_layers,
            self.max_batch_size,
            self.num_heads,
            self.max_seq_len,
            self.head_dim
        )

        self.k_cache = torch.zeros(cache_shape, dtype=self.dtype, device=self.device)
        self.v_cache = torch.zeros(cache_shape, dtype=self.dtype, device=self.device)

        # Calculate memory usage
        bytes_per_element = 2 if self.dtype in [torch.float16, torch.bfloat16] else 4
        total_bytes = 2 * math.prod(cache_shape) * bytes_per_element
        print(f"[KVCache] Allocated {total_bytes / 1e9:.2f} GB for KV cache")

    def update(
        self,
        layer_idx: int,
        key: torch.Tensor,
        value: torch.Tensor,
        positions: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Update cache and return full key/value tensors.

        Args:
            layer_idx: Layer index
            key: New keys [batch, num_heads, seq_len, head_dim]
            value: New values [batch, num_heads, seq_len, head_dim]
            positions: Optional position indices

        Returns:
            Full cached keys and values up to current position
        """
        batch_size, num_heads, seq_len, head_dim = key.shape

        if positions is None:
            # Auto-increment positions
            start_pos = self.seq_positions[:batch_size]
            positions = start_pos.unsqueeze(1) + torch.arange(seq_len, device=self.device)
            self.seq_positions[:batch_size] += seq_len

        # Store new KV
        for b in range(batch_size):
            pos = positions[b] if positions.dim() > 1 else positions
            self.k_cache[layer_idx, b, :, pos] = key[b]
            self.v_cache[layer_idx, b, :, pos] = value[b]

        # Return full cache up to current position
        max_pos = self.seq_positions[:batch_size].max().item()
        return (
            self.k_cache[layer_idx, :batch_size, :, :max_pos],
            self.v_cache[layer_idx, :batch_size, :, :max_pos]
        )

    def get(self, layer_idx: int, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get cached KV for a layer."""
        max_pos = self.seq_positions[:batch_size].max().item()
        return (
            self.k_cache[layer_idx, :batch_size, :, :max_pos],
            self.v_cache[layer_idx, :batch_size, :, :max_pos]
        )

    def reset(self, batch_indices: Optional[torch.Tensor] = None):
        """Reset cache for specified batch indices or all."""
        if batch_indices is None:
            self.k_cache.zero_()
            self.v_cache.zero_()
            self.seq_positions.zero_()
        else:
            self.k_cache[:, batch_indices].zero_()
            self.v_cache[:, batch_indices].zero_()
            self.seq_positions[batch_indices] = 0

    def get_seq_length(self, batch_idx: int = 0) -> int:
        """Get current sequence length for a batch element."""
        return self.seq_positions[batch_idx].item()


class PagedKVCache:
    """
    Paged KV Cache for memory-efficient long sequence generation.

    Uses a page table to map logical positions to physical pages.
    This allows efficient memory sharing and reduces fragmentation.

    Based on vLLM's PagedAttention.
    """

    def __init__(
        self,
        num_layers: int = 32,
        num_heads: int = 32,
        head_dim: int = 128,
        page_size: int = 16,
        max_pages: int = 256,
        dtype: torch.dtype = torch.bfloat16,
        device: torch.device = None
    ):
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.head_dim = head_dim
        self.page_size = page_size
        self.max_pages = max_pages
        self.dtype = dtype
        self.device = device or torch.device("cpu")

        # Physical page pool: [num_layers, max_pages, page_size, num_heads, head_dim]
        self.k_pages = torch.zeros(
            (num_layers, max_pages, page_size, num_heads, head_dim),
            dtype=dtype, device=self.device
        )
        self.v_pages = torch.zeros(
            (num_layers, max_pages, page_size, num_heads, head_dim),
            dtype=dtype, device=self.device
        )

        # Free page list
        self.free_pages = list(range(max_pages))

        # Page tables per sequence: {seq_id: [page_indices]}
        self.page_tables: Dict[int, List[int]] = {}

        # Sequence positions
        self.seq_positions: Dict[int, int] = {}

        bytes_per_element = 2 if dtype in [torch.float16, torch.bfloat16] else 4
        total_bytes = 2 * num_layers * max_pages * page_size * num_heads * head_dim * bytes_per_element
        print(f"[PagedKVCache] Pool size: {total_bytes / 1e9:.2f} GB ({max_pages} pages)")

    def allocate_sequence(self, seq_id: int, initial_pages: int = 1) -> bool:
        """Allocate pages for a new sequence."""
        if len(self.free_pages) < initial_pages:
            return False

        pages = [self.free_pages.pop(0) for _ in range(initial_pages)]
        self.page_tables[seq_id] = pages
        self.seq_positions[seq_id] = 0
        return True

    def free_sequence(self, seq_id: int):
        """Free all pages for a sequence."""
        if seq_id in self.page_tables:
            self.free_pages.extend(self.page_tables[seq_id])
            del self.page_tables[seq_id]
            del self.seq_positions[seq_id]

    def _ensure_capacity(self, seq_id: int, required_pages: int) -> bool:
        """Ensure sequence has enough pages allocated."""
        current_pages = len(self.page_tables[seq_id])
        if current_pages >= required_pages:
            return True

        needed = required_pages - current_pages
        if len(self.free_pages) < needed:
            return False

        new_pages = [self.free_pages.pop(0) for _ in range(needed)]
        self.page_tables[seq_id].extend(new_pages)
        return True

    def update(
        self,
        seq_id: int,
        layer_idx: int,
        key: torch.Tensor,
        value: torch.Tensor
    ) -> bool:
        """
        Update cache for a sequence.

        Args:
            seq_id: Sequence identifier
            layer_idx: Layer index
            key: New keys [seq_len, num_heads, head_dim]
            value: New values [seq_len, num_heads, head_dim]

        Returns:
            True if successful
        """
        if seq_id not in self.page_tables:
            if not self.allocate_sequence(seq_id):
                return False

        seq_len = key.shape[0]
        start_pos = self.seq_positions[seq_id]
        end_pos = start_pos + seq_len

        # Calculate required pages
        required_pages = (end_pos + self.page_size - 1) // self.page_size
        if not self._ensure_capacity(seq_id, required_pages):
            return False

        # Write to pages
        pages = self.page_tables[seq_id]
        for i in range(seq_len):
            pos = start_pos + i
            page_idx = pos // self.page_size
            offset = pos % self.page_size
            physical_page = pages[page_idx]

            self.k_pages[layer_idx, physical_page, offset] = key[i]
            self.v_pages[layer_idx, physical_page, offset] = value[i]

        self.seq_positions[seq_id] = end_pos
        return True

    def get(
        self,
        seq_id: int,
        layer_idx: int
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get cached KV for a sequence.

        Returns:
            Keys and values [seq_len, num_heads, head_dim]
        """
        if seq_id not in self.page_tables:
            return None, None

        seq_len = self.seq_positions[seq_id]
        if seq_len == 0:
            return None, None

        pages = self.page_tables[seq_id]

        # Gather from pages
        keys = []
        values = []

        for pos in range(seq_len):
            page_idx = pos // self.page_size
            offset = pos % self.page_size
            physical_page = pages[page_idx]

            keys.append(self.k_pages[layer_idx, physical_page, offset])
            values.append(self.v_pages[layer_idx, physical_page, offset])

        return torch.stack(keys), torch.stack(values)

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        used_pages = self.max_pages - len(self.free_pages)
        return {
            "used_pages": used_pages,
            "free_pages": len(self.free_pages),
            "utilization": used_pages / self.max_pages,
            "active_sequences": len(self.page_tables),
            "total_tokens": sum(self.seq_positions.values())
        }


class RotaryEmbeddingCache:
    """
    Cache for rotary position embeddings (RoPE).

    Pre-computes cos/sin values for efficiency.
    """

    def __init__(
        self,
        dim: int,
        max_seq_len: int = 8192,
        base: float = 10000.0,
        device: torch.device = None
    ):
        self.dim = dim
        self.max_seq_len = max_seq_len
        self.base = base
        self.device = device or torch.device("cpu")

        # Compute inverse frequencies
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2, device=self.device).float() / dim))
        self.register_buffer("inv_freq", inv_freq)

        # Pre-compute embeddings
        self._build_cache()

    def _build_cache(self):
        """Build cos/sin cache."""
        positions = torch.arange(self.max_seq_len, device=self.device)
        freqs = torch.outer(positions, self.inv_freq)
        emb = torch.cat([freqs, freqs], dim=-1)

        self.cos_cache = emb.cos()
        self.sin_cache = emb.sin()

    def get(self, seq_len: int, offset: int = 0) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get cos/sin for positions [offset, offset + seq_len)."""
        return (
            self.cos_cache[offset:offset + seq_len],
            self.sin_cache[offset:offset + seq_len]
        )

    def register_buffer(self, name: str, tensor: torch.Tensor):
        """Register a buffer (for compatibility)."""
        setattr(self, name, tensor)
