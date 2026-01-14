"""
Logging Middleware - Request and response logging with sensitive data masking.
"""

from typing import Callable, List
import logging
import time
import json

from .base import BaseMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """
    Logging middleware for request and response logging.
    
    Features:
    - Request logging (method, path, headers, body)
    - Response logging (status, headers, body)
    - Timing information
    - Sensitive data masking
    - Structured logging
    """

    def __init__(
        self,
        log_requests: bool = True,
        log_responses: bool = True,
        log_request_body: bool = False,
        log_response_body: bool = False,
        log_headers: bool = True,
        mask_sensitive_data: bool = True,
        sensitive_fields: List[str] = None
    ):
        """
        Initialize logging middleware.
        
        Args:
            log_requests: Whether to log requests
            log_responses: Whether to log responses
            log_request_body: Whether to log request body (can be large)
            log_response_body: Whether to log response body (can be large)
            log_headers: Whether to log headers
            mask_sensitive_data: Whether to mask sensitive data
            sensitive_fields: List of field names to mask (case-insensitive)
        """
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.log_headers = log_headers
        self.mask_sensitive_data = mask_sensitive_data

        # Default sensitive fields
        default_sensitive = {
            "password", "api_key", "token", "secret", "authorization",
            "x-api-key", "cookie", "session", "csrf", "credit_card"
        }

        if sensitive_fields:
            self.sensitive_fields = default_sensitive.union(
                {f.lower() for f in sensitive_fields}
            )
        else:
            self.sensitive_fields = default_sensitive

        logger.info("Logging middleware initialized")

    def _mask_value(self, value: str) -> str:
        """Mask sensitive value."""
        if not value:
            return value

        if len(value) <= 4:
            return "***"

        # Show first 4 chars, mask the rest
        return f"{value[:4]}{'*' * (len(value) - 4)}"

    def _mask_dict(self, data: dict) -> dict:
        """Recursively mask sensitive fields in dictionary."""
        if not self.mask_sensitive_data:
            return data

        masked = {}
        for key, value in data.items():
            key_lower = key.lower()

            if key_lower in self.sensitive_fields:
                # Mask sensitive field
                if isinstance(value, str):
                    masked[key] = self._mask_value(value)
                else:
                    masked[key] = "***"
            elif isinstance(value, dict):
                # Recursively mask nested dict
                masked[key] = self._mask_dict(value)
            elif isinstance(value, list):
                # Mask list items
                masked[key] = [
                    self._mask_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                masked[key] = value

        return masked

    def _parse_headers(self, headers: List[tuple]) -> dict:
        """Parse headers into dict."""
        return {
            k.decode() if isinstance(k, bytes) else k:
            v.decode() if isinstance(v, bytes) else v
            for k, v in headers
        }

    async def _log_request(self, scope: dict, body: bytes = None):
        """Log HTTP request."""
        if not self.log_requests:
            return

        method = scope.get("method", "")
        path = scope.get("path", "")
        query_string = scope.get("query_string", b"").decode()

        log_data = {
            "type": "request",
            "method": method,
            "path": path,
            "query_string": query_string,
        }

        # Add headers if enabled
        if self.log_headers:
            headers = self._parse_headers(scope.get("headers", []))
            log_data["headers"] = self._mask_dict(headers)

        # Add body if enabled
        if self.log_request_body and body:
            try:
                # Try to parse as JSON
                body_str = body.decode()
                body_json = json.loads(body_str)
                log_data["body"] = self._mask_dict(body_json)
            except Exception:
                # Not JSON, just log size
                log_data["body_size"] = len(body)

        logger.info(f"Request: {method} {path}", extra=log_data)

    async def _log_response(self, status_code: int, headers: List[tuple], body: bytes, duration: float):
        """Log HTTP response."""
        if not self.log_responses:
            return

        log_data = {
            "type": "response",
            "status_code": status_code,
            "duration_ms": round(duration * 1000, 2),
        }

        # Add headers if enabled
        if self.log_headers:
            headers_dict = self._parse_headers(headers)
            log_data["headers"] = headers_dict

        # Add body if enabled
        if self.log_response_body and body:
            try:
                # Try to parse as JSON
                body_str = body.decode()
                body_json = json.loads(body_str)
                log_data["body"] = body_json
            except Exception:
                # Not JSON, just log size
                log_data["body_size"] = len(body)

        logger.info(f"Response: {status_code} ({duration*1000:.2f}ms)", extra=log_data)

    async def __call__(self, scope: dict, receive: Callable, send: Callable, app: Callable):
        """Process request through logging middleware."""
        if scope["type"] != "http":
            return await app(scope, receive, send)

        start_time = time.time()

        # Capture request body if needed
        request_body = b""
        if self.log_request_body:
            async def receive_with_logging():
                nonlocal request_body
                message = await receive()
                if message["type"] == "http.request":
                    body = message.get("body", b"")
                    request_body += body
                return message

            receive_func = receive_with_logging
        else:
            receive_func = receive

        # Log request
        await self._log_request(scope, request_body if self.log_request_body else None)

        # Capture response
        status_code = None
        response_headers = []
        response_body = b""

        async def send_with_logging(message):
            nonlocal status_code, response_headers, response_body

            if message["type"] == "http.response.start":
                status_code = message["status"]
                response_headers = message.get("headers", [])
            elif message["type"] == "http.response.body":
                if self.log_response_body:
                    response_body += message.get("body", b"")

            await send(message)

        # Call next middleware/app
        await app(scope, receive_func, send_with_logging)

        # Log response
        duration = time.time() - start_time
        await self._log_response(
            status_code or 500,
            response_headers,
            response_body if self.log_response_body else b"",
            duration
        )
