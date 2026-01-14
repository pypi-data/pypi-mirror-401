"""
REST API routes for Resource Management.

Provides endpoints for monitoring and managing computational resources:
- GPU statistics and allocation
- Request queue status
- Circuit breaker states
- Batch processing metrics
"""

from fastapi import APIRouter, Depends, HTTPException

from neuralforge.dependencies.common import get_app

router = APIRouter(prefix="/api/resources", tags=["Resources"])


@router.get("/gpu")
async def get_gpu_stats(app = Depends(get_app)):
    """
    Get GPU statistics for all devices.
    
    Returns:
        List of GPU configurations with current stats
    
    Example:
        ```json
        [
            {
                "device_id": 0,
                "memory_total_mb": 16384,
                "memory_allocated_mb": 8192,
                "memory_available_mb": 8192,
                "utilization_percent": 75.5,
                "temperature_celsius": 65.0,
                "power_usage_watts": 250.0,
                "health_status": "healthy"
            }
        ]
        ```
    """
    if not hasattr(app, 'resources'):
        raise HTTPException(
            status_code=503,
            detail="Resource manager not configured"
        )

    stats = await app.resources.get_gpu_stats()

    return [
        {
            "device_id": gpu.device_id,
            "memory_total_mb": gpu.memory_total_mb,
            "memory_allocated_mb": gpu.memory_allocated_mb,
            "memory_available_mb": gpu.memory_available_mb,
            "memory_utilization": gpu.memory_utilization,
            "utilization_percent": gpu.utilization_percent,
            "temperature_celsius": gpu.temperature_celsius,
            "power_usage_watts": gpu.power_usage_watts,
            "health_status": gpu.health_status,
        }
        for gpu in stats
    ]


@router.get("/queue")
async def get_queue_stats(app = Depends(get_app)):
    """
    Get request queue statistics.
    
    Returns:
        Queue depth and statistics by priority
    
    Example:
        ```json
        {
            "total_size": 150,
            "by_priority": {
                "CRITICAL": 5,
                "HIGH": 20,
                "NORMAL": 100,
                "LOW": 25
            },
            "max_size": 10000,
            "utilization": 0.015
        }
        ```
    """
    if not hasattr(app, 'resources') or not app.resources.request_queue:
        raise HTTPException(
            status_code=503,
            detail="Request queue not configured"
        )

    return app.resources.request_queue.get_stats()


@router.get("/circuit-breakers")
async def get_circuit_breaker_states(app = Depends(get_app)):
    """
    Get states of all circuit breakers.
    
    Returns:
        Dictionary of circuit breaker names and their states
    
    Example:
        ```json
        {
            "default": "closed",
            "model-inference": "closed",
            "database": "half_open"
        }
        ```
    """
    if not hasattr(app, 'resources'):
        raise HTTPException(
            status_code=503,
            detail="Resource manager not configured"
        )

    return await app.resources.get_circuit_breaker_states()


@router.post("/circuit-breakers/{name}/reset")
async def reset_circuit_breaker(name: str, app = Depends(get_app)):
    """
    Manually reset a circuit breaker.
    
    Args:
        name: Circuit breaker name
    
    Returns:
        Success message
    
    Example:
        POST /api/resources/circuit-breakers/default/reset
    """
    if not hasattr(app, 'resources'):
        raise HTTPException(
            status_code=503,
            detail="Resource manager not configured"
        )

    breaker = app.resources.get_circuit_breaker(name)
    if not breaker:
        raise HTTPException(
            status_code=404,
            detail=f"Circuit breaker '{name}' not found"
        )

    breaker.reset()

    return {
        "message": f"Circuit breaker '{name}' reset successfully",
        "state": breaker.state.value
    }


@router.get("/health")
async def get_resource_health(app = Depends(get_app)):
    """
    Get overall resource health status.
    
    Returns:
        Health status of all resources
    
    Example:
        ```json
        {
            "status": "healthy",
            "gpu_available": true,
            "queue_depth": 150,
            "circuit_breakers_open": 0,
            "details": {
                "gpus": 2,
                "queue_utilization": 0.015,
                "circuit_breakers": ["default", "model-inference"]
            }
        }
        ```
    """
    if not hasattr(app, 'resources'):
        return {
            "status": "not_configured",
            "gpu_available": False,
            "queue_depth": 0,
            "circuit_breakers_open": 0
        }

    # Get GPU stats
    gpu_stats = await app.resources.get_gpu_stats()

    # Get queue stats
    queue_depth = 0
    queue_utilization = 0.0
    if app.resources.request_queue:
        queue_stats = app.resources.request_queue.get_stats()
        queue_depth = queue_stats["total_size"]
        queue_utilization = queue_stats["utilization"]

    # Get circuit breaker states
    cb_states = await app.resources.get_circuit_breaker_states()
    open_breakers = sum(1 for state in cb_states.values() if state == "open")

    # Determine overall health
    status = "healthy"
    if open_breakers > 0:
        status = "degraded"
    if queue_utilization > 0.9:
        status = "degraded"

    return {
        "status": status,
        "gpu_available": len(gpu_stats) > 0,
        "queue_depth": queue_depth,
        "circuit_breakers_open": open_breakers,
        "details": {
            "gpus": len(gpu_stats),
            "queue_utilization": queue_utilization,
            "circuit_breakers": list(cb_states.keys())
        }
    }
