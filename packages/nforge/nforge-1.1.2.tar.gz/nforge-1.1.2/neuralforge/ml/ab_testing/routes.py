"""
REST API routes for A/B testing.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from neuralforge.dependencies.common import get_db
from neuralforge.ml.ab_testing.manager import ExperimentManager
from neuralforge.ml.ab_testing.schemas import (
    ExperimentCreate,
    ExperimentUpdate,
    ExperimentInfo,
    MetricRecord,
    AssignmentResponse,
    ExperimentResults,
)
from neuralforge.ml.ab_testing.exceptions import (
    ExperimentNotFoundError,
    ExperimentAlreadyExistsError,
    ExperimentNotRunningError,
    VariantNotFoundError,
)

router = APIRouter(prefix="/api/ab", tags=["A/B Testing"])


@router.post("/experiments", response_model=ExperimentInfo, status_code=201)
async def create_experiment(
    experiment: ExperimentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new A/B test experiment.
    
    Example:
        ```json
        {
            "name": "model-v2-test",
            "description": "Testing new model version",
            "variants": [
                {
                    "name": "control",
                    "model_name": "sentiment-analyzer",
                    "model_version": "1.0.0",
                    "traffic_percentage": 50,
                    "is_control": true
                },
                {
                    "name": "variant_a",
                    "model_name": "sentiment-analyzer",
                    "model_version": "2.0.0",
                    "traffic_percentage": 50
                }
            ],
            "primary_metric": "accuracy"
        }
        ```
    """
    manager = ExperimentManager(db)

    try:
        return await manager.create_experiment(experiment)
    except ExperimentAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/experiments", response_model=List[ExperimentInfo])
async def list_experiments(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """List all experiments with optional filters."""
    manager = ExperimentManager(db)
    return await manager.list_experiments(status=status, limit=limit, offset=offset)


@router.get("/experiments/{experiment_id}", response_model=ExperimentInfo)
async def get_experiment(
    experiment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get experiment by ID."""
    manager = ExperimentManager(db)

    try:
        return await manager.get_experiment(experiment_id)
    except ExperimentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/experiments/{experiment_id}", response_model=ExperimentInfo)
async def update_experiment(
    experiment_id: int,
    updates: ExperimentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update experiment configuration."""
    manager = ExperimentManager(db)

    try:
        return await manager.update_experiment(experiment_id, updates)
    except ExperimentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/experiments/{experiment_id}", status_code=204)
async def delete_experiment(
    experiment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete experiment."""
    manager = ExperimentManager(db)

    deleted = await manager.delete_experiment(experiment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Experiment not found")


@router.post("/experiments/{experiment_id}/start", response_model=ExperimentInfo)
async def start_experiment(
    experiment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Start running experiment."""
    manager = ExperimentManager(db)

    try:
        return await manager.start_experiment(experiment_id)
    except ExperimentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/experiments/{experiment_id}/stop", response_model=ExperimentInfo)
async def stop_experiment(
    experiment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Stop experiment."""
    manager = ExperimentManager(db)

    try:
        return await manager.stop_experiment(experiment_id)
    except ExperimentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/assign/{experiment_name}", response_model=AssignmentResponse)
async def get_assignment(
    experiment_name: str,
    user_id: str = Query(..., description="User identifier"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get variant assignment for user.
    
    Returns consistent assignment for the same user.
    
    Example:
        GET /api/ab/assign/model-v2-test?user_id=user123
    """
    manager = ExperimentManager(db)

    try:
        return await manager.get_assignment(experiment_name, user_id)
    except ExperimentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExperimentNotRunningError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except VariantNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/metrics", status_code=201)
async def record_metric(
    metric: MetricRecord,
    db: AsyncSession = Depends(get_db)
):
    """
    Record metric for variant.
    
    Example:
        ```json
        {
            "experiment_name": "model-v2-test",
            "variant_name": "variant_a",
            "metric_name": "accuracy",
            "metric_value": 0.95,
            "user_id": "user123"
        }
        ```
    """
    manager = ExperimentManager(db)

    try:
        await manager.record_metric(metric)
        return {"message": "Metric recorded successfully"}
    except (ExperimentNotFoundError, VariantNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/experiments/{experiment_id}/results", response_model=ExperimentResults)
async def get_results(
    experiment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get experiment results with statistical analysis.
    
    Returns:
        - Metrics for each variant
        - Statistical significance
        - Winner determination
        - Recommendations
    """
    manager = ExperimentManager(db)

    try:
        return await manager.analyze_results(experiment_id)
    except ExperimentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
