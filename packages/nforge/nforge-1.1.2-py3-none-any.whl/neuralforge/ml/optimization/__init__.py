"""
Model optimization module - Model quantization, pruning, and optimization.

Provides:
- Model quantization (INT8, FP16)
- Model pruning
- ONNX export
- Performance benchmarking
"""

from neuralforge.ml.optimization.exceptions import (
    OptimizationError,
    QuantizationError,
    PruningError,
    ExportError,
    BenchmarkError,
    ModelNotFoundError,
    InvalidConfigError,
)
from neuralforge.ml.optimization.quantizer import ModelQuantizer
from neuralforge.ml.optimization.benchmarker import PerformanceBenchmarker
from neuralforge.ml.optimization.schemas import (
    QuantizationConfig,
    QuantizationResult,
    PruningConfig,
    PruningResult,
    BenchmarkConfig,
    BenchmarkResultInfo,
    LatencyStats,
    MemoryStats,
    OptimizedModelInfo,
)

__all__ = [
    # Exceptions
    'OptimizationError',
    'QuantizationError',
    'PruningError',
    'ExportError',
    'BenchmarkError',
    'ModelNotFoundError',
    'InvalidConfigError',
    # Core
    'ModelQuantizer',
    'PerformanceBenchmarker',
    # Schemas
    'QuantizationConfig',
    'QuantizationResult',
    'PruningConfig',
    'PruningResult',
    'BenchmarkConfig',
    'BenchmarkResultInfo',
    'LatencyStats',
    'MemoryStats',
    'OptimizedModelInfo',
]
