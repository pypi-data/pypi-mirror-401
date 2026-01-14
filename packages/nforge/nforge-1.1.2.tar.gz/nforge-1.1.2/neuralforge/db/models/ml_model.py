"""
SQLAlchemy model for ML models.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, JSON, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from neuralforge.db.base import Base


class MLModel(Base):
    """
    Database model for ML models in the registry.
    
    Stores metadata, metrics, and deployment information for registered models.
    """

    __tablename__ = "ml_models"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Model identification
    name = Column(String(255), nullable=False, index=True)
    version = Column(String(50), nullable=False, index=True)

    # Model information
    framework = Column(String(100))  # pytorch, tensorflow, sklearn, etc.
    task_type = Column(String(100))  # classification, regression, generation, etc.

    # Performance metrics
    accuracy = Column(Float)
    f1_score = Column(Float)
    precision_score = Column(Float)
    recall = Column(Float)
    custom_metrics = Column(JSON)  # Additional metrics as JSON

    # Model details
    model_size_mb = Column(Float)
    input_schema = Column(JSON)  # Input schema definition
    output_schema = Column(JSON)  # Output schema definition

    # Deployment status
    is_active = Column(Boolean, default=True, index=True)
    is_deployed = Column(Boolean, default=False, index=True)
    deployment_url = Column(String(500))

    # Additional metadata
    description = Column(Text)
    tags = Column(JSON)  # List of tags
    created_by = Column(String(255))
    artifact_path = Column(String(500))  # Path to model file/directory

    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deployed_at = Column(DateTime)

    # Constraints
    __table_args__ = (
        UniqueConstraint('name', 'version', name='uq_model_name_version'),
    )

    def __repr__(self):
        return f"<MLModel(name='{self.name}', version='{self.version}')>"
