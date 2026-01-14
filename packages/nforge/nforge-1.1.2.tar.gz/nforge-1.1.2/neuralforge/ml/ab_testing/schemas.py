"""
Pydantic schemas for A/B testing.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class ExperimentStatus(str, Enum):
    """Experiment status enum."""
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class AssignmentStrategy(str, Enum):
    """Assignment strategy enum."""
    USER_HASH = "user_hash"
    RANDOM = "random"
    STICKY = "sticky"


class VariantConfig(BaseModel):
    """Configuration for a variant."""
    name: str = Field(..., description="Variant name (e.g., control, variant_a)")
    model_name: str = Field(..., description="Model name")
    model_version: str = Field(..., description="Model version")
    traffic_percentage: float = Field(..., ge=0, le=100, description="Traffic percentage (0-100)")
    is_control: bool = Field(default=False, description="Is this the control variant?")
    description: Optional[str] = Field(None, description="Variant description")
    config: Optional[Dict] = Field(None, description="Additional configuration")

    model_config = {"json_schema_extra": {
        "example": {
            "name": "control",
            "model_name": "sentiment-analyzer",
            "model_version": "1.0.0",
            "traffic_percentage": 50,
            "is_control": True
        }
    }}


class ExperimentCreate(BaseModel):
    """Schema for creating an experiment."""
    name: str = Field(..., description="Experiment name")
    description: Optional[str] = Field(None, description="Experiment description")
    variants: List[VariantConfig] = Field(..., min_length=2, description="List of variants (minimum 2)")
    primary_metric: str = Field(..., description="Primary metric to optimize")
    assignment_strategy: AssignmentStrategy = Field(
        default=AssignmentStrategy.USER_HASH,
        description="Assignment strategy"
    )
    minimum_sample_size: int = Field(default=1000, ge=100, description="Minimum sample size per variant")
    confidence_level: float = Field(default=0.95, ge=0.8, le=0.99, description="Confidence level (0.8-0.99)")
    minimum_improvement: float = Field(default=0.05, ge=0.01, description="Minimum improvement required")
    duration_days: Optional[int] = Field(None, ge=1, description="Experiment duration in days")
    created_by: Optional[str] = Field(None, description="Creator email/username")

    @field_validator('variants')
    @classmethod
    def validate_traffic_allocation(cls, variants: List[VariantConfig]) -> List[VariantConfig]:
        """Validate traffic allocation sums to 100."""
        total = sum(v.traffic_percentage for v in variants)
        if abs(total - 100.0) > 0.01:  # Allow small floating point errors
            raise ValueError(f"Traffic allocation must sum to 100, got {total}")

        # Check for exactly one control
        control_count = sum(1 for v in variants if v.is_control)
        if control_count != 1:
            raise ValueError(f"Exactly one variant must be marked as control, got {control_count}")

        return variants

    model_config = {"json_schema_extra": {
        "example": {
            "name": "model-v2-test",
            "description": "Testing new model version",
            "variants": [
                {
                    "name": "control",
                    "model_name": "sentiment-analyzer",
                    "model_version": "1.0.0",
                    "traffic_percentage": 50,
                    "is_control": True
                },
                {
                    "name": "variant_a",
                    "model_name": "sentiment-analyzer",
                    "model_version": "2.0.0",
                    "traffic_percentage": 50
                }
            ],
            "primary_metric": "accuracy",
            "minimum_sample_size": 1000,
            "confidence_level": 0.95
        }
    }}


class ExperimentUpdate(BaseModel):
    """Schema for updating an experiment."""
    description: Optional[str] = None
    status: Optional[ExperimentStatus] = None
    duration_days: Optional[int] = Field(None, ge=1)

    model_config = {"json_schema_extra": {
        "example": {
            "description": "Updated description",
            "status": "paused"
        }
    }}


class VariantInfo(BaseModel):
    """Variant information."""
    id: int
    name: str
    model_name: str
    model_version: str
    traffic_percentage: float
    is_control: bool
    is_active: bool
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class ExperimentInfo(BaseModel):
    """Experiment information."""
    id: int
    name: str
    description: Optional[str]
    status: str
    primary_metric: str
    assignment_strategy: str
    minimum_sample_size: int
    confidence_level: float
    minimum_improvement: float
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    duration_days: Optional[int]
    winner: Optional[str]
    winner_confidence: Optional[float]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MetricRecord(BaseModel):
    """Schema for recording a metric."""
    experiment_name: str = Field(..., description="Experiment name")
    variant_name: str = Field(..., description="Variant name")
    metric_name: str = Field(..., description="Metric name")
    metric_value: float = Field(..., description="Metric value")
    metric_type: Optional[str] = Field(None, description="Metric type")
    user_id: Optional[str] = Field(None, description="User ID")
    prediction_id: Optional[str] = Field(None, description="Prediction ID")

    model_config = {"json_schema_extra": {
        "example": {
            "experiment_name": "model-v2-test",
            "variant_name": "variant_a",
            "metric_name": "accuracy",
            "metric_value": 0.95,
            "user_id": "user123"
        }
    }}


class AssignmentResponse(BaseModel):
    """Response for variant assignment."""
    experiment_name: str
    variant_name: str
    model_name: str
    model_version: str
    is_control: bool
    assigned_at: datetime

    model_config = {"json_schema_extra": {
        "example": {
            "experiment_name": "model-v2-test",
            "variant_name": "variant_a",
            "model_name": "sentiment-analyzer",
            "model_version": "2.0.0",
            "is_control": False,
            "assigned_at": "2025-12-27T12:00:00Z"
        }
    }}


class VariantMetrics(BaseModel):
    """Metrics for a variant."""
    variant_name: str
    sample_size: int
    mean: float
    std_dev: float
    confidence_interval: tuple[float, float]

    model_config = {"json_schema_extra": {
        "example": {
            "variant_name": "control",
            "sample_size": 1500,
            "mean": 0.92,
            "std_dev": 0.05,
            "confidence_interval": [0.91, 0.93]
        }
    }}


class ExperimentResults(BaseModel):
    """Experiment results."""
    experiment_id: int
    experiment_name: str
    status: str
    primary_metric: str
    variants: List[VariantMetrics]
    winner: Optional[str]
    winner_confidence: Optional[float]
    p_value: Optional[float]
    is_significant: bool
    has_sufficient_sample: bool
    recommendation: str

    model_config = {"json_schema_extra": {
        "example": {
            "experiment_id": 1,
            "experiment_name": "model-v2-test",
            "status": "running",
            "primary_metric": "accuracy",
            "variants": [
                {
                    "variant_name": "control",
                    "sample_size": 1500,
                    "mean": 0.92,
                    "std_dev": 0.05,
                    "confidence_interval": [0.91, 0.93]
                },
                {
                    "variant_name": "variant_a",
                    "sample_size": 1480,
                    "mean": 0.95,
                    "std_dev": 0.04,
                    "confidence_interval": [0.94, 0.96]
                }
            ],
            "winner": "variant_a",
            "winner_confidence": 0.98,
            "p_value": 0.001,
            "is_significant": True,
            "has_sufficient_sample": True,
            "recommendation": "Rollout variant_a to 100%"
        }
    }}
