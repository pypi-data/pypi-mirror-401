"""
REST API routes for batch prediction.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import uuid

from neuralforge.ml.serving.batch import BatchPredictor

router = APIRouter(prefix="/api/predict", tags=["Batch Prediction"])

# Global batch predictor instance
_batch_predictor = None


class BatchPredictionRequest(BaseModel):
    """Batch prediction request."""
    inputs: List[Any]
    batch_size: Optional[int] = 32

    model_config = {"json_schema_extra": {
        "example": {
            "inputs": [
                {"text": "Great product!"},
                {"text": "Not good"},
                {"text": "Amazing!"}
            ],
            "batch_size": 32
        }
    }}


class BatchPredictionResponse(BaseModel):
    """Batch prediction response."""
    batch_id: str
    predictions: List[Any]
    batch_size: int

    model_config = {"json_schema_extra": {
        "example": {
            "batch_id": "batch_123",
            "predictions": [
                {"sentiment": "positive"},
                {"sentiment": "negative"},
                {"sentiment": "positive"}
            ],
            "batch_size": 3
        }
    }}


def get_batch_predictor() -> BatchPredictor:
    """Get batch predictor instance."""
    global _batch_predictor
    if _batch_predictor is None:
        _batch_predictor = BatchPredictor()
    return _batch_predictor


@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    request: BatchPredictionRequest,
    predictor: BatchPredictor = Depends(get_batch_predictor)
):
    """
    Batch prediction endpoint.
    
    Processes multiple inputs in a single request.
    """
    try:
        # Process batch
        predictions = predictor.predict_batch(request.inputs)

        batch_id = str(uuid.uuid4())

        return BatchPredictionResponse(
            batch_id=batch_id,
            predictions=predictions,
            batch_size=len(predictions)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


@router.get("/batch/stats")
async def get_batch_stats(
    predictor: BatchPredictor = Depends(get_batch_predictor)
) -> Dict[str, Any]:
    """Get batch predictor statistics."""
    return predictor.get_stats()
