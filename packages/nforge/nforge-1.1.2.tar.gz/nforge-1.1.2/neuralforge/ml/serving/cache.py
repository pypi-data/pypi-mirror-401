"""
Model Cache - Advanced model caching with LRU and memory management.
"""

import logging
from typing import Any, Optional, Dict, List
from collections import OrderedDict
import time

logger = logging.getLogger(__name__)


class ModelCache:
    """
    LRU cache for ML models with memory management.
    
    Features:
    - LRU eviction policy
    - Memory-aware caching
    - Cache statistics
    - Cache warming
    
    Example:
        ```python
        cache = ModelCache(max_size=5, max_memory_mb=2048)
        
        # Cache model
        cache.put("sentiment_v1", model, size_mb=100)
        
        # Get model
        model = cache.get("sentiment_v1")
        
        # Warm cache
        cache.warm(["sentiment_v1", "classifier_v2"])
        
        # Get stats
        stats = cache.get_stats()
        print(f"Hit rate: {stats['hit_rate']:.2%}")
        ```
    """

    def __init__(
        self,
        max_size: int = 10,
        max_memory_mb: float = 4096,
        ttl_seconds: Optional[int] = None
    ):
        """
        Initialize model cache.
        
        Args:
            max_size: Maximum number of models to cache
            max_memory_mb: Maximum memory usage in MB
            ttl_seconds: Optional TTL for cache entries
        """
        self.max_size = max_size
        self.max_memory_mb = max_memory_mb
        self.ttl_seconds = ttl_seconds

        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._current_memory_mb = 0.0

        # Statistics
        self._hits = 0
        self._misses = 0
        self._evictions = 0

        logger.info(f"ModelCache initialized: max_size={max_size}, max_memory_mb={max_memory_mb}")

    def get(self, key: str) -> Optional[Any]:
        """
        Get model from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached model or None
        """
        if key not in self._cache:
            self._misses += 1
            logger.debug(f"Cache miss: {key}")
            return None

        entry = self._cache[key]

        # Check TTL
        if self.ttl_seconds and time.time() - entry['timestamp'] > self.ttl_seconds:
            self._remove(key)
            self._misses += 1
            logger.debug(f"Cache expired: {key}")
            return None

        # Move to end (most recently used)
        self._cache.move_to_end(key)

        self._hits += 1
        logger.debug(f"Cache hit: {key}")

        return entry['model']

    def put(
        self,
        key: str,
        model: Any,
        size_mb: Optional[float] = None
    ):
        """
        Put model in cache.
        
        Args:
            key: Cache key
            model: Model to cache
            size_mb: Model size in MB (estimated if not provided)
        """
        # Estimate size if not provided
        if size_mb is None:
            size_mb = self._estimate_size(model)

        # Check if model fits in cache
        if size_mb > self.max_memory_mb:
            logger.warning(f"Model {key} ({size_mb}MB) exceeds max memory, not caching")
            return

        # Remove existing entry if present
        if key in self._cache:
            self._remove(key)

        # Evict until we have space
        while (
            len(self._cache) >= self.max_size or
            self._current_memory_mb + size_mb > self.max_memory_mb
        ):
            if not self._cache:
                break
            self._evict_lru()

        # Add to cache
        self._cache[key] = {
            'model': model,
            'size_mb': size_mb,
            'timestamp': time.time()
        }
        self._current_memory_mb += size_mb

        logger.info(f"Cached model: {key} ({size_mb:.2f}MB)")

    def _remove(self, key: str):
        """Remove entry from cache."""
        if key in self._cache:
            entry = self._cache.pop(key)
            self._current_memory_mb -= entry['size_mb']

    def _evict_lru(self):
        """Evict least recently used entry."""
        if not self._cache:
            return

        # Get first item (least recently used)
        key, entry = self._cache.popitem(last=False)
        self._current_memory_mb -= entry['size_mb']
        self._evictions += 1

        logger.info(f"Evicted LRU model: {key} ({entry['size_mb']:.2f}MB)")

    def _estimate_size(self, model: Any) -> float:
        """
        Estimate model size in MB.
        
        Args:
            model: Model to estimate
        
        Returns:
            Estimated size in MB
        """
        try:
            import sys
            size_bytes = sys.getsizeof(model)

            # Try to get more accurate size for PyTorch models
            if hasattr(model, 'parameters'):
                param_size = sum(p.numel() * p.element_size() for p in model.parameters())
                buffer_size = sum(b.numel() * b.element_size() for b in model.buffers())
                size_bytes = param_size + buffer_size

            return size_bytes / (1024 ** 2)
        except Exception as e:
            logger.warning(f"Failed to estimate model size: {e}")
            return 100.0  # Default estimate

    def warm(self, keys: List[str], loader_fn: Optional[callable] = None):
        """
        Warm cache with models.
        
        Args:
            keys: List of model keys to load
            loader_fn: Optional function to load models (key -> model)
        """
        if not loader_fn:
            logger.warning("No loader function provided for cache warming")
            return

        logger.info(f"Warming cache with {len(keys)} models")

        for key in keys:
            if key in self._cache:
                continue

            try:
                model = loader_fn(key)
                if model:
                    self.put(key, model)
            except Exception as e:
                logger.error(f"Failed to warm cache for {key}: {e}")

    def clear(self):
        """Clear entire cache."""
        self._cache.clear()
        self._current_memory_mb = 0.0
        logger.info("Cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0.0

        return {
            'size': len(self._cache),
            'max_size': self.max_size,
            'memory_mb': self._current_memory_mb,
            'max_memory_mb': self.max_memory_mb,
            'memory_usage': self._current_memory_mb / self.max_memory_mb if self.max_memory_mb > 0 else 0.0,
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': hit_rate,
            'evictions': self._evictions,
            'keys': list(self._cache.keys())
        }

    def contains(self, key: str) -> bool:
        """Check if key is in cache."""
        return key in self._cache

    def __len__(self) -> int:
        """Get number of cached models."""
        return len(self._cache)

    def __contains__(self, key: str) -> bool:
        """Check if key is in cache."""
        return self.contains(key)
