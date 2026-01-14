"""
Cache Manager - Caching layer with Redis support.
"""

from typing import Optional, Any, Dict, Callable
from dataclasses import dataclass
import asyncio
import logging
import hashlib
import pickle
import time
from functools import wraps

logger = logging.getLogger(__name__)


# ============================================================================
# Configuration
# ============================================================================

@dataclass
class CacheConfig:
    """Cache configuration."""
    backend: str = "redis"  # redis, memory
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    default_ttl: int = 300
    key_prefix: str = "neuralforge:"
    max_memory: str = "2gb"
    eviction_policy: str = "allkeys-lru"
    serializer: str = "pickle"  # pickle, json, msgpack


# ============================================================================
# Cache Backends
# ============================================================================

class CacheBackend:
    """Base class for cache backends."""

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        raise NotImplementedError

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache."""
        raise NotImplementedError

    async def delete(self, key: str):
        """Delete key from cache."""
        raise NotImplementedError

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        raise NotImplementedError

    async def clear(self):
        """Clear all cache."""
        raise NotImplementedError

    async def ping(self) -> bool:
        """Check if backend is available."""
        raise NotImplementedError

    async def close(self):
        """Close connections."""
        pass


class RedisBackend(CacheBackend):
    """Redis cache backend."""

    def __init__(self, config: CacheConfig):
        self.config = config
        self.client = None
        self._lock = asyncio.Lock()

    async def _ensure_connected(self):
        """Ensure Redis connection is established."""
        if self.client is None:
            async with self._lock:
                if self.client is None:
                    try:
                        import redis.asyncio as redis

                        self.client = redis.Redis(
                            host=self.config.host,
                            port=self.config.port,
                            db=self.config.db,
                            password=self.config.password,
                            decode_responses=False,  # We handle serialization
                        )

                        # Test connection
                        await self.client.ping()
                        logger.info(f"Connected to Redis at {self.config.host}:{self.config.port}")

                    except ImportError:
                        raise ImportError(
                            "redis is required for Redis backend. "
                            "Install with: pip install redis"
                        )
                    except Exception as e:
                        logger.error(f"Failed to connect to Redis: {e}")
                        raise

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis."""
        await self._ensure_connected()

        try:
            value = await self.client.get(self.config.key_prefix + key)

            if value is None:
                return None

            # Deserialize
            if self.config.serializer == "pickle":
                return pickle.loads(value)
            elif self.config.serializer == "json":
                import json
                return json.loads(value.decode())
            elif self.config.serializer == "msgpack":
                import msgpack
                return msgpack.unpackb(value)

            return value

        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in Redis."""
        await self._ensure_connected()

        try:
            # Serialize
            if self.config.serializer == "pickle":
                serialized = pickle.dumps(value)
            elif self.config.serializer == "json":
                import json
                serialized = json.dumps(value).encode()
            elif self.config.serializer == "msgpack":
                import msgpack
                serialized = msgpack.packb(value)
            else:
                serialized = value

            # Set with TTL
            ttl = ttl or self.config.default_ttl
            await self.client.setex(
                self.config.key_prefix + key,
                ttl,
                serialized
            )

        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {e}")
            raise

    async def delete(self, key: str):
        """Delete key from Redis."""
        await self._ensure_connected()

        try:
            await self.client.delete(self.config.key_prefix + key)
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {e}")

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        await self._ensure_connected()

        try:
            return await self.client.exists(self.config.key_prefix + key) > 0
        except Exception as e:
            logger.error(f"Error checking key {key} in Redis: {e}")
            return False

    async def clear(self):
        """Clear all cache."""
        await self._ensure_connected()

        try:
            # Delete all keys with prefix
            pattern = self.config.key_prefix + "*"
            cursor = 0

            while True:
                cursor, keys = await self.client.scan(cursor, match=pattern, count=100)
                if keys:
                    await self.client.delete(*keys)
                if cursor == 0:
                    break

            logger.info("Cleared cache")

        except Exception as e:
            logger.error(f"Error clearing cache: {e}")

    async def ping(self) -> bool:
        """Check if Redis is available."""
        try:
            await self._ensure_connected()
            return await self.client.ping()
        except Exception:
            return False

    async def close(self):
        """Close Redis connection."""
        if self.client:
            await self.client.close()
            logger.info("Closed Redis connection")

    async def delete_pattern(self, pattern: str):
        """Delete all keys matching pattern."""
        await self._ensure_connected()

        try:
            full_pattern = self.config.key_prefix + pattern
            cursor = 0

            while True:
                cursor, keys = await self.client.scan(cursor, match=full_pattern, count=100)
                if keys:
                    await self.client.delete(*keys)
                if cursor == 0:
                    break

        except Exception as e:
            logger.error(f"Error deleting pattern {pattern}: {e}")

    async def get_stats(self) -> Dict[str, Any]:
        """Get Redis stats."""
        await self._ensure_connected()

        try:
            info = await self.client.info()

            return {
                "used_memory_mb": info.get("used_memory", 0) / (1024 ** 2),
                "total_keys": info.get("db0", {}).get("keys", 0),
                "hit_rate": self._calculate_hit_rate(info),
                "connected_clients": info.get("connected_clients", 0),
            }
        except Exception as e:
            logger.error(f"Error getting Redis stats: {e}")
            return {}

    def _calculate_hit_rate(self, info: dict) -> float:
        """Calculate cache hit rate."""
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses

        if total == 0:
            return 0.0

        return hits / total


class MemoryBackend(CacheBackend):
    """In-memory cache backend (for development/testing)."""

    def __init__(self, config: CacheConfig):
        self.config = config
        self.cache: Dict[str, tuple[Any, float]] = {}  # key -> (value, expiry)
        self._lock = asyncio.Lock()

        # Stats
        self.hits = 0
        self.misses = 0

    async def get(self, key: str) -> Optional[Any]:
        """Get value from memory cache."""
        async with self._lock:
            if key not in self.cache:
                self.misses += 1
                return None

            value, expiry = self.cache[key]

            # Check if expired
            if expiry < time.time():
                del self.cache[key]
                self.misses += 1
                return None

            self.hits += 1
            return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in memory cache."""
        ttl = ttl or self.config.default_ttl
        expiry = time.time() + ttl

        async with self._lock:
            self.cache[key] = (value, expiry)

    async def delete(self, key: str):
        """Delete key from memory cache."""
        async with self._lock:
            self.cache.pop(key, None)

    async def exists(self, key: str) -> bool:
        """Check if key exists in memory cache."""
        return await self.get(key) is not None

    async def clear(self):
        """Clear all cache."""
        async with self._lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0

    async def ping(self) -> bool:
        """Memory backend is always available."""
        return True

    async def delete_pattern(self, pattern: str):
        """Delete all keys matching pattern."""
        import fnmatch

        async with self._lock:
            keys_to_delete = [
                key for key in self.cache.keys()
                if fnmatch.fnmatch(key, pattern)
            ]

            for key in keys_to_delete:
                del self.cache[key]

    async def get_stats(self) -> Dict[str, Any]:
        """Get memory cache stats."""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0.0

        return {
            "total_keys": len(self.cache),
            "hit_rate": hit_rate,
            "hits": self.hits,
            "misses": self.misses,
        }


