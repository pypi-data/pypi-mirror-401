"""
Database model for prediction metrics aggregations.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class PredictionMetric(Base):
    """Prediction metrics aggregation model."""

    __tablename__ = "prediction_metrics"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Scope
    model_name = Column(String(255), nullable=False)
    model_version = Column(String(50))
    time_bucket = Column(DateTime(timezone=True), nullable=False)  # Hourly buckets

    # Counts
    total_predictions = Column(Integer, default=0)
    successful_predictions = Column(Integer, default=0)
    failed_predictions = Column(Integer, default=0)

    # Latency stats
    avg_latency_ms = Column(Float)
    p50_latency_ms = Column(Float)
    p95_latency_ms = Column(Float)
    p99_latency_ms = Column(Float)
    max_latency_ms = Column(Float)

    # Confidence stats
    avg_confidence = Column(Float)
    min_confidence = Column(Float)
    max_confidence = Column(Float)

    # Throughput
    requests_per_second = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Constraints
    __table_args__ = (
        UniqueConstraint('model_name', 'model_version', 'time_bucket', name='uq_model_time_bucket'),
        Index('idx_metrics_model_time', 'model_name', 'time_bucket'),
    )

    def __repr__(self):
        return f"<PredictionMetric(model='{self.model_name}', bucket='{self.time_bucket}')>"
