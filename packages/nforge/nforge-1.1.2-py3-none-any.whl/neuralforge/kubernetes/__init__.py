"""
NeuralForge Kubernetes Operator

Provides Kubernetes-native deployment and management
for NeuralForge ML services.
"""

from neuralforge.kubernetes.operator import (
    NeuralForgeOperator,
    NeuralForgeResource,
)
from neuralforge.kubernetes.scaling import (
    AutoScaler,
    ScalingMetrics,
    ScalingPolicy,
)
from neuralforge.kubernetes.manifests import (
    generate_deployment,
    generate_service,
    generate_hpa,
    generate_configmap,
)

__all__ = [
    # Operator
    "NeuralForgeOperator",
    "NeuralForgeResource",
    # Scaling
    "AutoScaler",
    "ScalingMetrics",
    "ScalingPolicy",
    # Manifests
    "generate_deployment",
    "generate_service",
    "generate_hpa",
    "generate_configmap",
]
