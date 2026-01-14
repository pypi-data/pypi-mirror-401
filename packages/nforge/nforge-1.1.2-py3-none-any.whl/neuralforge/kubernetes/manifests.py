"""
Kubernetes Manifest Generation for NeuralForge.

Generates Kubernetes manifests for NeuralForge deployments.
"""

from typing import Any, Dict, Optional
from neuralforge.kubernetes.operator import NeuralForgeSpec


def generate_deployment(
    name: str,
    namespace: str,
    spec: NeuralForgeSpec,
    image: str = "neuralforge/serving:latest"
) -> Dict[str, Any]:
    """
    Generate a Kubernetes Deployment manifest.
    
    Args:
        name: Resource name
        namespace: Target namespace
        spec: NeuralForge spec
        image: Container image
    
    Returns:
        Deployment manifest dictionary
    """
    labels = {
        "app": f"nf-{name}",
        "app.kubernetes.io/name": name,
        "app.kubernetes.io/component": "serving",
        "app.kubernetes.io/managed-by": "neuralforge-operator",
    }
    
    # Build container spec
    container = {
        "name": "neuralforge",
        "image": image,
        "ports": [
            {"containerPort": spec.port, "name": "http"},
            {"containerPort": spec.grpc_port, "name": "grpc"},
        ],
        "resources": {
            "requests": {
                "cpu": spec.cpu_request,
                "memory": spec.memory_request,
            },
            "limits": {
                "cpu": spec.cpu_limit,
                "memory": spec.memory_limit,
            },
        },
        "env": [
            {"name": "MODEL_NAME", "value": spec.model_name},
            {"name": "MODEL_VERSION", "value": spec.model_version},
            {"name": "PORT", "value": str(spec.port)},
            {"name": "GRPC_PORT", "value": str(spec.grpc_port)},
        ],
        "livenessProbe": {
            "httpGet": {
                "path": spec.health_check_path,
                "port": spec.port,
            },
            "initialDelaySeconds": 30,
            "periodSeconds": 10,
            "timeoutSeconds": 5,
            "failureThreshold": 3,
        },
        "readinessProbe": {
            "httpGet": {
                "path": spec.readiness_path,
                "port": spec.port,
            },
            "initialDelaySeconds": 10,
            "periodSeconds": 5,
            "timeoutSeconds": 3,
            "failureThreshold": 3,
        },
    }
    
    # Add environment variables
    for key, value in spec.environment.items():
        container["env"].append({"name": key, "value": value})
    
    # Add GPU resources if requested
    if spec.gpu_count > 0:
        container["resources"]["limits"]["nvidia.com/gpu"] = str(spec.gpu_count)
    
    # Build deployment
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": f"nf-{name}",
            "namespace": namespace,
            "labels": labels,
        },
        "spec": {
            "replicas": spec.replicas,
            "selector": {
                "matchLabels": {"app": f"nf-{name}"},
            },
            "template": {
                "metadata": {
                    "labels": labels,
                },
                "spec": {
                    "containers": [container],
                },
            },
            "strategy": {
                "type": "RollingUpdate",
                "rollingUpdate": {
                    "maxSurge": "25%",
                    "maxUnavailable": "25%",
                },
            },
        },
    }
    
    # Add config map reference
    if spec.config_map:
        deployment["spec"]["template"]["spec"]["volumes"] = [
            {
                "name": "config",
                "configMap": {"name": spec.config_map},
            }
        ]
        container["volumeMounts"] = [
            {"name": "config", "mountPath": "/etc/neuralforge"}
        ]
    
    # Add secret reference
    if spec.secret:
        if "volumes" not in deployment["spec"]["template"]["spec"]:
            deployment["spec"]["template"]["spec"]["volumes"] = []
        deployment["spec"]["template"]["spec"]["volumes"].append({
            "name": "secrets",
            "secret": {"secretName": spec.secret},
        })
        if "volumeMounts" not in container:
            container["volumeMounts"] = []
        container["volumeMounts"].append({
            "name": "secrets",
            "mountPath": "/etc/neuralforge/secrets",
            "readOnly": True,
        })
    
    return deployment


def generate_service(
    name: str,
    namespace: str,
    spec: NeuralForgeSpec,
    service_type: str = "ClusterIP"
) -> Dict[str, Any]:
    """
    Generate a Kubernetes Service manifest.
    
    Args:
        name: Resource name
        namespace: Target namespace
        spec: NeuralForge spec
        service_type: Service type (ClusterIP, NodePort, LoadBalancer)
    
    Returns:
        Service manifest dictionary
    """
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": f"nf-{name}",
            "namespace": namespace,
            "labels": {
                "app": f"nf-{name}",
                "app.kubernetes.io/managed-by": "neuralforge-operator",
            },
        },
        "spec": {
            "type": service_type,
            "selector": {
                "app": f"nf-{name}",
            },
            "ports": [
                {
                    "name": "http",
                    "port": spec.port,
                    "targetPort": spec.port,
                    "protocol": "TCP",
                },
                {
                    "name": "grpc",
                    "port": spec.grpc_port,
                    "targetPort": spec.grpc_port,
                    "protocol": "TCP",
                },
            ],
        },
    }