# ============================================================================
# Cache Manager
# ============================================================================

class CacheManager:
    """
    Cache manager with support for multiple backends.
    
    Features:
    - Redis or in-memory backends
    - Automatic serialization
    - TTL support
    - Pattern-based deletion
    - Cache statistics
    - Decorator for easy caching
    """

    def __init__(self, app: "NeuralForge"):
        self.app = app
        self.backend: Optional[CacheBackend] = None
        self.config: Optional[CacheConfig] = None

        logger.info("Initialized CacheManager")

    def configure(
        self,
        backend: str = "redis",
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        default_ttl: int = 300,
        **kwargs
    ):
        """Configure cache backend."""
        self.config = CacheConfig(
            backend=backend,
            host=host,
            port=port,
            db=db,
            password=password,
            default_ttl=default_ttl,
            **kwargs
        )

        # Create backend
        if backend == "redis":
            self.backend = RedisBackend(self.config)
        elif backend == "memory":
            self.backend = MemoryBackend(self.config)
        else:
            raise ValueError(f"Unknown cache backend: {backend}")

        logger.info(f"Configured cache backend: {backend}")

    def _ensure_backend(self):
        """Ensure backend is configured."""
        if self.backend is None:
            # Default to memory backend
            self.configure(backend="memory")

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found
        """
        self._ensure_backend()
        return await self.backend.get(key)

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ):
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
        """
        self._ensure_backend()
        await self.backend.set(key, value, ttl)

    async def delete(self, key: str):
        """Delete key from cache."""
        self._ensure_backend()
        await self.backend.delete(key)

    async def delete_pattern(self, pattern: str):
        """
        Delete all keys matching pattern.
        
        Args:
            pattern: Pattern to match (supports wildcards)
        
        Example:
            >>> await cache.delete_pattern("user:*")
        """
        self._ensure_backend()
        await self.backend.delete_pattern(pattern)

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        self._ensure_backend()
        return await self.backend.exists(key)

    async def clear(self):
        """Clear entire cache."""
        self._ensure_backend()
        await self.backend.clear()

    async def ping(self) -> bool:
        """Check if cache backend is available."""
        self._ensure_backend()
        return await self.backend.ping()

    async def get_or_compute(
        self,
        key: str,
        compute_fn: Callable,
        ttl: Optional[int] = None
    ) -> Any:
        """
        Get value from cache or compute it.
        
        Args:
            key: Cache key
            compute_fn: Function to compute value if not cached
            ttl: Time to live in seconds
        
        Returns:
            Cached or computed value
        
        Example:
            >>> result = await cache.get_or_compute(
            >>>     "expensive_computation",
            >>>     lambda: expensive_function(),
            >>>     ttl=3600
            >>> )
        """
        # Try to get from cache
        value = await self.get(key)

        if value is not None:
            return value

        # Compute value
        if asyncio.iscoroutinefunction(compute_fn):
            value = await compute_fn()
        else:
            value = compute_fn()

        # Store in cache
        await self.set(key, value, ttl)

        return value

    async def get_hit_rate(self) -> float:
        """Get cache hit rate."""
        self._ensure_backend()
        stats = await self.backend.get_stats()
        return stats.get("hit_rate", 0.0)

    async def get_size_mb(self) -> float:
        """Get cache size in MB."""
        self._ensure_backend()
        stats = await self.backend.get_stats()
        return stats.get("used_memory_mb", 0.0)

    async def get_key_count(self) -> int:
        """Get number of keys in cache."""
        self._ensure_backend()
        stats = await self.backend.get_stats()
        return stats.get("total_keys", 0)

    async def cleanup(self):
        """Cleanup cache resources."""
        if self.backend:
            await self.backend.close()


# ============================================================================
# Cache Decorator
# ============================================================================

def cache(
    ttl: int = 300,
    key_builder: Optional[Callable] = None,
    key_prefix: str = ""
):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds
        key_builder: Function to build cache key from arguments
        key_prefix: Prefix for cache key
    
    Example:
        >>> @cache(ttl=600, key_prefix="predictions")
        >>> async def predict(model_name: str, data: dict):
        >>>     return await expensive_prediction(model_name, data)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get cache manager from app (assumes it's available)
            # In production, this would be injected properly
            try:
                from neuralforge import app
                cache_manager = app.cache
            except Exception:
                # If cache not available, just call function
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

            # Build cache key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                # Default: hash function name and arguments
                key_data = f"{func.__name__}:{args}:{kwargs}"
                cache_key = hashlib.md5(key_data.encode()).hexdigest()

            if key_prefix:
                cache_key = f"{key_prefix}:{cache_key}"

            # Try to get from cache
            cached_value = await cache_manager.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Call function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Store in cache
            await cache_manager.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator
