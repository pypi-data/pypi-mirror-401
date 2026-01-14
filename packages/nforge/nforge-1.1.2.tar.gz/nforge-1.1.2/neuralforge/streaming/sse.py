"""
Server-Sent Events (SSE) Support for NeuralForge.

Provides SSE streaming for LLM token-by-token output
and real-time data streaming.
"""

import asyncio
import json
import logging
from typing import Any, AsyncIterator, Callable, Dict, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class SSEMessage:
    """
    Represents a Server-Sent Event message.
    
    Attributes:
        data: The message data (will be JSON serialized if not a string)
        event: Optional event type
        id: Optional message ID
        retry: Optional retry interval in milliseconds
    
    Example:
        >>> msg = SSEMessage(data={"token": "Hello"}, event="token")
        >>> print(msg.encode())
        event: token
        data: {"token": "Hello"}
    """
    data: Any
    event: Optional[str] = None
    id: Optional[str] = None
    retry: Optional[int] = None
    
    def encode(self) -> str:
        """Encode the message as SSE format."""
        lines = []
        
        if self.id is not None:
            lines.append(f"id: {self.id}")
        
        if self.event is not None:
            lines.append(f"event: {self.event}")
        
        if self.retry is not None:
            lines.append(f"retry: {self.retry}")
        
        # Serialize data
        if isinstance(self.data, str):
            data_str = self.data
        else:
            data_str = json.dumps(self.data)
        
        # Handle multi-line data
        for line in data_str.split('\n'):
            lines.append(f"data: {line}")
        
        lines.append("")  # Empty line to end message
        return "\n".join(lines) + "\n"


@dataclass
class SSEResponse:
    """
    SSE Response wrapper for streaming.
    
    Wraps an async generator to produce SSE-formatted output.
    
    Example:
        ```python
        async def generate_tokens():
            for token in ["Hello", " ", "World"]:
                yield SSEMessage(data={"token": token}, event="token")
        
        response = SSEResponse(generate_tokens())
        async for chunk in response:
            print(chunk)
        ```
    """
    generator: AsyncIterator[SSEMessage]
    content_type: str = "text/event-stream"
    headers: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        # Set default SSE headers
        default_headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
        self.headers = {**default_headers, **self.headers}
    
    async def __aiter__(self) -> AsyncIterator[bytes]:
        """Iterate over SSE messages as bytes."""
        try:
            async for message in self.generator:
                if isinstance(message, SSEMessage):
                    yield message.encode().encode('utf-8')
                elif isinstance(message, str):
                    yield f"data: {message}\n\n".encode('utf-8')
                elif isinstance(message, dict):
                    yield f"data: {json.dumps(message)}\n\n".encode('utf-8')
                else:
                    yield f"data: {str(message)}\n\n".encode('utf-8')
        except asyncio.CancelledError:
            logger.debug("SSE stream cancelled")
            raise
        except Exception as e:
            logger.error(f"SSE stream error: {e}")
            # Send error event
            error_msg = SSEMessage(
                data={"error": str(e)},
                event="error"
            )
            yield error_msg.encode().encode('utf-8')
            raise


class SSEStreamContext:
    """
    Context manager for SSE streaming.
    
    Handles connection lifecycle and cleanup.
    
    Example:
        ```python
        async with SSEStreamContext() as ctx:
            async for token in llm.generate(prompt):
                await ctx.send(token)
        ```
    """
    
    def __init__(
        self,
        heartbeat_interval: float = 15.0,
        max_duration: Optional[float] = None
    ):
        self.heartbeat_interval = heartbeat_interval
        self.max_duration = max_duration
        self._started_at: Optional[datetime] = None
        self._message_count: int = 0
        self._closed: bool = False
        self._heartbeat_task: Optional[asyncio.Task] = None
    
    async def __aenter__(self):
        self._started_at = datetime.utcnow()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._closed = True
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
    
    @property
    def duration_seconds(self) -> float:
        """Get stream duration in seconds."""
        if self._started_at is None:
            return 0.0
        return (datetime.utcnow() - self._started_at).total_seconds()
    
    @property
    def message_count(self) -> int:
        """Get number of messages sent."""
        return self._message_count
    
    def is_expired(self) -> bool:
        """Check if stream has exceeded max duration."""
        if self.max_duration is None:
            return False
        return self.duration_seconds >= self.max_duration
    
    def create_message(
        self,
        data: Any,
        event: Optional[str] = None,
        id: Optional[str] = None
    ) -> SSEMessage:
        """Create an SSE message."""
        self._message_count += 1
        return SSEMessage(
            data=data,
            event=event,
            id=id or str(self._message_count)
        )


