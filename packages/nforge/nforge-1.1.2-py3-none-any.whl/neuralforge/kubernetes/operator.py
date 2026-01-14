"""
Kubernetes Operator for NeuralForge.

Provides a Kubernetes operator pattern implementation
for managing NeuralForge ML deployments.
"""

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

# Check for kubernetes client availability
try:
    from kubernetes import client, config, watch
    from kubernetes.client.rest import ApiException
    K8S_AVAILABLE = True
except ImportError:
    K8S_AVAILABLE = False
    client = None
    config = None


class ResourcePhase(Enum):
    """Phase of a NeuralForge resource."""
    PENDING = "Pending"
    CREATING = "Creating"
    RUNNING = "Running"
    SCALING = "Scaling"
    UPDATING = "Updating"
    FAILED = "Failed"
    TERMINATING = "Terminating"


@dataclass
class NeuralForgeSpec:
    """Specification for a NeuralForge deployment."""
    model_name: str
    model_version: str = "latest"
    replicas: int = 1
    
    # Resources
    cpu_request: str = "100m"
    cpu_limit: str = "1000m"
    memory_request: str = "256Mi"
    memory_limit: str = "2Gi"
    gpu_count: int = 0
    
    # Scaling
    min_replicas: int = 1
    max_replicas: int = 10
    target_cpu_utilization: int = 80
    target_memory_utilization: int = 80
    scale_up_cooldown: int = 60
    scale_down_cooldown: int = 300
    
    # Serving
    port: int = 8000
    grpc_port: int = 50051
    health_check_path: str = "/health"
    readiness_path: str = "/ready"
    
    # Configuration
    environment: Dict[str, str] = field(default_factory=dict)
    config_map: Optional[str] = None
    secret: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NeuralForgeSpec":
        """Create spec from dictionary."""
        return cls(
            model_name=data.get("modelName", ""),
            model_version=data.get("modelVersion", "latest"),
            replicas=data.get("replicas", 1),
            cpu_request=data.get("resources", {}).get("cpuRequest", "100m"),
            cpu_limit=data.get("resources", {}).get("cpuLimit", "1000m"),
            memory_request=data.get("resources", {}).get("memoryRequest", "256Mi"),
            memory_limit=data.get("resources", {}).get("memoryLimit", "2Gi"),
            gpu_count=data.get("resources", {}).get("gpuCount", 0),
            min_replicas=data.get("scaling", {}).get("minReplicas", 1),
            max_replicas=data.get("scaling", {}).get("maxReplicas", 10),
            target_cpu_utilization=data.get("scaling", {}).get("targetCPU", 80),
            port=data.get("port", 8000),
            grpc_port=data.get("grpcPort", 50051),
            environment=data.get("environment", {}),
        )


