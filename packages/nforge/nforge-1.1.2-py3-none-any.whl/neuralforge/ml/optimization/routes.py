"""
REST API routes for model optimization.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from neuralforge.dependencies.common import get_db
from neuralforge.ml.optimization.quantizer import ModelQuantizer
from neuralforge.ml.optimization.benchmarker import PerformanceBenchmarker
from neuralforge.ml.optimization.schemas import (
    OptimizationRequest,
    OptimizedModelInfo,
    BenchmarkConfig,
    BenchmarkResultInfo,
)
from neuralforge.db.models.optimized_model import OptimizedModel
from neuralforge.db.models.benchmark_result import BenchmarkResult

router = APIRouter(prefix="/api/optimization", tags=["Model Optimization"])


# ========================================================================
# Quantization
# ========================================================================

@router.post("/quantize", status_code=201)
async def quantize_model(
    request: OptimizationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Quantize a model.
    
    Note: This endpoint provides the API structure.
    Actual quantization requires loading the model from registry.
    """
    try:
        _quantizer = ModelQuantizer()

        # Create optimization record
        optimized = OptimizedModel(
            source_model_name=request.source_model_name,
            source_model_version=request.source_model_version,
            optimized_name=f"{request.source_model_name}_quantized",
            optimization_type="quantization",
            config=request.config
        )

        db.add(optimized)
        await db.commit()
        await db.refresh(optimized)

        return {
            "optimized_model_id": optimized.id,
            "message": "Quantization initiated. Load model from registry to complete."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quantization failed: {str(e)}")


@router.get("/quantized", response_model=List[OptimizedModelInfo])
async def list_quantized_models(
    db: AsyncSession = Depends(get_db)
):
    """List quantized models."""
    result = await db.execute(
        select(OptimizedModel).where(OptimizedModel.optimization_type == "quantization")
    )
    models = result.scalars().all()

    return [OptimizedModelInfo.model_validate(m) for m in models]


# ========================================================================
# Benchmarking
# ========================================================================

@router.post("/benchmark", status_code=201)
async def run_benchmark(
    model_name: str = Query(...),
    config: BenchmarkConfig = BenchmarkConfig(),
    db: AsyncSession = Depends(get_db)
):
    """
    Run performance benchmark.
    
    Note: This endpoint provides the API structure.
    Actual benchmarking requires loading the model.
    """
    try:
        _benchmarker = PerformanceBenchmarker(db)

        # Create benchmark record
        result = BenchmarkResult(
            model_name=model_name,
            batch_size=config.batch_size,
            num_iterations=config.num_iterations,
            device=config.device.value,
            avg_latency_ms=0.0  # Placeholder
        )

        db.add(result)
        await db.commit()
        await db.refresh(result)

        return {
            "benchmark_id": result.id,
            "message": "Benchmark initiated. Load model to complete."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark failed: {str(e)}")


@router.get("/benchmarks", response_model=List[BenchmarkResultInfo])
async def list_benchmarks(
    model_name: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """List benchmark results."""
    query = select(BenchmarkResult)

    if model_name:
        query = query.where(BenchmarkResult.model_name == model_name)

    query = query.order_by(BenchmarkResult.benchmark_date.desc()).limit(limit)

    result = await db.execute(query)
    benchmarks = result.scalars().all()

    return [BenchmarkResultInfo.model_validate(b) for b in benchmarks]


@router.get("/benchmarks/{benchmark_id}", response_model=BenchmarkResultInfo)
async def get_benchmark(
    benchmark_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get benchmark result by ID."""
    result = await db.execute(
        select(BenchmarkResult).where(BenchmarkResult.id == benchmark_id)
    )
    benchmark = result.scalar_one_or_none()

    if not benchmark:
        raise HTTPException(status_code=404, detail="Benchmark not found")

    return BenchmarkResultInfo.model_validate(benchmark)


# ========================================================================
# Optimized Models
# ========================================================================

@router.get("/models", response_model=List[OptimizedModelInfo])
async def list_optimized_models(
    optimization_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List optimized models."""
    query = select(OptimizedModel)

    if optimization_type:
        query = query.where(OptimizedModel.optimization_type == optimization_type)

    result = await db.execute(query)
    models = result.scalars().all()

    return [OptimizedModelInfo.model_validate(m) for m in models]


@router.get("/models/{model_id}", response_model=OptimizedModelInfo)
async def get_optimized_model(
    model_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get optimized model by ID."""
    result = await db.execute(
        select(OptimizedModel).where(OptimizedModel.id == model_id)
    )
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(status_code=404, detail="Optimized model not found")

    return OptimizedModelInfo.model_validate(model)


@router.delete("/models/{model_id}", status_code=204)
async def delete_optimized_model(
    model_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete optimized model."""
    result = await db.execute(
        select(OptimizedModel).where(OptimizedModel.id == model_id)
    )
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(status_code=404, detail="Optimized model not found")

    await db.delete(model)
    await db.commit()
