"""
Auto-scaling Support for NeuralForge Kubernetes Deployments.

Provides custom scaling logic and metrics integration.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ScalingDirection(Enum):
    """Direction of scaling action."""
    UP = "up"
    DOWN = "down"
    NONE = "none"


@dataclass
class ScalingMetrics:
    """Metrics used for scaling decisions."""
    cpu_utilization: float = 0.0
    memory_utilization: float = 0.0
    request_rate: float = 0.0  # requests per second
    average_latency_ms: float = 0.0
    queue_depth: int = 0
    gpu_utilization: float = 0.0
    concurrent_requests: int = 0
    
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cpu_utilization": self.cpu_utilization,
            "memory_utilization": self.memory_utilization,
            "request_rate": self.request_rate,
            "average_latency_ms": self.average_latency_ms,
            "queue_depth": self.queue_depth,
            "gpu_utilization": self.gpu_utilization,
            "concurrent_requests": self.concurrent_requests,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ScalingPolicy:
    """
    Policy for scaling decisions.
    
    Defines thresholds and behavior for auto-scaling.
    """
    # CPU thresholds
    cpu_scale_up_threshold: float = 80.0
    cpu_scale_down_threshold: float = 30.0
    
    # Memory thresholds
    memory_scale_up_threshold: float = 85.0
    memory_scale_down_threshold: float = 40.0
    
    # Latency thresholds (in ms)
    latency_scale_up_threshold: float = 500.0
    latency_scale_down_threshold: float = 100.0
    
    # Queue thresholds
    queue_scale_up_threshold: int = 10
    queue_scale_down_threshold: int = 0
    
    # Scaling behavior
    scale_up_step: int = 2  # Add this many replicas
    scale_down_step: int = 1  # Remove this many replicas
    
    # Cooldowns (seconds)
    scale_up_cooldown: int = 60
    scale_down_cooldown: int = 300
    
    # Replica limits
    min_replicas: int = 1
    max_replicas: int = 10
    
    # Custom metric weights (for combined scoring)
    cpu_weight: float = 0.4
    memory_weight: float = 0.2
    latency_weight: float = 0.3
    queue_weight: float = 0.1


@dataclass
class ScalingDecision:
    """Result of a scaling decision."""
    direction: ScalingDirection
    current_replicas: int
    desired_replicas: int
    reason: str
    metrics: ScalingMetrics
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def should_scale(self) -> bool:
        return self.direction != ScalingDirection.NONE
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "direction": self.direction.value,
            "current_replicas": self.current_replicas,
            "desired_replicas": self.desired_replicas,
            "reason": self.reason,
            "should_scale": self.should_scale,
            "timestamp": self.timestamp.isoformat(),
        }


class AutoScaler:
    """
    Custom auto-scaler for NeuralForge deployments.
    
    Provides intelligent scaling based on multiple metrics
    beyond standard CPU/memory utilization.
    
    Example:
        ```python
        from neuralforge.kubernetes import AutoScaler, ScalingPolicy
        
        scaler = AutoScaler(policy=ScalingPolicy(
            cpu_scale_up_threshold=75,
            max_replicas=20
        ))
        
        metrics = await scaler.collect_metrics(deployment_name)
        decision = scaler.evaluate(metrics, current_replicas=3)
        
        if decision.should_scale:
            await scaler.apply_decision(decision)
        ```
    """
    
    def __init__(
        self,
        policy: ScalingPolicy = None,
        metrics_collector: Optional[Callable] = None
    ):
        self.policy = policy or ScalingPolicy()
        self.metrics_collector = metrics_collector
        
        self._last_scale_up: Optional[datetime] = None
        self._last_scale_down: Optional[datetime] = None
        self._metrics_history: List[ScalingMetrics] = []
        self._max_history = 100
    
    async def collect_metrics(
        self,
        deployment_name: str,
        namespace: str = "default"
    ) -> ScalingMetrics:
        """
        Collect current metrics for a deployment.
        
        Args:
            deployment_name: Name of the deployment
            namespace: Kubernetes namespace
        
        Returns:
            Current scaling metrics
        """
        if self.metrics_collector:
            return await self.metrics_collector(deployment_name, namespace)
        
        # Default mock metrics (would integrate with Prometheus in production)
        metrics = ScalingMetrics(
            cpu_utilization=0.0,
            memory_utilization=0.0,
            request_rate=0.0,
            average_latency_ms=0.0,
        )
        
        # Store in history
        self._metrics_history.append(metrics)
        if len(self._metrics_history) > self._max_history:
            self._metrics_history.pop(0)
        
        return metrics
    
    def evaluate(
        self,
        metrics: ScalingMetrics,
        current_replicas: int
    ) -> ScalingDecision:
        """
        Evaluate metrics and determine scaling action.
        
        Args:
            metrics: Current metrics
            current_replicas: Current replica count
        
        Returns:
            Scaling decision
        """
        reasons = []
        should_scale_up = False
        should_scale_down = True  # Assume we can scale down unless proven otherwise
        
        # Check CPU
        if metrics.cpu_utilization >= self.policy.cpu_scale_up_threshold:
            should_scale_up = True
            reasons.append(f"CPU at {metrics.cpu_utilization:.1f}%")
        if metrics.cpu_utilization > self.policy.cpu_scale_down_threshold:
            should_scale_down = False
        
        # Check memory
        if metrics.memory_utilization >= self.policy.memory_scale_up_threshold:
            should_scale_up = True
            reasons.append(f"Memory at {metrics.memory_utilization:.1f}%")
        if metrics.memory_utilization > self.policy.memory_scale_down_threshold:
            should_scale_down = False
        
        # Check latency
        if metrics.average_latency_ms >= self.policy.latency_scale_up_threshold:
            should_scale_up = True
            reasons.append(f"Latency at {metrics.average_latency_ms:.0f}ms")
        if metrics.average_latency_ms > self.policy.latency_scale_down_threshold:
            should_scale_down = False
        
        # Check queue depth
        if metrics.queue_depth >= self.policy.queue_scale_up_threshold:
            should_scale_up = True
            reasons.append(f"Queue depth at {metrics.queue_depth}")
        if metrics.queue_depth > self.policy.queue_scale_down_threshold:
            should_scale_down = False
        
        # Determine direction
        now = datetime.utcnow()
        
        if should_scale_up:
            # Check cooldown
            if self._last_scale_up:
                elapsed = (now - self._last_scale_up).total_seconds()
                if elapsed < self.policy.scale_up_cooldown:
                    return ScalingDecision(
                        direction=ScalingDirection.NONE,
                        current_replicas=current_replicas,
                        desired_replicas=current_replicas,
                        reason=f"Scale up cooldown ({elapsed:.0f}s / {self.policy.scale_up_cooldown}s)",
                        metrics=metrics,
                    )
            
            desired = min(
                current_replicas + self.policy.scale_up_step,
                self.policy.max_replicas
            )
            
            if desired > current_replicas:
                return ScalingDecision(
                    direction=ScalingDirection.UP,
                    current_replicas=current_replicas,
                    desired_replicas=desired,
                    reason="; ".join(reasons),
                    metrics=metrics,
                )
            else:
                return ScalingDecision(
                    direction=ScalingDirection.NONE,
                    current_replicas=current_replicas,
                    desired_replicas=desired,
                    reason="At max replicas",
                    metrics=metrics,
                )
        
        elif should_scale_down and current_replicas > self.policy.min_replicas:
            # Check cooldown
            if self._last_scale_down:
                elapsed = (now - self._last_scale_down).total_seconds()
                if elapsed < self.policy.scale_down_cooldown:
                    return ScalingDecision(
                        direction=ScalingDirection.NONE,
                        current_replicas=current_replicas,
                        desired_replicas=current_replicas,
                        reason=f"Scale down cooldown ({elapsed:.0f}s / {self.policy.scale_down_cooldown}s)",
                        metrics=metrics,
                    )
            
            desired = max(
                current_replicas - self.policy.scale_down_step,
                self.policy.min_replicas
            )
            
            return ScalingDecision(
                direction=ScalingDirection.DOWN,
                current_replicas=current_replicas,
                desired_replicas=desired,
                reason="Low resource utilization",
                metrics=metrics,
            )
        
        return ScalingDecision(
            direction=ScalingDirection.NONE,
            current_replicas=current_replicas,
            desired_replicas=current_replicas,
            reason="Metrics within normal range",
            metrics=metrics,
        )
    
    def calculate_score(self, metrics: ScalingMetrics) -> float:
        """
        Calculate a combined scaling score.
        
        Score > 1.0 suggests scale up
        Score < 1.0 suggests scale down
        
        Args:
            metrics: Current metrics
        
        Returns:
            Combined score
        """
        # Normalize metrics to 0-1 scale based on thresholds
        cpu_score = metrics.cpu_utilization / self.policy.cpu_scale_up_threshold
        memory_score = metrics.memory_utilization / self.policy.memory_scale_up_threshold
        latency_score = metrics.average_latency_ms / self.policy.latency_scale_up_threshold
        queue_score = metrics.queue_depth / max(self.policy.queue_scale_up_threshold, 1)
        
        # Weighted average
        score = (
            cpu_score * self.policy.cpu_weight +
            memory_score * self.policy.memory_weight +
            latency_score * self.policy.latency_weight +
            queue_score * self.policy.queue_weight
        )
        
        return score
    
    def record_scale_event(self, direction: ScalingDirection):
        """Record that a scaling event occurred."""
        now = datetime.utcnow()
        if direction == ScalingDirection.UP:
            self._last_scale_up = now
        elif direction == ScalingDirection.DOWN:
            self._last_scale_down = now
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of recent metrics."""
        if not self._metrics_history:
            return {}
        
        recent = self._metrics_history[-10:]
        
        return {
            "sample_count": len(recent),
            "avg_cpu": sum(m.cpu_utilization for m in recent) / len(recent),
            "avg_memory": sum(m.memory_utilization for m in recent) / len(recent),
            "avg_latency": sum(m.average_latency_ms for m in recent) / len(recent),
            "max_queue": max(m.queue_depth for m in recent),
        }
