"""
Structured Logging for NeuralForge.

Provides structured JSON logging with support for
distributed tracing correlation and metric integration.
"""

import logging
import json
import sys
import traceback
from datetime import datetime
from typing import Any, Dict, Optional
from contextvars import ContextVar


# Context variables for correlation
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
trace_id_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)
span_id_var: ContextVar[Optional[str]] = ContextVar("span_id", default=None)


class StructuredLogRecord(logging.LogRecord):
    """Extended LogRecord with structured data."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.structured_data: Dict[str, Any] = {}


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    
    Outputs logs as single-line JSON for easy parsing.
    
    Example output:
        {"timestamp": "2026-01-12T12:00:00Z", "level": "INFO", 
         "message": "Request processed", "request_id": "abc123"}
    """
    
    def __init__(
        self,
        include_timestamp: bool = True,
        include_level: bool = True,
        include_logger: bool = True,
        include_location: bool = False,
        include_exception: bool = True,
        include_correlation: bool = True,
        extra_fields: Dict[str, Any] = None,
        timestamp_format: str = "iso"
    ):
        super().__init__()
        self.include_timestamp = include_timestamp
        self.include_level = include_level
        self.include_logger = include_logger
        self.include_location = include_location
        self.include_exception = include_exception
        self.include_correlation = include_correlation
        self.extra_fields = extra_fields or {}
        self.timestamp_format = timestamp_format
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {}
        
        # Timestamp
        if self.include_timestamp:
            if self.timestamp_format == "iso":
                log_data["timestamp"] = datetime.utcfromtimestamp(record.created).isoformat() + "Z"
            elif self.timestamp_format == "epoch":
                log_data["timestamp"] = record.created
            else:
                log_data["timestamp"] = self.formatTime(record, self.timestamp_format)
        
        # Level
        if self.include_level:
            log_data["level"] = record.levelname
        
        # Message
        log_data["message"] = record.getMessage()
        
        # Logger name
        if self.include_logger:
            log_data["logger"] = record.name
        
        # Location
        if self.include_location:
            log_data["location"] = {
                "file": record.filename,
                "line": record.lineno,
                "function": record.funcName,
            }
        
        # Correlation IDs
        if self.include_correlation:
            request_id = request_id_var.get()
            trace_id = trace_id_var.get()
            span_id = span_id_var.get()
            
            if request_id:
                log_data["request_id"] = request_id
            if trace_id:
                log_data["trace_id"] = trace_id
            if span_id:
                log_data["span_id"] = span_id
        
        # Exception
        if self.include_exception and record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info) if record.exc_info[0] else None,
            }
        
        # Structured data from record
        if hasattr(record, 'structured_data') and record.structured_data:
            log_data.update(record.structured_data)
        
        # Extra fields from record
        for key in ['extra', 'data', 'context']:
            if hasattr(record, key):
                extra = getattr(record, key)
                if isinstance(extra, dict):
                    log_data.update(extra)
        
        # Global extra fields
        log_data.update(self.extra_fields)
        
        return json.dumps(log_data, default=str)


class StructuredLogger(logging.Logger):
    """
    Logger with structured logging support.
    
    Example:
        ```python
        logger = get_structured_logger("my_service")
        
        logger.info("Request processed", extra={
            "data": {"user_id": 123, "latency_ms": 45}
        })
        ```
    """
    
    def _log(
        self,
        level: int,
        msg: object,
        args,
        exc_info=None,
        extra: Dict[str, Any] = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        **kwargs
    ):
        # Merge structured data
        if extra is None:
            extra = {}
        
        # Handle 'data' kwarg
        if 'data' in kwargs:
            extra['structured_data'] = kwargs.pop('data')
        
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel + 1)
    
    def with_context(self, **context) -> "StructuredLogger":
        """Create a child logger with additional context."""
        child = self.getChild(str(id(context)))
        child._context = context
        return child


