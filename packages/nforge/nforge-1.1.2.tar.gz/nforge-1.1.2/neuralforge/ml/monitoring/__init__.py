"""
Monitoring module - Prediction monitoring and observability.

Provides:
- Async prediction logging
- Performance metrics (latency, throughput)
- Error tracking
- Confidence distribution analysis
- Alert system
- Dashboard API
"""

from neuralforge.ml.monitoring.exceptions import (
    MonitoringError,
    PredictionNotFoundError,
    InvalidTimeRangeError,
    AlertRuleNotFoundError,
    AlertNotFoundError,
    MetricsNotAvailableError,
)
from neuralforge.ml.monitoring.logger import PredictionLogger
from neuralforge.ml.monitoring.metrics import MetricsCollector
from neuralforge.ml.monitoring.alerts import AlertManager
from neuralforge.ml.monitoring.schemas import (
    PredictionLog,
    PredictionInfo,
    LatencyStats,
    ThroughputStats,
    ErrorStats,
    ConfidenceDistribution,
    MetricsSummary,
    AlertRuleCreate,
    AlertRuleInfo,
    AlertInfo,
)

__all__ = [
    # Exceptions
    'MonitoringError',
    'PredictionNotFoundError',
    'InvalidTimeRangeError',
    'AlertRuleNotFoundError',
    'AlertNotFoundError',
    'MetricsNotAvailableError',
    # Core
    'PredictionLogger',
    'MetricsCollector',
    'AlertManager',
    # Schemas
    'PredictionLog',
    'PredictionInfo',
    'LatencyStats',
    'ThroughputStats',
    'ErrorStats',
    'ConfidenceDistribution',
    'MetricsSummary',
    'AlertRuleCreate',
    'AlertRuleInfo',
    'AlertInfo',
]
