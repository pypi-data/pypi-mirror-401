"""
Model Loader - Runtime model loading and serving.

This module provides in-memory model management for serving predictions.
For model metadata and versioning, see neuralforge.ml.registry.
"""

from typing import Dict, List, Optional, Type, Any
from datetime import datetime
from pydantic import BaseModel, Field
import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


# ============================================================================
# Data Models
# ============================================================================

class ModelMetadata(BaseModel):
    """Metadata for a registered model."""

    name: str = Field(..., description="Model name")
    version: str = Field(..., description="Semantic version (e.g., 1.0.0)")
    description: str = Field(default="", description="Model description")
    framework: str = Field(..., description="ML framework (pytorch, tensorflow, etc.)")
    task_type: str = Field(..., description="Task type (classification, regression, etc.)")

    # Resource requirements
    model_size_mb: float = Field(..., description="Model size in MB")
    gpu_required: bool = Field(default=False, description="Requires GPU")
    min_memory_mb: int = Field(default=512, description="Minimum memory required")
    max_batch_size: int = Field(default=1, description="Maximum batch size")

    # Performance metrics
    avg_latency_ms: Optional[float] = Field(None, description="Average latency")
    throughput_rps: Optional[float] = Field(None, description="Throughput (req/sec)")

    # Provenance
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(..., description="Creator email/username")
    training_dataset: Optional[str] = Field(None, description="Training dataset name")

    # Deployment
    status: str = Field(default="development", description="Model status")
    artifact_path: str = Field(..., description="Path to model artifacts")

    # Additional metadata
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Model metrics")

    input_schema: Optional[Type] = Field(None, description="Input Pydantic model")
    output_schema: Optional[Type] = Field(None, description="Output Pydantic model")

    model_config = {"arbitrary_types_allowed": True}


class LoadedModel:
    """Wrapper for a loaded model instance."""

    def __init__(
        self,
        name: str,
        version: str,
        model_instance: Any,
        metadata: ModelMetadata
    ):
        self.name = name
        self.version = version
        self.model_instance = model_instance
        self.metadata = metadata
        self.load_time = datetime.utcnow()
        self.last_used = datetime.utcnow()
        self.prediction_count = 0

    async def predict(self, inputs: List[Any]) -> List[Any]:
        """Run prediction on inputs."""
        self.last_used = datetime.utcnow()
        self.prediction_count += 1

        return await self.model_instance.predict(inputs)

    def get_memory_usage_mb(self) -> float:
        """Get model memory usage."""
        return self.metadata.model_size_mb

    def __repr__(self) -> str:
        return f"<LoadedModel(name='{self.name}', version='{self.version}')>"


# ============================================================================
# Model Registry
# ============================================================================

