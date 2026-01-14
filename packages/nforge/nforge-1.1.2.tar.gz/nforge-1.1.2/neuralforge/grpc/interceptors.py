"""
gRPC Interceptors for NeuralForge.

Provides middleware-like functionality for gRPC requests.
"""

import asyncio
import logging
import time
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

# Check for grpcio availability
try:
    import grpc
    from grpc import aio as grpc_aio
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False
    grpc = None
    grpc_aio = None


class BaseInterceptor:
    """Base class for gRPC interceptors."""
    
    def __init__(self):
        self._request_count = 0
        self._error_count = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get interceptor statistics."""
        return {
            "interceptor": self.__class__.__name__,
            "request_count": self._request_count,
            "error_count": self._error_count,
        }


class LoggingInterceptor(BaseInterceptor):
    """
    Logs all gRPC requests and responses.
    
    Example:
        ```python
        server = GRPCServer(app)
        server.add_interceptor(LoggingInterceptor())
        ```
    """
    
    def __init__(
        self,
        log_request: bool = True,
        log_response: bool = True,
        log_errors: bool = True,
        include_metadata: bool = False
    ):
        super().__init__()
        self.log_request = log_request
        self.log_response = log_response
        self.log_errors = log_errors
        self.include_metadata = include_metadata
    
    async def intercept_unary_unary(
        self,
        continuation: Callable,
        client_call_details: Any,
        request: Any
    ) -> Any:
        """Intercept unary-unary calls."""
        method = client_call_details.method
        start_time = time.perf_counter()
        self._request_count += 1
        
        if self.log_request:
            logger.info(f"gRPC Request: {method}")
            if self.include_metadata and client_call_details.metadata:
                logger.debug(f"  Metadata: {dict(client_call_details.metadata)}")
        
        try:
            response = await continuation(client_call_details, request)
            
            elapsed = (time.perf_counter() - start_time) * 1000
            
            if self.log_response:
                logger.info(f"gRPC Response: {method} [{elapsed:.2f}ms]")
            
            return response
            
        except Exception as e:
            self._error_count += 1
            elapsed = (time.perf_counter() - start_time) * 1000
            
            if self.log_errors:
                logger.error(f"gRPC Error: {method} [{elapsed:.2f}ms] - {e}")
            
            raise
    
    async def intercept_unary_stream(
        self,
        continuation: Callable,
        client_call_details: Any,
        request: Any
    ):
        """Intercept unary-stream calls."""
        method = client_call_details.method
        start_time = time.perf_counter()
        self._request_count += 1
        
        if self.log_request:
            logger.info(f"gRPC Stream Request: {method}")
        
        try:
            async for response in continuation(client_call_details, request):
                yield response
            
            elapsed = (time.perf_counter() - start_time) * 1000
            if self.log_response:
                logger.info(f"gRPC Stream Complete: {method} [{elapsed:.2f}ms]")
                
        except Exception as e:
            self._error_count += 1
            if self.log_errors:
                logger.error(f"gRPC Stream Error: {method} - {e}")
            raise


class AuthInterceptor(BaseInterceptor):
    """
    Authentication interceptor for gRPC.
    
    Validates tokens or API keys in request metadata.
    
    Example:
        ```python
        async def validate_token(token: str) -> bool:
            return token == "valid-token"
        
        server = GRPCServer(app)
        server.add_interceptor(AuthInterceptor(
            validator=validate_token,
            metadata_key="authorization"
        ))
        ```
    """
    
    def __init__(
        self,
        validator: Callable[[str], bool] = None,
        metadata_key: str = "authorization",
        skip_methods: Optional[list] = None
    ):
        super().__init__()
        self.validator = validator
        self.metadata_key = metadata_key.lower()
        self.skip_methods = skip_methods or []
    
    def _should_skip(self, method: str) -> bool:
        """Check if method should skip auth."""
        for skip in self.skip_methods:
            if skip in method:
                return True
        return False
    
    def _get_token(self, metadata: Any) -> Optional[str]:
        """Extract token from metadata."""
        if not metadata:
            return None
        
        for key, value in metadata:
            if key.lower() == self.metadata_key:
                # Handle "Bearer <token>" format
                if value.lower().startswith("bearer "):
                    return value[7:]
                return value
        
        return None
    
    async def intercept_unary_unary(
        self,
        continuation: Callable,
        client_call_details: Any,
        request: Any
    ) -> Any:
        """Intercept and validate authentication."""
        method = client_call_details.method
        self._request_count += 1
        
        if self._should_skip(method):
            return await continuation(client_call_details, request)
        
        token = self._get_token(client_call_details.metadata)
        
        if not token:
            self._error_count += 1
            if GRPC_AVAILABLE:
                context = grpc_aio.ServicerContext()
                await context.abort(
                    grpc.StatusCode.UNAUTHENTICATED,
                    "Missing authentication token"
                )
            raise PermissionError("Missing authentication token")
        
        # Validate token
        if self.validator:
            if asyncio.iscoroutinefunction(self.validator):
                is_valid = await self.validator(token)
            else:
                is_valid = self.validator(token)
            
            if not is_valid:
                self._error_count += 1
                if GRPC_AVAILABLE:
                    context = grpc_aio.ServicerContext()
                    await context.abort(
                        grpc.StatusCode.PERMISSION_DENIED,
                        "Invalid authentication token"
                    )
                raise PermissionError("Invalid authentication token")
        
        return await continuation(client_call_details, request)


class MetricsInterceptor(BaseInterceptor):
    """
    Collects metrics for gRPC requests.
    
    Tracks latency, throughput, and error rates.
    
    Example:
        ```python
        metrics = MetricsInterceptor()
        server.add_interceptor(metrics)
        
        # Later, get metrics
        stats = metrics.get_detailed_stats()
        ```
    """
    
    def __init__(self, histogram_buckets: Optional[list] = None):
        super().__init__()
        self.histogram_buckets = histogram_buckets or [
            0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0
        ]
        self._latencies: Dict[str, list] = {}
        self._method_counts: Dict[str, int] = {}
        self._method_errors: Dict[str, int] = {}
        self._started_at = datetime.utcnow()
    
    async def intercept_unary_unary(
        self,
        continuation: Callable,
        client_call_details: Any,
        request: Any
    ) -> Any:
        """Intercept and collect metrics."""
        method = client_call_details.method
        start_time = time.perf_counter()
        self._request_count += 1
        
        # Update method count
        self._method_counts[method] = self._method_counts.get(method, 0) + 1
        
        try:
            response = await continuation(client_call_details, request)
            
            # Record latency
            latency = time.perf_counter() - start_time
            if method not in self._latencies:
                self._latencies[method] = []
            self._latencies[method].append(latency)
            
            # Keep only last 1000 latencies per method
            if len(self._latencies[method]) > 1000:
                self._latencies[method] = self._latencies[method][-1000:]
            
            return response
            
        except Exception as e:
            self._error_count += 1
            self._method_errors[method] = self._method_errors.get(method, 0) + 1
            raise
    
    def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed metrics."""
        uptime = (datetime.utcnow() - self._started_at).total_seconds()
        
        stats = {
            "uptime_seconds": round(uptime, 2),
            "total_requests": self._request_count,
            "total_errors": self._error_count,
            "error_rate": round(
                self._error_count / max(self._request_count, 1), 4
            ),
            "requests_per_second": round(
                self._request_count / max(uptime, 1), 2
            ),
            "methods": {},
        }
        
        # Per-method stats
        for method, count in self._method_counts.items():
            method_stats = {
                "count": count,
                "errors": self._method_errors.get(method, 0),
            }
            
            if method in self._latencies and self._latencies[method]:
                latencies = sorted(self._latencies[method])
                method_stats["latency"] = {
                    "min_ms": round(latencies[0] * 1000, 2),
                    "max_ms": round(latencies[-1] * 1000, 2),
                    "avg_ms": round(sum(latencies) / len(latencies) * 1000, 2),
                    "p50_ms": round(self._percentile(latencies, 50) * 1000, 2),
                    "p95_ms": round(self._percentile(latencies, 95) * 1000, 2),
                    "p99_ms": round(self._percentile(latencies, 99) * 1000, 2),
                }
            
            stats["methods"][method] = method_stats
        
        return stats
    
    def _percentile(self, data: list, percentile: int) -> float:
        """Calculate percentile."""
        if not data:
            return 0.0
        index = int(len(data) * percentile / 100)
        return data[min(index, len(data) - 1)]
    
    def reset(self):
        """Reset all metrics."""
        self._request_count = 0
        self._error_count = 0
        self._latencies.clear()
        self._method_counts.clear()
        self._method_errors.clear()
        self._started_at = datetime.utcnow()


