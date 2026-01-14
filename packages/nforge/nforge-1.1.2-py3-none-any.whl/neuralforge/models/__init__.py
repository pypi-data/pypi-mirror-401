"""
Serving module - Runtime model loading and inference.

This module provides runtime model management, loading, and serving capabilities.
For model metadata and versioning, see neuralforge.ml.registry.

DEPRECATED: The old 'neuralforge.models' module has been renamed to 'neuralforge.serving'
for clarity. Please update your imports.
"""

import warnings

# Deprecation warning for old imports
warnings.warn(
    "neuralforge.models is deprecated and has been renamed to neuralforge.serving. "
    "Please update your imports: 'from neuralforge.serving import ...'",
    DeprecationWarning,
    stacklevel=2
)

# Re-export everything from serving for backward compatibility
from neuralforge.serving.loader import *

__all__ = [
    'ModelLoader',
    'LoadedModel',
    'ModelMetadata',
    'BaseModel',
    'PyTorchModel',
    'TensorFlowModel',
    'ONNXModel',
]