class ModelLoader:
    """
    Runtime model loader and manager.
    
    Handles model registration, versioning, loading, and lifecycle management.
    This is for IN-MEMORY model serving. For persistent model metadata,
    use neuralforge.ml.registry.ModelRegistry instead.
    
    Example:
        >>> loader = app.models
        >>> 
        >>> @loader.register(
        >>>     metadata=ModelMetadata(
        >>>         name="classifier",
        >>>         version="1.0.0",
        >>>         framework="pytorch",
        >>>         ...
        >>>     )
        >>> )
        >>> class MyModel(PyTorchModel):
        >>>     def load(self):
        >>>         ...
        >>>     
        >>>     async def predict(self, inputs):
        >>>         ...
    """

    def __init__(self, app: "NeuralForge"):
        self.app = app

        # Registry storage
        self._models: Dict[str, Dict[str, Type]] = {}  # {name: {version: class}}
        self._metadata: Dict[str, Dict[str, ModelMetadata]] = {}  # {name: {version: metadata}}
        self._loaded: Dict[str, LoadedModel] = {}  # {name:version: LoadedModel}

        # Locks for thread-safety
        self._load_locks: Dict[str, asyncio.Lock] = {}

        logger.info("Initialized ModelLoader")

    # ========================================================================
    # Registration
    # ========================================================================

    def register(
        self,
        model_class: Type = None,
        metadata: ModelMetadata = None,
        **kwargs
    ):
        """
        Register a model class.
        
        Can be used as a decorator or called directly.
        
        Example:
            >>> @registry.register(metadata=ModelMetadata(...))
            >>> class MyModel(PyTorchModel):
            >>>     pass
            >>> 
            >>> # Or directly:
            >>> registry.register(MyModel, metadata=ModelMetadata(...))
        """
        def decorator(cls: Type) -> Type:
            if metadata is None:
                raise ValueError("metadata is required for model registration")

            # Store model class and metadata
            if metadata.name not in self._models:
                self._models[metadata.name] = {}
                self._metadata[metadata.name] = {}

            self._models[metadata.name][metadata.version] = cls
            self._metadata[metadata.name][metadata.version] = metadata

            logger.info(
                f"Registered model: {metadata.name} v{metadata.version} "
                f"({metadata.framework})"
            )

            return cls

        # Allow usage as @register or @register()
        if model_class is None:
            return decorator
        else:
            return decorator(model_class)

    # ========================================================================
    # Model Loading
    # ========================================================================

    async def load(
        self,
        name: str,
        version: str = "latest",
        force_reload: bool = False
    ) -> LoadedModel:
        """
        Load a model by name and version.
        
        Args:
            name: Model name
            version: Model version or "latest"
            force_reload: Force reload even if already loaded
        
        Returns:
            LoadedModel instance
        
        Example:
            >>> model = await registry.load("classifier", version="1.0.0")
            >>> results = await model.predict(inputs)
        """
        # Resolve version
        if version == "latest":
            version = self._get_latest_version(name)

        model_key = f"{name}:{version}"

        # Check if already loaded
        if model_key in self._loaded and not force_reload:
            logger.debug(f"Using cached model: {model_key}")
            return self._loaded[model_key]

        # Get or create lock for this model
        if model_key not in self._load_locks:
            self._load_locks[model_key] = asyncio.Lock()

        # Load with lock to prevent concurrent loading
        async with self._load_locks[model_key]:
            # Double-check after acquiring lock
            if model_key in self._loaded and not force_reload:
                return self._loaded[model_key]

            logger.info(f"Loading model: {model_key}")

            # Get model class and metadata
            if name not in self._models:
                raise ValueError(f"Model not found: {name}")

            if version not in self._models[name]:
                raise ValueError(
                    f"Version not found: {name}:{version}. "
                    f"Available: {list(self._models[name].keys())}"
                )

            model_class = self._models[name][version]
            metadata = self._metadata[name][version]

            # Instantiate model
            model_instance = model_class(metadata)

            # Load model weights/artifacts
            await asyncio.get_event_loop().run_in_executor(
                None,
                model_instance.load
            )

            # Wrap in LoadedModel
            loaded_model = LoadedModel(
                name=name,
                version=version,
                model_instance=model_instance,
                metadata=metadata
            )

            # Cache
            self._loaded[model_key] = loaded_model

            logger.info(f"✓ Model loaded: {model_key}")

            return loaded_model

    async def unload(self, name: str, version: str = "latest"):
        """
        Unload a model from memory.
        
        Args:
            name: Model name
            version: Model version
        """
        if version == "latest":
            version = self._get_latest_version(name)

        model_key = f"{name}:{version}"

        if model_key in self._loaded:
            del self._loaded[model_key]
            logger.info(f"Unloaded model: {model_key}")

    async def unload_all(self):
        """Unload all models from memory."""
        model_keys = list(self._loaded.keys())
        for model_key in model_keys:
            del self._loaded[model_key]

        logger.info(f"Unloaded {len(model_keys)} models")

    # ========================================================================
    # Model Discovery
    # ========================================================================

    def list_models(self) -> List[str]:
        """Get list of all registered model names."""
        return list(self._models.keys())

    def list_versions(self, name: str) -> List[str]:
        """Get list of all versions for a model."""
        if name not in self._models:
            return []
        return list(self._models[name].keys())

    def get_metadata(self, name: str, version: str = "latest") -> ModelMetadata:
        """Get metadata for a model."""
        if version == "latest":
            version = self._get_latest_version(name)

        if name not in self._metadata:
            raise ValueError(f"Model not found: {name}")

        if version not in self._metadata[name]:
            raise ValueError(f"Version not found: {name}:{version}")

        return self._metadata[name][version]

    def is_loaded(self, name: str, version: str = "latest") -> bool:
        """Check if a model is currently loaded."""
        if version == "latest":
            version = self._get_latest_version(name)

        model_key = f"{name}:{version}"
        return model_key in self._loaded

    def list_loaded(self) -> List[str]:
        """Get list of currently loaded models."""
        return list(self._loaded.keys())

    # ========================================================================
    # Utility Methods
    # ========================================================================

    def _get_latest_version(self, name: str) -> str:
        """Get the latest version of a model."""
        if name not in self._models:
            raise ValueError(f"Model not found: {name}")

        versions = list(self._models[name].keys())

        if not versions:
            raise ValueError(f"No versions found for model: {name}")

        # Simple string sort (works for semantic versions like 1.0.0, 1.1.0, etc.)
        # For production, use proper semantic version comparison
        return sorted(versions)[-1]

    async def get_total_memory_usage(self) -> float:
        """Get total memory usage of all loaded models in MB."""
        return sum(
            model.get_memory_usage_mb()
            for model in self._loaded.values()
        )

    async def cleanup(self):
        """Cleanup resources."""
        await self.unload_all()


