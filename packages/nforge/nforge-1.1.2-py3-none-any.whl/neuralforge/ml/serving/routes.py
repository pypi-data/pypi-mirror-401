"""
REST API routes for system management (GPU, cache).
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any

from neuralforge.ml.serving import GPUManager, ModelCache

router = APIRouter(prefix="/api/system", tags=["System Management"])

# Global instances
_gpu_manager = None
_model_cache = None


def get_gpu_manager() -> GPUManager:
    """Get GPU manager instance."""
    global _gpu_manager
    if _gpu_manager is None:
        _gpu_manager = GPUManager()
    return _gpu_manager


def get_model_cache() -> ModelCache:
    """Get model cache instance."""
    global _model_cache
    if _model_cache is None:
        _model_cache = ModelCache()
    return _model_cache


# ========================================================================
# GPU Management
# ========================================================================

@router.get("/gpu")
async def get_gpu_info(
    gpu_mgr: GPUManager = Depends(get_gpu_manager)
) -> Dict[str, Any]:
    """Get GPU information."""
    return gpu_mgr.get_device_info()


@router.get("/devices")
async def get_devices(
    gpu_mgr: GPUManager = Depends(get_gpu_manager)
) -> Dict[str, Any]:
    """Get available devices."""
    info = gpu_mgr.get_device_info()
    return {
        'default_device': info['default_device'],
        'cuda_available': info['cuda_available'],
        'mps_available': info['mps_available'],
        'num_gpus': info['num_gpus']
    }


@router.get("/memory")
async def get_memory_info(
    device: str = "cuda",
    gpu_mgr: GPUManager = Depends(get_gpu_manager)
) -> Dict[str, float]:
    """Get memory information for device."""
    return gpu_mgr.get_memory_info(device)


@router.post("/gpu/clear-cache")
async def clear_gpu_cache(
    gpu_mgr: GPUManager = Depends(get_gpu_manager)
):
    """Clear GPU cache."""
    gpu_mgr.clear_cache()
    return {"message": "GPU cache cleared"}


# ========================================================================
# Model Cache
# ========================================================================

@router.get("/cache/stats")
async def get_cache_stats(
    cache: ModelCache = Depends(get_model_cache)
) -> Dict[str, Any]:
    """Get cache statistics."""
    return cache.get_stats()


@router.post("/cache/clear")
async def clear_cache(
    cache: ModelCache = Depends(get_model_cache)
):
    """Clear model cache."""
    cache.clear()
    return {"message": "Cache cleared"}


@router.get("/health")
async def health_check(
    gpu_mgr: GPUManager = Depends(get_gpu_manager),
    cache: ModelCache = Depends(get_model_cache)
) -> Dict[str, Any]:
    """System health check."""
    gpu_info = gpu_mgr.get_device_info()
    cache_stats = cache.get_stats()

    return {
        'status': 'healthy',
        'gpu': {
            'available': gpu_info['cuda_available'] or gpu_info['mps_available'],
            'device': gpu_info['default_device']
        },
        'cache': {
            'size': cache_stats['size'],
            'hit_rate': cache_stats['hit_rate']
        }
    }
