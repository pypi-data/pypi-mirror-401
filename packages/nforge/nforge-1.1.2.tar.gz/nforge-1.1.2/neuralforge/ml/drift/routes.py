"""
REST API routes for drift detection.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from neuralforge.dependencies.common import get_db
from neuralforge.ml.drift.detector import DriftDetector
from neuralforge.ml.drift.baseline import BaselineManager
from neuralforge.ml.drift.schemas import (
    BaselineCreate,
    BaselineInfo,
    DriftDetectionRequest,
    DriftDetectionResult,
    DriftDetectionInfo,
    DriftSummary,
)
from neuralforge.ml.drift.exceptions import (
    BaselineNotFoundError,
    InsufficientDataError,
)

router = APIRouter(prefix="/api/drift", tags=["Drift Detection"])


# ========================================================================
# Baseline Management
# ========================================================================

@router.post("/baselines", response_model=BaselineInfo, status_code=201)
async def create_baseline(
    baseline: BaselineCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a drift baseline."""
    manager = BaselineManager(db)
    return await manager.create_baseline(baseline)


@router.get("/baselines", response_model=List[BaselineInfo])
async def list_baselines(
    model_name: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List drift baselines."""
    manager = BaselineManager(db)
    return await manager.list_baselines(model_name=model_name)


@router.get("/baselines/{baseline_id}", response_model=BaselineInfo)
async def get_baseline(
    baseline_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get baseline by ID."""
    manager = BaselineManager(db)

    try:
        baselines = await manager.list_baselines()
        baseline = next((b for b in baselines if b.id == baseline_id), None)

        if not baseline:
            raise HTTPException(status_code=404, detail="Baseline not found")

        return baseline
    except BaselineNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/baselines/{baseline_id}", status_code=204)
async def delete_baseline(
    baseline_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a baseline."""
    manager = BaselineManager(db)

    deleted = await manager.delete_baseline(baseline_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Baseline not found")


# ========================================================================
# Drift Detection
# ========================================================================

@router.post("/detect", response_model=DriftDetectionResult)
async def detect_drift(
    request: DriftDetectionRequest,
    db: AsyncSession = Depends(get_db)
):
    """Detect drift in current data."""
    detector = DriftDetector(db)

    try:
        # Convert data to DataFrame
        current_data = pd.DataFrame(request.current_data)

        result = await detector.detect_drift(
            model_name=request.model_name,
            baseline_name=request.baseline_name,
            current_data=current_data,
            features=request.features,
            detection_window=request.detection_window
        )

        return result

    except BaselineNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drift detection failed: {str(e)}")


@router.get("/detections", response_model=List[DriftDetectionInfo])
async def list_detections(
    model_name: Optional[str] = Query(None),
    drift_detected: Optional[bool] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """List drift detections."""
    from sqlalchemy import select, and_
    from neuralforge.db.models.drift_detection import DriftDetection

    query = select(DriftDetection)

    conditions = []
    if model_name:
        conditions.append(DriftDetection.model_name == model_name)
    if drift_detected is not None:
        conditions.append(DriftDetection.drift_detected == drift_detected)

    if conditions:
        query = query.where(and_(*conditions))

    query = query.order_by(DriftDetection.detected_at.desc()).limit(limit)

    result = await db.execute(query)
    detections = result.scalars().all()

    return [DriftDetectionInfo.model_validate(d) for d in detections]


@router.get("/detections/{detection_id}", response_model=DriftDetectionInfo)
async def get_detection(
    detection_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detection by ID."""
    from sqlalchemy import select
    from neuralforge.db.models.drift_detection import DriftDetection

    result = await db.execute(
        select(DriftDetection).where(DriftDetection.id == detection_id)
    )
    detection = result.scalar_one_or_none()

    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")

    return DriftDetectionInfo.model_validate(detection)


@router.get("/models/{model_name}/drift", response_model=DriftSummary)
async def get_model_drift_summary(
    model_name: str,
    model_version: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get drift summary for a model."""
    from sqlalchemy import select
    from neuralforge.db.models.drift_detection import DriftDetection

    # Build query
    query = select(DriftDetection).where(DriftDetection.model_name == model_name)

    if model_version:
        query = query.where(DriftDetection.model_version == model_version)

    # Get all detections
    result = await db.execute(query)
    all_detections = result.scalars().all()

    # Calculate summary
    total_detections = len(all_detections)
    drift_detected_count = sum(1 for d in all_detections if d.drift_detected)
    drift_rate = drift_detected_count / total_detections if total_detections > 0 else 0.0

    # Severity breakdown
    severity_breakdown = {}
    for detection in all_detections:
        if detection.drift_detected and detection.drift_severity:
            severity_breakdown[detection.drift_severity] = severity_breakdown.get(detection.drift_severity, 0) + 1

    # Recent detections
    recent_query = query.order_by(DriftDetection.detected_at.desc()).limit(limit)
    result = await db.execute(recent_query)
    recent_detections = result.scalars().all()

    return DriftSummary(
        model_name=model_name,
        model_version=model_version,
        total_detections=total_detections,
        drift_detected_count=drift_detected_count,
        drift_rate=drift_rate,
        severity_breakdown=severity_breakdown,
        recent_detections=[DriftDetectionInfo.model_validate(d) for d in recent_detections]
    )
