"""
Pydantic schemas for drift detection.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum


class DistributionType(str, Enum):
    """Distribution type enum."""
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"


class DriftSeverity(str, Enum):
    """Drift severity enum."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BaselineCreate(BaseModel):
    """Schema for creating a baseline."""
    model_name: str = Field(..., description="Model name")
    model_version: str = Field(..., description="Model version")
    baseline_name: str = Field(..., description="Baseline name")
    feature_name: str = Field(..., description="Feature name")
    distribution_type: DistributionType
    distribution_data: Dict[str, Any] = Field(..., description="Distribution data (histogram/categories)")
    mean: Optional[float] = None
    std_dev: Optional[float] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    percentiles: Optional[Dict[str, float]] = None
    categories: Optional[Dict[str, int]] = None
    sample_size: int = Field(..., ge=1)

    model_config = {"json_schema_extra": {
        "example": {
            "model_name": "sentiment-analyzer",
            "model_version": "1.0.0",
            "baseline_name": "production_v1",
            "feature_name": "text_length",
            "distribution_type": "numerical",
            "distribution_data": {"bins": [0, 10, 20, 30], "counts": [100, 200, 150]},
            "mean": 15.5,
            "std_dev": 5.2,
            "sample_size": 1000
        }
    }}


class BaselineInfo(BaseModel):
    """Baseline information."""
    id: int
    model_name: str
    model_version: str
    baseline_name: str
    feature_name: str
    distribution_type: str
    sample_size: int
    created_at: datetime

    model_config = {"from_attributes": True}


class FeatureDriftResult(BaseModel):
    """Drift detection result for a single feature."""
    feature_name: str
    ks_statistic: Optional[float] = None
    ks_p_value: Optional[float] = None
    psi_score: Optional[float] = None
    js_divergence: Optional[float] = None
    drift_detected: bool
    drift_severity: DriftSeverity
    sample_size: int

    model_config = {"json_schema_extra": {
        "example": {
            "feature_name": "text_length",
            "ks_statistic": 0.15,
            "ks_p_value": 0.001,
            "psi_score": 0.25,
            "js_divergence": 0.12,
            "drift_detected": True,
            "drift_severity": "high",
            "sample_size": 500
        }
    }}


class DriftDetectionResult(BaseModel):
    """Overall drift detection result."""
    model_name: str
    model_version: str
    baseline_name: str
    drift_detected: bool
    drift_severity: DriftSeverity
    overall_psi: float
    feature_results: List[FeatureDriftResult]
    sample_size: int
    detection_window: Optional[str] = None
    detected_at: datetime

    model_config = {"json_schema_extra": {
        "example": {
            "model_name": "sentiment-analyzer",
            "model_version": "1.0.0",
            "baseline_name": "production_v1",
            "drift_detected": True,
            "drift_severity": "medium",
            "overall_psi": 0.15,
            "sample_size": 500,
            "detection_window": "24h"
        }
    }}


class DriftDetectionInfo(BaseModel):
    """Drift detection information."""
    id: int
    model_name: str
    model_version: str
    baseline_name: str
    feature_name: Optional[str]
    ks_statistic: Optional[float]
    ks_p_value: Optional[float]
    psi_score: Optional[float]
    js_divergence: Optional[float]
    drift_detected: bool
    drift_severity: Optional[str]
    sample_size: int
    detection_window: Optional[str]
    detected_at: datetime

    model_config = {"from_attributes": True}


class DriftDetectionRequest(BaseModel):
    """Request for drift detection."""
    model_name: str
    baseline_name: str
    current_data: Dict[str, List[Any]] = Field(..., description="Feature name to values mapping")
    features: Optional[List[str]] = Field(None, description="Specific features to check (None = all)")
    detection_window: Optional[str] = Field(None, description="Time window (e.g., '24h')")

    model_config = {"json_schema_extra": {
        "example": {
            "model_name": "sentiment-analyzer",
            "baseline_name": "production_v1",
            "current_data": {
                "text_length": [10, 15, 20, 25],
                "word_count": [5, 7, 9, 11]
            },
            "features": ["text_length"],
            "detection_window": "24h"
        }
    }}


class DriftSummary(BaseModel):
    """Drift summary for a model."""
    model_name: str
    model_version: Optional[str]
    total_detections: int
    drift_detected_count: int
    drift_rate: float
    severity_breakdown: Dict[str, int]
    recent_detections: List[DriftDetectionInfo]

    model_config = {"json_schema_extra": {
        "example": {
            "model_name": "sentiment-analyzer",
            "total_detections": 100,
            "drift_detected_count": 25,
            "drift_rate": 0.25,
            "severity_breakdown": {
                "low": 10,
                "medium": 10,
                "high": 5
            }
        }
    }}
