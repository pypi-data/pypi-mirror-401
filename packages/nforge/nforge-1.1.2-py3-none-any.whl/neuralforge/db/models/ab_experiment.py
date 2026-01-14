"""
Database model for A/B testing experiments.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class ABExperiment(Base):
    """A/B testing experiment model."""

    __tablename__ = "ab_experiments"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Basic info
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)

    # Status
    status = Column(
        String(50),
        nullable=False,
        default="draft",
        index=True
    )  # draft, running, paused, completed, failed

    # Configuration
    traffic_allocation = Column(JSON, nullable=False)  # {"control": 50, "variant_a": 50}
    assignment_strategy = Column(
        String(50),
        default="user_hash"
    )  # user_hash, random, sticky

    # Success criteria
    primary_metric = Column(String(100), nullable=False)  # accuracy, latency, conversion
    minimum_sample_size = Column(Integer, default=1000)
    confidence_level = Column(Float, default=0.95)
    minimum_improvement = Column(Float, default=0.05)  # 5% improvement required

    # Timing
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    duration_days = Column(Integer)

    # Results
    winner = Column(String(100))  # variant name
    winner_confidence = Column(Float)

    # Metadata
    created_by = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_ab_experiments_status', 'status'),
        Index('idx_ab_experiments_created_at', 'created_at'),
    )

    def __repr__(self):
        return f"<ABExperiment(id={self.id}, name='{self.name}', status='{self.status}')>"
