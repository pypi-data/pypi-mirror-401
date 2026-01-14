"""
Database model for optimized models.
"""

from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime, JSON, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class OptimizedModel(Base):
    """Optimized model record."""

    __tablename__ = "optimized_models"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Source model
    source_model_name = Column(String(255), nullable=False)
    source_model_version = Column(String(50), nullable=False)

    # Optimized model info
    optimized_name = Column(String(255), nullable=False)
    optimization_type = Column(String(50), nullable=False)  # quantization, pruning, onnx

    # Optimization config
    config = Column(JSON, nullable=False)

    # Model files
    model_path = Column(String(500))
    model_size_bytes = Column(BigInteger)

    # Performance metrics
    baseline_latency_ms = Column(Float)
    optimized_latency_ms = Column(Float)
    speedup_factor = Column(Float)
    baseline_memory_mb = Column(Float)
    optimized_memory_mb = Column(Float)
    memory_reduction = Column(Float)

    # Accuracy metrics
    baseline_accuracy = Column(Float)
    optimized_accuracy = Column(Float)
    accuracy_loss = Column(Float)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_optimized_source', 'source_model_name', 'source_model_version'),
        Index('idx_optimized_type', 'optimization_type'),
    )

    def __repr__(self):
        return f"<OptimizedModel(name='{self.optimized_name}', type='{self.optimization_type}')>"
