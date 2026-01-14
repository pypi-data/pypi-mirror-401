"""
Streaming Response Classes for NeuralForge.

Provides response wrappers for streaming HTTP responses.
"""

import asyncio
import json
import logging
from typing import Any, AsyncIterator, Dict, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class StreamingResponse:
    """
    Generic streaming response wrapper.
    
    Wraps an async generator for HTTP streaming responses.
    
    Example:
        ```python
        @app.stream("/data")
        async def stream_data():
            async def generate():
                for i in range(100):
                    yield f"chunk_{i}"
            
            return StreamingResponse(
                content=generate(),
                media_type="text/plain"
            )
        ```
    """
    content: AsyncIterator[Union[str, bytes]]
    media_type: str = "application/octet-stream"
    status_code: int = 200
    headers: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        # Ensure streaming headers are set
        default_headers = {
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
        }
        self.headers = {**default_headers, **self.headers}
    
    async def __aiter__(self) -> AsyncIterator[bytes]:
        """Iterate over response chunks."""
        async for chunk in self.content:
            if isinstance(chunk, str):
                yield chunk.encode('utf-8')
            else:
                yield chunk


@dataclass
class TokenStreamResponse:
    """
    Specialized streaming response for LLM token output.
    
    Optimized for token-by-token streaming with metadata.
    
    Example:
        ```python
        @app.stream("/generate")
        async def generate(prompt: str):
            async def token_gen():
                async for token in model.generate(prompt):
                    yield token
            
            return TokenStreamResponse(
                tokens=token_gen(),
                model_name="gpt-4",
                format="sse"
            )
        ```
    """
    tokens: AsyncIterator[str]
    model_name: Optional[str] = None
    format: str = "sse"  # "sse", "json", "text"
    include_usage: bool = True
    headers: Dict[str, str] = field(default_factory=dict)
    
    # Internal tracking
    _started_at: Optional[datetime] = field(default=None, init=False)
    _first_token_at: Optional[datetime] = field(default=None, init=False)
    _token_count: int = field(default=0, init=False)
    
    def __post_init__(self):
        if self.format == "sse":
            self.media_type = "text/event-stream"
        elif self.format == "json":
            self.media_type = "application/x-ndjson"
        else:
            self.media_type = "text/plain"
        
        default_headers = {
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
        self.headers = {**default_headers, **self.headers}
    
    async def __aiter__(self) -> AsyncIterator[bytes]:
        """Iterate over formatted token chunks."""
        self._started_at = datetime.utcnow()
        
        try:
            async for token in self.tokens:
                if self._first_token_at is None:
                    self._first_token_at = datetime.utcnow()
                
                self._token_count += 1
                
                if self.format == "sse":
                    yield self._format_sse(token)
                elif self.format == "json":
                    yield self._format_json(token)
                else:
                    yield token.encode('utf-8')
            
            # Send completion message
            if self.include_usage:
                yield self._format_completion()
                
        except Exception as e:
            logger.error(f"Token stream error: {e}")
            yield self._format_error(str(e))
            raise
    
    def _format_sse(self, token: str) -> bytes:
        """Format token as SSE event."""
        data = {
            "token": token,
            "index": self._token_count,
        }
        return f"event: token\ndata: {json.dumps(data)}\n\n".encode('utf-8')
    
    def _format_json(self, token: str) -> bytes:
        """Format token as NDJSON."""
        data = {
            "token": token,
            "index": self._token_count,
        }
        return (json.dumps(data) + "\n").encode('utf-8')
    
    def _format_completion(self) -> bytes:
        """Format completion message."""
        data = {
            "finished": True,
            "total_tokens": self._token_count,
            "model": self.model_name,
        }
        
        if self._started_at and self._first_token_at:
            ttft = (self._first_token_at - self._started_at).total_seconds()
            total_time = (datetime.utcnow() - self._started_at).total_seconds()
            
            data["usage"] = {
                "time_to_first_token_ms": round(ttft * 1000, 2),
                "total_time_ms": round(total_time * 1000, 2),
                "tokens_per_second": round(
                    self._token_count / total_time, 2
                ) if total_time > 0 else 0,
            }
        
        if self.format == "sse":
            return f"event: done\ndata: {json.dumps(data)}\n\n".encode('utf-8')
        elif self.format == "json":
            return (json.dumps(data) + "\n").encode('utf-8')
        else:
            return json.dumps(data).encode('utf-8')
    
    def _format_error(self, error: str) -> bytes:
        """Format error message."""
        data = {"error": error, "type": "stream_error"}
        
        if self.format == "sse":
            return f"event: error\ndata: {json.dumps(data)}\n\n".encode('utf-8')
        elif self.format == "json":
            return (json.dumps(data) + "\n").encode('utf-8')
        else:
            return json.dumps(data).encode('utf-8')


class JSONStreamResponse:
    """
    Streaming response for JSON arrays.
    
    Streams JSON array items one by one.
    
    Example:
        ```python
        @app.stream("/items")
        async def stream_items():
            async def generate():
                for item in large_dataset:
                    yield item
            
            return JSONStreamResponse(generate())
        ```
    """
    
    def __init__(
        self,
        items: AsyncIterator[Dict[str, Any]],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ):
        self.items = items
        self.status_code = status_code
        self.media_type = "application/json"
        self.headers = headers or {}
        self.headers.setdefault("Cache-Control", "no-cache")
    
    async def __aiter__(self) -> AsyncIterator[bytes]:
        """Iterate over JSON array items."""
        yield b"["
        
        first = True
        async for item in self.items:
            if not first:
                yield b","
            first = False
            yield json.dumps(item).encode('utf-8')
        
        yield b"]"


class ChunkedResponse:
    """
    Chunked transfer encoding response.
    
    For streaming large files or data.
    """
    
    def __init__(
        self,
        content: AsyncIterator[bytes],
        media_type: str = "application/octet-stream",
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ):
        self.content = content
        self.media_type = media_type
        self.status_code = status_code
        self.headers = headers or {}
        self.headers["Transfer-Encoding"] = "chunked"
    
    async def __aiter__(self) -> AsyncIterator[bytes]:
        """Iterate over chunks."""
        async for chunk in self.content:
            if chunk:
                # Format as HTTP chunked encoding
                size = len(chunk)
                yield f"{size:x}\r\n".encode('utf-8')
                yield chunk
                yield b"\r\n"
        
        # End of chunks
        yield b"0\r\n\r\n"
