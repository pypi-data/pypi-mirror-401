"""
OpenTelemetry Integration for NeuralForge.

Provides distributed tracing, metrics, and logging
using OpenTelemetry standards.
"""

import logging
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from contextvars import ContextVar

logger = logging.getLogger(__name__)

# Check for OpenTelemetry availability
try:
    from opentelemetry import trace, metrics
    from opentelemetry.trace import Span, Tracer, SpanKind, Status, StatusCode
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None
    metrics = None

# Context variable for current span
_current_span: ContextVar[Optional[Any]] = ContextVar('current_span', default=None)


@dataclass
class OTelConfig:
    """Configuration for OpenTelemetry integration."""
    service_name: str = "neuralforge"
    service_version: str = "1.1.0"
    environment: str = "development"
    
    # Tracing
    enable_tracing: bool = True
    trace_sample_rate: float = 1.0  # 1.0 = 100% sampling
    
    # Metrics
    enable_metrics: bool = True
    metrics_export_interval_ms: int = 60000  # 1 minute
    
    # Exporters
    exporter: str = "console"  # "console", "otlp", "jaeger", "zipkin"
    otlp_endpoint: Optional[str] = None
    otlp_headers: Optional[Dict[str, str]] = None
    
    # Instrumentation
    auto_instrument_http: bool = True
    auto_instrument_db: bool = True
    auto_instrument_cache: bool = True


