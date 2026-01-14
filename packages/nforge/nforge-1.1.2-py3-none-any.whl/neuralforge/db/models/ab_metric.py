"""
Database model for A/B testing metrics.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class ABMetric(Base):
    """A/B testing metric model."""

    __tablename__ = "ab_metrics"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    experiment_id = Column(
        Integer,
        ForeignKey("ab_experiments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    variant_id = Column(
        Integer,
        ForeignKey("ab_variants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Metric data
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String(50))  # latency, accuracy, conversion, custom

    # Context
    user_id = Column(String(255))
    prediction_id = Column(String(255))

    # Timing
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Indexes
    __table_args__ = (
        Index('idx_ab_metrics_experiment_variant', 'experiment_id', 'variant_id'),
        Index('idx_ab_metrics_metric_name', 'metric_name'),
        Index('idx_ab_metrics_recorded_at', 'recorded_at'),
    )

    def __repr__(self):
        return f"<ABMetric(id={self.id}, metric_name='{self.metric_name}', value={self.metric_value})>"
