"""
Drift detection exceptions.
"""


class DriftError(Exception):
    """Base exception for drift detection errors."""
    pass


class BaselineNotFoundError(DriftError):
    """Raised when baseline is not found."""
    pass


class InsufficientDataError(DriftError):
    """Raised when insufficient data for drift detection."""
    pass


class InvalidDistributionError(DriftError):
    """Raised when distribution data is invalid."""
    pass


class DriftDetectionError(DriftError):
    """Raised when drift detection fails."""
    pass
