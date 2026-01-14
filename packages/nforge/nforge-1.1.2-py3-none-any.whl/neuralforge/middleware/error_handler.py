"""
Global Error Handler Middleware.

Catches all exceptions and provides production-safe error responses.
"""

from neuralforge.routing.exceptions import HTTPException
from pydantic import ValidationError
from typing import Callable, Any
import logging
import traceback

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """
    Global error handler middleware.
    
    Catches and handles:
    - HTTPException: Known HTTP errors
    - ValidationError: Pydantic validation errors
    - Exception: All other unexpected errors
    
    Features:
    - Production-safe error messages
    - Detailed logging
    - Proper status codes
    - No stack trace leakage in production
    
    Example:
        app = NeuralForge()
        app.add_middleware(ErrorHandlerMiddleware())
    """

    def __init__(self, debug: bool = False):
        """
        Initialize error handler.
        
        Args:
            debug: If True, include stack traces in responses (development only)
        """
        self.debug = debug

    async def __call__(
        self,
        request: Any,
        call_next: Callable
    ) -> dict:
        """
        Handle request and catch errors.
        
        Args:
            request: Request object
            call_next: Next middleware/handler
        
        Returns:
            Response dict with proper error handling
        """
        try:
            # Call next middleware/handler
            response = await call_next(request)
            return response

        except HTTPException as e:
            # Known HTTP errors - these are intentional
            logger.warning(
                f"HTTP {e.status_code}: {e.detail}",
                extra={
                    "path": request.path if hasattr(request, 'path') else "unknown",
                    "method": request.method if hasattr(request, 'method') else "unknown",
                    "status_code": e.status_code
                }
            )

            return self._format_error_response(
                status_code=e.status_code,
                error=e.detail,
                error_type="http_error"
            )

        except ValidationError as e:
            # Pydantic validation errors
            logger.warning(
                f"Validation error: {e}",
                extra={
                    "path": request.path if hasattr(request, 'path') else "unknown",
                    "errors": e.errors()
                }
            )

            return self._format_error_response(
                status_code=422,
                error="Validation failed",
                details=e.errors(),
                error_type="validation_error"
            )

        except ValueError as e:
            # Business logic errors
            logger.warning(
                f"Value error: {e}",
                extra={
                    "path": request.path if hasattr(request, 'path') else "unknown"
                }
            )

            return self._format_error_response(
                status_code=400,
                error=str(e),
                error_type="value_error"
            )

        except FileNotFoundError as e:
            # Resource not found
            logger.error(
                f"File not found: {e}",
                extra={
                    "path": request.path if hasattr(request, 'path') else "unknown"
                }
            )

            return self._format_error_response(
                status_code=404,
                error="Resource not found",
                error_type="not_found"
            )

        except MemoryError:
            # Resource exhaustion
            logger.critical(
                "Out of memory",
                extra={
                    "path": request.path if hasattr(request, 'path') else "unknown"
                }
            )

            return self._format_error_response(
                status_code=503,
                error="Service temporarily unavailable due to resource constraints",
                error_type="memory_error"
            )

        except Exception as e:
            # Unexpected errors - log with full stack trace
            logger.error(
                f"Unhandled exception: {e}",
                exc_info=True,
                extra={
                    "path": request.path if hasattr(request, 'path') else "unknown",
                    "method": request.method if hasattr(request, 'method') else "unknown",
                    "error_type": type(e).__name__
                }
            )

            # In production, don't leak error details
            error_message = str(e) if self.debug else "Internal server error"

            response = self._format_error_response(
                status_code=500,
                error=error_message,
                error_type="internal_error"
            )

            # Add stack trace in debug mode
            if self.debug:
                response["stack_trace"] = traceback.format_exc()

            return response

    def _format_error_response(
        self,
        status_code: int,
        error: str,
        error_type: str,
        details: Any = None
    ) -> dict:
        """
        Format error response.
        
        Args:
            status_code: HTTP status code
            error: Error message
            error_type: Type of error
            details: Optional additional details
        
        Returns:
            Formatted error response dict
        """
        response = {
            "error": error,
            "error_type": error_type,
            "status_code": status_code
        }

        if details is not None:
            response["details"] = details

        return response


__all__ = ["ErrorHandlerMiddleware"]
