"""
Drift Detector - Detect data and concept drift.
"""

import logging
import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from neuralforge.ml.drift.schemas import (
    DriftDetectionResult,
    FeatureDriftResult,
    DriftSeverity,
)
from neuralforge.ml.drift.baseline import BaselineManager
from neuralforge.ml.drift.tests import StatisticalTests
from neuralforge.ml.drift.exceptions import BaselineNotFoundError, InsufficientDataError
from neuralforge.db.models.drift_baseline import DriftBaseline
from neuralforge.db.models.drift_detection import DriftDetection

logger = logging.getLogger(__name__)


class DriftDetector:
    """
    Drift detection for ML models.
    
    Example:
        ```python
        detector = DriftDetector(db_session)
        
        # Detect drift
        current_data = pd.DataFrame({
            'feature1': [1, 2, 3],
            'feature2': ['a', 'b', 'c']
        })
        
        result = await detector.detect_drift(
            model_name="sentiment",
            baseline_name="production_v1",
            current_data=current_data
        )
        
        if result.drift_detected:
            print(f"Drift severity: {result.drift_severity}")
        ```
    """

    def __init__(self, db: AsyncSession):
        """Initialize drift detector."""
        self.db = db
        self.baseline_mgr = BaselineManager(db)
        self.tests = StatisticalTests()

    async def detect_drift(
        self,
        model_name: str,
        baseline_name: str,
        current_data: pd.DataFrame,
        features: Optional[List[str]] = None,
        detection_window: Optional[str] = None
    ) -> DriftDetectionResult:
        """
        Detect drift in current data vs baseline.
        
        Args:
            model_name: Model name
            baseline_name: Baseline name
            current_data: Current data to check
            features: Specific features to check (None = all)
            detection_window: Time window (e.g., '24h')
        
        Returns:
            Drift detection result
        """
        if len(current_data) < 2:
            raise InsufficientDataError("Need at least 2 samples for drift detection")

        # Get baselines
        baselines = await self.baseline_mgr.get_baseline(model_name, baseline_name)

        if not baselines:
            raise BaselineNotFoundError(f"No baselines found for {model_name}/{baseline_name}")

        # Filter features
        features_to_check = features or [b.feature_name for b in baselines]

        # Detect drift for each feature
        feature_results = []
        for baseline in baselines:
            if baseline.feature_name not in features_to_check:
                continue

            if baseline.feature_name not in current_data.columns:
                logger.warning(f"Feature {baseline.feature_name} not in current data, skipping")
                continue

            current_values = current_data[baseline.feature_name].dropna()

            if len(current_values) < 2:
                logger.warning(f"Insufficient data for {baseline.feature_name}, skipping")
                continue

            feature_result = await self._detect_feature_drift(baseline, current_values)
            feature_results.append(feature_result)

            # Save detection to database
            await self._save_detection(
                model_name=model_name,
                model_version=baseline.model_version,
                baseline_name=baseline_name,
                feature_result=feature_result,
                detection_window=detection_window
            )

        # Calculate overall drift
        overall_drift = self._calculate_overall_drift(feature_results)

        # Save overall detection
        await self._save_overall_detection(
            model_name=model_name,
            model_version=baselines[0].model_version,
            baseline_name=baseline_name,
            overall_drift=overall_drift,
            sample_size=len(current_data),
            detection_window=detection_window
        )

        await self.db.commit()

        return DriftDetectionResult(
            model_name=model_name,
            model_version=baselines[0].model_version,
            baseline_name=baseline_name,
            drift_detected=overall_drift['drift_detected'],
            drift_severity=DriftSeverity(overall_drift['severity']),
            overall_psi=overall_drift['psi'],
            feature_results=feature_results,
            sample_size=len(current_data),
            detection_window=detection_window,
            detected_at=datetime.now()
        )

    async def _detect_feature_drift(
        self,
        baseline: DriftBaseline,
        current_values: pd.Series
    ) -> FeatureDriftResult:
        """Detect drift for a single feature."""
        current_array = current_values.to_numpy()

        if baseline.distribution_type == "numerical":
            return self._detect_numerical_drift(baseline, current_array)
        else:
            return self._detect_categorical_drift(baseline, current_values)

    def _detect_numerical_drift(
        self,
        baseline: DriftBaseline,
        current_values: np.ndarray
    ) -> FeatureDriftResult:
        """Detect drift for numerical feature."""
        # Reconstruct baseline distribution
        baseline_data = baseline.distribution_data
        baseline_bins = np.array(baseline_data['bins'])
        baseline_counts = np.array(baseline_data['counts'])

        # Generate baseline samples (approximate)
        baseline_samples = []
        for i in range(len(baseline_counts)):
            if i < len(baseline_bins) - 1:
                mid_point = (baseline_bins[i] + baseline_bins[i + 1]) / 2
                baseline_samples.extend([mid_point] * int(baseline_counts[i]))
        baseline_array = np.array(baseline_samples)

        # Calculate drift metrics
        ks_stat, ks_p = self.tests.kolmogorov_smirnov(baseline_array, current_values)
        psi = self.tests.population_stability_index(baseline_array, current_values)
        js_div = self.tests.jensen_shannon_divergence(baseline_array, current_values)

        # Determine drift
        drift_detected = psi >= 0.1 or ks_p < 0.05
        severity = self.tests.classify_drift_severity(psi, ks_p)

        return FeatureDriftResult(
            feature_name=baseline.feature_name,
            ks_statistic=ks_stat,
            ks_p_value=ks_p,
            psi_score=psi,
            js_divergence=js_div,
            drift_detected=drift_detected,
            drift_severity=DriftSeverity(severity),
            sample_size=len(current_values)
        )

    def _detect_categorical_drift(
        self,
        baseline: DriftBaseline,
        current_values: pd.Series
    ) -> FeatureDriftResult:
        """Detect drift for categorical feature."""
        baseline_categories = baseline.categories
        current_counts = current_values.value_counts().to_dict()
        current_categories = {str(k): int(v) for k, v in current_counts.items()}

        # Chi-square test
        chi2, p_value = self.tests.chi_square_categorical(baseline_categories, current_categories)

        # Calculate PSI for categorical
        total_baseline = sum(baseline_categories.values())
        total_current = sum(current_categories.values())

        psi = 0.0
        all_cats = set(baseline_categories.keys()) | set(current_categories.keys())

        for cat in all_cats:
            baseline_pct = baseline_categories.get(cat, 0.0001) / total_baseline
            current_pct = current_categories.get(cat, 0.0001) / total_current
            psi += (current_pct - baseline_pct) * np.log(current_pct / baseline_pct)

        # Determine drift
        drift_detected = psi >= 0.1 or p_value < 0.05
        severity = self.tests.classify_drift_severity(psi, p_value)

        return FeatureDriftResult(
            feature_name=baseline.feature_name,
            ks_statistic=chi2,
            ks_p_value=p_value,
            psi_score=psi,
            js_divergence=None,
            drift_detected=drift_detected,
            drift_severity=DriftSeverity(severity),
            sample_size=len(current_values)
        )

    def _calculate_overall_drift(
        self,
        feature_results: List[FeatureDriftResult]
    ) -> Dict[str, Any]:
        """Calculate overall drift score."""
        if not feature_results:
            return {
                'drift_detected': False,
                'severity': 'none',
                'psi': 0.0
            }

        # Average PSI across features
        psi_scores = [r.psi_score for r in feature_results if r.psi_score is not None]
        overall_psi = np.mean(psi_scores) if psi_scores else 0.0

        # Count drift detections
        drift_count = sum(1 for r in feature_results if r.drift_detected)
        drift_rate = drift_count / len(feature_results)

        # Determine overall severity
        if drift_rate >= 0.5:
            # Majority of features drifted
            severities = [r.drift_severity.value for r in feature_results if r.drift_detected]
            severity_scores = {
                'none': 0, 'low': 1, 'medium': 2, 'high': 3, 'critical': 4
            }
            avg_severity_score = np.mean([severity_scores[s] for s in severities])

            if avg_severity_score >= 3.5:
                severity = 'critical'
            elif avg_severity_score >= 2.5:
                severity = 'high'
            elif avg_severity_score >= 1.5:
                severity = 'medium'
            else:
                severity = 'low'
        else:
            severity = self.tests.classify_drift_severity(overall_psi)

        return {
            'drift_detected': drift_count > 0,
            'severity': severity,
            'psi': float(overall_psi)
        }

    async def _save_detection(
        self,
        model_name: str,
        model_version: str,
        baseline_name: str,
        feature_result: FeatureDriftResult,
        detection_window: Optional[str]
    ):
        """Save feature drift detection."""
        detection = DriftDetection(
            model_name=model_name,
            model_version=model_version,
            baseline_name=baseline_name,
            feature_name=feature_result.feature_name,
            ks_statistic=feature_result.ks_statistic,
            ks_p_value=feature_result.ks_p_value,
            psi_score=feature_result.psi_score,
            js_divergence=feature_result.js_divergence,
            drift_detected=feature_result.drift_detected,
            drift_severity=feature_result.drift_severity.value,
            sample_size=feature_result.sample_size,
            detection_window=detection_window
        )

        self.db.add(detection)

    async def _save_overall_detection(
        self,
        model_name: str,
        model_version: str,
        baseline_name: str,
        overall_drift: Dict[str, Any],
        sample_size: int,
        detection_window: Optional[str]
    ):
        """Save overall drift detection."""
        detection = DriftDetection(
            model_name=model_name,
            model_version=model_version,
            baseline_name=baseline_name,
            feature_name=None,  # NULL for overall
            psi_score=overall_drift['psi'],
            drift_detected=overall_drift['drift_detected'],
            drift_severity=overall_drift['severity'],
            sample_size=sample_size,
            detection_window=detection_window
        )

        self.db.add(detection)
