"""
Autotuning for runtime parameter optimization.

Automatically finds optimal parameters (block sizes, batch sizes,
memory layouts) for the current hardware at runtime.

Similar to:
- Triton's autotuning for kernel parameters
- TensorRT's layer profiling
- XLA's auto-tuning phase
"""

import torch
import torch.nn as nn
from typing import Optional, Dict, Any, List, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import json
import hashlib
import os


class TuningMetric(Enum):
    """Metrics to optimize for."""
    LATENCY = "latency"          # Minimize time
    THROUGHPUT = "throughput"    # Maximize tokens/sec
    MEMORY = "memory"            # Minimize memory
    BALANCED = "balanced"        # Balance latency and memory


@dataclass
class AutotuneConfig:
    """Configuration for autotuning."""
    # What to optimize
    metric: TuningMetric = TuningMetric.LATENCY

    # Search parameters
    num_trials: int = 20         # Number of configurations to try
    warmup_iters: int = 5        # Warmup iterations per trial
    benchmark_iters: int = 10    # Benchmark iterations per trial

    # Caching
    use_cache: bool = True
    cache_dir: str = ".tpu_inl_cache"

    # Early stopping
    early_stop_threshold: float = 0.05  # Stop if improvement < 5%


@dataclass
class TuningResult:
    """Result of autotuning."""
    best_config: Dict[str, Any]
    best_metric: float
    all_results: List[Tuple[Dict[str, Any], float]]
    tuning_time: float


