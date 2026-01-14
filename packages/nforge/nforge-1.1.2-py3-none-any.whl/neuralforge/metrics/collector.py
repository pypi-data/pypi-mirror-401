"""Metrics Collector - Prometheus-compatible metrics."""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Try to import prometheus_client, fall back to stub if not available
try:
    from prometheus_client import (
        Counter as PrometheusCounter,
        Histogram as PrometheusHistogram,
        Gauge as PrometheusGauge,
        CollectorRegistry,
        generate_latest
    )
    PROMETHEUS_AVAILABLE = True
except ImportError:
    logger.warning("prometheus_client not installed, using stub metrics")
    PROMETHEUS_AVAILABLE = False
    CollectorRegistry = None
    generate_latest = None

class MetricsCollector:
    """Collects and exports Prometheus-compatible metrics."""

    def __init__(self, app):
        """Initialize MetricsCollector.
        
        Args:
            app: NeuralForge application instance
        """
        self.app = app
        self._metrics: Dict[str, any] = {}

        if PROMETHEUS_AVAILABLE:
            self.registry = CollectorRegistry()
            logger.info("Initialized MetricsCollector with Prometheus")
        else:
            self.registry = None
            logger.info("Initialized MetricsCollector (stub mode)")

    def counter(
        self,
        name: str,
        description: str = "",
        labels: Optional[List[str]] = None
    ):
        """Create or get a counter metric."""
        if name in self._metrics:
            return self._metrics[name]

        if PROMETHEUS_AVAILABLE:
            metric = PrometheusCounter(
                name,
                description or f"Counter for {name}",
                labels or [],
                registry=self.registry
            )
        else:
            metric = Counter(name, labels or [])

        self._metrics[name] = metric
        return metric

    def histogram(
        self,
        name: str,
        description: str = "",
        labels: Optional[List[str]] = None,
        buckets: Optional[List[float]] = None
    ):
        """Create or get a histogram metric."""
        if name in self._metrics:
            return self._metrics[name]

        if PROMETHEUS_AVAILABLE:
            kwargs = {
                "name": name,
                "documentation": description or f"Histogram for {name}",
                "labelnames": labels or [],
                "registry": self.registry
            }
            if buckets:
                kwargs["buckets"] = buckets
            metric = PrometheusHistogram(**kwargs)
        else:
            metric = Histogram(name, labels or [])

        self._metrics[name] = metric
        return metric

    def gauge(
        self,
        name: str,
        description: str = "",
        labels: Optional[List[str]] = None
    ):
        """Create or get a gauge metric."""
        if name in self._metrics:
            return self._metrics[name]

        if PROMETHEUS_AVAILABLE:
            metric = PrometheusGauge(
                name,
                description or f"Gauge for {name}",
                labels or [],
                registry=self.registry
            )
        else:
            metric = Gauge(name, labels or [])

        self._metrics[name] = metric
        return metric

    def export_metrics(self) -> bytes:
        """Export metrics in Prometheus text format."""
        if PROMETHEUS_AVAILABLE and self.registry:
            return generate_latest(self.registry)
        else:
            # Return stub metrics
            output = "# Prometheus metrics (stub mode)\n"
            for name, metric in self._metrics.items():
                if isinstance(metric, Counter):
                    output += f"{name} {metric.value}\n"
                elif isinstance(metric, Gauge):
                    output += f"{name} {metric.value}\n"
            return output.encode()


# Stub implementations for when prometheus_client is not available
class Counter:
    """Stub counter metric."""
    def __init__(self, name: str, labels: List[str]):
        """Initialize Counter.
        
        Args:
            name: Metric name
            labels: Label names
        """
        self.name = name
        self._label_names = labels  # Renamed to avoid shadowing labels() method
        self.value = 0

    def inc(self, amount: float = 1, **labels):
        """Increment counter."""
        self.value += amount

    def labels(self, **labels):
        """Return self for chaining (stub)."""
        return self


class Histogram:
    """Stub histogram metric."""
    def __init__(self, name: str, labels: List[str]):
        """Initialize Histogram.
        
        Args:
            name: Metric name
            labels: Label names
        """
        self.name = name
        self.label_names = labels
        self.values = []

    def observe(self, value: float, **labels):
        """Observe value."""
        self.values.append(value)

    def labels(self, **labels):
        """Return self for chaining (stub)."""
        return self


class Gauge:
    """Stub gauge metric."""
    def __init__(self, name: str, labels: List[str]):
        """Initialize Gauge.
        
        Args:
            name: Metric name
            labels: Label names
        """
        self.name = name
        self._label_names = labels  # Renamed to avoid shadowing labels() method
        self.value = 0.0

    def set(self, value: float, **labels):
        """Set gauge value."""
        self.value = value

    def inc(self, amount: float = 1, **labels):
        """Increment gauge."""
        self.value += amount

    def dec(self, amount: float = 1, **labels):
        """Decrement gauge."""
        self.value -= amount

    def labels(self, **labels):
        """Return self for chaining (stub)."""
        return self

