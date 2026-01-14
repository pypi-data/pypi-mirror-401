"""
Resource Manager - GPU/CPU resource allocation and management.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from collections import deque
import time

logger = logging.getLogger(__name__)


# ============================================================================
# Configuration Classes
# ============================================================================

class SharingStrategy(str, Enum):
    """GPU sharing strategies."""
    TIME_SLICING = "time-slicing"
    MPS = "mps"  # Multi-Process Service
    MIG = "mig"  # Multi-Instance GPU
    EXCLUSIVE = "exclusive"


@dataclass
class GPUConfig:
    """Configuration for a single GPU."""
    device_id: int
    memory_total_mb: float
    memory_allocated_mb: float = 0.0
    utilization_percent: float = 0.0
    temperature_celsius: float = 0.0
    power_usage_watts: float = 0.0
    processes: List[str] = None
    health_status: str = "healthy"

    def __post_init__(self):
        if self.processes is None:
            self.processes = []

    @property
    def memory_available_mb(self) -> float:
        """Get available memory."""
        return self.memory_total_mb - self.memory_allocated_mb

    @property
    def memory_utilization(self) -> float:
        """Get memory utilization ratio (0.0-1.0)."""
        return self.memory_allocated_mb / self.memory_total_mb if self.memory_total_mb > 0 else 0.0


@dataclass
class GPUPool:
    """GPU pool configuration."""
    devices: List[int]
    memory_fraction: float = 0.9
    allow_growth: bool = True
    sharing_strategy: SharingStrategy = SharingStrategy.TIME_SLICING
    max_concurrent_models: int = 2


@dataclass
class BatchConfig:
    """Batching configuration."""
    enabled: bool = True
    max_batch_size: int = 32
    timeout_ms: int = 100
    min_batch_size: int = 1
    strategy: str = "dynamic"  # dynamic, fixed, adaptive


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout_seconds: float = 60.0
    excluded_exceptions: List[type] = None

    def __post_init__(self):
        if self.excluded_exceptions is None:
            self.excluded_exceptions = []


# ============================================================================
# Circuit Breaker
# ============================================================================

class CircuitBreakerState(str, Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """
    Circuit breaker for preventing cascading failures.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Too many failures, reject requests immediately
    - HALF_OPEN: Testing recovery, allow limited requests
    """

    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config

        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.last_state_change: float = time.time()

    def call(self, func):
        """Decorator to wrap function with circuit breaker."""
        async def wrapper(*args, **kwargs):
            # Check if circuit is open
            if self.state == CircuitBreakerState.OPEN:
                # Check if timeout has passed
                if time.time() - self.last_failure_time >= self.config.timeout_seconds:
                    logger.info(f"Circuit breaker {self.name}: Transitioning to HALF_OPEN")
                    self.state = CircuitBreakerState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise CircuitBreakerOpenError(
                        f"Circuit breaker {self.name} is OPEN"
                    )

            try:
                result = await func(*args, **kwargs)
                self._on_success()
                return result

            except Exception as e:
                # Check if exception should be ignored
                if type(e) in self.config.excluded_exceptions:
                    raise

                self._on_failure()
                raise

        return wrapper

    def _on_success(self):
        """Handle successful request."""
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1

            if self.success_count >= self.config.success_threshold:
                logger.info(f"Circuit breaker {self.name}: Transitioning to CLOSED")
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                self.last_state_change = time.time()

        elif self.state == CircuitBreakerState.CLOSED:
            # Reset failure count on success
            self.failure_count = 0

    def _on_failure(self):
        """Handle failed request."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitBreakerState.HALF_OPEN:
            logger.warning(f"Circuit breaker {self.name}: Failed in HALF_OPEN, back to OPEN")
            self.state = CircuitBreakerState.OPEN
            self.success_count = 0
            self.last_state_change = time.time()

        elif self.state == CircuitBreakerState.CLOSED:
            if self.failure_count >= self.config.failure_threshold:
                logger.error(
                    f"Circuit breaker {self.name}: Transitioning to OPEN "
                    f"after {self.failure_count} failures"
                )
                self.state = CircuitBreakerState.OPEN
                self.last_state_change = time.time()

    def reset(self):
        """Manually reset circuit breaker."""
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_state_change = time.time()
        logger.info(f"Circuit breaker {self.name}: Manually reset to CLOSED")


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass


# ============================================================================
# Request Queue
# ============================================================================

class PriorityLevel(int, Enum):
    """Request priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class QueuedRequest:
    """Request in queue."""
    id: str
    data: Any
    priority: PriorityLevel
    timestamp: float
    timeout: float
    future: asyncio.Future


class RequestQueue:
    """
    Priority queue for managing incoming requests.
    
    Supports:
    - Priority-based ordering
    - Request timeouts
    - Queue size limits
    - Overflow handling
    """

    def __init__(
        self,
        max_size: int = 10000,
        overflow_strategy: str = "reject",  # reject, drop_oldest
        timeout_seconds: float = 30.0
    ):
        self.max_size = max_size
        self.overflow_strategy = overflow_strategy
        self.default_timeout = timeout_seconds

        # Separate queues for each priority level
        self.queues: Dict[PriorityLevel, deque] = {
            level: deque() for level in PriorityLevel
        }

        self._lock = asyncio.Lock()
        self._not_empty = asyncio.Condition(self._lock)

    async def enqueue(
        self,
        request_id: str,
        data: Any,
        priority: PriorityLevel = PriorityLevel.NORMAL,
        timeout: Optional[float] = None
    ) -> asyncio.Future:
        """
        Add request to queue.
        
        Returns:
            Future that will be resolved when request is processed
        """
        async with self._lock:
            # Check if queue is full
            if self.size >= self.max_size:
                if self.overflow_strategy == "reject":
                    raise QueueFullError(f"Queue is full (size: {self.size})")
                elif self.overflow_strategy == "drop_oldest":
                    # Drop oldest low priority request
                    self._drop_oldest_low_priority()

            # Create queued request
            queued_request = QueuedRequest(
                id=request_id,
                data=data,
                priority=priority,
                timestamp=time.time(),
                timeout=timeout or self.default_timeout,
                future=asyncio.Future()
            )

            # Add to appropriate priority queue
            self.queues[priority].append(queued_request)

            # Notify waiting consumers
            self._not_empty.notify()

            return queued_request.future

    async def dequeue(self, batch_size: int = 1) -> List[QueuedRequest]:
        """
        Get requests from queue (highest priority first).
        
        Args:
            batch_size: Number of requests to dequeue
        
        Returns:
            List of queued requests
        """
        async with self._not_empty:
            # Wait for requests
            while self.size == 0:
                await self._not_empty.wait()

            requests = []

            # Dequeue from highest priority first
            for priority in sorted(PriorityLevel, reverse=True):
                queue = self.queues[priority]

                while queue and len(requests) < batch_size:
                    req = queue.popleft()

                    # Check if request has timed out
                    if time.time() - req.timestamp > req.timeout:
                        req.future.set_exception(
                            TimeoutError(f"Request {req.id} timed out in queue")
                        )
                        continue

                    requests.append(req)

                if len(requests) >= batch_size:
                    break

            return requests

    def _drop_oldest_low_priority(self):
        """Drop oldest low priority request."""
        for priority in [PriorityLevel.LOW, PriorityLevel.NORMAL]:
            queue = self.queues[priority]
            if queue:
                dropped = queue.popleft()
                dropped.future.set_exception(
                    QueueFullError(f"Request {dropped.id} dropped due to queue overflow")
                )
                logger.warning(f"Dropped request {dropped.id} (priority: {priority})")
                return

    @property
    def size(self) -> int:
        """Get total queue size."""
        return sum(len(q) for q in self.queues.values())

    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        return {
            "total_size": self.size,
            "by_priority": {
                priority.name: len(queue)
                for priority, queue in self.queues.items()
            },
            "max_size": self.max_size,
            "utilization": self.size / self.max_size if self.max_size > 0 else 0.0
        }


class QueueFullError(Exception):
    """Raised when queue is full and overflow strategy is reject."""
    pass


# ============================================================================
# Batch Manager
# ============================================================================

class BatchManager:
    """
    Manages request batching for efficient GPU utilization.
    
    Strategies:
    - Dynamic: Wait for requests up to timeout, submit when batch is ready
    - Fixed: Always wait for exact batch size
    - Adaptive: Adjust batch size based on queue depth and latency
    """

    def __init__(self, config: BatchConfig):
        self.config = config
        self.pending_requests: List[QueuedRequest] = []
        self.last_submit_time: float = time.time()

        self._lock = asyncio.Lock()
        self._batch_ready = asyncio.Event()

    async def add_request(self, request: QueuedRequest):
        """Add request to pending batch."""
        async with self._lock:
            self.pending_requests.append(request)

            # Check if batch is ready
            if self._should_submit_batch():
                self._batch_ready.set()

    def _should_submit_batch(self) -> bool:
        """Check if batch should be submitted."""
        if not self.config.enabled:
            return len(self.pending_requests) >= 1

        batch_size = len(self.pending_requests)
        time_elapsed_ms = (time.time() - self.last_submit_time) * 1000

        if self.config.strategy == "dynamic":
            # Submit if batch is full or timeout reached
            return (
                batch_size >= self.config.max_batch_size or
                (batch_size >= self.config.min_batch_size and
                 time_elapsed_ms >= self.config.timeout_ms)
            )

        elif self.config.strategy == "fixed":
            # Only submit when exact batch size is reached
            return batch_size >= self.config.max_batch_size

        elif self.config.strategy == "adaptive":
            # Adaptive logic (simplified)
            if batch_size >= self.config.max_batch_size:
                return True

            # Submit smaller batches if queue is growing
            if batch_size >= self.config.min_batch_size and time_elapsed_ms >= self.config.timeout_ms / 2:
                return True

            return False

        return False

    async def get_batch(self) -> List[QueuedRequest]:
        """Get a batch of requests."""
        # Wait for batch to be ready
        await self._batch_ready.wait()

        async with self._lock:
            batch = self.pending_requests[:self.config.max_batch_size]
            self.pending_requests = self.pending_requests[self.config.max_batch_size:]

            self.last_submit_time = time.time()
            self._batch_ready.clear()

            # If there are still pending requests, set event again
            if self._should_submit_batch():
                self._batch_ready.set()

            return batch


# ============================================================================
# Resource Manager
# ============================================================================

class ResourceManager:
    """
    Central manager for computational resources (GPU/CPU).
    
    Responsibilities:
    - GPU pool management
    - Request queuing
    - Batching
    - Circuit breaking
    - Resource allocation
    """

    def __init__(self, app: "NeuralForge"):
        self.app = app

        # GPU management
        self.gpu_pool: Optional[GPUPool] = None
        self.gpu_configs: Dict[int, GPUConfig] = {}

        # Request management
        self.request_queue: Optional[RequestQueue] = None
        self.batch_manager: Optional[BatchManager] = None

        # Circuit breakers
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}

        # Configuration
        self.max_concurrent_requests: int = 100
        self.request_timeout: float = 30.0

        logger.info("Initialized ResourceManager")

    # ========================================================================
    # GPU Configuration
    # ========================================================================

    def configure_gpu(self, pool: GPUPool):
        """Configure GPU pool."""
        self.gpu_pool = pool

        # Initialize GPU configs
        for device_id in pool.devices:
            self.gpu_configs[device_id] = self._get_gpu_info(device_id)

        logger.info(
            f"Configured GPU pool with {len(pool.devices)} devices: {pool.devices}"
        )

    def _get_gpu_info(self, device_id: int) -> GPUConfig:
        """Get GPU information (requires torch/nvidia-ml-py)."""
        try:
            import torch

            if torch.cuda.is_available() and device_id < torch.cuda.device_count():
                props = torch.cuda.get_device_properties(device_id)
                memory_total = props.total_memory / (1024 ** 2)  # Convert to MB

                return GPUConfig(
                    device_id=device_id,
                    memory_total_mb=memory_total,
                    health_status="healthy"
                )
        except ImportError:
            logger.warning("PyTorch not available, GPU info unavailable")
        except Exception as e:
            logger.error(f"Error getting GPU info: {e}")

        # Fallback
        return GPUConfig(
            device_id=device_id,
            memory_total_mb=16384,  # Assume 16GB
            health_status="unknown"
        )

    async def get_gpu_stats(self) -> List[GPUConfig]:
        """Get current GPU statistics."""
        stats = []

        try:
            import torch

            for device_id, config in self.gpu_configs.items():
                if torch.cuda.is_available():
                    # Update memory usage
                    config.memory_allocated_mb = torch.cuda.memory_allocated(device_id) / (1024 ** 2)

                    # Update utilization (requires nvidia-ml-py for detailed stats)
                    try:
                        import pynvml
                        pynvml.nvmlInit()
                        handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)

                        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                        config.utilization_percent = utilization.gpu

                        temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                        config.temperature_celsius = temperature

                        power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # mW to W
                        config.power_usage_watts = power

                    except ImportError:
                        pass  # pynvml not available

                stats.append(config)

        except Exception as e:
            logger.error(f"Error getting GPU stats: {e}")

        return stats

    # ========================================================================
    # Queue Configuration
    # ========================================================================

    def configure_queue(
        self,
        max_size: int = 10000,
        overflow_strategy: str = "reject",
        timeout_seconds: float = 30.0
    ):
        """Configure request queue."""
        self.request_queue = RequestQueue(
            max_size=max_size,
            overflow_strategy=overflow_strategy,
            timeout_seconds=timeout_seconds
        )

        logger.info(f"Configured request queue (max_size: {max_size})")

    def configure_batching(self, config: BatchConfig):
        """Configure request batching."""
        self.batch_manager = BatchManager(config)
        logger.info(f"Configured batching: {config}")

    async def get_queue_depth(self) -> int:
        """Get current queue depth."""
        if self.request_queue:
            return self.request_queue.size
        return 0

    # ========================================================================
    # Circuit Breaker Configuration
    # ========================================================================

    def configure_circuit_breaker(
        self,
        name: str,
        config: CircuitBreakerConfig
    ) -> CircuitBreaker:
        """Configure circuit breaker for a resource."""
        breaker = CircuitBreaker(name, config)
        self.circuit_breakers[name] = breaker

        logger.info(f"Configured circuit breaker: {name}")

        return breaker

    def get_circuit_breaker(self, name: str) -> Optional[CircuitBreaker]:
        """Get circuit breaker by name."""
        return self.circuit_breakers.get(name)

    async def get_circuit_breaker_states(self) -> Dict[str, str]:
        """Get states of all circuit breakers."""
        return {
            name: breaker.state.value
            for name, breaker in self.circuit_breakers.items()
        }

    # ========================================================================
    # Resource Allocation
    # ========================================================================

    def allocate_gpu(self, required_memory_mb: float = 0) -> Optional[int]:
        """
        Allocate a GPU for a model.
        
        Returns:
            GPU device ID or None if no GPU available
        """
        if not self.gpu_pool:
            return None

        # Find GPU with most available memory
        best_gpu = None
        max_available = 0

        for device_id, config in self.gpu_configs.items():
            available = config.memory_available_mb

            if available >= required_memory_mb and available > max_available:
                best_gpu = device_id
                max_available = available

        if best_gpu is not None:
            # Mark memory as allocated
            self.gpu_configs[best_gpu].memory_allocated_mb += required_memory_mb
            logger.info(f"Allocated GPU {best_gpu} ({required_memory_mb} MB)")

        return best_gpu

    def release_gpu(self, device_id: int, memory_mb: float):
        """Release GPU memory."""
        if device_id in self.gpu_configs:
            self.gpu_configs[device_id].memory_allocated_mb -= memory_mb
            logger.info(f"Released GPU {device_id} ({memory_mb} MB)")

    # ========================================================================
    # Configuration Helpers
    # ========================================================================

    def configure(
        self,
        max_concurrent_requests: int = 100,
        request_timeout: float = 30.0,
        queue_max_size: int = 10000,
        circuit_breaker_enabled: bool = True,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: float = 60.0
    ):
        """Configure resource manager with common settings."""
        self.max_concurrent_requests = max_concurrent_requests
        self.request_timeout = request_timeout

        # Configure queue
        self.configure_queue(
            max_size=queue_max_size,
            timeout_seconds=request_timeout
        )

        # Configure default circuit breaker
        if circuit_breaker_enabled:
            self.configure_circuit_breaker(
                "default",
                CircuitBreakerConfig(
                    failure_threshold=circuit_breaker_threshold,
                    timeout_seconds=circuit_breaker_timeout
                )
            )

    # ========================================================================
    # Cleanup
    # ========================================================================

    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up ResourceManager")

        # Reset circuit breakers
        for breaker in self.circuit_breakers.values():
            breaker.reset()