class RateLimitInterceptor(BaseInterceptor):
    """
    Rate limiting interceptor for gRPC.
    
    Limits requests per client based on metadata.
    
    Example:
        ```python
        server.add_interceptor(RateLimitInterceptor(
            rate=100,  # 100 requests
            per=60,    # per 60 seconds
            key_func=lambda meta: meta.get('client-id', 'default')
        ))
        ```
    """
    
    def __init__(
        self,
        rate: int = 100,
        per: int = 60,
        key_func: Optional[Callable] = None
    ):
        super().__init__()
        self.rate = rate
        self.per = per
        self.key_func = key_func
        self._buckets: Dict[str, Dict] = {}
    
    def _get_key(self, metadata: Any) -> str:
        """Get rate limit key from metadata."""
        if self.key_func:
            meta_dict = dict(metadata) if metadata else {}
            return self.key_func(meta_dict)
        return "default"
    
    def _check_rate_limit(self, key: str) -> bool:
        """Check if request is within rate limit."""
        now = time.time()
        
        if key not in self._buckets:
            self._buckets[key] = {
                "tokens": self.rate,
                "last_update": now
            }
        
        bucket = self._buckets[key]
        elapsed = now - bucket["last_update"]
        
        # Refill tokens based on elapsed time
        tokens_to_add = elapsed * (self.rate / self.per)
        bucket["tokens"] = min(self.rate, bucket["tokens"] + tokens_to_add)
        bucket["last_update"] = now
        
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        
        return False
    
    async def intercept_unary_unary(
        self,
        continuation: Callable,
        client_call_details: Any,
        request: Any
    ) -> Any:
        """Intercept and apply rate limiting."""
        self._request_count += 1
        
        key = self._get_key(client_call_details.metadata)
        
        if not self._check_rate_limit(key):
            self._error_count += 1
            if GRPC_AVAILABLE:
                context = grpc_aio.ServicerContext()
                await context.abort(
                    grpc.StatusCode.RESOURCE_EXHAUSTED,
                    f"Rate limit exceeded for {key}"
                )
            raise RuntimeError(f"Rate limit exceeded for {key}")
        
        return await continuation(client_call_details, request)
