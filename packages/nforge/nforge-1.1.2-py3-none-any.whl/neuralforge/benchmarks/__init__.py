"""
NeuralForge Benchmark Suite

Provides comprehensive benchmarking infrastructure
including reporters and competitor comparison.
"""

from neuralforge.benchmarks.reporters import (
    BenchmarkMetrics,
    BenchmarkReport,
    MarkdownReporter,
    HTMLReporter,
    JSONReporter,
    generate_report,
)
from neuralforge.benchmarks.comparison import (
    CompetitorBenchmark,
    ComparisonResult,
    FastAPIBenchmark,
    BentoMLBenchmark,
    NeuralForgeBenchmark,
    RayServeBenchmark,
    compare_frameworks,
    generate_comparison_table,
)
from neuralforge.benchmarks.streaming import (
    StreamingBenchmark,
    StreamingMetrics,
    measure_ttft,
    measure_tokens_per_second,
)
from neuralforge.benchmarks.runner import (
    BenchmarkRunner,
    BenchmarkSuite,
    BenchmarkConfig,
    ScenarioResult,
    scenario,
)
from neuralforge.benchmarks.memory import (
    MemoryProfiler,
    MemoryProfile,
    MemorySnapshot,
    profile_inference,
)

__all__ = [
    # Reporters
    "BenchmarkMetrics",
    "BenchmarkReport",
    "MarkdownReporter",
    "HTMLReporter",
    "JSONReporter",
    "generate_report",
    # Comparison
    "CompetitorBenchmark",
    "ComparisonResult",
    "FastAPIBenchmark",
    "BentoMLBenchmark",
    "NeuralForgeBenchmark",
    "RayServeBenchmark",
    "compare_frameworks",
    "generate_comparison_table",
    # Streaming
    "StreamingBenchmark",
    "StreamingMetrics",
    "measure_ttft",
    "measure_tokens_per_second",
    # Runner
    "BenchmarkRunner",
    "BenchmarkSuite",
    "BenchmarkConfig",
    "ScenarioResult",
    "scenario",
    # Memory
    "MemoryProfiler",
    "MemoryProfile",
    "MemorySnapshot",
    "profile_inference",
]