class TracingManager:
    """
    Manages distributed tracing with OpenTelemetry.
    
    Provides automatic instrumentation for HTTP requests,
    database operations, and custom spans.
    
    Example:
        ```python
        from neuralforge.observability import TracingManager, OTelConfig
        
        app = NeuralForge()
        tracing = TracingManager(app)
        
        tracing.configure(OTelConfig(
            service_name="my-service",
            exporter="otlp",
            otlp_endpoint="http://otel-collector:4317"
        ))
        
        # Custom spans
        with tracing.span("process_data") as span:
            span.set_attribute("data_size", 1000)
            result = process(data)
        ```
    """
    
    def __init__(self, app: Any = None):
        self.app = app
        self._config: Optional[OTelConfig] = None
        self._tracer: Optional[Any] = None
        self._meter: Optional[Any] = None
        self._enabled = False
        self._provider = None
        
        # Metrics
        self._request_counter = None
        self._request_duration = None
        self._active_requests = None
        
        logger.info("TracingManager initialized")
    
    @property
    def is_available(self) -> bool:
        """Check if OpenTelemetry is available."""
        return OTEL_AVAILABLE
    
    @property
    def is_enabled(self) -> bool:
        """Check if tracing is enabled."""
        return self._enabled and self.is_available
    
    def configure(self, config: OTelConfig = None, **kwargs):
        """
        Configure OpenTelemetry integration.
        
        Args:
            config: OTelConfig object or None to use kwargs
            **kwargs: Config options if config is None
        """
        if config is None:
            config = OTelConfig(**kwargs)
        
        self._config = config
        
        if not OTEL_AVAILABLE:
            logger.warning(
                "OpenTelemetry not installed. Install with: "
                "pip install opentelemetry-api opentelemetry-sdk"
            )
            return
        
        try:
            self._setup_tracing(config)
            self._setup_metrics(config)
            self._enabled = True
            logger.info(f"OpenTelemetry configured: {config.exporter}")
        except Exception as e:
            logger.error(f"Failed to configure OpenTelemetry: {e}")
            self._enabled = False
    
    def _setup_tracing(self, config: OTelConfig):
        """Setup tracing provider and exporter."""
        if not config.enable_tracing:
            return
        
        # Create resource
        resource = Resource.create({
            SERVICE_NAME: config.service_name,
            "service.version": config.service_version,
            "deployment.environment": config.environment,
        })
        
        # Create tracer provider
        self._provider = TracerProvider(resource=resource)
        
        # Setup exporter
        exporter = self._create_trace_exporter(config)
        if exporter:
            processor = BatchSpanProcessor(exporter)
            self._provider.add_span_processor(processor)
        
        # Set global tracer provider
        trace.set_tracer_provider(self._provider)
        
        # Get tracer
        self._tracer = trace.get_tracer(
            config.service_name,
            config.service_version
        )
    
    def _setup_metrics(self, config: OTelConfig):
        """Setup metrics provider."""
        if not config.enable_metrics:
            return
        
        # Create meter
        self._meter = metrics.get_meter(
            config.service_name,
            config.service_version
        )
        
        # Create standard metrics
        self._request_counter = self._meter.create_counter(
            name="neuralforge.requests",
            description="Total number of requests",
            unit="1"
        )
        
        self._request_duration = self._meter.create_histogram(
            name="neuralforge.request.duration",
            description="Request duration in milliseconds",
            unit="ms"
        )
        
        self._active_requests = self._meter.create_up_down_counter(
            name="neuralforge.requests.active",
            description="Number of active requests",
            unit="1"
        )
    
    def _create_trace_exporter(self, config: OTelConfig):
        """Create trace exporter based on config."""
        try:
            if config.exporter == "console":
                from opentelemetry.sdk.trace.export import ConsoleSpanExporter
                return ConsoleSpanExporter()
            
            elif config.exporter == "otlp":
                from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
                    OTLPSpanExporter
                )
                return OTLPSpanExporter(
                    endpoint=config.otlp_endpoint,
                    headers=config.otlp_headers
                )
            
            elif config.exporter == "jaeger":
                from opentelemetry.exporter.jaeger.thrift import JaegerExporter
                return JaegerExporter()
            
            elif config.exporter == "zipkin":
                from opentelemetry.exporter.zipkin.json import ZipkinExporter
                return ZipkinExporter()
            
            else:
                logger.warning(f"Unknown exporter: {config.exporter}")
                return None
                
        except ImportError as e:
            logger.warning(f"Exporter not available: {e}")
            return None
    
    def span(
        self,
        name: str,
        kind: str = "internal",
        attributes: Optional[Dict[str, Any]] = None
    ):
        """
        Create a span context manager.
        
        Args:
            name: Span name
            kind: Span kind ("internal", "server", "client", "producer", "consumer")
            attributes: Initial span attributes
        
        Returns:
            Context manager yielding the span
        
        Example:
            with tracing.span("process_request", kind="server") as span:
                span.set_attribute("user_id", user_id)
                result = process()
        """
        if not self.is_enabled:
            return _NoOpSpanContext()
        
        span_kind_map = {
            "internal": SpanKind.INTERNAL,
            "server": SpanKind.SERVER,
            "client": SpanKind.CLIENT,
            "producer": SpanKind.PRODUCER,
            "consumer": SpanKind.CONSUMER,
        }
        
        return _SpanContext(
            self._tracer,
            name,
            span_kind_map.get(kind, SpanKind.INTERNAL),
            attributes
        )
    
    def trace(
        self,
        name: Optional[str] = None,
        kind: str = "internal",
        record_args: bool = False,
        record_result: bool = False
    ):
        """
        Decorator to trace a function.
        
        Args:
            name: Span name (defaults to function name)
            kind: Span kind
            record_args: Record function arguments as attributes
            record_result: Record function result as attribute
        
        Example:
            @tracing.trace(record_args=True)
            async def predict(model_name: str, data: dict):
                return model.predict(data)
        """
        def decorator(func: Callable):
            span_name = name or func.__name__
            
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                with self.span(span_name, kind) as span:
                    if record_args:
                        span.set_attribute("args", str(args)[:100])
                        span.set_attribute("kwargs", str(kwargs)[:100])
                    
                    try:
                        result = await func(*args, **kwargs)
                        
                        if record_result:
                            span.set_attribute("result", str(result)[:100])
                        
                        return result
                        
                    except Exception as e:
                        span.record_exception(e)
                        if OTEL_AVAILABLE:
                            span.set_status(Status(StatusCode.ERROR, str(e)))
                        raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                with self.span(span_name, kind) as span:
                    if record_args:
                        span.set_attribute("args", str(args)[:100])
                        span.set_attribute("kwargs", str(kwargs)[:100])
                    
                    try:
                        result = func(*args, **kwargs)
                        
                        if record_result:
                            span.set_attribute("result", str(result)[:100])
                        
                        return result
                        
                    except Exception as e:
                        span.record_exception(e)
                        if OTEL_AVAILABLE:
                            span.set_status(Status(StatusCode.ERROR, str(e)))
                        raise
            
            import asyncio
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper
        
        return decorator
    
    def record_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        attributes: Optional[Dict[str, Any]] = None
    ):
        """
        Record HTTP request metrics.
        
        Args:
            method: HTTP method
            path: Request path
            status_code: Response status code
            duration_ms: Request duration in milliseconds
            attributes: Additional attributes
        """
        if not self.is_enabled or not self._request_counter:
            return
        
        labels = {
            "http.method": method,
            "http.route": path,
            "http.status_code": str(status_code),
        }
        if attributes:
            labels.update({k: str(v) for k, v in attributes.items()})
        
        self._request_counter.add(1, labels)
        self._request_duration.record(duration_ms, labels)
    
    def get_current_span(self) -> Optional[Any]:
        """Get the current active span."""
        if not self.is_enabled:
            return None
        return trace.get_current_span()
    
    def inject_context(self, carrier: Dict[str, str]):
        """Inject trace context into headers for propagation."""
        if not self.is_enabled:
            return
        
        try:
            from opentelemetry.propagate import inject
            inject(carrier)
        except Exception as e:
            logger.debug(f"Failed to inject context: {e}")
    
    def extract_context(self, carrier: Dict[str, str]):
        """Extract trace context from incoming headers."""
        if not self.is_enabled:
            return None
        
        try:
            from opentelemetry.propagate import extract
            return extract(carrier)
        except Exception as e:
            logger.debug(f"Failed to extract context: {e}")
            return None
    
    def shutdown(self):
        """Shutdown the tracer provider."""
        if self._provider:
            self._provider.shutdown()
            logger.info("TracingManager shutdown complete")


