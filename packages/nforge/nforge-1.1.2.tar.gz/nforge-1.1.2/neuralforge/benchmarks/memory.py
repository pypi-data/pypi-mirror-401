"""
Memory Profiling Scenarios for NeuralForge Benchmarks.

Provides memory usage tracking during benchmark runs.
"""

import asyncio
import logging
import tracemalloc
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class MemorySnapshot:
    """Snapshot of memory usage at a point in time."""
    timestamp: datetime
    current_bytes: int
    peak_bytes: int
    allocated_blocks: int = 0
    label: str = ""
    
    @property
    def current_mb(self) -> float:
        return self.current_bytes / (1024 * 1024)
    
    @property
    def peak_mb(self) -> float:
        return self.peak_bytes / (1024 * 1024)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "current_mb": round(self.current_mb, 2),
            "peak_mb": round(self.peak_mb, 2),
            "current_bytes": self.current_bytes,
            "peak_bytes": self.peak_bytes,
            "allocated_blocks": self.allocated_blocks,
            "label": self.label,
        }


@dataclass
class MemoryProfile:
    """Complete memory profile for a benchmark run."""
    name: str
    snapshots: List[MemorySnapshot] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    baseline_bytes: int = 0
    top_allocations: List[Dict[str, Any]] = field(default_factory=list)
    
    @property
    def peak_mb(self) -> float:
        if not self.snapshots:
            return 0.0
        return max(s.peak_mb for s in self.snapshots)
    
    @property
    def delta_mb(self) -> float:
        """Memory increase from baseline."""
        if not self.snapshots:
            return 0.0
        final = self.snapshots[-1].current_bytes
        return (final - self.baseline_bytes) / (1024 * 1024)
    
    @property
    def duration_seconds(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "peak_mb": round(self.peak_mb, 2),
            "delta_mb": round(self.delta_mb, 2),
            "baseline_mb": round(self.baseline_bytes / (1024 * 1024), 2),
            "duration_seconds": round(self.duration_seconds, 3),
            "snapshot_count": len(self.snapshots),
            "top_allocations": self.top_allocations[:10],
        }


class MemoryProfiler:
    """
    Memory profiler for benchmark scenarios.
    
    Uses tracemalloc for Python memory tracking.
    
    Example:
        ```python
        profiler = MemoryProfiler()
        
        with profiler.profile("inference_batch"):
            results = await run_inference(batch)
        
        profile = profiler.get_profile()
        print(f"Peak memory: {profile.peak_mb}MB")
        ```
    """
    
    def __init__(self, snapshot_interval: float = 0.1):
        """
        Initialize profiler.
        
        Args:
            snapshot_interval: Seconds between automatic snapshots
        """
        self.snapshot_interval = snapshot_interval
        self._profile: Optional[MemoryProfile] = None
        self._is_profiling = False
        self._snapshot_task: Optional[asyncio.Task] = None
    
    def start(self, name: str = "default", nframes: int = 10):
        """
        Start memory profiling.
        
        Args:
            name: Profile name
            nframes: Stack frames to capture
        """
        if self._is_profiling:
            logger.warning("Already profiling, stopping previous session")
            self.stop()
        
        tracemalloc.start(nframes)
        
        current, _ = tracemalloc.get_traced_memory()
        
        self._profile = MemoryProfile(
            name=name,
            start_time=datetime.utcnow(),
            baseline_bytes=current,
        )
        self._is_profiling = True
        
        logger.debug(f"Started memory profiling: {name}")
    
    def snapshot(self, label: str = ""):
        """Take a memory snapshot."""
        if not self._is_profiling or self._profile is None:
            return
        
        current, peak = tracemalloc.get_traced_memory()
        
        snapshot = MemorySnapshot(
            timestamp=datetime.utcnow(),
            current_bytes=current,
            peak_bytes=peak,
            label=label,
        )
        
        self._profile.snapshots.append(snapshot)
    
    def stop(self) -> Optional[MemoryProfile]:
        """
        Stop profiling and return profile.
        
        Returns:
            MemoryProfile with all collected data
        """
        if not self._is_profiling:
            return None
        
        # Final snapshot
        self.snapshot(label="final")
        
        # Get top allocations
        if self._profile:
            self._profile.end_time = datetime.utcnow()
            
            try:
                snapshot = tracemalloc.take_snapshot()
                top_stats = snapshot.statistics('traceback')[:10]
                
                self._profile.top_allocations = [
                    {
                        "size_mb": round(stat.size / (1024 * 1024), 3),
                        "count": stat.count,
                        "traceback": [str(line) for line in stat.traceback.format()[:3]],
                    }
                    for stat in top_stats
                ]
            except Exception as e:
                logger.debug(f"Could not get top allocations: {e}")
        
        tracemalloc.stop()
        self._is_profiling = False
        
        profile = self._profile
        self._profile = None
        
        logger.debug(f"Stopped memory profiling: {profile.name if profile else 'unknown'}")
        
        return profile
    
    def profile(self, name: str = "default"):
        """Context manager for profiling."""
        return MemoryProfileContext(self, name)
    
    async def profile_async(
        self,
        func: Callable,
        *args,
        name: str = "async_profile",
        **kwargs
    ) -> tuple:
        """
        Profile an async function.
        
        Args:
            func: Async function to profile
            *args: Arguments to pass
            name: Profile name
            **kwargs: Keyword arguments
        
        Returns:
            Tuple of (result, MemoryProfile)
        """
        self.start(name)
        self.snapshot(label="start")
        
        try:
            result = await func(*args, **kwargs)
            self.snapshot(label="after_execution")
            return result, self.stop()
        except Exception as e:
            self.snapshot(label="on_error")
            return None, self.stop()
    
    def get_current_usage(self) -> Dict[str, float]:
        """Get current memory usage without starting a full profile."""
        if tracemalloc.is_tracing():
            current, peak = tracemalloc.get_traced_memory()
        else:
            tracemalloc.start()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        
        return {
            "current_mb": round(current / (1024 * 1024), 2),
            "peak_mb": round(peak / (1024 * 1024), 2),
        }


class MemoryProfileContext:
    """Context manager for memory profiling."""
    
    def __init__(self, profiler: MemoryProfiler, name: str):
        self.profiler = profiler
        self.name = name
        self.profile: Optional[MemoryProfile] = None
    
    def __enter__(self):
        self.profiler.start(self.name)
        self.profiler.snapshot(label="context_enter")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.profiler.snapshot(label="context_exit")
        self.profile = self.profiler.stop()
        return False
    
    async def __aenter__(self):
        self.profiler.start(self.name)
        self.profiler.snapshot(label="async_context_enter")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.profiler.snapshot(label="async_context_exit")
        self.profile = self.profiler.stop()
        return False


async def profile_inference(
    inference_func: Callable,
    inputs: List[Any],
    batch_size: int = 1,
    iterations: int = 10
) -> MemoryProfile:
    """
    Profile memory usage for inference operations.
    
    Args:
        inference_func: Async function that performs inference
        inputs: List of inputs to process
        batch_size: Batch size for processing
        iterations: Number of iterations
    
    Returns:
        MemoryProfile with results
    """
    profiler = MemoryProfiler()
    profiler.start("inference_profile")
    
    for i in range(iterations):
        profiler.snapshot(label=f"iteration_{i}_start")
        
        for j in range(0, len(inputs), batch_size):
            batch = inputs[j:j + batch_size]
            await inference_func(batch)
        
        profiler.snapshot(label=f"iteration_{i}_end")
    
    return profiler.stop()
