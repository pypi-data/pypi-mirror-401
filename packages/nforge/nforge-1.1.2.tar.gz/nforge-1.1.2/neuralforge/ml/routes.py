"""
REST API routes for Model Registry.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from neuralforge.ml.registry import ModelRegistry
from neuralforge.ml.metadata import ModelMetadata, ModelInfo
from neuralforge.ml.exceptions import ModelNotFoundError, ModelAlreadyExistsError
from neuralforge.dependencies.common import get_db_session

router = APIRouter(prefix="/api/models", tags=["Model Registry"])


@router.post("/", status_code=201, response_model=ModelInfo)
async def register_model(
    metadata: ModelMetadata,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Register a new model in the registry.
    
    Args:
        metadata: Model metadata
        db: Database session
    
    Returns:
        Registered model information
    
    Raises:
        409: Model already exists
    
    Example:
        ```json
        {
            "name": "sentiment-analyzer",
            "version": "1.0.0",
            "framework": "transformers",
            "task_type": "classification",
            "accuracy": 0.92,
            "f1_score": 0.89
        }
        ```
    """
    registry = ModelRegistry(db)

    try:
        model = await registry.register(None, metadata)
        return ModelInfo.model_validate(model)
    except ModelAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/", response_model=List[ModelInfo])
async def list_models(
    name: Optional[str] = Query(None, description="Filter by model name"),
    framework: Optional[str] = Query(None, description="Filter by framework"),
    task_type: Optional[str] = Query(None, description="Filter by task type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_deployed: Optional[bool] = Query(None, description="Filter by deployment status"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Results to skip"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    List models with optional filters.
    
    Args:
        name: Filter by model name
        framework: Filter by framework (pytorch, tensorflow, etc.)
        task_type: Filter by task type (classification, regression, etc.)
        is_active: Filter by active status
        is_deployed: Filter by deployment status
        limit: Maximum number of results
        offset: Number of results to skip
        db: Database session
    
    Returns:
        List of model information
    
    Example:
        GET /api/models?framework=pytorch&is_deployed=true
    """
    registry = ModelRegistry(db)

    models = await registry.list_models(
        name=name,
        framework=framework,
        task_type=task_type,
        is_active=is_active,
        is_deployed=is_deployed,
        limit=limit,
        offset=offset
    )

    return [ModelInfo.model_validate(m) for m in models]


@router.get("/{name}/{version}", response_model=ModelInfo)
async def get_model(
    name: str,
    version: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get specific model version.
    
    Args:
        name: Model name
        version: Model version or "latest"
        db: Database session
    
    Returns:
        Model information
    
    Raises:
        404: Model not found
    
    Example:
        GET /api/models/sentiment-analyzer/1.0.0
        GET /api/models/sentiment-analyzer/latest
    """
    registry = ModelRegistry(db)

    try:
        model = await registry.load(name, version)
        return ModelInfo.model_validate(model)
    except ModelNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{name}/versions", response_model=List[str])
async def get_model_versions(
    name: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get all versions of a model.
    
    Args:
        name: Model name
        db: Database session
    
    Returns:
        List of version strings
    
    Example:
        GET /api/models/sentiment-analyzer/versions
        Returns: ["2.0.0", "1.5.0", "1.0.0"]
    """
    registry = ModelRegistry(db)
    versions = await registry.get_versions(name)
    return versions


@router.patch("/{name}/{version}", response_model=ModelInfo)
async def update_model(
    name: str,
    version: str,
    updates: dict,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update model metadata.
    
    Args:
        name: Model name
        version: Model version
        updates: Fields to update
        db: Database session
    
    Returns:
        Updated model information
    
    Raises:
        404: Model not found
    
    Example:
        PATCH /api/models/sentiment-analyzer/1.0.0
        ```json
        {
            "is_deployed": true,
            "deployment_url": "https://api.example.com/predict"
        }
        ```
    """
    registry = ModelRegistry(db)

    try:
        model = await registry.update(name, version, **updates)
        return ModelInfo.model_validate(model)
    except ModelNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{name}/{version}", status_code=204)
async def delete_model(
    name: str,
    version: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a model from the registry.
    
    Args:
        name: Model name
        version: Model version
        db: Database session
    
    Raises:
        404: Model not found
    
    Example:
        DELETE /api/models/sentiment-analyzer/1.0.0
    """
    registry = ModelRegistry(db)

    deleted = await registry.delete(name, version)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{name}' version '{version}' not found"
        )
