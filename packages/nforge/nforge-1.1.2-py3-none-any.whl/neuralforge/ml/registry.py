"""
Model Registry for NeuralForge.

Centralized management of ML models with versioning support.
"""

from typing import Optional, List, Dict, Any, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
import logging

from neuralforge.ml.metadata import ModelMetadata
from neuralforge.ml.exceptions import (
    ModelNotFoundError,
    ModelAlreadyExistsError,
)
from neuralforge.db.models.ml_model import MLModel

logger = logging.getLogger(__name__)


class ModelRegistry:
    """
    Centralized registry for ML models.
    
    Features:
    - Model registration with metadata
    - Semantic versioning support
    - Model discovery and search
    - Lifecycle management (load, unload, delete)
    - Version management (latest, specific version)
    
    Example:
        ```python
        registry = ModelRegistry(db_session)
        
        # Register a model
        metadata = ModelMetadata(
            name="sentiment-analyzer",
            version="1.0.0",
            framework="transformers",
            accuracy=0.92
        )
        await registry.register(MyModel, metadata)
        
        # Load a model
        model = await registry.load("sentiment-analyzer", "1.0.0")
        
        # List all models
        models = await registry.list_models()
        ```
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the model registry.
        
        Args:
            db_session: Async database session
        """
        self.db = db_session
        self._loaded_models: Dict[str, Any] = {}

    async def register(
        self,
        model_class: Optional[Type] = None,
        metadata: ModelMetadata = None,
    ) -> MLModel:
        """
        Register a new model in the registry.
        
        Args:
            model_class: Model class to register (optional for now)
            metadata: Model metadata
        
        Returns:
            Registered model database record
        
        Raises:
            ModelAlreadyExistsError: If model with same name/version exists
        
        Example:
            ```python
            metadata = ModelMetadata(
                name="classifier",
                version="1.0.0",
                framework="pytorch",
                accuracy=0.95
            )
            model = await registry.register(ClassifierModel, metadata)
            ```
        """
        # Check if model already exists
        existing = await self._get_model_record(metadata.name, metadata.version)
        if existing:
            raise ModelAlreadyExistsError(
                f"Model '{metadata.name}' version '{metadata.version}' already exists"
            )

        # Create model record
        model_record = MLModel(
            name=metadata.name,
            version=metadata.version,
            framework=metadata.framework,
            task_type=metadata.task_type,
            accuracy=metadata.accuracy,
            f1_score=metadata.f1_score,
            precision_score=metadata.precision_score,
            recall=metadata.recall,
            custom_metrics=metadata.custom_metrics,
            model_size_mb=metadata.model_size_mb,
            input_schema=metadata.input_schema,
            output_schema=metadata.output_schema,
            is_active=metadata.is_active,
            is_deployed=metadata.is_deployed,
            deployment_url=metadata.deployment_url,
            description=metadata.description,
            tags=metadata.tags,
            created_by=metadata.created_by,
            artifact_path=metadata.artifact_path,
        )

        self.db.add(model_record)
        await self.db.commit()
        await self.db.refresh(model_record)

        logger.info(
            f"Registered model: {metadata.name} v{metadata.version} "
            f"(framework: {metadata.framework})"
        )

        return model_record

    async def load(
        self,
        name: str,
        version: Optional[str] = "latest"
    ) -> MLModel:
        """
        Load a model by name and version.
        
        Args:
            name: Model name
            version: Model version or "latest" (default: "latest")
        
        Returns:
            Model database record
        
        Raises:
            ModelNotFoundError: If model not found
        
        Example:
            ```python
            # Load specific version
            model = await registry.load("classifier", "1.0.0")
            
            # Load latest version
            model = await registry.load("classifier")
            ```
        """
        # Check cache
        cache_key = f"{name}:{version}"
        if cache_key in self._loaded_models:
            logger.debug(f"Returning cached model: {cache_key}")
            return self._loaded_models[cache_key]

        # Get model record
        if version == "latest":
            model_record = await self._get_latest_model(name)
        else:
            model_record = await self._get_model_record(name, version)

        if not model_record:
            raise ModelNotFoundError(
                f"Model '{name}' version '{version}' not found in registry"
            )

        # Cache the model
        self._loaded_models[cache_key] = model_record

        logger.info(f"Loaded model: {name} v{model_record.version}")

        return model_record

    async def list_models(
        self,
        name: Optional[str] = None,
        framework: Optional[str] = None,
        task_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_deployed: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[MLModel]:
        """
        List models with optional filters.
        
        Args:
            name: Filter by model name
            framework: Filter by framework
            task_type: Filter by task type
            is_active: Filter by active status
            is_deployed: Filter by deployment status
            limit: Maximum number of results (default: 100)
            offset: Number of results to skip (default: 0)
        
        Returns:
            List of model records
        
        Example:
            ```python
            # List all models
            models = await registry.list_models()
            
            # List PyTorch models
            models = await registry.list_models(framework="pytorch")
            
            # List deployed models
            models = await registry.list_models(is_deployed=True)
            ```
        """
        query = select(MLModel)

        # Apply filters
        if name:
            query = query.where(MLModel.name == name)
        if framework:
            query = query.where(MLModel.framework == framework)
        if task_type:
            query = query.where(MLModel.task_type == task_type)
        if is_active is not None:
            query = query.where(MLModel.is_active == is_active)
        if is_deployed is not None:
            query = query.where(MLModel.is_deployed == is_deployed)

        # Order by creation date (newest first)
        query = query.order_by(desc(MLModel.created_at))

        # Apply pagination
        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        models = result.scalars().all()

        logger.debug(f"Listed {len(models)} models (filters: name={name}, framework={framework})")

        return list(models)

    async def update(
        self,
        name: str,
        version: str,
        **updates
    ) -> MLModel:
        """
        Update model metadata.
        
        Args:
            name: Model name
            version: Model version
            **updates: Fields to update
        
        Returns:
            Updated model record
        
        Raises:
            ModelNotFoundError: If model not found
        
        Example:
            ```python
            model = await registry.update(
                "classifier",
                "1.0.0",
                is_deployed=True,
                deployment_url="https://api.example.com/predict"
            )
            ```
        """
        model = await self._get_model_record(name, version)
        if not model:
            raise ModelNotFoundError(f"Model '{name}' version '{version}' not found")

        # Update fields
        for key, value in updates.items():
            if hasattr(model, key):
                setattr(model, key, value)

        await self.db.commit()
        await self.db.refresh(model)

        # Clear cache
        cache_key = f"{name}:{version}"
        self._loaded_models.pop(cache_key, None)

        logger.info(f"Updated model: {name} v{version}")

        return model

    async def delete(self, name: str, version: str) -> bool:
        """
        Delete a model from the registry.
        
        Args:
            name: Model name
            version: Model version
        
        Returns:
            True if deleted, False if not found
        
        Example:
            ```python
            deleted = await registry.delete("classifier", "1.0.0")
            ```
        """
        model = await self._get_model_record(name, version)
        if not model:
            return False

        await self.db.delete(model)
        await self.db.commit()

        # Remove from cache
        cache_key = f"{name}:{version}"
        self._loaded_models.pop(cache_key, None)

        logger.info(f"Deleted model: {name} v{version}")

        return True

    async def get_versions(self, name: str) -> List[str]:
        """
        Get all versions of a model.
        
        Args:
            name: Model name
        
        Returns:
            List of version strings, sorted by creation date (newest first)
        
        Example:
            ```python
            versions = await registry.get_versions("classifier")
            # Returns: ["2.0.0", "1.5.0", "1.0.0"]
            ```
        """
        query = select(MLModel.version).where(
            MLModel.name == name
        ).order_by(desc(MLModel.created_at))

        result = await self.db.execute(query)
        versions = result.scalars().all()

        return list(versions)

    async def _get_model_record(
        self,
        name: str,
        version: str
    ) -> Optional[MLModel]:
        """Get model record by name and version."""
        query = select(MLModel).where(
            and_(
                MLModel.name == name,
                MLModel.version == version
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _get_latest_model(self, name: str) -> Optional[MLModel]:
        """
        Get latest version of a model using semantic versioning.
        
        Orders by semantic version (major.minor.patch) rather than timestamp
        to ensure correct "latest" selection even when models are created rapidly.
        """
        query = select(MLModel).where(
            MLModel.name == name
        ).order_by(MLModel.created_at.desc())

        result = await self.db.execute(query)
        models = result.scalars().all()

        if not models:
            return None

        # Sort by semantic version
        def version_key(model):
            """Convert version string to tuple for comparison."""
            try:
                parts = model.version.split('.')
                return tuple(int(p) for p in parts)
            except (ValueError, AttributeError):
                return (0, 0, 0)

        # Get model with highest semantic version
        latest = max(models, key=version_key)
        return latest

    def clear_cache(self):
        """Clear the model cache."""
        self._loaded_models.clear()
        logger.debug("Cleared model cache")