# ============================================================================
# Base Model Classes
# ============================================================================

class MLBaseModel:
    """
    Base class for all model implementations.
    
    Subclass this to create your own model wrapper.
    """

    def __init__(self, metadata: ModelMetadata):
        self.metadata = metadata
        self.name = metadata.name
        self.version = metadata.version
        self.artifact_path = Path(metadata.artifact_path)

    def load(self):
        """
        Load model weights and initialize.
        
        This method should be overridden by subclasses.
        """
        raise NotImplementedError

    async def predict(self, inputs: List[Any]) -> List[Any]:
        """
        Run inference on inputs.
        
        This method should be overridden by subclasses.
        
        Args:
            inputs: List of input objects
        
        Returns:
            List of output objects
        """
        raise NotImplementedError

    def preprocess(self, inputs: List[Any]) -> Any:
        """Preprocess inputs before inference."""
        return inputs

    def postprocess(self, outputs: Any, inputs: List[Any]) -> List[Any]:
        """Postprocess model outputs."""
        return outputs

    def validate(self) -> bool:
        """Validate model after loading."""
        return True


class PyTorchModel(MLBaseModel):
    """Base class for PyTorch models."""

    def __init__(self, metadata: ModelMetadata):
        super().__init__(metadata)
        self.model = None
        self.device = None

    def load(self):
        """Load PyTorch model - override in subclass."""
        import torch

        # Set device
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() and self.metadata.gpu_required
            else "cpu"
        )

        logger.info(f"PyTorch device: {self.device}")


class TensorFlowModel(MLBaseModel):
    """Base class for TensorFlow models."""

    def __init__(self, metadata: ModelMetadata):
        super().__init__(metadata)
        self.model = None

    def load(self):
        """Load TensorFlow model - override in subclass."""
        import tensorflow as tf

        # Configure GPU
        if self.metadata.gpu_required:
            gpus = tf.config.list_physical_devices('GPU')
            if gpus:
                tf.config.experimental.set_memory_growth(gpus[0], True)


class ONNXModel(MLBaseModel):
    """Base class for ONNX models."""

    def __init__(self, metadata: ModelMetadata):
        super().__init__(metadata)
        self.session = None

    def load(self):
        """Load ONNX model - override in subclass."""
        # Users should import onnxruntime in their subclass

        # Configure providers
        providers = []
        if self.metadata.gpu_required:
            providers.append('CUDAExecutionProvider')
        providers.append('CPUExecutionProvider')

        logger.info(f"ONNX providers: {providers}")
