"""
Prediction monitoring exceptions.
"""


class MonitoringError(Exception):
    """Base exception for monitoring errors."""
    pass


class PredictionNotFoundError(MonitoringError):
    """Raised when prediction is not found."""
    pass


class InvalidTimeRangeError(MonitoringError):
    """Raised when time range is invalid."""
    pass


class AlertRuleNotFoundError(MonitoringError):
    """Raised when alert rule is not found."""
    pass


class AlertNotFoundError(MonitoringError):
    """Raised when alert is not found."""
    pass


class MetricsNotAvailableError(MonitoringError):
    """Raised when metrics are not available."""
    pass
