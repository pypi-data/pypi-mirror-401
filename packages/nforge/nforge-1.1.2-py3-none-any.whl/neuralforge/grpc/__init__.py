"""
NeuralForge gRPC Module

Provides gRPC server support for high-performance
microservice communication.
"""

from neuralforge.grpc.server import (
    GRPCServer,
    GRPCServicer,
    ServiceDefinition,
    grpc_service,
    grpc_method,
    # Streaming support
    StreamingResponse,
    TokenStreamingMixin,
    stream_to_client,
    bidirectional_stream,
)
from neuralforge.grpc.interceptors import (
    LoggingInterceptor,
    AuthInterceptor,
    MetricsInterceptor,
    RateLimitInterceptor,
)

__all__ = [
    # Server
    "GRPCServer",
    "GRPCServicer",
    "ServiceDefinition",
    # Decorators
    "grpc_service",
    "grpc_method",
    # Streaming
    "StreamingResponse",
    "TokenStreamingMixin",
    "stream_to_client",
    "bidirectional_stream",
    # Interceptors
    "LoggingInterceptor",
    "AuthInterceptor",
    "MetricsInterceptor",
    "RateLimitInterceptor",
]
