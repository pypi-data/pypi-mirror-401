"""
Streaming Benchmarks for NeuralForge.

Measures LLM-specific metrics like time-to-first-token (TTFT)
and tokens-per-second throughput.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Callable, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class StreamingMetrics:
    """Metrics for streaming benchmarks."""
    total_tokens: int = 0
    total_time_ms: float = 0.0
    time_to_first_token_ms: float = 0.0
    tokens_per_second: float = 0.0
    inter_token_latency_ms: List[float] = field(default_factory=list)
    
    @property
    def avg_inter_token_latency_ms(self) -> float:
        if not self.inter_token_latency_ms:
            return 0.0
        return sum(self.inter_token_latency_ms) / len(self.inter_token_latency_ms)
    
    @property
    def p50_itl_ms(self) -> float:
        return self._percentile(50)
    
    @property
    def p99_itl_ms(self) -> float:
        return self._percentile(99)
    
    def _percentile(self, p: int) -> float:
        if not self.inter_token_latency_ms:
            return 0.0
        sorted_latencies = sorted(self.inter_token_latency_ms)
        index = int(len(sorted_latencies) * p / 100)
        return sorted_latencies[min(index, len(sorted_latencies) - 1)]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_tokens": self.total_tokens,
            "total_time_ms": round(self.total_time_ms, 2),
            "time_to_first_token_ms": round(self.time_to_first_token_ms, 2),
            "tokens_per_second": round(self.tokens_per_second, 2),
            "inter_token_latency": {
                "avg_ms": round(self.avg_inter_token_latency_ms, 2),
                "p50_ms": round(self.p50_itl_ms, 2),
                "p99_ms": round(self.p99_itl_ms, 2),
            }
        }


class StreamingBenchmark:
    """
    Benchmark streaming/LLM inference performance.
    
    Measures key metrics for LLM serving:
    - Time to First Token (TTFT)
    - Tokens per Second
    - Inter-Token Latency (ITL)
    
    Example:
        ```python
        benchmark = StreamingBenchmark()
        
        async def generate_tokens(prompt: str):
            for token in ["Hello", " ", "World"]:
                yield token
        
        result = await benchmark.measure(generate_tokens, "test prompt")
        print(f"TTFT: {result.time_to_first_token_ms}ms")
        print(f"Tokens/sec: {result.tokens_per_second}")
        ```
    """
    
    def __init__(
        self,
        warmup_iterations: int = 3,
        measure_iterations: int = 10
    ):
        self.warmup_iterations = warmup_iterations
        self.measure_iterations = measure_iterations
    
    async def measure(
        self,
        generator_func: Callable[..., AsyncIterator[str]],
        *args,
        **kwargs
    ) -> StreamingMetrics:
        """
        Measure streaming performance.
        
        Args:
            generator_func: Async generator function that yields tokens
            *args: Arguments to pass to generator
            **kwargs: Keyword arguments to pass to generator
        
        Returns:
            StreamingMetrics with all measurements
        """
        # Warmup
        for _ in range(self.warmup_iterations):
            async for _ in generator_func(*args, **kwargs):
                pass
        
        # Measure
        all_metrics: List[StreamingMetrics] = []
        
        for _ in range(self.measure_iterations):
            metrics = await self._measure_single(generator_func, *args, **kwargs)
            all_metrics.append(metrics)
        
        # Aggregate results
        return self._aggregate_metrics(all_metrics)
    
    async def _measure_single(
        self,
        generator_func: Callable[..., AsyncIterator[str]],
        *args,
        **kwargs
    ) -> StreamingMetrics:
        """Measure a single streaming call."""
        metrics = StreamingMetrics()
        
        start_time = time.perf_counter()
        first_token_time = None
        last_token_time = start_time
        
        async for token in generator_func(*args, **kwargs):
            now = time.perf_counter()
            
            if first_token_time is None:
                first_token_time = now
                metrics.time_to_first_token_ms = (now - start_time) * 1000
            else:
                # Inter-token latency
                itl = (now - last_token_time) * 1000
                metrics.inter_token_latency_ms.append(itl)
            
            metrics.total_tokens += 1
            last_token_time = now
        
        end_time = time.perf_counter()
        metrics.total_time_ms = (end_time - start_time) * 1000
        
        if metrics.total_time_ms > 0:
            metrics.tokens_per_second = metrics.total_tokens / (metrics.total_time_ms / 1000)
        
        return metrics
    
    def _aggregate_metrics(self, all_metrics: List[StreamingMetrics]) -> StreamingMetrics:
        """Aggregate multiple measurement runs."""
        if not all_metrics:
            return StreamingMetrics()
        
        result = StreamingMetrics()
        
        # Average values
        result.total_tokens = int(sum(m.total_tokens for m in all_metrics) / len(all_metrics))
        result.total_time_ms = sum(m.total_time_ms for m in all_metrics) / len(all_metrics)
        result.time_to_first_token_ms = sum(m.time_to_first_token_ms for m in all_metrics) / len(all_metrics)
        result.tokens_per_second = sum(m.tokens_per_second for m in all_metrics) / len(all_metrics)
        
        # Combine all inter-token latencies
        for m in all_metrics:
            result.inter_token_latency_ms.extend(m.inter_token_latency_ms)
        
        return result


async def measure_ttft(
    generator_func: Callable[..., AsyncIterator[str]],
    *args,
    iterations: int = 10,
    **kwargs
) -> Dict[str, float]:
    """
    Measure Time to First Token (TTFT).
    
    Args:
        generator_func: Async generator function
        *args: Arguments to pass to generator
        iterations: Number of measurements
        **kwargs: Keyword arguments to pass to generator
    
    Returns:
        Dictionary with TTFT statistics
    """
    ttft_values: List[float] = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        async for token in generator_func(*args, **kwargs):
            ttft = (time.perf_counter() - start) * 1000
            ttft_values.append(ttft)
            break  # Only measure first token
    
    if not ttft_values:
        return {"min_ms": 0, "max_ms": 0, "avg_ms": 0, "p50_ms": 0, "p99_ms": 0}
    
    sorted_values = sorted(ttft_values)
    
    return {
        "min_ms": round(min(ttft_values), 2),
        "max_ms": round(max(ttft_values), 2),
        "avg_ms": round(sum(ttft_values) / len(ttft_values), 2),
        "p50_ms": round(sorted_values[len(sorted_values) // 2], 2),
        "p99_ms": round(sorted_values[int(len(sorted_values) * 0.99)], 2),
    }


async def measure_tokens_per_second(
    generator_func: Callable[..., AsyncIterator[str]],
    *args,
    iterations: int = 10,
    **kwargs
) -> Dict[str, float]:
    """
    Measure tokens per second throughput.
    
    Args:
        generator_func: Async generator function
        *args: Arguments to pass to generator
        iterations: Number of measurements
        **kwargs: Keyword arguments to pass to generator
    
    Returns:
        Dictionary with throughput statistics
    """
    tps_values: List[float] = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        token_count = 0
        
        async for token in generator_func(*args, **kwargs):
            token_count += 1
        
        elapsed = time.perf_counter() - start
        if elapsed > 0:
            tps_values.append(token_count / elapsed)
    
    if not tps_values:
        return {"min": 0, "max": 0, "avg": 0, "p50": 0, "p99": 0}
    
    sorted_values = sorted(tps_values)
    
    return {
        "min": round(min(tps_values), 1),
        "max": round(max(tps_values), 1),
        "avg": round(sum(tps_values) / len(tps_values), 1),
        "p50": round(sorted_values[len(sorted_values) // 2], 1),
        "p99": round(sorted_values[int(len(sorted_values) * 0.99)], 1),
    }


class ConcurrentStreamingBenchmark:
    """
    Benchmark streaming under concurrent load.
    
    Measures how well the system handles multiple
    simultaneous streaming requests.
    """
    
    def __init__(
        self,
        concurrent_requests: List[int] = None,
        iterations_per_level: int = 5
    ):
        self.concurrent_levels = concurrent_requests or [1, 5, 10, 25, 50]
        self.iterations = iterations_per_level
    
    async def measure(
        self,
        generator_func: Callable[..., AsyncIterator[str]],
        *args,
        **kwargs
    ) -> Dict[int, StreamingMetrics]:
        """
        Measure streaming at different concurrency levels.
        
        Returns:
            Dictionary mapping concurrency level to metrics
        """
        results: Dict[int, StreamingMetrics] = {}
        
        for level in self.concurrent_levels:
            logger.info(f"Measuring at concurrency level {level}")
            metrics = await self._measure_at_concurrency(
                generator_func, level, *args, **kwargs
            )
            results[level] = metrics
        
        return results
    
    async def _measure_at_concurrency(
        self,
        generator_func: Callable[..., AsyncIterator[str]],
        concurrency: int,
        *args,
        **kwargs
    ) -> StreamingMetrics:
        """Measure at a specific concurrency level."""
        all_metrics: List[StreamingMetrics] = []
        
        for _ in range(self.iterations):
            # Create concurrent tasks
            tasks = [
                self._measure_single_stream(generator_func, *args, **kwargs)
                for _ in range(concurrency)
            ]
            
            # Run concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Collect successful results
            for result in results:
                if isinstance(result, StreamingMetrics):
                    all_metrics.append(result)
        
        # Aggregate
        if not all_metrics:
            return StreamingMetrics()
        
        aggregated = StreamingMetrics()
        aggregated.total_tokens = int(sum(m.total_tokens for m in all_metrics) / len(all_metrics))
        aggregated.total_time_ms = sum(m.total_time_ms for m in all_metrics) / len(all_metrics)
        aggregated.time_to_first_token_ms = sum(m.time_to_first_token_ms for m in all_metrics) / len(all_metrics)
        aggregated.tokens_per_second = sum(m.tokens_per_second for m in all_metrics) / len(all_metrics)
        
        for m in all_metrics:
            aggregated.inter_token_latency_ms.extend(m.inter_token_latency_ms)
        
        return aggregated
    
    async def _measure_single_stream(
        self,
        generator_func: Callable[..., AsyncIterator[str]],
        *args,
        **kwargs
    ) -> StreamingMetrics:
        """Measure a single stream."""
        metrics = StreamingMetrics()
        
        start_time = time.perf_counter()
        first_token_time = None
        last_token_time = start_time
        
        try:
            async for token in generator_func(*args, **kwargs):
                now = time.perf_counter()
                
                if first_token_time is None:
                    first_token_time = now
                    metrics.time_to_first_token_ms = (now - start_time) * 1000
                else:
                    itl = (now - last_token_time) * 1000
                    metrics.inter_token_latency_ms.append(itl)
                
                metrics.total_tokens += 1
                last_token_time = now
            
            end_time = time.perf_counter()
            metrics.total_time_ms = (end_time - start_time) * 1000
            
            if metrics.total_time_ms > 0:
                metrics.tokens_per_second = metrics.total_tokens / (metrics.total_time_ms / 1000)
                
        except Exception as e:
            logger.debug(f"Stream error: {e}")
        
        return metrics