def get_structured_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance."""
    logging.setLoggerClass(StructuredLogger)
    logger = logging.getLogger(name)
    logging.setLoggerClass(logging.Logger)
    return logger


def configure_structured_logging(
    level: int = logging.INFO,
    format_type: str = "json",
    include_location: bool = False,
    service_name: str = None,
    service_version: str = None,
    environment: str = None,
    output: str = "stdout"
):
    """
    Configure structured logging for the application.
    
    Args:
        level: Logging level
        format_type: "json" or "text"
        include_location: Include file/line in logs
        service_name: Service name to include
        service_version: Service version
        environment: Environment name (dev, prod, etc.)
        output: "stdout", "stderr", or file path
    
    Example:
        ```python
        configure_structured_logging(
            level=logging.INFO,
            service_name="neuralforge-api",
            environment="production"
        )
        ```
    """
    # Build extra fields
    extra_fields = {}
    if service_name:
        extra_fields["service"] = service_name
    if service_version:
        extra_fields["version"] = service_version
    if environment:
        extra_fields["environment"] = environment
    
    # Create formatter
    if format_type == "json":
        formatter = StructuredFormatter(
            include_location=include_location,
            extra_fields=extra_fields
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
    
    # Create handler
    if output == "stdout":
        handler = logging.StreamHandler(sys.stdout)
    elif output == "stderr":
        handler = logging.StreamHandler(sys.stderr)
    else:
        handler = logging.FileHandler(output)
    
    handler.setFormatter(formatter)
    
    # Configure root logger
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)


def set_request_context(
    request_id: str = None,
    trace_id: str = None,
    span_id: str = None
):
    """Set context for log correlation."""
    if request_id:
        request_id_var.set(request_id)
    if trace_id:
        trace_id_var.set(trace_id)
    if span_id:
        span_id_var.set(span_id)


def clear_request_context():
    """Clear request context."""
    request_id_var.set(None)
    trace_id_var.set(None)
    span_id_var.set(None)


class RequestContextMiddleware:
    """
    ASGI middleware for request context.
    
    Automatically sets request_id and extracts trace context.
    """
    
    def __init__(self, app, generate_request_id: bool = True):
        self.app = app
        self.generate_request_id = generate_request_id
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            import uuid
            
            # Generate or extract request ID
            headers = dict(scope.get("headers", []))
            request_id = headers.get(b"x-request-id", b"").decode() or (
                str(uuid.uuid4()) if self.generate_request_id else None
            )
            
            # Extract trace context
            trace_id = headers.get(b"x-trace-id", b"").decode() or None
            span_id = headers.get(b"x-span-id", b"").decode() or None
            
            set_request_context(
                request_id=request_id,
                trace_id=trace_id,
                span_id=span_id
            )
            
            try:
                await self.app(scope, receive, send)
            finally:
                clear_request_context()
        else:
            await self.app(scope, receive, send)


# Convenience functions for structured logging
def log_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    **extra
):
    """Log an HTTP request with structured data."""
    logger.info(
        f"{method} {path} {status_code}",
        extra={
            "structured_data": {
                "type": "request",
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration_ms": round(duration_ms, 2),
                **extra
            }
        }
    )


def log_inference(
    logger: logging.Logger,
    model_name: str,
    latency_ms: float,
    batch_size: int = 1,
    **extra
):
    """Log an inference operation with structured data."""
    logger.info(
        f"Inference: {model_name}",
        extra={
            "structured_data": {
                "type": "inference",
                "model": model_name,
                "latency_ms": round(latency_ms, 2),
                "batch_size": batch_size,
                **extra
            }
        }
    )


def log_error(
    logger: logging.Logger,
    error: Exception,
    context: str = None,
    **extra
):
    """Log an error with structured data."""
    logger.error(
        context or str(error),
        exc_info=True,
        extra={
            "structured_data": {
                "type": "error",
                "error_type": type(error).__name__,
                "error_message": str(error),
                **extra
            }
        }
    )