class ParameterSpace:
    """
    Defines the parameter search space for autotuning.
    """

    def __init__(self):
        self.parameters: Dict[str, List[Any]] = {}

    def add_int(self, name: str, values: List[int]):
        """Add integer parameter with discrete values."""
        self.parameters[name] = values

    def add_float(self, name: str, values: List[float]):
        """Add float parameter with discrete values."""
        self.parameters[name] = values

    def add_bool(self, name: str):
        """Add boolean parameter."""
        self.parameters[name] = [True, False]

    def add_choice(self, name: str, choices: List[Any]):
        """Add categorical parameter."""
        self.parameters[name] = choices

    def get_configs(self, max_configs: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Generate all configurations or sample if too many.
        """
        import itertools

        # Calculate total combinations
        keys = list(self.parameters.keys())
        values = list(self.parameters.values())

        total = 1
        for v in values:
            total *= len(v)

        if max_configs is None or total <= max_configs:
            # Return all combinations
            configs = []
            for combo in itertools.product(*values):
                configs.append(dict(zip(keys, combo)))
            return configs
        else:
            # Random sample
            import random
            configs = []
            for _ in range(max_configs):
                config = {k: random.choice(v) for k, v in self.parameters.items()}
                if config not in configs:
                    configs.append(config)
            return configs


class Autotuner:
    """
    Runtime autotuning for optimal performance.
    """

    def __init__(self, config: Optional[AutotuneConfig] = None):
        self.config = config or AutotuneConfig()
        self._cache: Dict[str, TuningResult] = {}

        # Create cache directory
        if self.config.use_cache:
            os.makedirs(self.config.cache_dir, exist_ok=True)

    def _get_cache_key(
        self,
        model_name: str,
        input_shape: Tuple[int, ...],
        space: ParameterSpace
    ) -> str:
        """Generate cache key for this tuning configuration."""
        data = {
            "model": model_name,
            "input_shape": input_shape,
            "parameters": list(space.parameters.keys()),
            "device": str(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu")
        }
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16]

    def _load_cache(self, key: str) -> Optional[TuningResult]:
        """Load cached result."""
        if not self.config.use_cache:
            return None

        cache_file = os.path.join(self.config.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                data = json.load(f)
                return TuningResult(**data)
        return None

    def _save_cache(self, key: str, result: TuningResult):
        """Save result to cache."""
        if not self.config.use_cache:
            return

        cache_file = os.path.join(self.config.cache_dir, f"{key}.json")
        with open(cache_file, 'w') as f:
            json.dump({
                "best_config": result.best_config,
                "best_metric": result.best_metric,
                "all_results": result.all_results,
                "tuning_time": result.tuning_time
            }, f)

    def tune(
        self,
        model: nn.Module,
        space: ParameterSpace,
        input_fn: Callable[[], torch.Tensor],
        model_name: str = "model"
    ) -> TuningResult:
        """
        Tune model parameters.

        Args:
            model: Model to tune
            space: Parameter search space
            input_fn: Function that returns sample input
            model_name: Name for caching

        Returns:
            TuningResult with best configuration
        """
        sample_input = input_fn()
        cache_key = self._get_cache_key(model_name, tuple(sample_input.shape), space)

        # Check cache
        cached = self._load_cache(cache_key)
        if cached:
            print(f"[Autotuner] Using cached result for {model_name}")
            return cached

        print(f"[Autotuner] Tuning {model_name}...")
        start_time = time.perf_counter()

        # Get configurations to try
        configs = space.get_configs(self.config.num_trials)
        results = []

        best_metric = float('inf') if self.config.metric != TuningMetric.THROUGHPUT else 0
        best_config = None
        no_improvement_count = 0

        for i, config in enumerate(configs):
            try:
                metric = self._evaluate_config(model, config, input_fn)
                results.append((config, metric))

                # Track best
                is_better = (
                    (self.config.metric != TuningMetric.THROUGHPUT and metric < best_metric) or
                    (self.config.metric == TuningMetric.THROUGHPUT and metric > best_metric)
                )

                if is_better:
                    improvement = abs(metric - best_metric) / max(abs(best_metric), 1e-10)
                    best_metric = metric
                    best_config = config
                    no_improvement_count = 0
                    print(f"  [{i+1}/{len(configs)}] New best: {metric:.4f} ({config})")
                else:
                    no_improvement_count += 1

                # Early stopping
                if no_improvement_count >= 5:
                    print(f"  Early stopping after {i+1} trials")
                    break

            except Exception as e:
                print(f"  [{i+1}/{len(configs)}] Config failed: {e}")
                continue

        tuning_time = time.perf_counter() - start_time

        result = TuningResult(
            best_config=best_config or {},
            best_metric=best_metric,
            all_results=results,
            tuning_time=tuning_time
        )

        # Save to cache
        self._save_cache(cache_key, result)

        print(f"[Autotuner] Done in {tuning_time:.2f}s. Best: {best_metric:.4f}")
        return result

    def _evaluate_config(
        self,
        model: nn.Module,
        config: Dict[str, Any],
        input_fn: Callable[[], torch.Tensor]
    ) -> float:
        """Evaluate a single configuration."""
        device = next(model.parameters()).device

        # Apply configuration (implementation depends on what's being tuned)
        # This is a generic version - specific implementations would override

        # Warmup
        with torch.inference_mode():
            for _ in range(self.config.warmup_iters):
                x = input_fn().to(device)
                _ = model(x)

        if device.type == "cuda":
            torch.cuda.synchronize()

        # Benchmark
        times = []
        memory_peaks = []

        with torch.inference_mode():
            for _ in range(self.config.benchmark_iters):
                if device.type == "cuda":
                    torch.cuda.reset_peak_memory_stats()

                x = input_fn().to(device)

                start = time.perf_counter()
                _ = model(x)

                if device.type == "cuda":
                    torch.cuda.synchronize()

                times.append(time.perf_counter() - start)

                if device.type == "cuda":
                    memory_peaks.append(torch.cuda.max_memory_allocated() / 1e9)

        avg_time = sum(times) / len(times)
        avg_memory = sum(memory_peaks) / len(memory_peaks) if memory_peaks else 0

        if self.config.metric == TuningMetric.LATENCY:
            return avg_time
        elif self.config.metric == TuningMetric.THROUGHPUT:
            batch_size = input_fn().shape[0]
            return batch_size / avg_time
        elif self.config.metric == TuningMetric.MEMORY:
            return avg_memory
        else:  # BALANCED
            return avg_time * (1 + avg_memory)


def autotune(
    model: nn.Module,
    sample_input: torch.Tensor,
    config: Optional[AutotuneConfig] = None
) -> Dict[str, Any]:
    """
    Convenience function to autotune a model.

    Args:
        model: Model to tune
        sample_input: Sample input tensor
        config: Tuning configuration

    Returns:
        Best configuration dictionary
    """
    tuner = Autotuner(config)

    # Default parameter space for inference
    space = ParameterSpace()
    space.add_choice("dtype", [torch.float32, torch.float16, torch.bfloat16])
    space.add_bool("use_compile")

    if torch.cuda.is_available():
        space.add_bool("use_cuda_graphs")

    result = tuner.tune(
        model,
        space,
        lambda: sample_input.clone(),
        model_name=model.__class__.__name__
    )

    return result.best_config


class KernelAutotuner:
    """
    Specialized autotuner for kernel parameters (Triton, CUDA).
    """

    def __init__(self):
        self.results: Dict[str, Dict[str, Any]] = {}

    def autotune_block_size(
        self,
        kernel_fn: Callable,
        input_size: int,
        block_sizes: List[int] = [64, 128, 256, 512, 1024],
        warmup: int = 5,
        benchmark: int = 20
    ) -> int:
        """
        Find optimal block size for a kernel.

        Args:
            kernel_fn: Kernel function that takes block_size parameter
            input_size: Total input elements
            block_sizes: Block sizes to try
            warmup: Warmup iterations
            benchmark: Benchmark iterations

        Returns:
            Optimal block size
        """
        best_time = float('inf')
        best_block_size = block_sizes[0]

        for block_size in block_sizes:
            if block_size > input_size:
                continue

            # Warmup
            for _ in range(warmup):
                kernel_fn(block_size=block_size)

            torch.cuda.synchronize()

            # Benchmark
            start = time.perf_counter()
            for _ in range(benchmark):
                kernel_fn(block_size=block_size)
            torch.cuda.synchronize()

            elapsed = (time.perf_counter() - start) / benchmark

            if elapsed < best_time:
                best_time = elapsed
                best_block_size = block_size

        return best_block_size
