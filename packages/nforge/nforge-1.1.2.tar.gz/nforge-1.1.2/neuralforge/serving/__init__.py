"""
Serving module - Runtime model loading and inference.

Provides in-memory model management for serving predictions.
For persistent model metadata and versioning, see neuralforge.ml.registry.
"""

from neuralforge.serving.loader import (
    ModelLoader,
    LoadedModel,
    ModelMetadata,
    BaseModel,
    PyTorchModel,
    TensorFlowModel,
    ONNXModel,
)

__all__ = [
    'ModelLoader',
    'LoadedModel',
    'ModelMetadata',
    'BaseModel',
    'PyTorchModel',
    'TensorFlowModel',
    'ONNXModel',
]
