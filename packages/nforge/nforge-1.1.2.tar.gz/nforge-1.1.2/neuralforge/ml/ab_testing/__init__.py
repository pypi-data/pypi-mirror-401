"""
A/B Testing module - ML model experimentation framework.

Provides:
- Experiment management
- Traffic splitting and variant assignment
- Metrics collection and analysis
- Statistical significance testing
- Automatic winner determination and rollout
"""

from neuralforge.ml.ab_testing.exceptions import (
    ABTestingError,
    ExperimentNotFoundError,
    ExperimentAlreadyExistsError,
    ExperimentNotRunningError,
    VariantNotFoundError,
    InvalidTrafficAllocationError,
    InsufficientSampleSizeError,
    NoWinnerError,
)
from neuralforge.ml.ab_testing.manager import ExperimentManager
from neuralforge.ml.ab_testing.schemas import (
    ExperimentCreate,
    ExperimentUpdate,
    ExperimentInfo,
    VariantConfig,
    MetricRecord,
    AssignmentResponse,
    ExperimentResults,
)

__all__ = [
    # Exceptions
    'ABTestingError',
    'ExperimentNotFoundError',
    'ExperimentAlreadyExistsError',
    'ExperimentNotRunningError',
    'VariantNotFoundError',
    'InvalidTrafficAllocationError',
    'InsufficientSampleSizeError',
    'NoWinnerError',
    # Core
    'ExperimentManager',
    # Schemas
    'ExperimentCreate',
    'ExperimentUpdate',
    'ExperimentInfo',
    'VariantConfig',
    'MetricRecord',
    'AssignmentResponse',
    'ExperimentResults',
]
