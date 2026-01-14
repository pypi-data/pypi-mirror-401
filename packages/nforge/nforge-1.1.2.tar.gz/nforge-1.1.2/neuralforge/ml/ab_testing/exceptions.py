"""
A/B Testing exceptions.
"""


class ABTestingError(Exception):
    """Base exception for A/B testing errors."""
    pass


class ExperimentNotFoundError(ABTestingError):
    """Raised when experiment is not found."""
    pass


class ExperimentAlreadyExistsError(ABTestingError):
    """Raised when experiment already exists."""
    pass


class ExperimentNotRunningError(ABTestingError):
    """Raised when trying to use a non-running experiment."""
    pass


class VariantNotFoundError(ABTestingError):
    """Raised when variant is not found."""
    pass


class InvalidTrafficAllocationError(ABTestingError):
    """Raised when traffic allocation is invalid."""
    pass


class InsufficientSampleSizeError(ABTestingError):
    """Raised when sample size is too small for analysis."""
    pass


class NoWinnerError(ABTestingError):
    """Raised when no clear winner can be determined."""
    pass
