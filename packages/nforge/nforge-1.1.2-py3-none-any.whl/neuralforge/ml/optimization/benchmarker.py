"""
Performance Benchmarker - Benchmark model performance.
"""

import logging
import time
import numpy as np
from typing import Any, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from neuralforge.ml.optimization.exceptions import BenchmarkError
from neuralforge.ml.optimization.schemas import LatencyStats, MemoryStats, BenchmarkResultInfo
from neuralforge.db.models.benchmark_result import BenchmarkResult

logger = logging.getLogger(__name__)


class PerformanceBenchmarker:
    """
    Benchmark model performance.
    
    Measures latency, throughput, and memory usage.
    
    Example:
        ```python
        benchmarker = PerformanceBenchmarker(db_session)
        
        # Benchmark latency
        latency_stats = benchmarker.benchmark_latency(
            model=model,
            test_input=input_tensor,
            num_iterations=100
        )
        
        print(f"P95 latency: {latency_stats.p95_ms}ms")
        ```
    """

    def __init__(self, db: Optional[AsyncSession] = None):
        """
        Initialize benchmarker.
        
        Args:
            db: Optional database session for saving results
        """
        self.db = db
        self._check_dependencies()

    def _check_dependencies(self):
        """Check if required libraries are available."""
        try:
            import torch
            self.torch = torch
            self.torch_available = True
        except ImportError:
            self.torch = None
            self.torch_available = False

    def benchmark_latency(
        self,
        model: Any,
        test_input: Any,
        num_iterations: int = 100,
        warmup_iterations: int = 10
    ) -> LatencyStats:
        """
        Benchmark model latency.
        
        Args:
            model: Model to benchmark
            test_input: Test input
            num_iterations: Number of iterations
            warmup_iterations: Warmup iterations
        
        Returns:
            Latency statistics
        """
        try:
            model.eval()
            latencies = []

            # Warmup
            if self.torch_available:
                with self.torch.no_grad():
                    for _ in range(warmup_iterations):
                        _ = model(test_input)
            else:
                for _ in range(warmup_iterations):
                    _ = model(test_input)

            # Benchmark
            if self.torch_available:
                with self.torch.no_grad():
                    for _ in range(num_iterations):
                        start = time.time()
                        _ = model(test_input)
                        latency_ms = (time.time() - start) * 1000
                        latencies.append(latency_ms)
            else:
                for _ in range(num_iterations):
                    start = time.time()
                    _ = model(test_input)
                    latency_ms = (time.time() - start) * 1000
                    latencies.append(latency_ms)

            # Calculate statistics
            latencies_array = np.array(latencies)

            return LatencyStats(
                avg_ms=float(np.mean(latencies_array)),
                p50_ms=float(np.percentile(latencies_array, 50)),
                p95_ms=float(np.percentile(latencies_array, 95)),
                p99_ms=float(np.percentile(latencies_array, 99)),
                min_ms=float(np.min(latencies_array)),
                max_ms=float(np.max(latencies_array))
            )

        except Exception as e:
            raise BenchmarkError(f"Latency benchmarking failed: {str(e)}")

    def benchmark_throughput(
        self,
        model: Any,
        test_input: Any,
        batch_size: int = 1,
        duration_seconds: int = 10
    ) -> float:
        """
        Benchmark model throughput.
        
        Args:
            model: Model to benchmark
            test_input: Test input
            batch_size: Batch size
            duration_seconds: Benchmark duration
        
        Returns:
            Throughput in queries per second
        """
        try:
            model.eval()

            start_time = time.time()
            num_queries = 0

            if self.torch_available:
                with self.torch.no_grad():
                    while time.time() - start_time < duration_seconds:
                        _ = model(test_input)
                        num_queries += batch_size
            else:
                while time.time() - start_time < duration_seconds:
                    _ = model(test_input)
                    num_queries += batch_size

            elapsed = time.time() - start_time
            throughput = num_queries / elapsed

            return throughput

        except Exception as e:
            raise BenchmarkError(f"Throughput benchmarking failed: {str(e)}")

    def profile_memory(
        self,
        model: Any,
        test_input: Any
    ) -> MemoryStats:
        """
        Profile memory usage.
        
        Args:
            model: Model to profile
            test_input: Test input
        
        Returns:
            Memory statistics
        """
        try:
            if not self.torch_available:
                return MemoryStats(peak_mb=0.0, avg_mb=0.0)

            # Reset memory stats
            if self.torch.cuda.is_available():
                self.torch.cuda.reset_peak_memory_stats()
                self.torch.cuda.empty_cache()

            model.eval()

            # Run inference
            with self.torch.no_grad():
                _ = model(test_input)

            # Get memory stats
            if self.torch.cuda.is_available():
                peak_memory = self.torch.cuda.max_memory_allocated() / (1024 ** 2)  # MB
                current_memory = self.torch.cuda.memory_allocated() / (1024 ** 2)
            else:
                # CPU memory (approximate)
                peak_memory = 0.0
                current_memory = 0.0

            return MemoryStats(
                peak_mb=peak_memory,
                avg_mb=current_memory
            )

        except Exception as e:
            logger.error(f"Memory profiling failed: {e}")
            return MemoryStats(peak_mb=0.0, avg_mb=0.0)

    async def save_benchmark_result(
        self,
        model_name: str,
        latency_stats: LatencyStats,
        batch_size: int = 1,
        num_iterations: int = 100,
        model_version: Optional[str] = None,
        optimization_type: Optional[str] = None,
        device: str = "cpu",
        throughput_qps: Optional[float] = None,
        memory_stats: Optional[MemoryStats] = None
    ) -> BenchmarkResultInfo:
        """
        Save benchmark result to database.
        
        Args:
            model_name: Model name
            latency_stats: Latency statistics
            batch_size: Batch size
            num_iterations: Number of iterations
            model_version: Optional model version
            optimization_type: Optional optimization type
            device: Device used
            throughput_qps: Optional throughput
            memory_stats: Optional memory stats
        
        Returns:
            Saved benchmark result
        """
        if not self.db:
            raise BenchmarkError("Database session required to save results")

        result = BenchmarkResult(
            model_name=model_name,
            model_version=model_version,
            optimization_type=optimization_type,
            batch_size=batch_size,
            num_iterations=num_iterations,
            device=device,
            avg_latency_ms=latency_stats.avg_ms,
            p50_latency_ms=latency_stats.p50_ms,
            p95_latency_ms=latency_stats.p95_ms,
            p99_latency_ms=latency_stats.p99_ms,
            throughput_qps=throughput_qps,
            peak_memory_mb=memory_stats.peak_mb if memory_stats else None,
            avg_memory_mb=memory_stats.avg_mb if memory_stats else None
        )

        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)

        logger.info(f"Saved benchmark result for {model_name}")

        return BenchmarkResultInfo.model_validate(result)

    def compare_models(
        self,
        baseline_model: Any,
        optimized_model: Any,
        test_input: Any,
        num_iterations: int = 100
    ) -> Dict[str, Any]:
        """
        Compare baseline vs optimized model.
        
        Args:
            baseline_model: Baseline model
            optimized_model: Optimized model
            test_input: Test input
            num_iterations: Number of iterations
        
        Returns:
            Comparison results
        """
        try:
            # Benchmark baseline
            baseline_latency = self.benchmark_latency(
                baseline_model, test_input, num_iterations
            )
            baseline_memory = self.profile_memory(baseline_model, test_input)

            # Benchmark optimized
            optimized_latency = self.benchmark_latency(
                optimized_model, test_input, num_iterations
            )
            optimized_memory = self.profile_memory(optimized_model, test_input)

            # Calculate improvements
            speedup = baseline_latency.avg_ms / optimized_latency.avg_ms if optimized_latency.avg_ms > 0 else 1.0
            memory_reduction = (baseline_memory.peak_mb - optimized_memory.peak_mb) / baseline_memory.peak_mb if baseline_memory.peak_mb > 0 else 0.0

            return {
                'baseline_latency': baseline_latency,
                'optimized_latency': optimized_latency,
                'speedup_factor': speedup,
                'baseline_memory': baseline_memory,
                'optimized_memory': optimized_memory,
                'memory_reduction': memory_reduction
            }

        except Exception as e:
            raise BenchmarkError(f"Model comparison failed: {str(e)}")
