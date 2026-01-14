"""
Database model for predictions.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, Index
from sqlalchemy.sql import func

from neuralforge.db.base import Base


class Prediction(Base):
    """Prediction logging model."""

    __tablename__ = "predictions"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Model info
    model_name = Column(String(255), nullable=False, index=True)
    model_version = Column(String(50), nullable=False)

    # Request info
    request_id = Column(String(255), unique=True, index=True)
    user_id = Column(String(255))

    # Input/Output
    input_data = Column(JSON)
    output_data = Column(JSON)

    # Prediction details
    prediction_class = Column(String(255))
    confidence = Column(Float)

    # Performance
    latency_ms = Column(Float, nullable=False)
    preprocessing_ms = Column(Float)
    inference_ms = Column(Float)
    postprocessing_ms = Column(Float)

    # Status
    status = Column(String(50), nullable=False, index=True)  # success, error, timeout
    error_message = Column(Text)
    error_type = Column(String(100))

    # Metadata
    environment = Column(String(50))  # production, staging
    api_version = Column(String(50))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Indexes
    __table_args__ = (
        Index('idx_predictions_model', 'model_name', 'model_version'),
        Index('idx_predictions_created_at', 'created_at'),
    )

    def __repr__(self):
        return f"<Prediction(id={self.id}, model='{self.model_name}:{self.model_version}', status='{self.status}')>"
