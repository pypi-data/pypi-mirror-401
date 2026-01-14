"""
Database model for A/B testing variants.
"""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey, UniqueConstraint, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class ABVariant(Base):
    """A/B testing variant model."""

    __tablename__ = "ab_variants"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key
    experiment_id = Column(
        Integer,
        ForeignKey("ab_experiments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Variant info
    name = Column(String(100), nullable=False)  # control, variant_a, variant_b
    model_name = Column(String(255), nullable=False)
    model_version = Column(String(50), nullable=False)

    # Traffic
    traffic_percentage = Column(Float, nullable=False)  # 0-100
    is_control = Column(Boolean, default=False)

    # Status
    is_active = Column(Boolean, default=True)

    # Metadata
    description = Column(Text)
    config = Column(JSON)  # Additional variant configuration

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Constraints
    __table_args__ = (
        UniqueConstraint('experiment_id', 'name', name='uq_experiment_variant_name'),
        Index('idx_ab_variants_experiment', 'experiment_id'),
    )

    def __repr__(self):
        return f"<ABVariant(id={self.id}, name='{self.name}', model='{self.model_name}:{self.model_version}')>"
