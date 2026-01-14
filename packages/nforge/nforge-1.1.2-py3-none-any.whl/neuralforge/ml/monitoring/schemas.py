"""
Pydantic schemas for prediction monitoring.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum


class PredictionStatus(str, Enum):
    """Prediction status enum."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"


class AlertSeverity(str, Enum):
    """Alert severity enum."""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class AlertStatus(str, Enum):
    """Alert status enum."""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class PredictionLog(BaseModel):
    """Schema for logging a prediction."""
    model_name: str = Field(..., description="Model name")
    model_version: str = Field(..., description="Model version")
    request_id: Optional[str] = Field(None, description="Unique request ID")
    user_id: Optional[str] = Field(None, description="User ID")
    input_data: Optional[Dict[str, Any]] = Field(None, description="Input data")
    output_data: Optional[Dict[str, Any]] = Field(None, description="Output data")
    prediction_class: Optional[str] = Field(None, description="Predicted class/label")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Confidence score")
    latency_ms: float = Field(..., ge=0, description="Total latency in milliseconds")
    preprocessing_ms: Optional[float] = Field(None, ge=0)
    inference_ms: Optional[float] = Field(None, ge=0)
    postprocessing_ms: Optional[float] = Field(None, ge=0)
    status: PredictionStatus = Field(default=PredictionStatus.SUCCESS)
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    environment: Optional[str] = Field(None, description="Environment (production, staging)")
    api_version: Optional[str] = None

    model_config = {"json_schema_extra": {
        "example": {
            "model_name": "sentiment-analyzer",
            "model_version": "1.0.0",
            "request_id": "req_123",
            "user_id": "user_456",
            "input_data": {"text": "This is great!"},
            "output_data": {"sentiment": "positive", "score": 0.95},
            "prediction_class": "positive",
            "confidence": 0.95,
            "latency_ms": 45.2,
            "status": "success"
        }
    }}


class PredictionInfo(BaseModel):
    """Prediction information."""
    id: int
    model_name: str
    model_version: str
    request_id: Optional[str]
    user_id: Optional[str]
    prediction_class: Optional[str]
    confidence: Optional[float]
    latency_ms: float
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LatencyStats(BaseModel):
    """Latency statistics."""
    avg: float
    p50: float
    p95: float
    p99: float
    max: float
    sample_size: int

    model_config = {"json_schema_extra": {
        "example": {
            "avg": 45.2,
            "p50": 42.0,
            "p95": 78.5,
            "p99": 95.3,
            "max": 120.5,
            "sample_size": 1500
        }
    }}


class ThroughputStats(BaseModel):
    """Throughput statistics."""
    requests_per_second: float
    total_requests: int
    time_range: str

    model_config = {"json_schema_extra": {
        "example": {
            "requests_per_second": 125.5,
            "total_requests": 7530,
            "time_range": "1h"
        }
    }}


class ErrorStats(BaseModel):
    """Error statistics."""
    error_rate: float
    total_errors: int
    total_requests: int
    error_types: Dict[str, int]

    model_config = {"json_schema_extra": {
        "example": {
            "error_rate": 0.025,
            "total_errors": 15,
            "total_requests": 600,
            "error_types": {
                "timeout": 8,
                "validation_error": 5,
                "model_error": 2
            }
        }
    }}


class ConfidenceDistribution(BaseModel):
    """Confidence distribution statistics."""
    avg_confidence: float
    min_confidence: float
    max_confidence: float
    low_confidence_count: int  # < 0.5
    medium_confidence_count: int  # 0.5-0.8
    high_confidence_count: int  # > 0.8

    model_config = {"json_schema_extra": {
        "example": {
            "avg_confidence": 0.87,
            "min_confidence": 0.52,
            "max_confidence": 0.99,
            "low_confidence_count": 12,
            "medium_confidence_count": 45,
            "high_confidence_count": 543
        }
    }}


class MetricsSummary(BaseModel):
    """Overall metrics summary."""
    model_name: str
    model_version: Optional[str]
    time_range: str
    total_predictions: int
    successful_predictions: int
    failed_predictions: int
    latency: LatencyStats
    throughput: ThroughputStats
    errors: ErrorStats
    confidence: Optional[ConfidenceDistribution]

    model_config = {"json_schema_extra": {
        "example": {
            "model_name": "sentiment-analyzer",
            "model_version": "1.0.0",
            "time_range": "1h",
            "total_predictions": 1500,
            "successful_predictions": 1485,
            "failed_predictions": 15
        }
    }}


class AlertRuleCreate(BaseModel):
    """Schema for creating an alert rule."""
    name: str = Field(..., description="Rule name")
    description: Optional[str] = None
    model_name: Optional[str] = Field(None, description="Model name (null for all models)")
    model_version: Optional[str] = None
    metric_name: str = Field(..., description="Metric to monitor (latency, error_rate, confidence)")
    operator: str = Field(..., description="Comparison operator (gt, lt, eq)")
    threshold: float = Field(..., description="Threshold value")
    window_minutes: int = Field(default=5, ge=1, description="Time window in minutes")
    severity: AlertSeverity = Field(..., description="Alert severity")
    channels: List[str] = Field(default=["email"], description="Notification channels")

    model_config = {"json_schema_extra": {
        "example": {
            "name": "high-latency-alert",
            "description": "Alert when p95 latency exceeds 100ms",
            "model_name": "sentiment-analyzer",
            "metric_name": "p95_latency",
            "operator": "gt",
            "threshold": 100.0,
            "window_minutes": 5,
            "severity": "warning",
            "channels": ["email", "slack"]
        }
    }}


class AlertRuleInfo(BaseModel):
    """Alert rule information."""
    id: int
    name: str
    description: Optional[str]
    model_name: Optional[str]
    model_version: Optional[str]
    metric_name: str
    operator: str
    threshold: float
    window_minutes: int
    severity: str
    channels: List[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertInfo(BaseModel):
    """Alert information."""
    id: int
    alert_type: str
    severity: str
    model_name: Optional[str]
    model_version: Optional[str]
    message: str
    threshold_value: Optional[float]
    actual_value: Optional[float]
    status: str
    triggered_at: datetime
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]

    model_config = {"from_attributes": True}
