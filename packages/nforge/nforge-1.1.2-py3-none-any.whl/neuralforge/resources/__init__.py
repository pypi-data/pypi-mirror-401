"""
Resources module - GPU/CPU resource management.

Provides:
- GPU pool management and allocation
- Request queuing with priorities
- Request batching for efficiency
- Circuit breakers for fault tolerance
- Resource monitoring and health checks
"""

from neuralforge.resources.manager import (
    ResourceManager,
    GPUConfig,
    GPUPool,
    BatchConfig,
    CircuitBreakerConfig,
    CircuitBreaker,
    CircuitBreakerState,
    SharingStrategy,
    RequestQueue,
    BatchManager,
    PriorityLevel,
    QueuedRequest,
    CircuitBreakerOpenError,
    QueueFullError,
)

__all__ = [
    'ResourceManager',
    'GPUConfig',
    'GPUPool',
    'BatchConfig',
    'CircuitBreakerConfig',
    'CircuitBreaker',
    'CircuitBreakerState',
    'SharingStrategy',
    'RequestQueue',
    'BatchManager',
    'PriorityLevel',
    'QueuedRequest',
    'CircuitBreakerOpenError',
    'QueueFullError',
]
