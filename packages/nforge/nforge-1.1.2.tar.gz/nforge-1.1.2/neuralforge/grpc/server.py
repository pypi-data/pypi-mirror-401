"""
gRPC Server Implementation for NeuralForge.

Provides a gRPC server that runs alongside the HTTP server
for high-performance internal communication.
"""

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional, Type
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


# Check for grpcio availability
try:
    import grpc
    from grpc import aio as grpc_aio
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False
    grpc = None
    grpc_aio = None


class GRPCStatus(Enum):
    """gRPC server status."""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"


@dataclass
class ServiceDefinition:
    """Definition for a gRPC service."""
    name: str
    servicer_class: Type
    add_to_server_func: Optional[Callable] = None
    proto_file: Optional[str] = None
    methods: List[str] = field(default_factory=list)


class GRPCServicer:
    """
    Base class for gRPC service implementations.
    
    Extend this class to create your gRPC services.
    
    Example:
        ```python
        class MyInferenceService(GRPCServicer):
            async def Predict(self, request, context):
                result = await self.model.predict(request.input_data)
                return PredictResponse(output=result)
            
            async def StreamPredict(self, request, context):
                async for token in self.model.generate(request.prompt):
                    yield TokenResponse(token=token)
        ```
    """
    
    def __init__(self, app: Any = None):
        self.app = app
        self._started_at: Optional[datetime] = None
        self._request_count = 0
    
    async def on_start(self):
        """Called when the service starts."""
        self._started_at = datetime.utcnow()
        logger.info(f"gRPC service {self.__class__.__name__} started")
    
    async def on_stop(self):
        """Called when the service stops."""
        logger.info(f"gRPC service {self.__class__.__name__} stopped")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get service statistics."""
        stats = {
            "service_name": self.__class__.__name__,
            "request_count": self._request_count,
        }
        if self._started_at:
            uptime = (datetime.utcnow() - self._started_at).total_seconds()
            stats["uptime_seconds"] = round(uptime, 2)
        return stats


class GRPCServer:
    """
    gRPC Server for NeuralForge.
    
    Runs alongside the HTTP server to provide high-performance
    gRPC endpoints for internal microservice communication.
    
    Example:
        ```python
        from neuralforge import NeuralForge
        from neuralforge.grpc import GRPCServer, GRPCServicer
        
        app = NeuralForge()
        grpc_server = GRPCServer(app)
        
        # Register services
        grpc_server.register_service(
            MyInferenceService,
            add_func=add_InferenceServiceServicer_to_server
        )
        
        # Start server
        await grpc_server.start(port=50051)
        ```
    """
    
    def __init__(
        self,
        app: Any = None,
        max_workers: int = 10,
        max_message_length: int = 100 * 1024 * 1024,  # 100MB
        compression: bool = True,
        reflection: bool = True
    ):
        if not GRPC_AVAILABLE:
            logger.warning(
                "grpcio not installed. Install with: pip install grpcio grpcio-tools"
            )
        
        self.app = app
        self.max_workers = max_workers
        self.max_message_length = max_message_length
        self.compression = compression
        self.reflection = reflection
        
        self._server: Optional[Any] = None
        self._status = GRPCStatus.STOPPED
        self._services: Dict[str, ServiceDefinition] = {}
        self._servicer_instances: Dict[str, GRPCServicer] = {}
        self._interceptors: List[Any] = []
        self._port: Optional[int] = None
        self._started_at: Optional[datetime] = None
    
    @property
    def status(self) -> GRPCStatus:
        """Get server status."""
        return self._status
    
    @property
    def is_running(self) -> bool:
        """Check if server is running."""
        return self._status == GRPCStatus.RUNNING
    
    def add_interceptor(self, interceptor: Any):
        """
        Add a gRPC interceptor.
        
        Args:
            interceptor: gRPC interceptor instance
        """
        self._interceptors.append(interceptor)
        logger.debug(f"Added gRPC interceptor: {interceptor.__class__.__name__}")
    
    def register_service(
        self,
        servicer_class: Type[GRPCServicer],
        add_func: Optional[Callable] = None,
        name: Optional[str] = None
    ):
        """
        Register a gRPC service.
        
        Args:
            servicer_class: Service class extending GRPCServicer
            add_func: Function to add servicer to server (from generated code)
            name: Service name (defaults to class name)
        """
        service_name = name or servicer_class.__name__
        
        # Extract methods from class
        methods = []
        for attr_name in dir(servicer_class):
            if not attr_name.startswith('_') and callable(getattr(servicer_class, attr_name)):
                if attr_name not in ('on_start', 'on_stop', 'get_stats'):
                    methods.append(attr_name)
        
        self._services[service_name] = ServiceDefinition(
            name=service_name,
            servicer_class=servicer_class,
            add_to_server_func=add_func,
            methods=methods
        )
        
        logger.info(f"Registered gRPC service: {service_name} with methods: {methods}")
    
    async def start(
        self,
        host: str = "0.0.0.0",
        port: int = 50051,
        blocking: bool = False
    ):
        """
        Start the gRPC server.
        
        Args:
            host: Host to bind to
            port: Port to listen on
            blocking: If True, block until server stops
        """
        if not GRPC_AVAILABLE:
            raise RuntimeError(
                "grpcio not installed. Install with: pip install grpcio grpcio-tools"
            )
        
        if self._status != GRPCStatus.STOPPED:
            raise RuntimeError(f"Server is {self._status.value}")
        
        self._status = GRPCStatus.STARTING
        self._port = port
        
        try:
            # Configure server options
            options = [
                ('grpc.max_send_message_length', self.max_message_length),
                ('grpc.max_receive_message_length', self.max_message_length),
            ]
            
            if self.compression:
                options.append(('grpc.default_compression_algorithm', 2))  # GZIP
            
            # Create async server
            self._server = grpc_aio.server(
                interceptors=self._interceptors if self._interceptors else None,
                options=options
            )
            
            # Create and register servicer instances
            for name, service_def in self._services.items():
                servicer = service_def.servicer_class(self.app)
                self._servicer_instances[name] = servicer
                
                if service_def.add_to_server_func:
                    service_def.add_to_server_func(servicer, self._server)
                    logger.debug(f"Added servicer {name} to server")
            
            # Add listening port
            address = f"{host}:{port}"
            self._server.add_insecure_port(address)
            
            # Start server
            await self._server.start()
            self._status = GRPCStatus.RUNNING
            self._started_at = datetime.utcnow()
            
            logger.info(f"gRPC server started on {address}")
            
            # Notify servicers
            for servicer in self._servicer_instances.values():
                await servicer.on_start()
            
            if blocking:
                await self._server.wait_for_termination()
                
        except Exception as e:
            self._status = GRPCStatus.STOPPED
            logger.error(f"Failed to start gRPC server: {e}")
            raise
    
    async def stop(self, grace_period: float = 5.0):
        """
        Stop the gRPC server.
        
        Args:
            grace_period: Seconds to wait for pending RPCs
        """
        if self._status != GRPCStatus.RUNNING:
            return
        
        self._status = GRPCStatus.STOPPING
        
        try:
            # Notify servicers
            for servicer in self._servicer_instances.values():
                await servicer.on_stop()
            
            # Stop server with grace period
            await self._server.stop(grace_period)
            
            logger.info("gRPC server stopped")
            
        finally:
            self._status = GRPCStatus.STOPPED
            self._servicer_instances.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get server statistics."""
        stats = {
            "status": self._status.value,
            "port": self._port,
            "services": list(self._services.keys()),
            "interceptors": len(self._interceptors),
            "grpc_available": GRPC_AVAILABLE,
        }
        
        if self._started_at:
            uptime = (datetime.utcnow() - self._started_at).total_seconds()
            stats["uptime_seconds"] = round(uptime, 2)
        
        # Add service stats
        stats["service_stats"] = {
            name: servicer.get_stats()
            for name, servicer in self._servicer_instances.items()
        }
        
        return stats


