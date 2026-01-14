"""
HTTP Exceptions for NeuralForge.

Provides standard HTTP exception classes for error handling.
"""

from typing import Any, Dict, List, Optional


class HTTPException(Exception):
    """
    Base HTTP exception.
    
    Example:
        raise HTTPException(status_code=400, detail="Invalid request")
    """

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None
    ):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers or {}
        super().__init__(detail)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status_code={self.status_code}, detail={self.detail})"


class BadRequestException(HTTPException):
    """400 Bad Request."""

    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=400, detail=detail)


class UnauthorizedException(HTTPException):
    """401 Unauthorized."""

    def __init__(self, detail: str = "Unauthorized", headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=401, detail=detail, headers=headers)


class ForbiddenException(HTTPException):
    """403 Forbidden."""

    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail)


class NotFoundException(HTTPException):
    """404 Not Found."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class MethodNotAllowedException(HTTPException):
    """405 Method Not Allowed."""

    def __init__(self, detail: str = "Method not allowed", allowed_methods: List[str] = None):
        headers = {}
        if allowed_methods:
            headers["Allow"] = ", ".join(allowed_methods)
        super().__init__(status_code=405, detail=detail, headers=headers)


class ValidationException(HTTPException):
    """422 Unprocessable Entity - Validation errors."""

    def __init__(self, errors: List[Dict[str, Any]]):
        super().__init__(
            status_code=422,
            detail={"errors": errors}
        )


class InternalServerException(HTTPException):
    """500 Internal Server Error."""

    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(status_code=500, detail=detail)


class ServiceUnavailableException(HTTPException):
    """503 Service Unavailable."""

    def __init__(self, detail: str = "Service Unavailable"):
        super().__init__(status_code=503, detail=detail)
