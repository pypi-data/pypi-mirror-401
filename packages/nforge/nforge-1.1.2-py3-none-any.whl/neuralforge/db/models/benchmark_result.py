"""
Database model for benchmark results.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class BenchmarkResult(Base):
    """Benchmark result record."""

    __tablename__ = "benchmark_results"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Model info
    model_name = Column(String(255), nullable=False)
    model_version = Column(String(50))
    optimization_type = Column(String(50))

    # Benchmark config
    batch_size = Column(Integer, nullable=False)
    num_iterations = Column(Integer, nullable=False)
    device = Column(String(50))  # cpu, cuda, mps

    # Latency metrics
    avg_latency_ms = Column(Float, nullable=False)
    p50_latency_ms = Column(Float)
    p95_latency_ms = Column(Float)
    p99_latency_ms = Column(Float)

    # Throughput
    throughput_qps = Column(Float)  # queries per second

    # Memory
    peak_memory_mb = Column(Float)
    avg_memory_mb = Column(Float)

    # Metadata
    benchmark_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Indexes
    __table_args__ = (
        Index('idx_benchmark_model', 'model_name', 'model_version'),
    )

    def __repr__(self):
        return f"<BenchmarkResult(model='{self.model_name}', latency={self.avg_latency_ms}ms)>"
