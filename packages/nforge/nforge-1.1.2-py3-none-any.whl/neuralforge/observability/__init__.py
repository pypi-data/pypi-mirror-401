"""
NeuralForge Observability Module

Provides OpenTelemetry integration for distributed tracing,
metrics collection, and structured logging.
"""

from neuralforge.observability.tracer import (
    TracingManager,
    OTelConfig,
    auto_instrument_fastapi,
    auto_instrument_sqlalchemy,
    auto_instrument_redis,
)
from neuralforge.observability.logs import (
    StructuredFormatter,
    StructuredLogger,
    configure_structured_logging,
    get_structured_logger,
    set_request_context,
    clear_request_context,
    RequestContextMiddleware,
    log_request,
    log_inference,
    log_error,
)

__all__ = [
    # Tracing
    "TracingManager",
    "OTelConfig",
    "auto_instrument_fastapi",
    "auto_instrument_sqlalchemy",
    "auto_instrument_redis",
    # Logging
    "StructuredFormatter",
    "StructuredLogger",
    "configure_structured_logging",
    "get_structured_logger",
    "set_request_context",
    "clear_request_context",
    "RequestContextMiddleware",
    "log_request",
    "log_inference",
    "log_error",
]
