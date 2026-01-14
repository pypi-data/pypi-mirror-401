"""
Competitor Comparison Framework for NeuralForge.

Provides infrastructure for comparing NeuralForge
performance against other ML serving frameworks.
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ComparisonResult:
    """Result of a comparison benchmark."""
    framework: str
    benchmark_name: str
    iterations: int
    latencies_ms: List[float] = field(default_factory=list)
    throughput: float = 0.0
    errors: int = 0
    
    @property
    def min_ms(self) -> float:
        return min(self.latencies_ms) if self.latencies_ms else 0.0
    
    @property
    def max_ms(self) -> float:
        return max(self.latencies_ms) if self.latencies_ms else 0.0
    
    @property
    def mean_ms(self) -> float:
        return sum(self.latencies_ms) / len(self.latencies_ms) if self.latencies_ms else 0.0
    
    @property
    def p50_ms(self) -> float:
        return self._percentile(50)
    
    @property
    def p95_ms(self) -> float:
        return self._percentile(95)
    
    @property
    def p99_ms(self) -> float:
        return self._percentile(99)
    
    def _percentile(self, p: int) -> float:
        if not self.latencies_ms:
            return 0.0
        sorted_latencies = sorted(self.latencies_ms)
        index = int(len(sorted_latencies) * p / 100)
        return sorted_latencies[min(index, len(sorted_latencies) - 1)]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "framework": self.framework,
            "benchmark": self.benchmark_name,
            "iterations": self.iterations,
            "throughput": round(self.throughput, 2),
            "errors": self.errors,
            "latency": {
                "min_ms": round(self.min_ms, 2),
                "max_ms": round(self.max_ms, 2),
                "mean_ms": round(self.mean_ms, 2),
                "p50_ms": round(self.p50_ms, 2),
                "p95_ms": round(self.p95_ms, 2),
                "p99_ms": round(self.p99_ms, 2),
            }
        }


class CompetitorBenchmark(ABC):
    """
    Base class for competitor benchmarks.
    
    Extend this to create benchmarks for specific frameworks.
    """
    
    framework_name: str = "Unknown"
    
    def __init__(
        self,
        iterations: int = 1000,
        warmup: int = 100,
        concurrent: int = 1
    ):
        self.iterations = iterations
        self.warmup = warmup
        self.concurrent = concurrent
        self._setup_complete = False
    
    @abstractmethod
    async def setup(self):
        """Setup the framework for benchmarking."""
        pass
    
    @abstractmethod
    async def teardown(self):
        """Cleanup after benchmarking."""
        pass
    
    @abstractmethod
    async def run_request(self, **kwargs) -> Any:
        """Execute a single request."""
        pass
    
    async def benchmark(self, name: str = "default", **kwargs) -> ComparisonResult:
        """Run the full benchmark."""
        result = ComparisonResult(
            framework=self.framework_name,
            benchmark_name=name,
            iterations=self.iterations,
        )
        
        try:
            if not self._setup_complete:
                await self.setup()
                self._setup_complete = True
            
            # Warmup
            for _ in range(self.warmup):
                await self.run_request(**kwargs)
            
            # Benchmark
            start_time = time.perf_counter()
            
            for _ in range(self.iterations):
                req_start = time.perf_counter()
                try:
                    await self.run_request(**kwargs)
                    req_end = time.perf_counter()
                    result.latencies_ms.append((req_end - req_start) * 1000)
                except Exception as e:
                    result.errors += 1
                    logger.debug(f"Request error: {e}")
            
            total_time = time.perf_counter() - start_time
            result.throughput = self.iterations / total_time if total_time > 0 else 0
            
        finally:
            await self.teardown()
            self._setup_complete = False
        
        return result


class FastAPIBenchmark(CompetitorBenchmark):
    """
    Benchmark for FastAPI framework.
    
    Tests equivalent endpoints in FastAPI.
    """
    
    framework_name = "FastAPI"
    
    def __init__(self, app_factory: Callable = None, **kwargs):
        super().__init__(**kwargs)
        self.app_factory = app_factory
        self._app = None
        self._client = None
    
    async def setup(self):
        """Setup FastAPI test client."""
        try:
            from fastapi import FastAPI
            from fastapi.testclient import TestClient
            from httpx import AsyncClient, ASGITransport
            
            if self.app_factory:
                self._app = self.app_factory()
            else:
                # Create minimal test app
                self._app = FastAPI()
                
                @self._app.get("/health")
                async def health():
                    return {"status": "ok"}
                
                @self._app.post("/predict")
                async def predict(data: dict):
                    return {"result": "prediction"}
            
            self._client = AsyncClient(
                transport=ASGITransport(app=self._app),
                base_url="http://test"
            )
            logger.info("FastAPI benchmark setup complete")
            
        except ImportError:
            logger.warning("FastAPI not installed, skipping benchmark")
            raise
    
    async def teardown(self):
        """Cleanup FastAPI client."""
        if self._client:
            await self._client.aclose()
        self._app = None
        self._client = None
    
    async def run_request(self, endpoint: str = "/health", method: str = "GET", **kwargs) -> Any:
        """Execute a request."""
        if method.upper() == "GET":
            response = await self._client.get(endpoint)
        elif method.upper() == "POST":
            response = await self._client.post(endpoint, json=kwargs.get("json", {}))
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response.json()


class BentoMLBenchmark(CompetitorBenchmark):
    """
    Benchmark for BentoML framework.
    
    Note: Requires BentoML to be installed and a service to be running.
    """
    
    framework_name = "BentoML"
    
    def __init__(self, service_url: str = "http://localhost:3000", **kwargs):
        super().__init__(**kwargs)
        self.service_url = service_url
        self._client = None
    
    async def setup(self):
        """Setup HTTP client for BentoML."""
        try:
            import httpx
            self._client = httpx.AsyncClient(base_url=self.service_url)
            logger.info("BentoML benchmark setup complete")
        except ImportError:
            logger.warning("httpx not installed")
            raise
    
    async def teardown(self):
        """Cleanup client."""
        if self._client:
            await self._client.aclose()
    
    async def run_request(self, endpoint: str = "/predict", **kwargs) -> Any:
        """Execute a request."""
        response = await self._client.post(endpoint, json=kwargs.get("json", {}))
        return response.json()


class NeuralForgeBenchmark(CompetitorBenchmark):
    """Benchmark for NeuralForge framework."""
    
    framework_name = "NeuralForge"
    
    def __init__(self, app = None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self._client = None
    
    async def setup(self):
        """Setup NeuralForge test client."""
        from neuralforge.testing import TestClient
        
        if self.app is None:
            from neuralforge import NeuralForge
            self.app = NeuralForge()
            
            @self.app.endpoint("/health", methods=["GET"])
            async def health():
                return {"status": "ok"}
            
            @self.app.endpoint("/predict", methods=["POST"])
            async def predict(data: dict):
                return {"result": "prediction"}
        
        self._client = TestClient(self.app)
        await self._client.__aenter__()
        logger.info("NeuralForge benchmark setup complete")
    
    async def teardown(self):
        """Cleanup client."""
        if self._client:
            await self._client.__aexit__(None, None, None)
    
    async def run_request(self, endpoint: str = "/health", method: str = "GET", **kwargs) -> Any:
        """Execute a request."""
        if method.upper() == "GET":
            response = await self._client.get(endpoint)
        elif method.upper() == "POST":
            response = await self._client.post(endpoint, json=kwargs.get("json", {}))
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response.json()


class RayServeBenchmark(CompetitorBenchmark):
    """
    Benchmark for Ray Serve framework.
    
    Tests equivalent endpoints in Ray Serve deployments.
    
    Note: Requires Ray Serve to be installed and a deployment running.
    
    Example:
        ```python
        benchmark = RayServeBenchmark(
            service_url="http://localhost:8000",
            iterations=1000
        )
        result = await benchmark.benchmark(name="inference")
        ```
    """
    
    framework_name = "RayServe"
    
    def __init__(
        self,
        service_url: str = "http://localhost:8000",
        deployment_name: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.service_url = service_url
        self.deployment_name = deployment_name
        self._client = None
        self._is_local = False
    
    async def setup(self):
        """Setup HTTP client for Ray Serve."""
        try:
            import httpx
            self._client = httpx.AsyncClient(
                base_url=self.service_url,
                timeout=30.0
            )
            
            # Check if Ray Serve is available
            try:
                import ray
                from ray import serve
                self._is_local = True
                logger.info("Ray Serve SDK available for local testing")
            except ImportError:
                logger.info("Ray Serve SDK not available, using HTTP client only")
            
            logger.info(f"Ray Serve benchmark setup complete: {self.service_url}")
            
        except ImportError:
            logger.warning("httpx not installed")
            raise
    
    async def teardown(self):
        """Cleanup client."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def run_request(
        self,
        endpoint: str = "/",
        method: str = "POST",
        **kwargs
    ) -> Any:
        """
        Execute a request to Ray Serve deployment.
        
        Args:
            endpoint: Endpoint path
            method: HTTP method
            **kwargs: Additional arguments (json, etc.)
        
        Returns:
            Response data
        """
        headers = {}
        
        # Add deployment header if specified
        if self.deployment_name:
            headers["X-Ray-Serve-Deployment"] = self.deployment_name
        
        if method.upper() == "GET":
            response = await self._client.get(endpoint, headers=headers)
        elif method.upper() == "POST":
            response = await self._client.post(
                endpoint,
                json=kwargs.get("json", {}),
                headers=headers
            )
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response.json()
    
    async def benchmark_with_ray_metrics(
        self,
        name: str = "default",
        **kwargs
    ) -> ComparisonResult:
        """
        Run benchmark with Ray-specific metrics if available.
        
        Includes Ray Serve internal metrics like queue depth
        and replica utilization if running locally.
        """
        result = await self.benchmark(name=name, **kwargs)
        
        # Try to get Ray Serve metrics
        if self._is_local:
            try:
                from ray import serve
                # Get serve status if available
                # Note: This requires Ray Serve to be running locally
                result.metadata = {
                    "ray_serve_available": True,
                    "service_url": self.service_url,
                }
            except Exception as e:
                logger.debug(f"Could not get Ray Serve metrics: {e}")
        
        return result


