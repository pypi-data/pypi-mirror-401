"""
Model Quantizer - Quantize models for faster inference.
"""

import logging
from typing import Any, Dict
import time

from neuralforge.ml.optimization.exceptions import QuantizationError

logger = logging.getLogger(__name__)


class ModelQuantizer:
    """
    Quantize models for faster inference.
    
    Supports PyTorch dynamic/static quantization and FP16 conversion.
    
    Example:
        ```python
        quantizer = ModelQuantizer()
        
        # Dynamic quantization (easiest, PyTorch)
        quantized_model = quantizer.quantize_dynamic(
            model=pytorch_model,
            dtype="int8"
        )
        
        # FP16 conversion
        fp16_model = quantizer.quantize_to_fp16(model)
        ```
    
    Note:
        This is a framework integration layer. Actual quantization
        uses PyTorch's built-in quantization APIs.
    """

    def __init__(self):
        """Initialize quantizer."""
        self._check_dependencies()

    def _check_dependencies(self):
        """Check if required libraries are available."""
        try:
            import torch
            self.torch = torch
            self.torch_available = True
        except ImportError:
            self.torch = None
            self.torch_available = False
            logger.warning("PyTorch not available. Quantization features limited.")

    def quantize_dynamic(
        self,
        model: Any,
        dtype: str = "int8"
    ) -> Any:
        """
        Apply dynamic quantization to model.
        
        Dynamic quantization quantizes weights ahead of time and
        activations on-the-fly during inference.
        
        Args:
            model: PyTorch model
            dtype: Quantization dtype ('int8' or 'fp16')
        
        Returns:
            Quantized model
        
        Raises:
            QuantizationError: If quantization fails
        """
        if not self.torch_available:
            raise QuantizationError("PyTorch not available for quantization")

        try:
            if dtype == "int8":
                # Dynamic quantization to INT8
                quantized_model = self.torch.quantization.quantize_dynamic(
                    model,
                    {self.torch.nn.Linear},  # Quantize Linear layers
                    dtype=self.torch.qint8
                )
            elif dtype == "fp16":
                # Convert to half precision
                quantized_model = model.half()
            else:
                raise QuantizationError(f"Unsupported dtype: {dtype}")

            logger.info(f"Successfully quantized model to {dtype}")
            return quantized_model

        except Exception as e:
            raise QuantizationError(f"Quantization failed: {str(e)}")

    def quantize_static(
        self,
        model: Any,
        calibration_data: Any,
        dtype: str = "int8"
    ) -> Any:
        """
        Apply static quantization with calibration.
        
        Static quantization requires calibration data to determine
        optimal quantization parameters.
        
        Args:
            model: PyTorch model
            calibration_data: DataLoader for calibration
            dtype: Quantization dtype
        
        Returns:
            Quantized model
        """
        if not self.torch_available:
            raise QuantizationError("PyTorch not available for quantization")

        try:
            # Prepare model for static quantization
            model.qconfig = self.torch.quantization.get_default_qconfig('fbgemm')
            model_prepared = self.torch.quantization.prepare(model)

            # Calibrate with sample data
            model_prepared.eval()
            with self.torch.no_grad():
                for batch in calibration_data:
                    if isinstance(batch, (list, tuple)):
                        model_prepared(batch[0])
                    else:
                        model_prepared(batch)
                    break  # Use first batch for calibration

            # Convert to quantized model
            quantized_model = self.torch.quantization.convert(model_prepared)

            logger.info("Successfully applied static quantization")
            return quantized_model

        except Exception as e:
            raise QuantizationError(f"Static quantization failed: {str(e)}")

    def quantize_to_fp16(
        self,
        model: Any
    ) -> Any:
        """
        Convert model to FP16 (half precision).
        
        Args:
            model: PyTorch model
        
        Returns:
            FP16 model
        """
        if not self.torch_available:
            raise QuantizationError("PyTorch not available")

        try:
            return model.half()
        except Exception as e:
            raise QuantizationError(f"FP16 conversion failed: {str(e)}")

    def measure_model_size(
        self,
        model: Any
    ) -> float:
        """
        Measure model size in MB.
        
        Args:
            model: PyTorch model
        
        Returns:
            Model size in MB
        """
        if not self.torch_available:
            return 0.0

        try:
            import tempfile
            import os

            # Save model to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pt') as f:
                temp_path = f.name
                self.torch.save(model.state_dict(), temp_path)

            # Get file size
            size_bytes = os.path.getsize(temp_path)
            size_mb = size_bytes / (1024 * 1024)

            # Cleanup
            os.unlink(temp_path)

            return size_mb

        except Exception as e:
            logger.error(f"Failed to measure model size: {e}")
            return 0.0

    def compare_models(
        self,
        original_model: Any,
        quantized_model: Any,
        test_input: Any
    ) -> Dict[str, float]:
        """
        Compare original vs quantized model.
        
        Args:
            original_model: Original model
            quantized_model: Quantized model
            test_input: Test input tensor
        
        Returns:
            Comparison metrics
        """
        if not self.torch_available:
            return {}

        try:
            # Measure sizes
            original_size = self.measure_model_size(original_model)
            quantized_size = self.measure_model_size(quantized_model)

            # Measure inference time
            original_model.eval()
            quantized_model.eval()

            with self.torch.no_grad():
                # Original model
                start = time.time()
                for _ in range(100):
                    _ = original_model(test_input)
                original_time = (time.time() - start) / 100

                # Quantized model
                start = time.time()
                for _ in range(100):
                    _ = quantized_model(test_input)
                quantized_time = (time.time() - start) / 100

            return {
                'original_size_mb': original_size,
                'quantized_size_mb': quantized_size,
                'size_reduction': (original_size - quantized_size) / original_size if original_size > 0 else 0,
                'original_latency_ms': original_time * 1000,
                'quantized_latency_ms': quantized_time * 1000,
                'speedup_factor': original_time / quantized_time if quantized_time > 0 else 1.0
            }

        except Exception as e:
            logger.error(f"Model comparison failed: {e}")
            return {}