# Decorator for registering gRPC services
def grpc_service(name: str = None):
    """
    Decorator to mark a class as a gRPC service.
    
    Example:
        ```python
        @grpc_service("InferenceService")
        class MyInferenceService(GRPCServicer):
            async def Predict(self, request, context):
                return PredictResponse(...)
        ```
    
    Args:
        name: Service name (defaults to class name)
    """
    def decorator(cls: Type[GRPCServicer]):
        cls._grpc_service_name = name or cls.__name__
        return cls
    return decorator


def grpc_method(request_streaming: bool = False, response_streaming: bool = False):
    """
    Decorator to mark a method as a gRPC endpoint.
    
    Example:
        ```python
        class MyService(GRPCServicer):
            @grpc_method(response_streaming=True)
            async def StreamPredict(self, request, context):
                for token in generate():
                    yield TokenResponse(token=token)
        ```
    
    Args:
        request_streaming: If True, request is a stream
        response_streaming: If True, response is a stream
    """
    def decorator(func: Callable):
        func._grpc_request_streaming = request_streaming
        func._grpc_response_streaming = response_streaming
        return func
    return decorator


class StreamingResponse:
    """
    Helper for building streaming gRPC responses.
    
    Provides utilities for server-side streaming RPCs,
    including token-by-token streaming for LLM inference.
    
    Example:
        ```python
        class LLMService(GRPCServicer):
            @grpc_method(response_streaming=True)
            async def Generate(self, request, context):
                streamer = StreamingResponse(context)
                
                async for token in self.llm.generate(request.prompt):
                    if streamer.is_cancelled:
                        break
                    yield TokenResponse(token=token)
        ```
    """
    
    def __init__(self, context: Any):
        self.context = context
        self._token_count = 0
        self._start_time: Optional[datetime] = None
        self._first_token_time: Optional[datetime] = None
    
    @property
    def is_cancelled(self) -> bool:
        """Check if the RPC was cancelled by the client."""
        if self.context is None:
            return False
        try:
            return self.context.cancelled()
        except Exception:
            return False
    
    def start(self):
        """Mark the start of streaming."""
        self._start_time = datetime.utcnow()
    
    def record_token(self):
        """Record that a token was sent."""
        if self._first_token_time is None:
            self._first_token_time = datetime.utcnow()
        self._token_count += 1
    
    @property
    def token_count(self) -> int:
        """Get number of tokens sent."""
        return self._token_count
    
    @property
    def time_to_first_token_ms(self) -> Optional[float]:
        """Get time to first token in milliseconds."""
        if self._start_time and self._first_token_time:
            delta = self._first_token_time - self._start_time
            return delta.total_seconds() * 1000
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get streaming statistics."""
        stats = {
            "token_count": self._token_count,
        }
        if self.time_to_first_token_ms is not None:
            stats["ttft_ms"] = round(self.time_to_first_token_ms, 2)
        if self._start_time:
            elapsed = (datetime.utcnow() - self._start_time).total_seconds()
            stats["elapsed_seconds"] = round(elapsed, 3)
            if elapsed > 0:
                stats["tokens_per_second"] = round(self._token_count / elapsed, 1)
        return stats


class TokenStreamingMixin:
    """
    Mixin class for token-streaming gRPC services.
    
    Provides helper methods for LLM token streaming.
    
    Example:
        ```python
        class LLMService(GRPCServicer, TokenStreamingMixin):
            @grpc_method(response_streaming=True)
            async def StreamPredict(self, request, context):
                async for response in self.stream_tokens(
                    self.llm.generate(request.prompt),
                    context,
                    response_class=TokenResponse
                ):
                    yield response
        ```
    """
    
    async def stream_tokens(
        self,
        generator,
        context: Any,
        response_class: Type,
        token_field: str = "token",
        include_metadata: bool = True
    ):
        """
        Stream tokens from an async generator.
        
        Args:
            generator: Async generator yielding tokens
            context: gRPC context
            response_class: Response message class
            token_field: Field name for the token in response
            include_metadata: Include streaming metadata
        
        Yields:
            Response messages with tokens
        """
        streamer = StreamingResponse(context)
        streamer.start()
        
        index = 0
        async for token in generator:
            if streamer.is_cancelled:
                break
            
            streamer.record_token()
            
            # Build response
            response_data = {
                token_field: token,
                "index": index,
                "is_final": False,
            }
            
            yield response_class(**response_data)
            index += 1
        
        # Send final response if not cancelled
        if not streamer.is_cancelled and include_metadata:
            stats = streamer.get_stats()
            final_response = {
                token_field: "",
                "index": index,
                "is_final": True,
            }
            # Add metadata if response class supports it
            if hasattr(response_class, 'metadata'):
                final_response["metadata"] = stats
            
            yield response_class(**final_response)


async def stream_to_client(
    generator,
    context: Any,
    response_builder: Callable[[Any], Any],
    check_cancelled: bool = True
):
    """
    Utility for streaming responses to a gRPC client.
    
    Args:
        generator: Async generator producing items
        context: gRPC context for cancellation checking
        response_builder: Function to build response from item
        check_cancelled: Whether to check for client cancellation
    
    Yields:
        gRPC response messages
    
    Example:
        ```python
        async def StreamData(self, request, context):
            async for response in stream_to_client(
                self.data_generator(),
                context,
                lambda item: DataResponse(data=item)
            ):
                yield response
        ```
    """
    async for item in generator:
        if check_cancelled and context and hasattr(context, 'cancelled'):
            if context.cancelled():
                break
        
        yield response_builder(item)


async def bidirectional_stream(
    request_iterator,
    context: Any,
    handler: Callable[[Any], Any]
):
    """
    Utility for bidirectional streaming RPCs.
    
    Args:
        request_iterator: Async iterator of incoming requests
        context: gRPC context
        handler: Async function that takes request and returns response
    
    Yields:
        gRPC response messages
    
    Example:
        ```python
        async def Chat(self, request_iterator, context):
            async for response in bidirectional_stream(
                request_iterator,
                context,
                self.process_message
            ):
                yield response
        ```
    """
    async for request in request_iterator:
        if context and hasattr(context, 'cancelled') and context.cancelled():
            break
        
        response = await handler(request)
        if response is not None:
            yield response

