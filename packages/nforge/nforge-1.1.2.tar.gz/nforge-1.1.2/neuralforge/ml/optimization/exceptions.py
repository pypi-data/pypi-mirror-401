"""
Model optimization exceptions.
"""


class OptimizationError(Exception):
    """Base exception for optimization errors."""
    pass


class QuantizationError(OptimizationError):
    """Raised when quantization fails."""
    pass


class PruningError(OptimizationError):
    """Raised when pruning fails."""
    pass


class ExportError(OptimizationError):
    """Raised when model export fails."""
    pass


class BenchmarkError(OptimizationError):
    """Raised when benchmarking fails."""
    pass


class ModelNotFoundError(OptimizationError):
    """Raised when model is not found."""
    pass


class InvalidConfigError(OptimizationError):
    """Raised when optimization config is invalid."""
    pass
