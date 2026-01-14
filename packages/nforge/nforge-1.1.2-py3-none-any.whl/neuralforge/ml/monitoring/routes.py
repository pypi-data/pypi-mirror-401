"""
REST API routes for prediction monitoring.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from neuralforge.dependencies.common import get_db
from neuralforge.ml.monitoring.logger import PredictionLogger
from neuralforge.ml.monitoring.metrics import MetricsCollector
from neuralforge.ml.monitoring.alerts import AlertManager
from neuralforge.ml.monitoring.schemas import (
    PredictionLog,
    PredictionInfo,
    LatencyStats,
    ThroughputStats,
    ErrorStats,
    ConfidenceDistribution,
    MetricsSummary,
    AlertRuleCreate,
    AlertRuleInfo,
    AlertInfo,
)
from neuralforge.ml.monitoring.exceptions import (
    PredictionNotFoundError,
    InvalidTimeRangeError,
    MetricsNotAvailableError,
    AlertRuleNotFoundError,
    AlertNotFoundError,
)

router = APIRouter(prefix="/api/monitoring", tags=["Prediction Monitoring"])


# ========================================================================
# Prediction Logging
# ========================================================================

@router.post("/predictions", status_code=201)
async def log_prediction(
    prediction: PredictionLog,
    db: AsyncSession = Depends(get_db)
):
    """Log a prediction."""
    logger = PredictionLogger(db)
    request_id = await logger.log_prediction(prediction)
    return {"request_id": request_id, "message": "Prediction logged successfully"}


@router.post("/predictions/batch", status_code=201)
async def log_predictions_batch(
    predictions: List[PredictionLog],
    db: AsyncSession = Depends(get_db)
):
    """Batch log predictions."""
    logger = PredictionLogger(db)
    request_ids = await logger.log_batch(predictions)
    return {"request_ids": request_ids, "count": len(request_ids)}


@router.get("/predictions", response_model=List[PredictionInfo])
async def get_predictions(
    model_name: Optional[str] = Query(None),
    model_version: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """Query predictions."""
    logger = PredictionLogger(db)
    return await logger.get_predictions(
        model_name=model_name,
        model_version=model_version,
        status=status,
        limit=limit,
        offset=offset
    )


@router.get("/predictions/{prediction_id}", response_model=PredictionInfo)
async def get_prediction(
    prediction_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get prediction by ID."""
    logger = PredictionLogger(db)

    try:
        return await logger.get_prediction(prediction_id)
    except PredictionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ========================================================================
# Metrics
# ========================================================================

@router.get("/metrics/latency", response_model=LatencyStats)
async def get_latency_stats(
    model_name: str = Query(...),
    time_range: str = Query("1h", description="Time range (e.g., 1h, 24h, 7d)"),
    model_version: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get latency statistics."""
    metrics = MetricsCollector(db)

    try:
        return await metrics.get_latency_stats(model_name, time_range, model_version)
    except (InvalidTimeRangeError, MetricsNotAvailableError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metrics/throughput", response_model=ThroughputStats)
async def get_throughput_stats(
    model_name: str = Query(...),
    time_range: str = Query("1h"),
    model_version: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get throughput statistics."""
    metrics = MetricsCollector(db)

    try:
        return await metrics.get_throughput(model_name, time_range, model_version)
    except InvalidTimeRangeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metrics/errors", response_model=ErrorStats)
async def get_error_stats(
    model_name: str = Query(...),
    time_range: str = Query("1h"),
    model_version: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get error statistics."""
    metrics = MetricsCollector(db)

    try:
        return await metrics.get_error_stats(model_name, time_range, model_version)
    except InvalidTimeRangeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metrics/confidence", response_model=ConfidenceDistribution)
async def get_confidence_distribution(
    model_name: str = Query(...),
    time_range: str = Query("1h"),
    model_version: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get confidence distribution."""
    metrics = MetricsCollector(db)

    try:
        return await metrics.get_confidence_distribution(model_name, time_range, model_version)
    except (InvalidTimeRangeError, MetricsNotAvailableError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metrics/summary", response_model=MetricsSummary)
async def get_metrics_summary(
    model_name: str = Query(...),
    time_range: str = Query("1h"),
    model_version: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get overall metrics summary."""
    metrics = MetricsCollector(db)

    try:
        return await metrics.get_metrics_summary(model_name, time_range, model_version)
    except (InvalidTimeRangeError, MetricsNotAvailableError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========================================================================
# Alert Rules
# ========================================================================

@router.post("/alert-rules", response_model=AlertRuleInfo, status_code=201)
async def create_alert_rule(
    rule: AlertRuleCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create alert rule."""
    manager = AlertManager(db)
    return await manager.create_rule(rule)


@router.get("/alert-rules", response_model=List[AlertRuleInfo])
async def list_alert_rules(
    is_active: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List alert rules."""
    manager = AlertManager(db)
    return await manager.list_rules(is_active=is_active)


@router.get("/alert-rules/{rule_id}", response_model=AlertRuleInfo)
async def get_alert_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get alert rule by ID."""
    manager = AlertManager(db)

    try:
        return await manager.get_rule(rule_id)
    except AlertRuleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/alert-rules/{rule_id}", status_code=204)
async def delete_alert_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete alert rule."""
    manager = AlertManager(db)

    deleted = await manager.delete_rule(rule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Alert rule not found")


# ========================================================================
# Alerts
# ========================================================================

@router.get("/alerts", response_model=List[AlertInfo])
async def list_alerts(
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """List alerts."""
    manager = AlertManager(db)
    return await manager.list_alerts(status=status, severity=severity, limit=limit)


@router.get("/alerts/{alert_id}", response_model=AlertInfo)
async def get_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get alert by ID."""
    manager = AlertManager(db)

    try:
        return await manager.get_alert(alert_id)
    except AlertNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/alerts/{alert_id}/acknowledge", response_model=AlertInfo)
async def acknowledge_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Acknowledge alert."""
    manager = AlertManager(db)

    try:
        return await manager.acknowledge_alert(alert_id)
    except AlertNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/alerts/{alert_id}/resolve", response_model=AlertInfo)
async def resolve_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Resolve alert."""
    manager = AlertManager(db)

    try:
        return await manager.resolve_alert(alert_id)
    except AlertNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
