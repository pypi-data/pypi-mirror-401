"""
Model metadata schemas for NeuralForge.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, List, Any
from datetime import datetime
import re


class ModelMetadata(BaseModel):
    """
    Metadata for ML models.
    
    This class defines all the metadata associated with a registered model,
    including version, framework, metrics, and deployment information.
    """

    # Required fields
    name: str = Field(
        ...,
        description="Model name (e.g., 'sentiment-analyzer')",
        min_length=1,
        max_length=255
    )
    version: str = Field(
        ...,
        description="Semantic version (e.g., '1.0.0')",
        pattern=r"^\d+\.\d+\.\d+$"
    )

    # Optional model info
    framework: Optional[str] = Field(
        None,
        description="ML framework (pytorch, tensorflow, sklearn, transformers, etc.)"
    )
    task_type: Optional[str] = Field(
        None,
        description="Task type (classification, regression, generation, etc.)"
    )

    # Performance metrics
    accuracy: Optional[float] = Field(None, ge=0, le=1, description="Model accuracy")
    f1_score: Optional[float] = Field(None, ge=0, le=1, description="F1 score")
    precision_score: Optional[float] = Field(None, ge=0, le=1, description="Precision")
    recall: Optional[float] = Field(None, ge=0, le=1, description="Recall")
    custom_metrics: Optional[Dict[str, float]] = Field(
        None,
        description="Custom metrics (e.g., {'auc': 0.95, 'mse': 0.02})"
    )

    # Model information
    model_size_mb: Optional[float] = Field(None, ge=0, description="Model size in MB")
    input_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="Input schema definition"
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="Output schema definition"
    )

    # Deployment status
    is_active: bool = Field(True, description="Whether model is active")
    is_deployed: bool = Field(False, description="Whether model is deployed")
    deployment_url: Optional[str] = Field(None, description="Deployment URL if deployed")

    # Additional metadata
    description: Optional[str] = Field(None, description="Model description")
    tags: Optional[List[str]] = Field(None, description="Tags (e.g., ['production', 'nlp'])")
    created_by: Optional[str] = Field(None, description="Creator email or username")
    artifact_path: Optional[str] = Field(None, description="Path to model artifact")

    @field_validator('version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate semantic versioning format."""
        if not re.match(r'^\d+\.\d+\.\d+$', v):
            raise ValueError('Version must follow semantic versioning (e.g., 1.0.0)')
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate model name format."""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Model name can only contain letters, numbers, hyphens, and underscores')
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "sentiment-analyzer",
                "version": "1.0.0",
                "framework": "transformers",
                "task_type": "classification",
                "accuracy": 0.92,
                "f1_score": 0.89,
                "precision_score": 0.91,
                "recall": 0.87,
                "model_size_mb": 450.5,
                "description": "BERT-based sentiment classifier trained on IMDB dataset",
                "tags": ["production", "nlp", "sentiment"],
                "created_by": "ml-team@company.com",
                "artifact_path": "/models/sentiment-analyzer/v1.0.0"
            }
        }
    }


class ModelInfo(BaseModel):
    """
    Model information returned from registry queries.
    Includes metadata plus database fields.
    """

    id: int
    name: str
    version: str
    framework: Optional[str] = None
    task_type: Optional[str] = None
    accuracy: Optional[float] = None
    f1_score: Optional[float] = None
    is_active: bool
    is_deployed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