class _SpanContext:
    """Context manager for creating spans."""
    
    def __init__(
        self,
        tracer: Any,
        name: str,
        kind: Any,
        attributes: Optional[Dict[str, Any]] = None
    ):
        self._tracer = tracer
        self._name = name
        self._kind = kind
        self._attributes = attributes or {}
        self._span = None
    
    def __enter__(self):
        self._span = self._tracer.start_span(
            self._name,
            kind=self._kind,
            attributes=self._attributes
        )
        context = trace.set_span_in_context(self._span)
        _current_span.set(self._span)
        return self._span
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and self._span:
            self._span.record_exception(exc_val)
            self._span.set_status(Status(StatusCode.ERROR, str(exc_val)))
        
        if self._span:
            self._span.end()
        
        _current_span.set(None)
        return False


class _NoOpSpanContext:
    """No-op context manager when tracing is disabled."""
    
    def __enter__(self):
        return _NoOpSpan()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class _NoOpSpan:
    """No-op span when tracing is disabled."""
    
    def set_attribute(self, key: str, value: Any):
        pass
    
    def set_status(self, status: Any):
        pass
    
    def record_exception(self, exception: Exception):
        pass
    
    def add_event(self, name: str, attributes: Optional[Dict] = None):
        pass


def auto_instrument_fastapi(app: Any, tracing: TracingManager):
    """
    Auto-instrument a FastAPI application.
    
    Args:
        app: FastAPI application
        tracing: TracingManager instance
    """
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        FastAPIInstrumentor.instrument_app(app)
        logger.info("FastAPI auto-instrumentation enabled")
    except ImportError:
        logger.debug("FastAPI instrumentation not available")
    except Exception as e:
        logger.warning(f"Failed to instrument FastAPI: {e}")


def auto_instrument_sqlalchemy(engine: Any, tracing: TracingManager):
    """
    Auto-instrument SQLAlchemy.
    
    Args:
        engine: SQLAlchemy engine
        tracing: TracingManager instance
    """
    try:
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
        SQLAlchemyInstrumentor().instrument(engine=engine)
        logger.info("SQLAlchemy auto-instrumentation enabled")
    except ImportError:
        logger.debug("SQLAlchemy instrumentation not available")
    except Exception as e:
        logger.warning(f"Failed to instrument SQLAlchemy: {e}")


def auto_instrument_redis(tracing: TracingManager):
    """
    Auto-instrument Redis.
    
    Args:
        tracing: TracingManager instance
    """
    try:
        from opentelemetry.instrumentation.redis import RedisInstrumentor
        RedisInstrumentor().instrument()
        logger.info("Redis auto-instrumentation enabled")
    except ImportError:
        logger.debug("Redis instrumentation not available")
    except Exception as e:
        logger.warning(f"Failed to instrument Redis: {e}")
