"""
Database model for alert rules.
"""

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class AlertRule(Base):
    """Alert rule model."""

    __tablename__ = "alert_rules"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Rule info
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)

    # Scope
    model_name = Column(String(255))  # NULL for all models
    model_version = Column(String(50))

    # Condition
    metric_name = Column(String(100), nullable=False)  # latency, error_rate, confidence
    operator = Column(String(20), nullable=False)  # gt, lt, eq
    threshold = Column(Float, nullable=False)
    window_minutes = Column(Integer, default=5)

    # Alert config
    severity = Column(String(50), nullable=False)
    channels = Column(JSON)  # ["email", "slack"]

    # Status
    is_active = Column(Boolean, default=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<AlertRule(id={self.id}, name='{self.name}', active={self.is_active})>"
