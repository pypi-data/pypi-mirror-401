"""
Decorators for NeuralForge endpoints.

Provides convenient decorators for common endpoint patterns like
rate limiting, authentication, caching, etc.
"""

import functools
import time
from typing import Callable
import hashlib
import logging

logger = logging.getLogger(__name__)

# Try to import Redis
try:
    import redis as redis_module
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not installed. Rate limiting decorator will be disabled.")


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    def __init__(self, retry_after: int):
        """Initialize exception with retry_after time.
        
        Args:
            retry_after: Seconds until next request allowed
        """
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")


def rate_limit(
    requests: int = 100,
    per: str = "minute",
    redis_url: str = "redis://localhost:6379/0",
    key_prefix: str = "ratelimit:endpoint"
):
    """
    Decorator for per-endpoint rate limiting.
    
    Limits the number of requests to an endpoint within a time window.
    Uses Redis for distributed rate limiting.
    
    Args:
        requests: Number of requests allowed per time window
        per: Time window ("second", "minute", "hour", "day")
        redis_url: Redis connection URL
        key_prefix: Redis key prefix for this endpoint
    
    Returns:
        Decorated function with rate limiting
    
    Raises:
        RateLimitExceeded: When rate limit is exceeded
    
    Example:
        ```python
        from neuralforge.decorators import rate_limit
        
        @app.endpoint("/expensive-operation", methods=["POST"])
        @rate_limit(requests=10, per="hour")
        async def expensive_op():
            # This endpoint is limited to 10 requests per hour
            return {"status": "done"}
        ```
    
    Response when rate limited:
        ```json
        {
          "error": "Rate limit exceeded",
          "retry_after": 3600,
          "limit": "10 requests per hour"
        }
        ```
    """
    # Convert time window to seconds
    window_seconds = {
        "second": 1,
        "minute": 60,
        "hour": 3600,
        "day": 86400
    }.get(per.lower(), 60)

    def decorator(func: Callable) -> Callable:
        """Apply rate limiting to function.
        
        Args:
            func: Function to rate limit
            
        Returns:
            Rate-limited function
        """
        # Get endpoint name for rate limit key
        endpoint_name = func.__name__

        # Initialize Redis connection
        redis_client = None
        if REDIS_AVAILABLE:
            try:
                redis_client = redis_module.from_url(redis_url, decode_responses=True)
                redis_client.ping()
                logger.info(f"Rate limit decorator initialized for {endpoint_name}")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}. Rate limiting disabled for {endpoint_name}.")
                redis_client = None

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            """Execute function with rate limit check."""
            # If Redis not available, skip rate limiting
            if not redis_client:
                return await func(*args, **kwargs)

            # Generate rate limit key
            # Try to get user identifier from kwargs (api_key, user_id, etc.)
            identifier = None
            for key in ['api_key', 'user_id', 'user', 'request']:
                if key in kwargs:
                    identifier = str(kwargs[key])
                    break

            # Fall back to endpoint name if no identifier
            if not identifier:
                identifier = endpoint_name

            # Hash identifier for privacy
            hashed = hashlib.sha256(identifier.encode()).hexdigest()[:16]

            # Get current window
            current_window = int(time.time() / window_seconds)

            # Create Redis key
            rate_key = f"{key_prefix}:{endpoint_name}:{hashed}:{current_window}"

            try:
                # Increment counter
                current = redis_client.incr(rate_key)

                # Set expiry on first request
                if current == 1:
                    redis_client.expire(rate_key, window_seconds)

                # Check if over limit
                if current > requests:
                    # Get TTL for retry_after
                    ttl = redis_client.ttl(rate_key)
                    retry_after = max(1, ttl)

                    logger.warning(
                        f"Rate limit exceeded for {endpoint_name}",
                        extra={
                            "endpoint": endpoint_name,
                            "identifier": hashed,
                            "limit": requests,
                            "window": per,
                            "retry_after": retry_after
                        }
                    )

                    # Raise rate limit exception
                    raise RateLimitExceeded(retry_after)

                # Log remaining requests
                remaining = requests - current
                logger.debug(
                    f"Rate limit check passed for {endpoint_name}",
                    extra={
                        "endpoint": endpoint_name,
                        "remaining": remaining,
                        "limit": requests
                    }
                )

            except RateLimitExceeded:
                # Re-raise rate limit exceptions
                raise
            except Exception as e:
                # On error, allow request (fail open)
                logger.error(f"Rate limit check failed: {e}")

            # Call original function
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def cache(
    ttl: int = 300,
    redis_url: str = "redis://localhost:6379/0",
    key_prefix: str = "cache:endpoint"
):
    """
    Decorator for endpoint response caching.
    
    Caches endpoint responses in Redis for a specified time.
    
    Args:
        ttl: Time to live in seconds (default: 300 = 5 minutes)
        redis_url: Redis connection URL
        key_prefix: Redis key prefix for cache
    
    Returns:
        Decorated function with caching
    
    Example:
        ```python
        from neuralforge.decorators import cache
        
        @app.endpoint("/models", methods=["GET"])
        @cache(ttl=600)  # Cache for 10 minutes
        async def list_models():
            # Expensive operation
            models = await fetch_all_models()
            return {"models": models}
        ```
    """
    def decorator(func: Callable) -> Callable:
        """Apply caching to function.
        
        Args:
            func: Function to cache
            
        Returns:
            Cached function
        """
        endpoint_name = func.__name__

        # Initialize Redis connection
        redis_client = None
        if REDIS_AVAILABLE:
            try:
                redis_client = redis_module.from_url(redis_url, decode_responses=True)
                redis_client.ping()
                logger.info(f"Cache decorator initialized for {endpoint_name}")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}. Caching disabled for {endpoint_name}.")
                redis_client = None

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            """Execute function with caching."""
            # If Redis not available, skip caching
            if not redis_client:
                return await func(*args, **kwargs)

            # Generate cache key from function arguments
            import json
            cache_key_data = {
                "endpoint": endpoint_name,
                "args": str(args),
                "kwargs": {k: str(v) for k, v in kwargs.items()}
            }
            cache_key_str = json.dumps(cache_key_data, sort_keys=True)
            cache_key_hash = hashlib.sha256(cache_key_str.encode()).hexdigest()[:16]
            cache_key = f"{key_prefix}:{endpoint_name}:{cache_key_hash}"

            try:
                # Try to get from cache
                cached = redis_client.get(cache_key)
                if cached:
                    logger.debug(f"Cache hit for {endpoint_name}")
                    return json.loads(cached)

                # Cache miss - call function
                logger.debug(f"Cache miss for {endpoint_name}")
                result = await func(*args, **kwargs)

                # Store in cache
                redis_client.setex(cache_key, ttl, json.dumps(result))

                return result

            except Exception as e:
                # On error, call function directly
                logger.error(f"Cache operation failed: {e}")
                return await func(*args, **kwargs)

        return wrapper

    return decorator


# Export decorators
__all__ = [
    'rate_limit',
    'cache',
    'RateLimitExceeded'
]
