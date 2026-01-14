"""
Prediction Logger - Async prediction logging.
"""

import logging
import uuid
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from neuralforge.ml.monitoring.schemas import PredictionLog, PredictionInfo
from neuralforge.ml.monitoring.exceptions import PredictionNotFoundError
from neuralforge.db.models.prediction import Prediction

logger = logging.getLogger(__name__)


class PredictionLogger:
    """
    Async prediction logging.
    
    Provides non-blocking prediction logging with batch insert support.
    
    Example:
        ```python
        logger = PredictionLogger(db_session)
        
        # Log single prediction
        await logger.log_prediction(
            PredictionLog(
                model_name="sentiment",
                model_version="1.0.0",
                input_data={"text": "Great!"},
                output_data={"sentiment": "positive"},
                confidence=0.95,
                latency_ms=45.2,
                status="success"
            )
        )
        
        # Query predictions
        predictions = await logger.get_predictions(
            model_name="sentiment",
            limit=100
        )
        ```
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize prediction logger.
        
        Args:
            db: Async database session
        """
        self.db = db

    async def log_prediction(
        self,
        prediction_log: PredictionLog
    ) -> str:
        """
        Log a single prediction.
        
        Args:
            prediction_log: Prediction data
        
        Returns:
            Request ID
        """
        # Generate request ID if not provided
        request_id = prediction_log.request_id or f"req_{uuid.uuid4().hex[:12]}"

        # Create prediction record
        prediction = Prediction(
            model_name=prediction_log.model_name,
            model_version=prediction_log.model_version,
            request_id=request_id,
            user_id=prediction_log.user_id,
            input_data=prediction_log.input_data,
            output_data=prediction_log.output_data,
            prediction_class=prediction_log.prediction_class,
            confidence=prediction_log.confidence,
            latency_ms=prediction_log.latency_ms,
            preprocessing_ms=prediction_log.preprocessing_ms,
            inference_ms=prediction_log.inference_ms,
            postprocessing_ms=prediction_log.postprocessing_ms,
            status=prediction_log.status.value if hasattr(prediction_log.status, 'value') else prediction_log.status,
            error_message=prediction_log.error_message,
            error_type=prediction_log.error_type,
            environment=prediction_log.environment,
            api_version=prediction_log.api_version,
        )

        self.db.add(prediction)
        await self.db.commit()

        logger.debug(f"Logged prediction: {request_id}")

        return request_id

    async def log_batch(
        self,
        predictions: List[PredictionLog]
    ) -> List[str]:
        """
        Batch insert predictions.
        
        Args:
            predictions: List of prediction logs
        
        Returns:
            List of request IDs
        """
        request_ids = []

        for pred_log in predictions:
            request_id = pred_log.request_id or f"req_{uuid.uuid4().hex[:12]}"
            request_ids.append(request_id)

            prediction = Prediction(
                model_name=pred_log.model_name,
                model_version=pred_log.model_version,
                request_id=request_id,
                user_id=pred_log.user_id,
                input_data=pred_log.input_data,
                output_data=pred_log.output_data,
                prediction_class=pred_log.prediction_class,
                confidence=pred_log.confidence,
                latency_ms=pred_log.latency_ms,
                preprocessing_ms=pred_log.preprocessing_ms,
                inference_ms=pred_log.inference_ms,
                postprocessing_ms=pred_log.postprocessing_ms,
                status=pred_log.status.value if hasattr(pred_log.status, 'value') else pred_log.status,
                error_message=pred_log.error_message,
                error_type=pred_log.error_type,
                environment=pred_log.environment,
                api_version=pred_log.api_version,
            )

            self.db.add(prediction)

        await self.db.commit()

        logger.info(f"Batch logged {len(predictions)} predictions")

        return request_ids

    async def get_prediction(
        self,
        prediction_id: int
    ) -> PredictionInfo:
        """
        Get prediction by ID.
        
        Args:
            prediction_id: Prediction ID
        
        Returns:
            Prediction info
        
        Raises:
            PredictionNotFoundError: If prediction not found
        """
        result = await self.db.execute(
            select(Prediction).where(Prediction.id == prediction_id)
        )
        prediction = result.scalar_one_or_none()

        if not prediction:
            raise PredictionNotFoundError(f"Prediction {prediction_id} not found")

        return PredictionInfo.model_validate(prediction)

    async def get_predictions(
        self,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        status: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[PredictionInfo]:
        """
        Query predictions with filters.
        
        Args:
            model_name: Filter by model name
            model_version: Filter by model version
            status: Filter by status
            start_time: Filter by start time
            end_time: Filter by end time
            limit: Maximum results
            offset: Results offset
        
        Returns:
            List of predictions
        """
        query = select(Prediction)

        # Apply filters
        conditions = []
        if model_name:
            conditions.append(Prediction.model_name == model_name)
        if model_version:
            conditions.append(Prediction.model_version == model_version)
        if status:
            conditions.append(Prediction.status == status)
        if start_time:
            conditions.append(Prediction.created_at >= start_time)
        if end_time:
            conditions.append(Prediction.created_at <= end_time)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.order_by(Prediction.created_at.desc())
        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        predictions = result.scalars().all()

        return [PredictionInfo.model_validate(p) for p in predictions]

    async def get_prediction_count(
        self,
        model_name: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        status: Optional[str] = None
    ) -> int:
        """
        Get count of predictions matching filters.
        
        Args:
            model_name: Filter by model name
            start_time: Filter by start time
            end_time: Filter by end time
            status: Filter by status
        
        Returns:
            Count of predictions
        """
        query = select(func.count(Prediction.id))

        conditions = []
        if model_name:
            conditions.append(Prediction.model_name == model_name)
        if start_time:
            conditions.append(Prediction.created_at >= start_time)
        if end_time:
            conditions.append(Prediction.created_at <= end_time)
        if status:
            conditions.append(Prediction.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.db.execute(query)
        return result.scalar()

    async def delete_old_predictions(
        self,
        days: int = 30
    ) -> int:
        """
        Delete predictions older than specified days.
        
        Args:
            days: Number of days to keep
        
        Returns:
            Number of deleted predictions
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        result = await self.db.execute(
            select(Prediction).where(Prediction.created_at < cutoff_date)
        )
        predictions = result.scalars().all()

        count = len(predictions)
        for prediction in predictions:
            await self.db.delete(prediction)

        await self.db.commit()

        logger.info(f"Deleted {count} predictions older than {days} days")

        return count
