# TPU-INL: Cross-Platform Integrator Neuron Layer Acceleration

Unified acceleration layer for INL dynamics across all hardware backends.

## Features

- **Cross-Platform**: TPU, CUDA, AMD ROCm, Intel XPU, DirectML, CPU
- **Automatic Backend Detection**: Selects the best backend for your hardware
- **Triton Kernels**: Fused INL dynamics for 3-5x speedup on GPU
- **JAX/XLA**: Native TPU support with auto-fusion
- **Inference Runtime**: KV cache, streaming, batching, speculative decoding

## Installation

```bash
# Basic installation
pip install -e .

# With CUDA/Triton acceleration
pip install -e ".[cuda]"

# With TPU support
pip install -e ".[tpu]"

# With Intel support
pip install -e ".[intel]"
```

## Quick Start

```python
from tpu_inl import inl_dynamics, get_backend

# Check detected backend
print(f"Using backend: {get_backend()}")

# INL dynamics (auto-accelerated)
x_next, v_next = inl_dynamics(x, v, mu, alpha, beta, gate, dt=0.1)
```

## Inference Engine

```python
from tpu_inl.inference import InferenceEngine, EngineConfig

# Create engine with auto-detected backend
config = EngineConfig(backend="auto", use_kv_cache=True)
engine = InferenceEngine(model, tokenizer, config)

# Generate
output = engine.generate("Hello, how are you?", max_tokens=100)

# Stream
for token in engine.stream("Tell me a story"):
    print(token, end="", flush=True)
```

## Supported Backends

| Backend | Hardware | Acceleration |
|---------|----------|--------------|
| CUDA | NVIDIA GPU | Triton kernels |
| TPU | Google TPU | JAX/XLA |
| AMD | AMD GPU (ROCm) | Triton ROCm |
| Intel | Intel GPU/CPU | IPEX/oneDNN |
| DirectML | Windows GPU | DX12 |
| CPU | Any CPU | PyTorch |

## Optimizers

```python
from tpu_inl.optimizers import (
    apply_kernel_fusion,
    quantize_for_inference,
    get_optimal_parallelism,
)

# Fuse kernels
model = apply_kernel_fusion(model, strategy="triton")

# Quantize
model = quantize_for_inference(model, dtype="bf16")

# Get parallelism recommendation
config = get_optimal_parallelism(
    model_size_params=350_000_000,
    num_devices=8,
    memory_per_device_gb=80
)
```

## Architecture

```
tpu_inl/
├── autodetect.py       # Backend detection
├── backends/           # Hardware-specific implementations
│   ├── cpu.py          # PyTorch fallback
│   ├── cuda.py         # NVIDIA Triton
│   ├── tpu.py          # JAX/Pallas
│   ├── amd.py          # ROCm/Triton
│   ├── intel.py        # IPEX/oneDNN
│   └── directml.py     # Windows DX12
├── ops/                # Core operations
│   ├── inl_dynamics.py
│   ├── moe_routing.py
│   └── fused_ops.py
├── inference/          # Inference runtime
│   ├── engine.py       # Main engine
│   ├── kv_cache.py     # KV caching
│   ├── streaming.py    # Real-time streaming
│   ├── batching.py     # Continuous batching
│   └── speculative.py  # Speculative decoding
└── optimizers/         # Performance optimizations
    ├── kernel_fusion.py
    ├── memory_layout.py
    ├── quantization.py
    ├── autotuning.py
    └── scheduling.py
```

## License

Apache 2.0
