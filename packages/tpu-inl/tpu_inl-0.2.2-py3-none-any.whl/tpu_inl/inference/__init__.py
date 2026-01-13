"""
TPU-INL Inference Runtime

High-performance inference runtime for INL models across all backends.
Optimized for real-time and streaming applications.

Features:
---------
- Cross-platform: TPU, CUDA, AMD, Intel, DirectML, CPU
- Real-time streaming with KV cache
- Batched inference for throughput
- Continuous batching for variable-length inputs
- Speculative decoding support
- Quantized inference (INT8, FP8)

Usage:
------
from tpu_inl.inference import InferenceEngine, StreamingSession

# Create engine
engine = InferenceEngine(model, backend="auto")

# Single inference
output = engine.generate(prompt, max_tokens=100)

# Streaming inference
async for token in engine.stream(prompt):
    print(token, end="", flush=True)

# Real-time session
session = StreamingSession(engine)
session.start()
response = await session.generate("Hello!")
"""

from .engine import InferenceEngine, EngineConfig, GenerationConfig, GenerationMode
from .streaming import StreamingSession, StreamingConfig, StreamingMode, StreamingEngine
from .kv_cache import KVCache, PagedKVCache
from .batching import BatchScheduler, ContinuousBatcher
from .speculative import SpeculativeDecoder

__all__ = [
    # Core engine
    "InferenceEngine",
    "EngineConfig",
    "GenerationConfig",
    "GenerationMode",
    # Streaming
    "StreamingSession",
    "StreamingConfig",
    "StreamingMode",
    "StreamingEngine",
    # KV Cache
    "KVCache",
    "PagedKVCache",
    # Batching
    "BatchScheduler",
    "ContinuousBatcher",
    # Speculative decoding
    "SpeculativeDecoder",
]
