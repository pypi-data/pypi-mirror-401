"""
Benchmark Runner for NeuralForge.

Provides orchestration for running benchmark scenarios,
collecting metrics, and generating reports.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ScenarioResult:
    """Results from a single scenario run."""
    name: str
    iterations: int
    latencies_ms: List[float] = field(default_factory=list)
    errors: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def success_count(self) -> int:
        return len(self.latencies_ms)
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.errors
        return self.success_count / total if total > 0 else 0.0
    
    @property
    def duration_seconds(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    @property
    def throughput(self) -> float:
        if self.duration_seconds > 0:
            return self.success_count / self.duration_seconds
        return 0.0
    
    def get_percentile(self, p: float) -> float:
        """Get latency percentile (0-100)."""
        if not self.latencies_ms:
            return 0.0
        sorted_latencies = sorted(self.latencies_ms)
        idx = int(len(sorted_latencies) * p / 100)
        return sorted_latencies[min(idx, len(sorted_latencies) - 1)]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for reporting."""
        return {
            "name": self.name,
            "iterations": self.iterations,
            "count": self.success_count,
            "errors": self.errors,
            "success_rate": round(self.success_rate, 4),
            "duration_seconds": round(self.duration_seconds, 3),
            "throughput": round(self.throughput, 1),
            "min_ms": round(min(self.latencies_ms), 3) if self.latencies_ms else 0,
            "max_ms": round(max(self.latencies_ms), 3) if self.latencies_ms else 0,
            "mean_ms": round(sum(self.latencies_ms) / len(self.latencies_ms), 3) if self.latencies_ms else 0,
            "p50_ms": round(self.get_percentile(50), 3),
            "p90_ms": round(self.get_percentile(90), 3),
            "p95_ms": round(self.get_percentile(95), 3),
            "p99_ms": round(self.get_percentile(99), 3),
            "metadata": self.metadata,
        }


@dataclass
class BenchmarkConfig:
    """Configuration for benchmark runs."""
    iterations: int = 1000
    warmup: int = 100
    concurrent: int = 1
    timeout: float = 30.0
    cooldown: float = 1.0
    output_dir: Optional[Path] = None
    scenarios: List[str] = field(default_factory=list)


def scenario(
    name: str = None,
    iterations: int = None,
    warmup: int = None,
    concurrent: int = None,
    timeout: float = None
):
    """
    Decorator to mark a method as a benchmark scenario.
    
    Example:
        ```python
        class MyBenchmarks(BenchmarkSuite):
            @scenario(name="latency", iterations=1000, warmup=100)
            async def benchmark_latency(self):
                response = await self.client.get("/health")
                return response.elapsed.total_seconds() * 1000
        ```
    """
    def decorator(func: Callable):
        func._benchmark_scenario = True
        func._scenario_name = name or func.__name__
        func._scenario_iterations = iterations
        func._scenario_warmup = warmup
        func._scenario_concurrent = concurrent
        func._scenario_timeout = timeout
        return func
    return decorator


class BenchmarkSuite:
    """
    Base class for benchmark suites.
    
    Extend this class to create benchmark scenarios.
    
    Example:
        ```python
        class InferenceBenchmarks(BenchmarkSuite):
            async def setup(self):
                self.client = aiohttp.ClientSession()
            
            async def teardown(self):
                await self.client.close()
            
            @scenario(name="health_check", iterations=10000)
            async def benchmark_health(self):
                async with self.client.get(f"{self.endpoint}/health") as resp:
                    await resp.text()
        ```
    """
    
    def __init__(self, endpoint: str = "http://localhost:8000"):
        self.endpoint = endpoint
        self._results: Dict[str, ScenarioResult] = {}
    
    async def setup(self):
        """Called before running benchmarks."""
        pass
    
    async def teardown(self):
        """Called after running benchmarks."""
        pass
    
    def get_scenarios(self) -> List[Callable]:
        """Get all scenario methods."""
        scenarios = []
        for name in dir(self):
            method = getattr(self, name)
            if hasattr(method, '_benchmark_scenario') and method._benchmark_scenario:
                scenarios.append(method)
        return scenarios
    
    @property
    def results(self) -> Dict[str, ScenarioResult]:
        """Get all benchmark results."""
        return self._results


