"""
Database model for drift detections.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class DriftDetection(Base):
    """Drift detection model."""

    __tablename__ = "drift_detections"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Model info
    model_name = Column(String(255), nullable=False)
    model_version = Column(String(50), nullable=False)
    baseline_name = Column(String(255), nullable=False)

    # Detection info
    feature_name = Column(String(255))  # NULL for overall drift

    # Drift scores
    ks_statistic = Column(Float)
    ks_p_value = Column(Float)
    psi_score = Column(Float)
    js_divergence = Column(Float)

    # Classification
    drift_detected = Column(Boolean, nullable=False)
    drift_severity = Column(String(50))  # low, medium, high, critical

    # Sample info
    sample_size = Column(Integer, nullable=False)
    detection_window = Column(String(50))  # 1h, 24h, 7d

    # Timestamps
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Indexes
    __table_args__ = (
        Index('idx_detections_model', 'model_name', 'model_version'),
        Index('idx_detections_severity', 'drift_severity'),
    )

    def __repr__(self):
        return f"<DriftDetection(model='{self.model_name}', feature='{self.feature_name}', drift={self.drift_detected})>"
