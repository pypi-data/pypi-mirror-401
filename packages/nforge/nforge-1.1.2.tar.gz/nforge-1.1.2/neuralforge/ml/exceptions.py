"""
ML-specific exceptions for NeuralForge.
"""


class MLError(Exception):
    """Base exception for ML-related errors."""
    pass


class ModelNotFoundError(MLError):
    """Raised when a model is not found in the registry."""
    pass


class ModelAlreadyExistsError(MLError):
    """Raised when attempting to register a model that already exists."""
    pass


class ModelLoadError(MLError):
    """Raised when a model fails to load."""
    pass


class ModelValidationError(MLError):
    """Raised when model metadata validation fails."""
    pass


class VersionError(MLError):
    """Raised when there's an issue with model versioning."""
    pass
