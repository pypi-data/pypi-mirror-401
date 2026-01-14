"""
Logging configuration for NeuralForge applications.

Provides easy logging setup with sensible defaults.
"""

import logging
import sys
from typing import Optional
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    format: Optional[str] = None,
    log_file: Optional[str] = None,
    file_level: Optional[str] = None,
    json_format: bool = False
) -> None:
    """
    Configure logging for NeuralForge applications.

    Args:
        level: Console log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format: Custom log format string
        log_file: Optional file path for file logging
        file_level: Log level for file (defaults to same as console)
        json_format: Use JSON format for structured logging

    Example:
        from neuralforge.logging import setup_logging

        # Basic setup
        setup_logging(level="INFO")

        # With file logging
        setup_logging(
            level="INFO",
            log_file="logs/app.log",
            file_level="DEBUG"
        )

        # JSON format for production
        setup_logging(
            level="INFO",
            json_format=True,
            log_file="logs/app.json"
        )
    """
    # Default format
    if format is None:
        if json_format:
            format = "%(message)s"  # JSON formatter will handle structure
        else:
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Convert level string to logging constant
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Create handlers
    handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    if json_format:
        try:
            import json

            class JSONFormatter(logging.Formatter):
                """JSON log formatter."""

                def format(self, record):
                    """Format log record as JSON.
                    
                    Args:
                        record: Log record to format
                        
                    Returns:
                        JSON-formatted log string
                    """
                    log_data = {
                        "timestamp": self.formatTime(record),
                        "level": record.levelname,
                        "logger": record.name,
                        "message": record.getMessage(),
                        "module": record.module,
                        "function": record.funcName,
                        "line": record.lineno
                    }

                    if record.exc_info:
                        log_data["exception"] = self.formatException(record.exc_info)

                    return json.dumps(log_data)

            console_handler.setFormatter(JSONFormatter())
        except ImportError:
            # Fall back to regular format if json not available
            console_handler.setFormatter(logging.Formatter(format))
    else:
        console_handler.setFormatter(logging.Formatter(format))

    handlers.append(console_handler)

    # File handler (if specified)
    if log_file:
        # Create log directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_level_const = getattr(
            logging,
            (file_level or level).upper(),
            logging.INFO
        )
        file_handler.setLevel(file_level_const)

        if json_format:
            try:
                file_handler.setFormatter(JSONFormatter())
            except Exception:
                file_handler.setFormatter(logging.Formatter(format))
        else:
            file_handler.setFormatter(logging.Formatter(format))

        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=format,
        handlers=handlers,
        force=True  # Override any existing configuration
    )

    # Set specific loggers
    # Reduce noise from third-party libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    # NeuralForge loggers
    for logger_name in ["neuralforge", "uvicorn", "sqlalchemy.engine"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

    # Log initial message
    logger = logging.getLogger("neuralforge")
    logger.info(f"Logging configured: level={level}, file={log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance

    Example:
        from neuralforge.logging import get_logger

        logger = get_logger(__name__)
        logger.info("Application started")
    """
    return logging.getLogger(name)


__all__ = ["setup_logging", "get_logger"]
