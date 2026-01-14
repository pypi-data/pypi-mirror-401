"""
Drift detection module - Data and concept drift detection.

Provides:
- Statistical drift tests (KS, PSI, JS divergence)
- Feature distribution tracking
- Concept drift detection
- Alert integration
"""

from neuralforge.ml.drift.exceptions import (
    DriftError,
    BaselineNotFoundError,
    InsufficientDataError,
    InvalidDistributionError,
    DriftDetectionError,
)
from neuralforge.ml.drift.detector import DriftDetector
from neuralforge.ml.drift.baseline import BaselineManager
from neuralforge.ml.drift.tests import StatisticalTests
from neuralforge.ml.drift.schemas import (
    BaselineCreate,
    BaselineInfo,
    DriftDetectionRequest,
    DriftDetectionResult,
    FeatureDriftResult,
    DriftDetectionInfo,
    DriftSummary,
)

__all__ = [
    # Exceptions
    'DriftError',
    'BaselineNotFoundError',
    'InsufficientDataError',
    'InvalidDistributionError',
    'DriftDetectionError',
    # Core
    'DriftDetector',
    'BaselineManager',
    'StatisticalTests',
    # Schemas
    'BaselineCreate',
    'BaselineInfo',
    'DriftDetectionRequest',
    'DriftDetectionResult',
    'FeatureDriftResult',
    'DriftDetectionInfo',
    'DriftSummary',
]
