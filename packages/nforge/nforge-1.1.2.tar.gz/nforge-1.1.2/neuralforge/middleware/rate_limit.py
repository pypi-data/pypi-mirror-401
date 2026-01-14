"""
Rate Limiting Middleware - Redis-based rate limiting for production use.
"""

from typing import Callable, Optional, Tuple
import logging
import time
import hashlib

from .base import BaseMiddleware

logger = logging.getLogger(__name__)

# Try to import redis at module level
try:
    import redis as redis_module
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis_module = None


class RateLimitMiddleware(BaseMiddleware):
    """
    Redis-based rate limiting middleware.
    
    Features:
    - Fixed window rate limiting
    - Per-user or per-IP limiting
    - Configurable limits and windows
    - Rate limit headers (X-RateLimit-*)
    - Redis storage for distributed systems
    """

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        default_limit: int = 100,
        window_seconds: int = 3600,
        rate_limit_by: str = "ip",  # "ip", "user", "api_key"
        key_prefix: str = "ratelimit"
    ):
        """
        Initialize rate limiting middleware.
        
        Args:
            redis_url: Redis connection URL
            default_limit: Default number of requests per window
            window_seconds: Time window in seconds
            rate_limit_by: What to rate limit by (ip, user, api_key)
            key_prefix: Redis key prefix
        """
        self.redis_url = redis_url
        self.default_limit = default_limit
        self.window_seconds = window_seconds
        self.rate_limit_by = rate_limit_by
        self.key_prefix = key_prefix
        self.redis = None

        # Try to connect to Redis
        if not REDIS_AVAILABLE:
            logger.warning("Redis not installed, rate limiting disabled. Install: pip install redis")
            return

        try:
            self.redis = redis_module.from_url(redis_url, decode_responses=True)
            # Test connection
            self.redis.ping()
            logger.info(f"Rate limiting middleware initialized (Redis: {redis_url})")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Rate limiting disabled.")
            self.redis = None

    def _get_client_ip(self, scope: dict) -> str:
        """Extract client IP from scope."""
        # Check for forwarded IP first
        for header_name, header_value in scope.get("headers", []):
            if header_name.lower() == b"x-forwarded-for":
                # Get first IP from comma-separated list
                ip = header_value.decode().split(",")[0].strip()
                return ip
            elif header_name.lower() == b"x-real-ip":
                return header_value.decode()

        # Fall back to client address
        client = scope.get("client")
        if client:
            return client[0]

        return "unknown"

    def _get_api_key(self, scope: dict) -> Optional[str]:
        """Extract API key from headers."""
        for header_name, header_value in scope.get("headers", []):
            if header_name.lower() == b"x-api-key":
                return header_value.decode()
        return None

    def _get_rate_limit_key(self, scope: dict) -> str:
        """Generate rate limit key based on configuration."""
        if self.rate_limit_by == "ip":
            identifier = self._get_client_ip(scope)
        elif self.rate_limit_by == "api_key":
            identifier = self._get_api_key(scope) or self._get_client_ip(scope)
        else:
            # Default to IP
            identifier = self._get_client_ip(scope)

        # Hash the identifier for privacy
        hashed = hashlib.sha256(identifier.encode()).hexdigest()[:16]

        # Get current window
        current_window = int(time.time() / self.window_seconds)

        return f"{self.key_prefix}:{hashed}:{current_window}"

    async def _check_rate_limit(self, key: str) -> Tuple[bool, int, int]:
        """
        Check if request is within rate limit.
        
        Returns:
            Tuple of (allowed, remaining, reset_time)
        """
        if not self.redis:
            # Redis not available, allow all requests
            return True, self.default_limit, 0

        try:
            # Increment counter
            current = self.redis.incr(key)

            # Set expiry on first request
            if current == 1:
                self.redis.expire(key, self.window_seconds)

            # Get TTL for reset time
            ttl = self.redis.ttl(key)
            reset_time = int(time.time()) + ttl

            # Check if over limit
            remaining = max(0, self.default_limit - current)
            allowed = current <= self.default_limit

            return allowed, remaining, reset_time

        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            # On error, allow request
            return True, self.default_limit, 0

    async def _send_rate_limit_error(self, send: Callable, remaining: int, reset_time: int):
        """Send 429 Too Many Requests response."""
        import json

        error_body = json.dumps({
            "error": "Too Many Requests",
            "detail": "Rate limit exceeded. Please try again later.",
            "remaining": remaining,
            "reset_at": reset_time
        }).encode()

        await send({
            "type": "http.response.start",
            "status": 429,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(error_body)).encode()),
                (b"X-RateLimit-Limit", str(self.default_limit).encode()),
                (b"X-RateLimit-Remaining", str(remaining).encode()),
                (b"X-RateLimit-Reset", str(reset_time).encode()),
                (b"Retry-After", str(reset_time - int(time.time())).encode()),
            ],
        })

        await send({
            "type": "http.response.body",
            "body": error_body,
        })

    async def __call__(self, scope: dict, receive: Callable, send: Callable, app: Callable):
        """Process request through rate limiting middleware."""
        if scope["type"] != "http":
            return await app(scope, receive, send)

        # Get rate limit key
        key = self._get_rate_limit_key(scope)

        # Check rate limit
        allowed, remaining, reset_time = await self._check_rate_limit(key)

        if not allowed:
            logger.warning(f"Rate limit exceeded for key: {key}")
            await self._send_rate_limit_error(send, remaining, reset_time)
            return

        # Add rate limit headers to response
        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.extend([
                    (b"X-RateLimit-Limit", str(self.default_limit).encode()),
                    (b"X-RateLimit-Remaining", str(remaining).encode()),
                    (b"X-RateLimit-Reset", str(reset_time).encode()),
                ])
                message["headers"] = headers
            await send(message)

        await app(scope, receive, send_with_headers)