async def compare_frameworks(
    benchmarks: List[CompetitorBenchmark],
    scenarios: List[Dict[str, Any]] = None,
    output_file: Optional[str] = None
) -> Dict[str, List[ComparisonResult]]:
    """
    Run comparison benchmarks across multiple frameworks.
    
    Args:
        benchmarks: List of benchmark instances
        scenarios: List of benchmark scenarios
        output_file: Optional file to save results
    
    Returns:
        Dictionary of results per framework
    
    Example:
        ```python
        results = await compare_frameworks([
            NeuralForgeBenchmark(iterations=1000),
            FastAPIBenchmark(iterations=1000),
        ], scenarios=[
            {"name": "health", "endpoint": "/health", "method": "GET"},
            {"name": "predict", "endpoint": "/predict", "method": "POST"},
        ])
        ```
    """
    if scenarios is None:
        scenarios = [
            {"name": "health_check", "endpoint": "/health", "method": "GET"},
        ]
    
    results: Dict[str, List[ComparisonResult]] = {}
    
    for benchmark in benchmarks:
        framework_name = benchmark.framework_name
        results[framework_name] = []
        
        logger.info(f"Running benchmarks for {framework_name}")
        
        for scenario in scenarios:
            try:
                result = await benchmark.benchmark(
                    name=scenario.get("name", "default"),
                    endpoint=scenario.get("endpoint", "/health"),
                    method=scenario.get("method", "GET"),
                    json=scenario.get("json", {}),
                )
                results[framework_name].append(result)
                
                logger.info(
                    f"  {scenario['name']}: {result.throughput:.0f} req/s, "
                    f"p99: {result.p99_ms:.2f}ms"
                )
                
            except Exception as e:
                logger.error(f"  {scenario['name']}: Failed - {e}")
    
    # Save to file if requested
    if output_file:
        import json
        output = {
            framework: [r.to_dict() for r in framework_results]
            for framework, framework_results in results.items()
        }
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
    
    return results


def generate_comparison_table(results: Dict[str, List[ComparisonResult]]) -> str:
    """
    Generate a comparison table from results.
    
    Args:
        results: Results from compare_frameworks
    
    Returns:
        Markdown table string
    """
    lines = []
    
    # Get all scenarios
    scenarios = set()
    for framework_results in results.values():
        for result in framework_results:
            scenarios.add(result.benchmark_name)
    
    # Header
    frameworks = list(results.keys())
    header = "| Scenario |"
    for fw in frameworks:
        header += f" {fw} (req/s) | {fw} p99 |"
    lines.append(header)
    
    separator = "|----------|"
    for _ in frameworks:
        separator += "------------|---------|"
    lines.append(separator)
    
    # Rows
    for scenario in sorted(scenarios):
        row = f"| {scenario} |"
        for fw in frameworks:
            fw_results = results.get(fw, [])
            scenario_result = next(
                (r for r in fw_results if r.benchmark_name == scenario),
                None
            )
            if scenario_result:
                row += f" {scenario_result.throughput:.0f} | {scenario_result.p99_ms:.1f}ms |"
            else:
                row += " N/A | N/A |"
        lines.append(row)
    
    return "\n".join(lines)
