"""
NeuralForge Streaming Module

Provides SSE (Server-Sent Events) and WebSocket streaming support
for LLM inference and real-time data streaming.
"""

from neuralforge.streaming.sse import (
    SSEResponse,
    SSEMessage,
    stream_sse,
    TokenStreamBuilder,
    SSEStreamContext,
)
from neuralforge.streaming.websocket import (
    WebSocketManager,
    StreamingWebSocket,
)
from neuralforge.streaming.generators import (
    async_generator_wrapper,
    chunk_generator,
    timeout_generator,
)
from neuralforge.streaming.response import (
    StreamingResponse,
    TokenStreamResponse,
)

__all__ = [
    # SSE
    "SSEResponse",
    "SSEMessage",
    "stream_sse",
    "TokenStreamBuilder",
    "SSEStreamContext",
    # WebSocket
    "WebSocketManager",
    "StreamingWebSocket",
    # Generators
    "async_generator_wrapper",
    "chunk_generator",
    "timeout_generator",
    # Response
    "StreamingResponse",
    "TokenStreamResponse",
]
