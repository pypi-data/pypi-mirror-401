"""
CORS Middleware - Cross-Origin Resource Sharing support.
"""

from typing import List, Callable
import logging

from .base import BaseMiddleware

logger = logging.getLogger(__name__)


class CORSMiddleware(BaseMiddleware):
    """
    CORS middleware for handling cross-origin requests.
    
    Features:
    - Configurable allowed origins
    - Preflight request handling (OPTIONS)
    - Configurable allowed methods and headers
    - Credentials support
    """

    def __init__(
        self,
        allow_origins: List[str] = None,
        allow_methods: List[str] = None,
        allow_headers: List[str] = None,
        allow_credentials: bool = False,
        max_age: int = 600
    ):
        """
        Initialize CORS middleware.
        
        Args:
            allow_origins: List of allowed origins (use ["*"] for all)
            allow_methods: List of allowed HTTP methods
            allow_headers: List of allowed headers (use ["*"] for all)
            allow_credentials: Whether to allow credentials
            max_age: Preflight cache time in seconds
        """
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
        self.allow_headers = allow_headers or ["*"]
        self.allow_credentials = allow_credentials
        self.max_age = max_age

        logger.info(f"CORS middleware initialized: origins={self.allow_origins}")

    def _is_origin_allowed(self, origin: str) -> bool:
        """Check if origin is allowed."""
        if "*" in self.allow_origins:
            return True
        return origin in self.allow_origins

    def _get_cors_headers(self, origin: str = None) -> List[tuple]:
        """Get CORS headers to add to response."""
        headers = []

        # Access-Control-Allow-Origin
        if "*" in self.allow_origins:
            headers.append((b"Access-Control-Allow-Origin", b"*"))
        elif origin and self._is_origin_allowed(origin):
            headers.append((b"Access-Control-Allow-Origin", origin.encode()))

        # Access-Control-Allow-Methods
        methods = ", ".join(self.allow_methods)
        headers.append((b"Access-Control-Allow-Methods", methods.encode()))

        # Access-Control-Allow-Headers
        if "*" in self.allow_headers:
            headers.append((b"Access-Control-Allow-Headers", b"*"))
        else:
            allow_headers = ", ".join(self.allow_headers)
            headers.append((b"Access-Control-Allow-Headers", allow_headers.encode()))

        # Access-Control-Allow-Credentials
        if self.allow_credentials:
            headers.append((b"Access-Control-Allow-Credentials", b"true"))

        # Access-Control-Max-Age
        headers.append((b"Access-Control-Max-Age", str(self.max_age).encode()))

        return headers

    async def _send_preflight_response(self, send: Callable, origin: str = None):
        """Send preflight (OPTIONS) response."""
        headers = self._get_cors_headers(origin)

        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": headers,
        })

        await send({
            "type": "http.response.body",
            "body": b"",
        })

    async def __call__(self, scope: dict, receive: Callable, send: Callable, app: Callable):
        """Process request through CORS middleware."""
        if scope["type"] != "http":
            return await app(scope, receive, send)

        # Get origin from headers
        origin = None
        for header_name, header_value in scope.get("headers", []):
            if header_name.lower() == b"origin":
                origin = header_value.decode()
                break

        # Handle preflight request
        if scope["method"] == "OPTIONS":
            logger.debug(f"Handling CORS preflight request from origin: {origin}")
            await self._send_preflight_response(send, origin)
            return

        # Add CORS headers to response
        async def send_with_cors(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                cors_headers = self._get_cors_headers(origin)
                headers.extend(cors_headers)
                message["headers"] = headers
            await send(message)

        await app(scope, receive, send_with_cors)
