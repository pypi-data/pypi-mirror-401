"""
Database model for drift baselines.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, UniqueConstraint, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class DriftBaseline(Base):
    """Drift baseline model."""

    __tablename__ = "drift_baselines"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Model info
    model_name = Column(String(255), nullable=False)
    model_version = Column(String(50), nullable=False)

    # Baseline info
    baseline_name = Column(String(255), nullable=False)
    feature_name = Column(String(255), nullable=False)

    # Distribution data
    distribution_type = Column(String(50), nullable=False)  # numerical, categorical
    distribution_data = Column(JSON, nullable=False)  # histogram, categories

    # Statistics (for numerical features)
    mean = Column(Float)
    std_dev = Column(Float)
    min_value = Column(Float)
    max_value = Column(Float)
    percentiles = Column(JSON)  # p25, p50, p75, etc.

    # Categorical stats
    categories = Column(JSON)  # category counts

    # Metadata
    sample_size = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Constraints
    __table_args__ = (
        UniqueConstraint('model_name', 'model_version', 'baseline_name', 'feature_name',
                        name='uq_baseline_feature'),
        Index('idx_baselines_model', 'model_name', 'model_version'),
    )

    def __repr__(self):
        return f"<DriftBaseline(model='{self.model_name}', baseline='{self.baseline_name}', feature='{self.feature_name}')>"