class BenchmarkRunner:
    """
    Orchestrator for running benchmark scenarios.
    
    Example:
        ```python
        runner = BenchmarkRunner()
        
        suite = InferenceBenchmarks(endpoint="http://localhost:8000")
        results = await runner.run(suite)
        
        runner.save_results("benchmark_results.json")
        ```
    """
    
    def __init__(self, config: BenchmarkConfig = None):
        self.config = config or BenchmarkConfig()
        self._results: List[ScenarioResult] = []
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None
    
    async def run(
        self,
        suite: BenchmarkSuite,
        scenarios: List[str] = None
    ) -> List[ScenarioResult]:
        """
        Run benchmark scenarios.
        
        Args:
            suite: Benchmark suite to run
            scenarios: Specific scenarios to run (None = all)
        
        Returns:
            List of ScenarioResult objects
        """
        self._start_time = datetime.utcnow()
        self._results = []
        
        try:
            await suite.setup()
            
            available_scenarios = suite.get_scenarios()
            
            for scenario_method in available_scenarios:
                scenario_name = scenario_method._scenario_name
                
                # Skip if not in selected scenarios
                if scenarios and scenario_name not in scenarios:
                    continue
                
                logger.info(f"Running scenario: {scenario_name}")
                
                result = await self._run_scenario(scenario_method)
                self._results.append(result)
                suite._results[scenario_name] = result
                
                # Cooldown between scenarios
                if self.config.cooldown > 0:
                    await asyncio.sleep(self.config.cooldown)
            
        finally:
            await suite.teardown()
            self._end_time = datetime.utcnow()
        
        return self._results
    
    async def _run_scenario(self, scenario_method: Callable) -> ScenarioResult:
        """Run a single scenario."""
        name = scenario_method._scenario_name
        iterations = scenario_method._scenario_iterations or self.config.iterations
        warmup = scenario_method._scenario_warmup or self.config.warmup
        concurrent = scenario_method._scenario_concurrent or self.config.concurrent
        timeout = scenario_method._scenario_timeout or self.config.timeout
        
        result = ScenarioResult(
            name=name,
            iterations=iterations,
            metadata={
                "warmup": warmup,
                "concurrent": concurrent,
                "timeout": timeout,
            }
        )
        
        # Warmup
        logger.debug(f"Warmup: {warmup} iterations")
        for _ in range(warmup):
            try:
                await asyncio.wait_for(scenario_method(), timeout=timeout)
            except Exception as e:
                logger.debug(f"Warmup error (ignored): {e}")
        
        # Benchmark
        result.start_time = datetime.utcnow()
        
        if concurrent == 1:
            # Sequential execution
            for i in range(iterations):
                start = time.perf_counter()
                try:
                    await asyncio.wait_for(scenario_method(), timeout=timeout)
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    result.latencies_ms.append(elapsed_ms)
                except Exception as e:
                    result.errors += 1
                    logger.debug(f"Iteration {i} error: {e}")
                
                if (i + 1) % 100 == 0:
                    logger.info(f"  Progress: {i + 1}/{iterations}")
        else:
            # Concurrent execution
            await self._run_concurrent(scenario_method, result, iterations, concurrent, timeout)
        
        result.end_time = datetime.utcnow()
        
        logger.info(
            f"Scenario {name}: {result.success_count}/{iterations} success, "
            f"p99: {result.get_percentile(99):.2f}ms, "
            f"throughput: {result.throughput:.1f} req/s"
        )
        
        return result
    
    async def _run_concurrent(
        self,
        scenario_method: Callable,
        result: ScenarioResult,
        iterations: int,
        concurrent: int,
        timeout: float
    ):
        """Run scenario with concurrent requests."""
        semaphore = asyncio.Semaphore(concurrent)
        
        async def run_one():
            async with semaphore:
                start = time.perf_counter()
                try:
                    await asyncio.wait_for(scenario_method(), timeout=timeout)
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    result.latencies_ms.append(elapsed_ms)
                except Exception as e:
                    result.errors += 1
                    logger.debug(f"Concurrent error: {e}")
        
        # Run in batches
        tasks = [run_one() for _ in range(iterations)]
        for i in range(0, len(tasks), concurrent * 10):
            batch = tasks[i:i + concurrent * 10]
            await asyncio.gather(*batch, return_exceptions=True)
            
            if (i + len(batch)) % 100 == 0:
                logger.info(f"  Progress: {i + len(batch)}/{iterations}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all benchmark results."""
        return {
            "start_time": self._start_time.isoformat() if self._start_time else None,
            "end_time": self._end_time.isoformat() if self._end_time else None,
            "total_scenarios": len(self._results),
            "results": {r.name: r.to_dict() for r in self._results},
        }
    
    def save_results(self, path: str):
        """Save results to JSON file."""
        import json
        
        with open(path, "w") as f:
            json.dump(self.get_summary(), f, indent=2)
        
        logger.info(f"Results saved to: {path}")
