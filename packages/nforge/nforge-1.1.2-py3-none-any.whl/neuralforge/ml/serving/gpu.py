"""
GPU Manager - Manage GPU devices and placement.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class GPUManager:
    """
    Manage GPU devices and model placement.
    
    Supports CUDA (NVIDIA), MPS (Apple Silicon), and CPU fallback.
    
    Example:
        ```python
        gpu_mgr = GPUManager()
        
        # Get best device
        device = gpu_mgr.get_device()
        print(f"Using device: {device}")
        
        # Get device info
        info = gpu_mgr.get_device_info()
        print(f"Available GPUs: {info['num_gpus']}")
        
        # Move model to device
        model = model.to(device)
        ```
    """

    def __init__(self):
        """Initialize GPU manager."""
        self._check_dependencies()
        self._detect_devices()

    def _check_dependencies(self):
        """Check if PyTorch is available."""
        try:
            import torch
            self.torch = torch
            self.torch_available = True
        except ImportError:
            self.torch = None
            self.torch_available = False
            logger.warning("PyTorch not available. GPU features disabled.")

    def _detect_devices(self):
        """Detect available devices."""
        if not self.torch_available:
            self.cuda_available = False
            self.mps_available = False
            self.num_gpus = 0
            return

        # Check CUDA (NVIDIA)
        self.cuda_available = self.torch.cuda.is_available()
        self.num_gpus = self.torch.cuda.device_count() if self.cuda_available else 0

        # Check MPS (Apple Silicon)
        self.mps_available = (
            hasattr(self.torch.backends, 'mps') and
            self.torch.backends.mps.is_available()
        )

        logger.info(f"GPU Detection: CUDA={self.cuda_available}, MPS={self.mps_available}, GPUs={self.num_gpus}")

    def get_device(self, device_id: Optional[int] = None) -> str:
        """
        Get best available device.
        
        Priority: CUDA > MPS > CPU
        
        Args:
            device_id: Optional specific GPU ID
        
        Returns:
            Device string ('cuda', 'cuda:0', 'mps', 'cpu')
        """
        if not self.torch_available:
            return "cpu"

        if self.cuda_available:
            if device_id is not None and device_id < self.num_gpus:
                return f"cuda:{device_id}"
            return "cuda"

        if self.mps_available:
            return "mps"

        return "cpu"

    def get_device_info(self) -> Dict[str, Any]:
        """
        Get device information.
        
        Returns:
            Dictionary with device details
        """
        info = {
            'torch_available': self.torch_available,
            'cuda_available': self.cuda_available,
            'mps_available': self.mps_available,
            'num_gpus': self.num_gpus,
            'default_device': self.get_device(),
        }

        if self.cuda_available and self.torch_available:
            gpu_info = []
            for i in range(self.num_gpus):
                props = self.torch.cuda.get_device_properties(i)
                gpu_info.append({
                    'id': i,
                    'name': props.name,
                    'total_memory_mb': props.total_memory / (1024 ** 2),
                    'compute_capability': f"{props.major}.{props.minor}"
                })
            info['gpus'] = gpu_info

        return info

    def get_memory_info(self, device: Optional[str] = None) -> Dict[str, float]:
        """
        Get memory information for device.
        
        Args:
            device: Device string (default: current device)
        
        Returns:
            Memory info in MB
        """
        if not self.torch_available or not self.cuda_available:
            return {'allocated_mb': 0.0, 'reserved_mb': 0.0, 'free_mb': 0.0}

        if device and device.startswith('cuda'):
            device_id = int(device.split(':')[1]) if ':' in device else 0
        else:
            device_id = 0

        allocated = self.torch.cuda.memory_allocated(device_id) / (1024 ** 2)
        reserved = self.torch.cuda.memory_reserved(device_id) / (1024 ** 2)
        props = self.torch.cuda.get_device_properties(device_id)
        total = props.total_memory / (1024 ** 2)

        return {
            'allocated_mb': allocated,
            'reserved_mb': reserved,
            'total_mb': total,
            'free_mb': total - reserved
        }

    def clear_cache(self, device: Optional[str] = None):
        """
        Clear GPU cache.
        
        Args:
            device: Device to clear (default: all)
        """
        if not self.torch_available or not self.cuda_available:
            return

        self.torch.cuda.empty_cache()
        logger.info("GPU cache cleared")

    def optimize_for_device(
        self,
        model: Any,
        device: Optional[str] = None
    ) -> Any:
        """
        Optimize model for device.
        
        Args:
            model: Model to optimize
            device: Target device (default: best available)
        
        Returns:
            Optimized model
        """
        if not self.torch_available:
            return model

        target_device = device or self.get_device()

        # Move to device
        model = model.to(target_device)

        # Enable multi-GPU if available
        if self.cuda_available and self.num_gpus > 1 and target_device == "cuda":
            try:
                model = self.torch.nn.DataParallel(model)
                logger.info(f"Enabled DataParallel across {self.num_gpus} GPUs")
            except Exception as e:
                logger.warning(f"Failed to enable DataParallel: {e}")

        # Set to eval mode for inference
        model.eval()

        return model

    def get_optimal_batch_size(
        self,
        model_size_mb: float,
        device: Optional[str] = None
    ) -> int:
        """
        Estimate optimal batch size based on available memory.
        
        Args:
            model_size_mb: Model size in MB
            device: Target device
        
        Returns:
            Recommended batch size
        """
        if not self.cuda_available:
            return 1

        memory_info = self.get_memory_info(device)
        available_mb = memory_info['free_mb']

        # Reserve 20% for overhead
        usable_mb = available_mb * 0.8

        # Estimate batch size (rough heuristic)
        # Assume each sample uses ~2x model size
        estimated_batch_size = int(usable_mb / (model_size_mb * 2))

        # Clamp to reasonable range
        return max(1, min(estimated_batch_size, 128))
