"""
Baseline Manager - Manage drift detection baselines.
"""

import logging
import numpy as np
import pandas as pd
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from neuralforge.ml.drift.schemas import BaselineCreate, BaselineInfo
from neuralforge.ml.drift.exceptions import BaselineNotFoundError, InsufficientDataError
from neuralforge.db.models.drift_baseline import DriftBaseline

logger = logging.getLogger(__name__)


class BaselineManager:
    """
    Manage drift detection baselines.
    
    Example:
        ```python
        manager = BaselineManager(db_session)
        
        # Create baseline from training data
        data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': ['a', 'b', 'a', 'c', 'b']
        })
        
        await manager.create_baseline_from_dataframe(
            model_name="sentiment",
            model_version="1.0.0",
            baseline_name="production_v1",
            data=data
        )
        ```
    """

    def __init__(self, db: AsyncSession):
        """Initialize baseline manager."""
        self.db = db

    async def create_baseline(
        self,
        baseline_data: BaselineCreate
    ) -> BaselineInfo:
        """Create a single baseline."""
        baseline = DriftBaseline(
            model_name=baseline_data.model_name,
            model_version=baseline_data.model_version,
            baseline_name=baseline_data.baseline_name,
            feature_name=baseline_data.feature_name,
            distribution_type=baseline_data.distribution_type.value,
            distribution_data=baseline_data.distribution_data,
            mean=baseline_data.mean,
            std_dev=baseline_data.std_dev,
            min_value=baseline_data.min_value,
            max_value=baseline_data.max_value,
            percentiles=baseline_data.percentiles,
            categories=baseline_data.categories,
            sample_size=baseline_data.sample_size,
        )

        self.db.add(baseline)
        await self.db.commit()
        await self.db.refresh(baseline)

        logger.info(f"Created baseline: {baseline_data.baseline_name} for {baseline_data.feature_name}")

        return BaselineInfo.model_validate(baseline)

    async def create_baseline_from_dataframe(
        self,
        model_name: str,
        model_version: str,
        baseline_name: str,
        data: pd.DataFrame,
        features: Optional[List[str]] = None
    ) -> List[BaselineInfo]:
        """
        Create baselines from DataFrame.
        
        Args:
            model_name: Model name
            model_version: Model version
            baseline_name: Baseline name
            data: DataFrame with features
            features: Specific features (None = all columns)
        
        Returns:
            List of created baselines
        """
        if len(data) < 2:
            raise InsufficientDataError("Need at least 2 samples to create baseline")

        features_to_process = features or list(data.columns)
        baselines = []

        for feature in features_to_process:
            if feature not in data.columns:
                logger.warning(f"Feature {feature} not in data, skipping")
                continue

            values = data[feature].dropna()

            if len(values) < 2:
                logger.warning(f"Insufficient data for feature {feature}, skipping")
                continue

            # Determine distribution type
            if pd.api.types.is_numeric_dtype(values):
                baseline_data = self._create_numerical_baseline(
                    model_name, model_version, baseline_name, feature, values
                )
            else:
                baseline_data = self._create_categorical_baseline(
                    model_name, model_version, baseline_name, feature, values
                )

            baseline_info = await self.create_baseline(baseline_data)
            baselines.append(baseline_info)

        logger.info(f"Created {len(baselines)} baselines for {baseline_name}")

        return baselines

    def _create_numerical_baseline(
        self,
        model_name: str,
        model_version: str,
        baseline_name: str,
        feature_name: str,
        values: pd.Series
    ) -> BaselineCreate:
        """Create baseline for numerical feature."""
        arr = values.to_numpy()

        # Calculate statistics
        mean = float(np.mean(arr))
        std_dev = float(np.std(arr))
        min_val = float(np.min(arr))
        max_val = float(np.max(arr))

        # Calculate percentiles
        percentiles = {
            'p25': float(np.percentile(arr, 25)),
            'p50': float(np.percentile(arr, 50)),
            'p75': float(np.percentile(arr, 75)),
            'p90': float(np.percentile(arr, 90)),
            'p95': float(np.percentile(arr, 95)),
            'p99': float(np.percentile(arr, 99)),
        }

        # Create histogram
        counts, bin_edges = np.histogram(arr, bins=20)
        distribution_data = {
            'bins': bin_edges.tolist(),
            'counts': counts.tolist()
        }

        return BaselineCreate(
            model_name=model_name,
            model_version=model_version,
            baseline_name=baseline_name,
            feature_name=feature_name,
            distribution_type="numerical",
            distribution_data=distribution_data,
            mean=mean,
            std_dev=std_dev,
            min_value=min_val,
            max_value=max_val,
            percentiles=percentiles,
            sample_size=len(arr)
        )

    def _create_categorical_baseline(
        self,
        model_name: str,
        model_version: str,
        baseline_name: str,
        feature_name: str,
        values: pd.Series
    ) -> BaselineCreate:
        """Create baseline for categorical feature."""
        # Count categories
        value_counts = values.value_counts().to_dict()
        categories = {str(k): int(v) for k, v in value_counts.items()}

        # Create distribution data
        distribution_data = {
            'categories': categories,
            'total': len(values)
        }

        return BaselineCreate(
            model_name=model_name,
            model_version=model_version,
            baseline_name=baseline_name,
            feature_name=feature_name,
            distribution_type="categorical",
            distribution_data=distribution_data,
            categories=categories,
            sample_size=len(values)
        )

    async def get_baseline(
        self,
        model_name: str,
        baseline_name: str,
        feature_name: Optional[str] = None
    ) -> List[DriftBaseline]:
        """Get baseline(s) for model."""
        query = select(DriftBaseline).where(
            and_(
                DriftBaseline.model_name == model_name,
                DriftBaseline.baseline_name == baseline_name
            )
        )

        if feature_name:
            query = query.where(DriftBaseline.feature_name == feature_name)

        result = await self.db.execute(query)
        baselines = result.scalars().all()

        if not baselines:
            raise BaselineNotFoundError(
                f"Baseline '{baseline_name}' not found for model '{model_name}'"
            )

        return list(baselines)

    async def list_baselines(
        self,
        model_name: Optional[str] = None
    ) -> List[BaselineInfo]:
        """List all baselines."""
        query = select(DriftBaseline)

        if model_name:
            query = query.where(DriftBaseline.model_name == model_name)

        result = await self.db.execute(query)
        baselines = result.scalars().all()

        return [BaselineInfo.model_validate(b) for b in baselines]

    async def delete_baseline(
        self,
        baseline_id: int
    ) -> bool:
        """Delete a baseline."""
        result = await self.db.execute(
            select(DriftBaseline).where(DriftBaseline.id == baseline_id)
        )
        baseline = result.scalar_one_or_none()

        if not baseline:
            return False

        await self.db.delete(baseline)
        await self.db.commit()

        logger.info(f"Deleted baseline {baseline_id}")

        return True