@dataclass
class NeuralForgeStatus:
    """Status of a NeuralForge deployment."""
    phase: ResourcePhase = ResourcePhase.PENDING
    replicas: int = 0
    ready_replicas: int = 0
    available_replicas: int = 0
    message: str = ""
    last_updated: datetime = field(default_factory=datetime.utcnow)
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for K8s status update."""
        return {
            "phase": self.phase.value,
            "replicas": self.replicas,
            "readyReplicas": self.ready_replicas,
            "availableReplicas": self.available_replicas,
            "message": self.message,
            "lastUpdated": self.last_updated.isoformat(),
            "conditions": self.conditions,
        }


@dataclass
class NeuralForgeResource:
    """
    Represents a NeuralForge Custom Resource.
    
    Maps to the NeuralForge CRD in Kubernetes.
    """
    name: str
    namespace: str
    spec: NeuralForgeSpec
    status: NeuralForgeStatus = field(default_factory=NeuralForgeStatus)
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    uid: Optional[str] = None
    resource_version: Optional[str] = None
    
    @classmethod
    def from_kubernetes(cls, obj: Dict[str, Any]) -> "NeuralForgeResource":
        """Create from Kubernetes API object."""
        metadata = obj.get("metadata", {})
        spec_data = obj.get("spec", {})
        
        return cls(
            name=metadata.get("name", ""),
            namespace=metadata.get("namespace", "default"),
            spec=NeuralForgeSpec.from_dict(spec_data),
            labels=metadata.get("labels", {}),
            annotations=metadata.get("annotations", {}),
            uid=metadata.get("uid"),
            resource_version=metadata.get("resourceVersion"),
        )


class NeuralForgeOperator:
    """
    Kubernetes Operator for NeuralForge ML deployments.
    
    Watches NeuralForge custom resources and manages
    their lifecycle in the cluster.
    
    Example:
        ```python
        from neuralforge.kubernetes import NeuralForgeOperator
        
        operator = NeuralForgeOperator(namespace="ml-serving")
        await operator.start()
        ```
    """
    
    CRD_GROUP = "neuralforge.io"
    CRD_VERSION = "v1alpha1"
    CRD_PLURAL = "neuralforgeservices"
    
    def __init__(
        self,
        namespace: str = "default",
        kubeconfig: Optional[str] = None,
        in_cluster: bool = False
    ):
        self.namespace = namespace
        self.kubeconfig = kubeconfig
        self.in_cluster = in_cluster
        
        self._running = False
        self._watch_task = None
        self._reconcile_interval = 30
        self._resources: Dict[str, NeuralForgeResource] = {}
        self._handlers: Dict[str, Callable] = {}
        
        # K8s clients
        self._core_v1 = None
        self._apps_v1 = None
        self._custom_api = None
        self._autoscaling_v2 = None
        
        logger.info(f"NeuralForgeOperator initialized for namespace: {namespace}")
    
    @property
    def is_available(self) -> bool:
        """Check if Kubernetes client is available."""
        return K8S_AVAILABLE
    
    @property
    def is_running(self) -> bool:
        """Check if operator is running."""
        return self._running
    
    def _load_config(self):
        """Load Kubernetes configuration."""
        if not K8S_AVAILABLE:
            raise RuntimeError(
                "kubernetes package not installed. "
                "Install with: pip install kubernetes"
            )
        
        if self.in_cluster:
            config.load_incluster_config()
        elif self.kubeconfig:
            config.load_kube_config(config_file=self.kubeconfig)
        else:
            config.load_kube_config()
        
        self._core_v1 = client.CoreV1Api()
        self._apps_v1 = client.AppsV1Api()
        self._custom_api = client.CustomObjectsApi()
        self._autoscaling_v2 = client.AutoscalingV2Api()
    
    async def start(self):
        """Start the operator."""
        if self._running:
            logger.warning("Operator already running")
            return
        
        self._load_config()
        self._running = True
        
        logger.info("Starting NeuralForge Operator")
        
        # Start watch loop
        self._watch_task = asyncio.create_task(self._watch_loop())
        
        # Start reconcile loop
        asyncio.create_task(self._reconcile_loop())
    
    async def stop(self):
        """Stop the operator."""
        self._running = False
        
        if self._watch_task:
            self._watch_task.cancel()
            try:
                await self._watch_task
            except asyncio.CancelledError:
                pass
        
        logger.info("NeuralForge Operator stopped")
    
    async def _watch_loop(self):
        """Watch for NeuralForge resource events."""
        if not K8S_AVAILABLE:
            return
        
        w = watch.Watch()
        
        while self._running:
            try:
                stream = w.stream(
                    self._custom_api.list_namespaced_custom_object,
                    group=self.CRD_GROUP,
                    version=self.CRD_VERSION,
                    namespace=self.namespace,
                    plural=self.CRD_PLURAL,
                    timeout_seconds=60
                )
                
                for event in stream:
                    if not self._running:
                        break
                    
                    event_type = event["type"]
                    obj = event["object"]
                    
                    await self._handle_event(event_type, obj)
                    
            except Exception as e:
                logger.error(f"Watch error: {e}")
                await asyncio.sleep(5)
    
    async def _handle_event(self, event_type: str, obj: Dict[str, Any]):
        """Handle a resource event."""
        resource = NeuralForgeResource.from_kubernetes(obj)
        
        logger.info(f"Event: {event_type} for {resource.name}")
        
        if event_type == "ADDED":
            await self._on_create(resource)
        elif event_type == "MODIFIED":
            await self._on_update(resource)
        elif event_type == "DELETED":
            await self._on_delete(resource)
    
    async def _on_create(self, resource: NeuralForgeResource):
        """Handle resource creation."""
        self._resources[resource.name] = resource
        
        try:
            # Create deployment
            await self._create_deployment(resource)
            
            # Create service
            await self._create_service(resource)
            
            # Create HPA if scaling enabled
            if resource.spec.max_replicas > resource.spec.min_replicas:
                await self._create_hpa(resource)
            
            # Update status
            resource.status.phase = ResourcePhase.RUNNING
            resource.status.message = "Deployment created successfully"
            await self._update_status(resource)
            
        except Exception as e:
            logger.error(f"Failed to create resources for {resource.name}: {e}")
            resource.status.phase = ResourcePhase.FAILED
            resource.status.message = str(e)
            await self._update_status(resource)
    
    async def _on_update(self, resource: NeuralForgeResource):
        """Handle resource update."""
        old_resource = self._resources.get(resource.name)
        self._resources[resource.name] = resource
        
        try:
            # Update deployment
            await self._update_deployment(resource)
            
            resource.status.phase = ResourcePhase.RUNNING
            resource.status.message = "Update completed"
            await self._update_status(resource)
            
        except Exception as e:
            logger.error(f"Failed to update {resource.name}: {e}")
            resource.status.phase = ResourcePhase.FAILED
            resource.status.message = str(e)
            await self._update_status(resource)
    
    async def _on_delete(self, resource: NeuralForgeResource):
        """Handle resource deletion."""
        self._resources.pop(resource.name, None)
        
        try:
            # Delete deployment
            await self._delete_deployment(resource)
            
            # Delete service
            await self._delete_service(resource)
            
            # Delete HPA
            await self._delete_hpa(resource)
            
        except Exception as e:
            logger.error(f"Failed to delete {resource.name}: {e}")
    
    async def _reconcile_loop(self):
        """Periodic reconciliation loop."""
        while self._running:
            await asyncio.sleep(self._reconcile_interval)
            
            for name, resource in list(self._resources.items()):
                try:
                    await self._reconcile(resource)
                except Exception as e:
                    logger.error(f"Reconcile error for {name}: {e}")
    
    async def _reconcile(self, resource: NeuralForgeResource):
        """Reconcile resource state."""
        # Check deployment status
        try:
            deployment = self._apps_v1.read_namespaced_deployment(
                name=f"nf-{resource.name}",
                namespace=self.namespace
            )
            
            resource.status.replicas = deployment.status.replicas or 0
            resource.status.ready_replicas = deployment.status.ready_replicas or 0
            resource.status.available_replicas = deployment.status.available_replicas or 0
            
        except ApiException as e:
            if e.status == 404:
                # Deployment missing, recreate
                await self._create_deployment(resource)
    
    async def _create_deployment(self, resource: NeuralForgeResource):
        """Create Kubernetes deployment."""
        from neuralforge.kubernetes.manifests import generate_deployment
        
        deployment = generate_deployment(
            name=resource.name,
            namespace=self.namespace,
            spec=resource.spec
        )
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._apps_v1.create_namespaced_deployment,
            self.namespace,
            deployment
        )
        
        logger.info(f"Created deployment for {resource.name}")
    
    async def _update_deployment(self, resource: NeuralForgeResource):
        """Update Kubernetes deployment."""
        from neuralforge.kubernetes.manifests import generate_deployment
        
        deployment = generate_deployment(
            name=resource.name,
            namespace=self.namespace,
            spec=resource.spec
        )
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._apps_v1.patch_namespaced_deployment,
            f"nf-{resource.name}",
            self.namespace,
            deployment
        )
        
        logger.info(f"Updated deployment for {resource.name}")
    
    async def _delete_deployment(self, resource: NeuralForgeResource):
        """Delete Kubernetes deployment."""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._apps_v1.delete_namespaced_deployment,
                f"nf-{resource.name}",
                self.namespace
            )
            logger.info(f"Deleted deployment for {resource.name}")
        except ApiException as e:
            if e.status != 404:
                raise
    
    async def _create_service(self, resource: NeuralForgeResource):
        """Create Kubernetes service."""
        from neuralforge.kubernetes.manifests import generate_service
        
        service = generate_service(
            name=resource.name,
            namespace=self.namespace,
            spec=resource.spec
        )
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._core_v1.create_namespaced_service,
            self.namespace,
            service
        )
        
        logger.info(f"Created service for {resource.name}")
    
    async def _delete_service(self, resource: NeuralForgeResource):
        """Delete Kubernetes service."""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._core_v1.delete_namespaced_service,
                f"nf-{resource.name}",
                self.namespace
            )
            logger.info(f"Deleted service for {resource.name}")
        except ApiException as e:
            if e.status != 404:
                raise
    
    async def _create_hpa(self, resource: NeuralForgeResource):
        """Create Horizontal Pod Autoscaler."""
        from neuralforge.kubernetes.manifests import generate_hpa
        
        hpa = generate_hpa(
            name=resource.name,
            namespace=self.namespace,
            spec=resource.spec
        )
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self._autoscaling_v2.create_namespaced_horizontal_pod_autoscaler,
            self.namespace,
            hpa
        )
        
        logger.info(f"Created HPA for {resource.name}")
    
    async def _delete_hpa(self, resource: NeuralForgeResource):
        """Delete Horizontal Pod Autoscaler."""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._autoscaling_v2.delete_namespaced_horizontal_pod_autoscaler,
                f"nf-{resource.name}",
                self.namespace
            )
            logger.info(f"Deleted HPA for {resource.name}")
        except ApiException as e:
            if e.status != 404:
                raise
    
    async def _update_status(self, resource: NeuralForgeResource):
        """Update resource status in Kubernetes."""
        try:
            resource.status.last_updated = datetime.utcnow()
            
            body = {
                "status": resource.status.to_dict()
            }
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self._custom_api.patch_namespaced_custom_object_status(
                    group=self.CRD_GROUP,
                    version=self.CRD_VERSION,
                    namespace=self.namespace,
                    plural=self.CRD_PLURAL,
                    name=resource.name,
                    body=body
                )
            )
        except Exception as e:
            logger.error(f"Failed to update status for {resource.name}: {e}")
    
    def register_handler(self, event: str, handler: Callable):
        """
        Register a custom event handler.
        
        Args:
            event: Event type ("create", "update", "delete")
            handler: Callback function
        """
        self._handlers[event] = handler
    
    def get_resource(self, name: str) -> Optional[NeuralForgeResource]:
        """Get a tracked resource by name."""
        return self._resources.get(name)
    
    def list_resources(self) -> List[NeuralForgeResource]:
        """List all tracked resources."""
        return list(self._resources.values())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get operator statistics."""
        return {
            "running": self._running,
            "namespace": self.namespace,
            "resources": len(self._resources),
            "k8s_available": K8S_AVAILABLE,
            "resource_details": {
                name: {
                    "phase": res.status.phase.value,
                    "replicas": res.status.replicas,
                    "ready": res.status.ready_replicas,
                }
                for name, res in self._resources.items()
            }
        }