async def stream_sse(
    generator_func: Callable[..., AsyncIterator[Any]],
    *args,
    event_type: str = "message",
    include_done_event: bool = True,
    **kwargs
) -> SSEResponse:
    """
    Create an SSE response from an async generator function.
    
    Args:
        generator_func: Async generator function that yields data
        *args: Arguments to pass to generator function
        event_type: Default event type for messages
        include_done_event: Whether to send a 'done' event at the end
        **kwargs: Keyword arguments to pass to generator function
    
    Returns:
        SSEResponse ready for streaming
    
    Example:
        ```python
        async def generate_tokens(prompt: str):
            async for token in llm.generate(prompt):
                yield {"token": token}
        
        @app.stream("/generate")
        async def generate(prompt: str):
            return await stream_sse(generate_tokens, prompt)
        ```
    """
    async def wrapped_generator():
        index = 0
        try:
            async for item in generator_func(*args, **kwargs):
                yield SSEMessage(
                    data=item,
                    event=event_type,
                    id=str(index)
                )
                index += 1
            
            if include_done_event:
                yield SSEMessage(
                    data={"finished": True, "total_items": index},
                    event="done",
                    id=str(index)
                )
        except Exception as e:
            logger.error(f"Stream generator error: {e}")
            yield SSEMessage(
                data={"error": str(e), "type": type(e).__name__},
                event="error"
            )
            raise
    
    return SSEResponse(generator=wrapped_generator())


class TokenStreamBuilder:
    """
    Builder for creating token-by-token SSE streams.
    
    Optimized for LLM inference output.
    
    Example:
        ```python
        builder = TokenStreamBuilder()
        
        @app.stream("/chat")
        async def chat(prompt: str):
            async for token in llm.generate(prompt):
                builder.add_token(token)
            return builder.build()
        ```
    """
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        include_metadata: bool = True
    ):
        self.model_name = model_name
        self.include_metadata = include_metadata
        self._tokens: list = []
        self._started_at: Optional[datetime] = None
        self._first_token_at: Optional[datetime] = None
    
    async def stream_tokens(
        self,
        token_generator: AsyncIterator[str],
        chunk_size: int = 1
    ) -> AsyncIterator[SSEMessage]:
        """
        Stream tokens from a generator.
        
        Args:
            token_generator: Async generator yielding tokens
            chunk_size: Number of tokens to batch per message
        
        Yields:
            SSE messages containing tokens
        """
        self._started_at = datetime.utcnow()
        buffer = []
        index = 0
        
        async for token in token_generator:
            if self._first_token_at is None:
                self._first_token_at = datetime.utcnow()
            
            buffer.append(token)
            self._tokens.append(token)
            
            if len(buffer) >= chunk_size:
                yield SSEMessage(
                    data={
                        "tokens": buffer if chunk_size > 1 else buffer[0],
                        "index": index
                    },
                    event="token",
                    id=str(index)
                )
                buffer = []
                index += 1
        
        # Flush remaining buffer
        if buffer:
            yield SSEMessage(
                data={
                    "tokens": buffer if chunk_size > 1 else buffer[0],
                    "index": index
                },
                event="token",
                id=str(index)
            )
            index += 1
        
        # Send completion message with metadata
        if self.include_metadata:
            completion_data = {
                "finished": True,
                "total_tokens": len(self._tokens),
                "model": self.model_name,
            }
            
            if self._started_at and self._first_token_at:
                ttft = (self._first_token_at - self._started_at).total_seconds()
                total_time = (datetime.utcnow() - self._started_at).total_seconds()
                completion_data["time_to_first_token_ms"] = round(ttft * 1000, 2)
                completion_data["total_time_ms"] = round(total_time * 1000, 2)
                
                if len(self._tokens) > 1:
                    tokens_per_second = len(self._tokens) / total_time
                    completion_data["tokens_per_second"] = round(tokens_per_second, 2)
            
            yield SSEMessage(
                data=completion_data,
                event="done",
                id=str(index)
            )
    
    def get_full_text(self) -> str:
        """Get the complete generated text."""
        return "".join(self._tokens)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get streaming statistics."""
        stats = {
            "total_tokens": len(self._tokens),
            "model": self.model_name,
        }
        
        if self._started_at:
            total_time = (datetime.utcnow() - self._started_at).total_seconds()
            stats["total_time_seconds"] = round(total_time, 3)
            
            if self._first_token_at:
                ttft = (self._first_token_at - self._started_at).total_seconds()
                stats["time_to_first_token_seconds"] = round(ttft, 3)
        
        return stats
