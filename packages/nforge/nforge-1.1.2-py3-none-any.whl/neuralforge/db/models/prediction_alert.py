"""
Database model for prediction alerts.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class PredictionAlert(Base):
    """Prediction alert model."""

    __tablename__ = "prediction_alerts"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Alert info
    alert_type = Column(String(100), nullable=False)  # high_latency, low_accuracy, error_spike
    severity = Column(String(50), nullable=False)  # critical, warning, info

    # Scope
    model_name = Column(String(255), index=True)
    model_version = Column(String(50))

    # Details
    message = Column(Text, nullable=False)
    threshold_value = Column(Float)
    actual_value = Column(Float)
    alert_metadata = Column(JSON)  # Renamed from 'metadata' to avoid SQLAlchemy reserved word

    # Status
    status = Column(String(50), default='active', index=True)  # active, acknowledged, resolved
    acknowledged_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))

    # Timestamps
    triggered_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Indexes
    __table_args__ = (
        Index('idx_alerts_status', 'status'),
        Index('idx_alerts_triggered', 'triggered_at'),
    )

    def __repr__(self):
        return f"<PredictionAlert(id={self.id}, type='{self.alert_type}', severity='{self.severity}')>"