def generate_hpa(
    name: str,
    namespace: str,
    spec: NeuralForgeSpec
) -> Dict[str, Any]:
    """
    Generate a Horizontal Pod Autoscaler manifest.
    
    Args:
        name: Resource name
        namespace: Target namespace
        spec: NeuralForge spec
    
    Returns:
        HPA manifest dictionary
    """
    return {
        "apiVersion": "autoscaling/v2",
        "kind": "HorizontalPodAutoscaler",
        "metadata": {
            "name": f"nf-{name}",
            "namespace": namespace,
            "labels": {
                "app": f"nf-{name}",
                "app.kubernetes.io/managed-by": "neuralforge-operator",
            },
        },
        "spec": {
            "scaleTargetRef": {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "name": f"nf-{name}",
            },
            "minReplicas": spec.min_replicas,
            "maxReplicas": spec.max_replicas,
            "metrics": [
                {
                    "type": "Resource",
                    "resource": {
                        "name": "cpu",
                        "target": {
                            "type": "Utilization",
                            "averageUtilization": spec.target_cpu_utilization,
                        },
                    },
                },
                {
                    "type": "Resource",
                    "resource": {
                        "name": "memory",
                        "target": {
                            "type": "Utilization",
                            "averageUtilization": spec.target_memory_utilization,
                        },
                    },
                },
            ],
            "behavior": {
                "scaleUp": {
                    "stabilizationWindowSeconds": spec.scale_up_cooldown,
                    "policies": [
                        {
                            "type": "Percent",
                            "value": 100,
                            "periodSeconds": 15,
                        },
                    ],
                },
                "scaleDown": {
                    "stabilizationWindowSeconds": spec.scale_down_cooldown,
                    "policies": [
                        {
                            "type": "Percent",
                            "value": 10,
                            "periodSeconds": 60,
                        },
                    ],
                },
            },
        },
    }


def generate_configmap(
    name: str,
    namespace: str,
    data: Dict[str, str]
) -> Dict[str, Any]:
    """
    Generate a ConfigMap manifest.
    
    Args:
        name: ConfigMap name
        namespace: Target namespace
        data: Configuration data
    
    Returns:
        ConfigMap manifest dictionary
    """
    return {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": name,
            "namespace": namespace,
            "labels": {
                "app.kubernetes.io/managed-by": "neuralforge-operator",
            },
        },
        "data": data,
    }


def generate_crd() -> Dict[str, Any]:
    """
    Generate the NeuralForge CustomResourceDefinition.
    
    Returns:
        CRD manifest dictionary
    """
    return {
        "apiVersion": "apiextensions.k8s.io/v1",
        "kind": "CustomResourceDefinition",
        "metadata": {
            "name": "neuralforgeservices.neuralforge.io",
        },
        "spec": {
            "group": "neuralforge.io",
            "versions": [
                {
                    "name": "v1alpha1",
                    "served": True,
                    "storage": True,
                    "schema": {
                        "openAPIV3Schema": {
                            "type": "object",
                            "properties": {
                                "spec": {
                                    "type": "object",
                                    "required": ["modelName"],
                                    "properties": {
                                        "modelName": {"type": "string"},
                                        "modelVersion": {"type": "string", "default": "latest"},
                                        "replicas": {"type": "integer", "default": 1, "minimum": 1},
                                        "port": {"type": "integer", "default": 8000},
                                        "grpcPort": {"type": "integer", "default": 50051},
                                        "resources": {
                                            "type": "object",
                                            "properties": {
                                                "cpuRequest": {"type": "string", "default": "100m"},
                                                "cpuLimit": {"type": "string", "default": "1000m"},
                                                "memoryRequest": {"type": "string", "default": "256Mi"},
                                                "memoryLimit": {"type": "string", "default": "2Gi"},
                                                "gpuCount": {"type": "integer", "default": 0},
                                            },
                                        },
                                        "scaling": {
                                            "type": "object",
                                            "properties": {
                                                "minReplicas": {"type": "integer", "default": 1},
                                                "maxReplicas": {"type": "integer", "default": 10},
                                                "targetCPU": {"type": "integer", "default": 80},
                                                "targetMemory": {"type": "integer", "default": 80},
                                            },
                                        },
                                        "environment": {
                                            "type": "object",
                                            "additionalProperties": {"type": "string"},
                                        },
                                    },
                                },
                                "status": {
                                    "type": "object",
                                    "properties": {
                                        "phase": {"type": "string"},
                                        "replicas": {"type": "integer"},
                                        "readyReplicas": {"type": "integer"},
                                        "message": {"type": "string"},
                                        "lastUpdated": {"type": "string"},
                                    },
                                },
                            },
                        },
                    },
                    "subresources": {
                        "status": {},
                    },
                    "additionalPrinterColumns": [
                        {
                            "name": "Phase",
                            "type": "string",
                            "jsonPath": ".status.phase",
                        },
                        {
                            "name": "Ready",
                            "type": "integer",
                            "jsonPath": ".status.readyReplicas",
                        },
                        {
                            "name": "Age",
                            "type": "date",
                            "jsonPath": ".metadata.creationTimestamp",
                        },
                    ],
                },
            ],
            "scope": "Namespaced",
            "names": {
                "plural": "neuralforgeservices",
                "singular": "neuralforgeservice",
                "kind": "NeuralForgeService",
                "shortNames": ["nfs"],
            },
        },
    }
