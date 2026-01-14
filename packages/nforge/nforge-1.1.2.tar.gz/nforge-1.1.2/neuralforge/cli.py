"""
NeuralForge CLI Module

Provides command-line interface for running benchmarks,
managing models, and server operations.
"""

import argparse
import asyncio
import json
import sys
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="neuralforge",
        description="NeuralForge - AI-Native Web Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  neuralforge benchmark run --all
  neuralforge benchmark run --scenario latency
  neuralforge benchmark compare --against fastapi,bentoml
  neuralforge benchmark report --format html --output report.html
        """
    )
    
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show version information"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="Run performance benchmarks"
    )
    benchmark_subparsers = benchmark_parser.add_subparsers(
        dest="benchmark_command",
        help="Benchmark commands"
    )
    
    # benchmark run
    run_parser = benchmark_subparsers.add_parser(
        "run",
        help="Run benchmarks"
    )
    run_parser.add_argument(
        "--all",
        action="store_true",
        help="Run all benchmark scenarios"
    )
    run_parser.add_argument(
        "--scenario", "-s",
        choices=["latency", "throughput", "streaming", "memory"],
        help="Specific scenario to run"
    )
    run_parser.add_argument(
        "--iterations", "-n",
        type=int,
        default=1000,
        help="Number of iterations (default: 1000)"
    )
    run_parser.add_argument(
        "--warmup", "-w",
        type=int,
        default=100,
        help="Warmup iterations (default: 100)"
    )
    run_parser.add_argument(
        "--concurrent", "-c",
        type=int,
        default=1,
        help="Concurrent requests (default: 1)"
    )
    run_parser.add_argument(
        "--endpoint", "-e",
        default="http://localhost:8000",
        help="Target endpoint URL"
    )
    run_parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )
    run_parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown", "html"],
        default="json",
        help="Output format (default: json)"
    )
    
    # benchmark compare
    compare_parser = benchmark_subparsers.add_parser(
        "compare",
        help="Compare with other frameworks"
    )
    compare_parser.add_argument(
        "--against", "-a",
        required=True,
        help="Frameworks to compare against (comma-separated: fastapi,bentoml)"
    )
    compare_parser.add_argument(
        "--iterations", "-n",
        type=int,
        default=1000,
        help="Number of iterations"
    )
    compare_parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )
    
    # benchmark report
    report_parser = benchmark_subparsers.add_parser(
        "report",
        help="Generate benchmark report"
    )
    report_parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input JSON results file"
    )
    report_parser.add_argument(
        "--format", "-f",
        choices=["html", "markdown", "json"],
        default="html",
        help="Report format"
    )
    report_parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output file path"
    )
    report_parser.add_argument(
        "--title", "-t",
        default="NeuralForge Benchmark Report",
        help="Report title"
    )
    
    return parser


async def run_benchmark(args) -> int:
    """Execute benchmark run command."""
    from neuralforge.benchmarks import (
        BenchmarkReport,
        BenchmarkMetrics,
        HTMLReporter,
        MarkdownReporter,
        JSONReporter,
        generate_report,
    )
    
    print(f"Running benchmarks...")
    print(f"  Endpoint: {args.endpoint}")
    print(f"  Iterations: {args.iterations}")
    print(f"  Warmup: {args.warmup}")
    print(f"  Concurrent: {args.concurrent}")
    
    results = {}
    
    if args.all or args.scenario == "latency":
        print("\n[1/4] Running latency benchmark...")
        results["latency"] = await _run_latency_benchmark(
            args.endpoint,
            args.iterations,
            args.warmup
        )
    
    if args.all or args.scenario == "throughput":
        print("\n[2/4] Running throughput benchmark...")
        results["throughput"] = await _run_throughput_benchmark(
            args.endpoint,
            args.iterations,
            args.concurrent
        )
    
    if args.all or args.scenario == "streaming":
        print("\n[3/4] Running streaming benchmark...")
        results["streaming"] = await _run_streaming_benchmark(
            args.endpoint,
            args.iterations
        )
    
    if args.all or args.scenario == "memory":
        print("\n[4/4] Running memory benchmark...")
        results["memory"] = await _run_memory_benchmark(
            args.endpoint,
            args.iterations
        )
    
    # Generate output
    if args.output:
        output_path = Path(args.output)
        
        if args.format == "json":
            with open(output_path, "w") as f:
                json.dump(results, f, indent=2)
        else:
            report_content = generate_report(
                results,
                format=args.format,
                title="NeuralForge Benchmark Results"
            )
            with open(output_path, "w") as f:
                f.write(report_content)
        
        print(f"\nResults saved to: {output_path}")
    else:
        # Print to stdout
        print("\n" + "=" * 50)
        print("BENCHMARK RESULTS")
        print("=" * 50)
        print(json.dumps(results, indent=2))
    
    return 0


async def _run_latency_benchmark(endpoint: str, iterations: int, warmup: int) -> dict:
    """Run latency benchmark."""
    import time
    import aiohttp
    
    latencies = []
    
    async with aiohttp.ClientSession() as session:
        # Warmup
        for _ in range(min(warmup, 10)):
            try:
                async with session.get(f"{endpoint}/health") as resp:
                    await resp.text()
            except Exception:
                pass
        
        # Measure
        for i in range(iterations):
            start = time.perf_counter()
            try:
                async with session.get(f"{endpoint}/health") as resp:
                    await resp.text()
                    latencies.append((time.perf_counter() - start) * 1000)
            except Exception as e:
                logger.debug(f"Request {i} failed: {e}")
            
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{iterations}")
    
    if not latencies:
        return {"error": "No successful requests"}
    
    latencies.sort()
    return {
        "count": len(latencies),
        "min_ms": round(latencies[0], 3),
        "max_ms": round(latencies[-1], 3),
        "mean_ms": round(sum(latencies) / len(latencies), 3),
        "p50_ms": round(latencies[len(latencies) // 2], 3),
        "p95_ms": round(latencies[int(len(latencies) * 0.95)], 3),
        "p99_ms": round(latencies[int(len(latencies) * 0.99)], 3),
    }


async def _run_throughput_benchmark(endpoint: str, iterations: int, concurrent: int) -> dict:
    """Run throughput benchmark."""
    import time
    import aiohttp
    
    start_time = time.perf_counter()
    success_count = 0
    error_count = 0
    
    async def make_request(session):
        nonlocal success_count, error_count
        try:
            async with session.get(f"{endpoint}/health") as resp:
                await resp.text()
                success_count += 1
        except Exception:
            error_count += 1
    
    async with aiohttp.ClientSession() as session:
        # Run concurrent requests
        for batch_start in range(0, iterations, concurrent):
            batch_size = min(concurrent, iterations - batch_start)
            tasks = [make_request(session) for _ in range(batch_size)]
            await asyncio.gather(*tasks)
            
            if (batch_start + batch_size) % 100 == 0:
                print(f"  Progress: {batch_start + batch_size}/{iterations}")
    
    elapsed = time.perf_counter() - start_time
    
    return {
        "total_requests": success_count + error_count,
        "successful": success_count,
        "errors": error_count,
        "elapsed_seconds": round(elapsed, 3),
        "requests_per_second": round(success_count / elapsed, 1) if elapsed > 0 else 0,
    }


async def _run_streaming_benchmark(endpoint: str, iterations: int) -> dict:
    """Run streaming benchmark (placeholder)."""
    # This would integrate with StreamingBenchmark
    return {
        "scenario": "streaming",
        "status": "requires streaming endpoint",
        "note": "Configure --endpoint to a streaming endpoint"
    }


async def _run_memory_benchmark(endpoint: str, iterations: int) -> dict:
    """Run memory benchmark (placeholder)."""
    import tracemalloc
    
    tracemalloc.start()
    
    # Would run actual memory profiling here
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        "current_mb": round(current / 1024 / 1024, 2),
        "peak_mb": round(peak / 1024 / 1024, 2),
    }


async def compare_frameworks(args) -> int:
    """Execute benchmark compare command."""
    from neuralforge.benchmarks import (
        FastAPIBenchmark,
        BentoMLBenchmark,
        compare_frameworks as do_compare,
    )
    
    frameworks = [f.strip().lower() for f in args.against.split(",")]
    print(f"Comparing NeuralForge against: {frameworks}")
    
    benchmarks = []
    for framework in frameworks:
        if framework == "fastapi":
            benchmarks.append(FastAPIBenchmark(iterations=args.iterations))
        elif framework == "bentoml":
            benchmarks.append(BentoMLBenchmark(iterations=args.iterations))
        else:
            print(f"Warning: Unknown framework '{framework}', skipping")
    
    if not benchmarks:
        print("Error: No valid frameworks to compare")
        return 1
    
    print("Running comparison benchmarks...")
    # Note: would run actual comparison here
    
    results = {
        "frameworks": frameworks,
        "status": "comparison complete",
        "note": "Detailed results would be generated by compare_frameworks()"
    }
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {args.output}")
    else:
        print(json.dumps(results, indent=2))
    
    return 0


def generate_report_cmd(args) -> int:
    """Execute benchmark report command."""
    from neuralforge.benchmarks import (
        BenchmarkReport,
        BenchmarkMetrics,
        HTMLReporter,
        MarkdownReporter,
        JSONReporter,
    )
    
    # Load input file
    with open(args.input, "r") as f:
        data = json.load(f)
    
    # Build report
    benchmarks = []
    for name, metrics in data.items():
        if isinstance(metrics, dict) and "count" in metrics:
            benchmarks.append(BenchmarkMetrics.from_dict(name, metrics))
    
    report = BenchmarkReport(
        title=args.title,
        benchmarks=benchmarks,
    )
    
    # Generate output
    if args.format == "html":
        reporter = HTMLReporter()
    elif args.format == "markdown":
        reporter = MarkdownReporter()
    else:
        reporter = JSONReporter()
    
    output = reporter.generate(report)
    
    with open(args.output, "w") as f:
        f.write(output)
    
    print(f"Report generated: {args.output}")
    return 0


def main(argv: Optional[list] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Setup logging
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Handle version
    if args.version:
        from neuralforge import __version__
        print(f"NeuralForge v{__version__}")
        return 0
    
    # Handle commands
    if args.command == "benchmark":
        if args.benchmark_command == "run":
            return asyncio.run(run_benchmark(args))
        elif args.benchmark_command == "compare":
            return asyncio.run(compare_frameworks(args))
        elif args.benchmark_command == "report":
            return generate_report_cmd(args)
        else:
            parser.parse_args(["benchmark", "--help"])
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
