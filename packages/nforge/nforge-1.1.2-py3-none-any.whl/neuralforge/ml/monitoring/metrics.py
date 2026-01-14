"""
Metrics Collector - Collect and analyze prediction metrics.
"""

import logging
import numpy as np
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from neuralforge.ml.monitoring.schemas import (
    LatencyStats,
    ThroughputStats,
    ErrorStats,
    ConfidenceDistribution,
    MetricsSummary,
)
from neuralforge.ml.monitoring.exceptions import InvalidTimeRangeError, MetricsNotAvailableError
from neuralforge.db.models.prediction import Prediction

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Collect and analyze prediction metrics.
    
    Provides methods for calculating latency, throughput, error rates,
    and confidence distributions.
    
    Example:
        ```python
        metrics = MetricsCollector(db_session)
        
        # Get latency stats
        latency = await metrics.get_latency_stats("sentiment", "1h")
        print(f"P95 latency: {latency.p95}ms")
        
        # Get throughput
        throughput = await metrics.get_throughput("sentiment", "1h")
        print(f"RPS: {throughput.requests_per_second}")
        
        # Get error rate
        errors = await metrics.get_error_stats("sentiment", "1h")
        print(f"Error rate: {errors.error_rate:.2%}")
        ```
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize metrics collector.
        
        Args:
            db: Async database session
        """
        self.db = db

    def _parse_time_range(self, time_range: str) -> timedelta:
        """
        Parse time range string to timedelta.
        
        Args:
            time_range: Time range (e.g., "1h", "24h", "7d")
        
        Returns:
            Timedelta object
        
        Raises:
            InvalidTimeRangeError: If time range is invalid
        """
        try:
            if time_range.endswith('m'):
                return timedelta(minutes=int(time_range[:-1]))
            elif time_range.endswith('h'):
                return timedelta(hours=int(time_range[:-1]))
            elif time_range.endswith('d'):
                return timedelta(days=int(time_range[:-1]))
            else:
                raise ValueError("Invalid time range format")
        except (ValueError, IndexError):
            raise InvalidTimeRangeError(
                f"Invalid time range: {time_range}. Use format like '1h', '24h', '7d'"
            )

    async def get_latency_stats(
        self,
        model_name: str,
        time_range: str = "1h",
        model_version: Optional[str] = None
    ) -> LatencyStats:
        """
        Get latency statistics.
        
        Args:
            model_name: Model name
            time_range: Time range (e.g., "1h", "24h")
            model_version: Optional model version
        
        Returns:
            Latency statistics
        """
        delta = self._parse_time_range(time_range)
        start_time = datetime.utcnow() - delta

        # Query latencies
        query = select(Prediction.latency_ms).where(
            and_(
                Prediction.model_name == model_name,
                Prediction.created_at >= start_time,
                Prediction.status == "success"
            )
        )

        if model_version:
            query = query.where(Prediction.model_version == model_version)

        result = await self.db.execute(query)
        latencies = [float(lat) for lat in result.scalars().all()]

        if not latencies:
            raise MetricsNotAvailableError(
                f"No latency data available for {model_name} in {time_range}"
            )

        # Calculate percentiles
        p50 = float(np.percentile(latencies, 50))
        p95 = float(np.percentile(latencies, 95))
        p99 = float(np.percentile(latencies, 99))

        return LatencyStats(
            avg=float(np.mean(latencies)),
            p50=p50,
            p95=p95,
            p99=p99,
            max=float(np.max(latencies)),
            sample_size=len(latencies)
        )

    async def get_throughput(
        self,
        model_name: str,
        time_range: str = "1h",
        model_version: Optional[str] = None
    ) -> ThroughputStats:
        """
        Get throughput statistics.
        
        Args:
            model_name: Model name
            time_range: Time range
            model_version: Optional model version
        
        Returns:
            Throughput statistics
        """
        delta = self._parse_time_range(time_range)
        start_time = datetime.utcnow() - delta

        # Count predictions
        query = select(func.count(Prediction.id)).where(
            and_(
                Prediction.model_name == model_name,
                Prediction.created_at >= start_time
            )
        )

        if model_version:
            query = query.where(Prediction.model_version == model_version)

        result = await self.db.execute(query)
        total_requests = result.scalar()

        # Calculate RPS
        total_seconds = delta.total_seconds()
        requests_per_second = total_requests / total_seconds if total_seconds > 0 else 0.0

        return ThroughputStats(
            requests_per_second=requests_per_second,
            total_requests=total_requests,
            time_range=time_range
        )

    async def get_error_stats(
        self,
        model_name: str,
        time_range: str = "1h",
        model_version: Optional[str] = None
    ) -> ErrorStats:
        """
        Get error statistics.
        
        Args:
            model_name: Model name
            time_range: Time range
            model_version: Optional model version
        
        Returns:
            Error statistics
        """
        delta = self._parse_time_range(time_range)
        start_time = datetime.utcnow() - delta

        # Count total requests
        total_query = select(func.count(Prediction.id)).where(
            and_(
                Prediction.model_name == model_name,
                Prediction.created_at >= start_time
            )
        )

        if model_version:
            total_query = total_query.where(Prediction.model_version == model_version)

        result = await self.db.execute(total_query)
        total_requests = result.scalar()

        # Count errors
        error_query = select(func.count(Prediction.id)).where(
            and_(
                Prediction.model_name == model_name,
                Prediction.created_at >= start_time,
                Prediction.status.in_(["error", "timeout"])
            )
        )

        if model_version:
            error_query = error_query.where(Prediction.model_version == model_version)

        result = await self.db.execute(error_query)
        total_errors = result.scalar()

        # Get error types
        error_types_query = select(
            Prediction.error_type,
            func.count(Prediction.id)
        ).where(
            and_(
                Prediction.model_name == model_name,
                Prediction.created_at >= start_time,
                Prediction.error_type.isnot(None)
            )
        ).group_by(Prediction.error_type)

        if model_version:
            error_types_query = error_types_query.where(Prediction.model_version == model_version)

        result = await self.db.execute(error_types_query)
        error_types = {row[0]: row[1] for row in result.all()}

        # Calculate error rate
        error_rate = total_errors / total_requests if total_requests > 0 else 0.0

        return ErrorStats(
            error_rate=error_rate,
            total_errors=total_errors,
            total_requests=total_requests,
            error_types=error_types
        )

    async def get_confidence_distribution(
        self,
        model_name: str,
        time_range: str = "1h",
        model_version: Optional[str] = None
    ) -> ConfidenceDistribution:
        """
        Get confidence distribution statistics.
        
        Args:
            model_name: Model name
            time_range: Time range
            model_version: Optional model version
        
        Returns:
            Confidence distribution
        """
        delta = self._parse_time_range(time_range)
        start_time = datetime.utcnow() - delta

        # Query confidences
        query = select(Prediction.confidence).where(
            and_(
                Prediction.model_name == model_name,
                Prediction.created_at >= start_time,
                Prediction.confidence.isnot(None),
                Prediction.status == "success"
            )
        )

        if model_version:
            query = query.where(Prediction.model_version == model_version)

        result = await self.db.execute(query)
        confidences = [float(conf) for conf in result.scalars().all()]

        if not confidences:
            raise MetricsNotAvailableError(
                f"No confidence data available for {model_name} in {time_range}"
            )

        # Calculate distribution
        low_count = sum(1 for c in confidences if c < 0.5)
        medium_count = sum(1 for c in confidences if 0.5 <= c <= 0.8)
        high_count = sum(1 for c in confidences if c > 0.8)

        return ConfidenceDistribution(
            avg_confidence=float(np.mean(confidences)),
            min_confidence=float(np.min(confidences)),
            max_confidence=float(np.max(confidences)),
            low_confidence_count=low_count,
            medium_confidence_count=medium_count,
            high_confidence_count=high_count
        )

    async def get_metrics_summary(
        self,
        model_name: str,
        time_range: str = "1h",
        model_version: Optional[str] = None
    ) -> MetricsSummary:
        """
        Get overall metrics summary.
        
        Args:
            model_name: Model name
            time_range: Time range
            model_version: Optional model version
        
        Returns:
            Complete metrics summary
        """
        delta = self._parse_time_range(time_range)
        start_time = datetime.utcnow() - delta

        # Get counts
        total_query = select(func.count(Prediction.id)).where(
            and_(
                Prediction.model_name == model_name,
                Prediction.created_at >= start_time
            )
        )

        if model_version:
            total_query = total_query.where(Prediction.model_version == model_version)

        result = await self.db.execute(total_query)
        total_predictions = result.scalar()

        # Get successful count
        success_query = select(func.count(Prediction.id)).where(
            and_(
                Prediction.model_name == model_name,
                Prediction.created_at >= start_time,
                Prediction.status == "success"
            )
        )

        if model_version:
            success_query = success_query.where(Prediction.model_version == model_version)

        result = await self.db.execute(success_query)
        successful_predictions = result.scalar()

        failed_predictions = total_predictions - successful_predictions

        # Get individual metrics
        latency = await self.get_latency_stats(model_name, time_range, model_version)
        throughput = await self.get_throughput(model_name, time_range, model_version)
        errors = await self.get_error_stats(model_name, time_range, model_version)

        # Try to get confidence distribution
        try:
            confidence = await self.get_confidence_distribution(model_name, time_range, model_version)
        except MetricsNotAvailableError:
            confidence = None

        return MetricsSummary(
            model_name=model_name,
            model_version=model_version,
            time_range=time_range,
            total_predictions=total_predictions,
            successful_predictions=successful_predictions,
            failed_predictions=failed_predictions,
            latency=latency,
            throughput=throughput,
            errors=errors,
            confidence=confidence
        )
