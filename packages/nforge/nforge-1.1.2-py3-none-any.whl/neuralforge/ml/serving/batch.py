"""
Batch Predictor - Efficient batch prediction with dynamic batching.
"""

import logging
import asyncio
from typing import Any, List, Dict
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class BatchPredictor:
    """
    Batch prediction with dynamic batching.
    
    Collects individual prediction requests and batches them together
    for efficient processing.
    
    Example:
        ```python
        predictor = BatchPredictor(
            model=model,
            batch_size=32,
            timeout_ms=100
        )
        
        # Add requests (they will be batched automatically)
        future1 = predictor.predict_async(input1)
        future2 = predictor.predict_async(input2)
        
        # Get results
        result1 = await future1
        result2 = await future2
        ```
    """

    def __init__(
        self,
        model: Any = None,
        batch_size: int = 32,
        timeout_ms: int = 100,
        max_queue_size: int = 1000
    ):
        """
        Initialize batch predictor.
        
        Args:
            model: Model to use for predictions
            batch_size: Maximum batch size
            timeout_ms: Maximum wait time before processing batch
            max_queue_size: Maximum queue size
        """
        self.model = model
        self.batch_size = batch_size
        self.timeout_ms = timeout_ms / 1000.0  # Convert to seconds
        self.max_queue_size = max_queue_size

        self._queue: List[Dict[str, Any]] = []
        self._lock = asyncio.Lock()
        self._processing = False

        logger.info(f"BatchPredictor initialized: batch_size={batch_size}, timeout_ms={timeout_ms}")

    async def predict_async(self, input_data: Any) -> Any:
        """
        Async prediction with automatic batching.
        
        Args:
            input_data: Input for prediction
        
        Returns:
            Prediction result
        """
        # Create request
        request_id = str(uuid.uuid4())
        future = asyncio.Future()

        request = {
            'id': request_id,
            'input': input_data,
            'future': future,
            'timestamp': datetime.now()
        }

        # Add to queue
        async with self._lock:
            if len(self._queue) >= self.max_queue_size:
                raise RuntimeError("Batch queue is full")

            self._queue.append(request)

            # Trigger processing if batch is full
            if len(self._queue) >= self.batch_size:
                asyncio.create_task(self._process_batch())
            elif not self._processing:
                # Start timeout timer
                asyncio.create_task(self._process_after_timeout())

        # Wait for result
        return await future

    async def _process_after_timeout(self):
        """Process batch after timeout."""
        await asyncio.sleep(self.timeout_ms)

        async with self._lock:
            if self._queue and not self._processing:
                asyncio.create_task(self._process_batch())

    async def _process_batch(self):
        """Process current batch."""
        async with self._lock:
            if self._processing or not self._queue:
                return

            self._processing = True

            # Get batch
            batch_requests = self._queue[:self.batch_size]
            self._queue = self._queue[self.batch_size:]

        try:
            # Extract inputs
            inputs = [req['input'] for req in batch_requests]

            # Run batch prediction
            if self.model:
                results = await self._run_batch_prediction(inputs)
            else:
                # Mock results if no model
                results = [{'prediction': f'result_{i}'} for i in range(len(inputs))]

            # Set results
            for request, result in zip(batch_requests, results, strict=True):
                request['future'].set_result(result)

        except Exception as e:
            logger.error(f"Batch prediction failed: {e}")
            # Set exception for all requests
            for request in batch_requests:
                request['future'].set_exception(e)

        finally:
            async with self._lock:
                self._processing = False

                # Process remaining queue if needed
                if self._queue:
                    asyncio.create_task(self._process_batch())

    async def _run_batch_prediction(self, inputs: List[Any]) -> List[Any]:
        """
        Run batch prediction on model.
        
        Args:
            inputs: List of inputs
        
        Returns:
            List of predictions
        """
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()

        def predict():
            if hasattr(self.model, 'predict_batch'):
                return self.model.predict_batch(inputs)
            else:
                # Fallback to individual predictions
                return [self.model(inp) for inp in inputs]

        return await loop.run_in_executor(None, predict)

    def predict_batch(self, inputs: List[Any]) -> List[Any]:
        """
        Synchronous batch prediction.
        
        Args:
            inputs: List of inputs
        
        Returns:
            List of predictions
        """
        if not self.model:
            return [{'prediction': f'result_{i}'} for i in range(len(inputs))]

        if hasattr(self.model, 'predict_batch'):
            return self.model.predict_batch(inputs)
        else:
            # Fallback to individual predictions
            return [self.model(inp) for inp in inputs]

    def get_stats(self) -> Dict[str, Any]:
        """
        Get batch predictor statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            'queue_size': len(self._queue),
            'max_queue_size': self.max_queue_size,
            'batch_size': self.batch_size,
            'timeout_ms': self.timeout_ms * 1000,
            'processing': self._processing
        }
