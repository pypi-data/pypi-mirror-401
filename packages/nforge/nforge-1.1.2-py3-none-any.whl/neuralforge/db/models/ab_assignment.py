"""
Database model for A/B testing user assignments.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class ABAssignment(Base):
    """A/B testing user assignment model."""

    __tablename__ = "ab_assignments"

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

    # User identification
    user_id = Column(String(255), nullable=False)
    user_hash = Column(String(64), index=True)  # Hash for consistent assignment

    # Assignment
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Constraints
    __table_args__ = (
        UniqueConstraint('experiment_id', 'user_id', name='uq_experiment_user'),
        Index('idx_ab_assignments_experiment_user', 'experiment_id', 'user_id'),
        Index('idx_ab_assignments_user_hash', 'user_hash'),
    )

    def __repr__(self):
        return f"<ABAssignment(id={self.id}, experiment_id={self.experiment_id}, user_id='{self.user_id}')>"
