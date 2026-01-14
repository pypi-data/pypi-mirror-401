"""
Pydantic schemas for model optimization.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class OptimizationType(str, Enum):
    """Optimization type enum."""
    QUANTIZATION = "quantization"
    PRUNING = "pruning"
    ONNX = "onnx"


class QuantizationDtype(str, Enum):
    """Quantization data type."""
    INT8 = "int8"
    FP16 = "fp16"


class DeviceType(str, Enum):
    """Device type for benchmarking."""
    CPU = "cpu"
    CUDA = "cuda"
    MPS = "mps"


# ========================================================================
# Quantization Schemas
# ========================================================================

class QuantizationConfig(BaseModel):
    """Configuration for quantization."""
    dtype: QuantizationDtype = Field(default=QuantizationDtype.INT8)
    dynamic: bool = Field(default=True, description="Use dynamic quantization")

    model_config = {"json_schema_extra": {
        "example": {
            "dtype": "int8",
            "dynamic": True
        }
    }}


class QuantizationResult(BaseModel):
    """Result of quantization."""
    optimized_model_id: int
    original_size_mb: float
    quantized_size_mb: float
    size_reduction: float
    speedup_factor: Optional[float] = None

    model_config = {"json_schema_extra": {
        "example": {
            "optimized_model_id": 1,
            "original_size_mb": 100.5,
            "quantized_size_mb": 25.2,
            "size_reduction": 0.75,
            "speedup_factor": 2.3
        }
    }}


# ========================================================================
# Pruning Schemas
# ========================================================================

class PruningConfig(BaseModel):
    """Configuration for pruning."""
    amount: float = Field(..., ge=0.0, le=1.0, description="Fraction of weights to prune")
    structured: bool = Field(default=False, description="Use structured pruning")
    iterative: bool = Field(default=False, description="Use iterative pruning")

    model_config = {"json_schema_extra": {
        "example": {
            "amount": 0.3,
            "structured": False,
            "iterative": False
        }
    }}


class PruningResult(BaseModel):
    """Result of pruning."""
    optimized_model_id: int
    sparsity: float
    size_reduction: float
    speedup_factor: Optional[float] = None

    model_config = {"json_schema_extra": {
        "example": {
            "optimized_model_id": 2,
            "sparsity": 0.3,
            "size_reduction": 0.25,
            "speedup_factor": 1.5
        }
    }}


# ========================================================================
# ONNX Export Schemas
# ========================================================================

class ONNXExportConfig(BaseModel):
    """Configuration for ONNX export."""
    opset_version: int = Field(default=13, ge=7, le=18)
    optimize: bool = Field(default=True, description="Optimize ONNX model")

    model_config = {"json_schema_extra": {
        "example": {
            "opset_version": 13,
            "optimize": True
        }
    }}


class ONNXExportResult(BaseModel):
    """Result of ONNX export."""
    optimized_model_id: int
    onnx_path: str
    is_valid: bool

    model_config = {"json_schema_extra": {
        "example": {
            "optimized_model_id": 3,
            "onnx_path": "/models/model.onnx",
            "is_valid": True
        }
    }}


# ========================================================================
# Benchmark Schemas
# ========================================================================

class BenchmarkConfig(BaseModel):
    """Configuration for benchmarking."""
    batch_size: int = Field(default=1, ge=1)
    num_iterations: int = Field(default=100, ge=10)
    device: DeviceType = Field(default=DeviceType.CPU)
    warmup_iterations: int = Field(default=10, ge=0)

    model_config = {"json_schema_extra": {
        "example": {
            "batch_size": 1,
            "num_iterations": 100,
            "device": "cpu",
            "warmup_iterations": 10
        }
    }}


class BenchmarkResultInfo(BaseModel):
    """Benchmark result information."""
    id: int
    model_name: str
    model_version: Optional[str]
    optimization_type: Optional[str]
    batch_size: int
    num_iterations: int
    device: Optional[str]
    avg_latency_ms: float
    p50_latency_ms: Optional[float]
    p95_latency_ms: Optional[float]
    p99_latency_ms: Optional[float]
    throughput_qps: Optional[float]
    peak_memory_mb: Optional[float]
    avg_memory_mb: Optional[float]
    benchmark_date: datetime

    model_config = {"from_attributes": True}


class LatencyStats(BaseModel):
    """Latency statistics."""
    avg_ms: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    min_ms: float
    max_ms: float


class MemoryStats(BaseModel):
    """Memory statistics."""
    peak_mb: float
    avg_mb: float


class PerformanceComparison(BaseModel):
    """Performance comparison between models."""
    baseline_latency: LatencyStats
    optimized_latency: LatencyStats
    speedup_factor: float
    baseline_memory: Optional[MemoryStats] = None
    optimized_memory: Optional[MemoryStats] = None
    memory_reduction: Optional[float] = None


# ========================================================================
# Optimized Model Schemas
# ========================================================================

class OptimizedModelInfo(BaseModel):
    """Optimized model information."""
    id: int
    source_model_name: str
    source_model_version: str
    optimized_name: str
    optimization_type: str
    config: Dict[str, Any]
    model_path: Optional[str]
    model_size_bytes: Optional[int]
    baseline_latency_ms: Optional[float]
    optimized_latency_ms: Optional[float]
    speedup_factor: Optional[float]
    baseline_memory_mb: Optional[float]
    optimized_memory_mb: Optional[float]
    memory_reduction: Optional[float]
    baseline_accuracy: Optional[float]
    optimized_accuracy: Optional[float]
    accuracy_loss: Optional[float]
    created_at: datetime

    model_config = {"from_attributes": True}


class OptimizationRequest(BaseModel):
    """Request for model optimization."""
    source_model_name: str
    source_model_version: str
    optimization_type: OptimizationType
    config: Dict[str, Any]

    model_config = {"json_schema_extra": {
        "example": {
            "source_model_name": "sentiment-model",
            "source_model_version": "1.0.0",
            "optimization_type": "quantization",
            "config": {"dtype": "int8", "dynamic": True}
        }
    }}
