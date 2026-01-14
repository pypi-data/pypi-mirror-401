"""
WebSocket Streaming Support for NeuralForge.

Provides enhanced WebSocket utilities for bidirectional
streaming and real-time communication.
"""

import asyncio
import json
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class WebSocketState(Enum):
    """WebSocket connection state."""
    CONNECTING = "connecting"
    CONNECTED = "connected"
    CLOSING = "closing"
    CLOSED = "closed"


@dataclass
class WebSocketMessage:
    """
    Represents a WebSocket message.
    
    Attributes:
        type: Message type (text, binary, ping, pong, close)
        data: Message payload
        timestamp: When the message was created
    """
    type: str = "text"
    data: Any = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_json(self) -> str:
        """Serialize message to JSON."""
        if isinstance(self.data, (dict, list)):
            return json.dumps(self.data)
        return str(self.data)
    
    @classmethod
    def from_json(cls, data: str) -> "WebSocketMessage":
        """Create message from JSON string."""
        try:
            parsed = json.loads(data)
            return cls(type="text", data=parsed)
        except json.JSONDecodeError:
            return cls(type="text", data=data)


class StreamingWebSocket:
    """
    Enhanced WebSocket wrapper for streaming.
    
    Provides async iteration, message buffering,
    and connection management.
    
    Example:
        ```python
        @app.websocket("/ws/chat")
        async def chat_websocket(ws: StreamingWebSocket):
            async with ws:
                async for message in ws:
                    response = await process(message)
                    await ws.send_stream(generate_response(response))
        ```
    """
    
    def __init__(
        self,
        websocket: Any,  # The underlying websocket object
        max_message_size: int = 1024 * 1024,  # 1MB default
        ping_interval: float = 30.0,
        ping_timeout: float = 10.0
    ):
        self._websocket = websocket
        self.max_message_size = max_message_size
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        
        self._state = WebSocketState.CONNECTING
        self._connected_at: Optional[datetime] = None
        self._message_count_in = 0
        self._message_count_out = 0
        self._bytes_in = 0
        self._bytes_out = 0
        self._ping_task: Optional[asyncio.Task] = None
    
    @property
    def state(self) -> WebSocketState:
        """Get current connection state."""
        return self._state
    
    @property
    def is_connected(self) -> bool:
        """Check if connection is active."""
        return self._state == WebSocketState.CONNECTED
    
    async def __aenter__(self):
        """Enter async context - accept connection."""
        await self.accept()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context - close connection."""
        await self.close()
    
    async def accept(self):
        """Accept the WebSocket connection."""
        if hasattr(self._websocket, 'accept'):
            await self._websocket.accept()
        self._state = WebSocketState.CONNECTED
        self._connected_at = datetime.utcnow()
        logger.debug("WebSocket connection accepted")
    
    async def close(self, code: int = 1000, reason: str = ""):
        """Close the WebSocket connection."""
        if self._state in (WebSocketState.CLOSING, WebSocketState.CLOSED):
            return
        
        self._state = WebSocketState.CLOSING
        
        if self._ping_task:
            self._ping_task.cancel()
            try:
                await self._ping_task
            except asyncio.CancelledError:
                pass
        
        try:
            if hasattr(self._websocket, 'close'):
                await self._websocket.close(code=code, reason=reason)
        except Exception as e:
            logger.debug(f"Error closing WebSocket: {e}")
        finally:
            self._state = WebSocketState.CLOSED
            logger.debug(f"WebSocket closed: {code} {reason}")
    
    async def send(self, data: Any):
        """
        Send data through the WebSocket.
        
        Args:
            data: Data to send (will be JSON serialized if dict/list)
        """
        if not self.is_connected:
            raise RuntimeError("WebSocket is not connected")
        
        if isinstance(data, (dict, list)):
            message = json.dumps(data)
        elif isinstance(data, WebSocketMessage):
            message = data.to_json()
        else:
            message = str(data)
        
        if hasattr(self._websocket, 'send_text'):
            await self._websocket.send_text(message)
        elif hasattr(self._websocket, 'send'):
            await self._websocket.send(message)
        
        self._message_count_out += 1
        self._bytes_out += len(message.encode('utf-8'))
    
    async def send_bytes(self, data: bytes):
        """Send binary data through the WebSocket."""
        if not self.is_connected:
            raise RuntimeError("WebSocket is not connected")
        
        if hasattr(self._websocket, 'send_bytes'):
            await self._websocket.send_bytes(data)
        elif hasattr(self._websocket, 'send'):
            await self._websocket.send(data)
        
        self._message_count_out += 1
        self._bytes_out += len(data)
    
    async def receive(self) -> WebSocketMessage:
        """
        Receive a message from the WebSocket.
        
        Returns:
            WebSocketMessage containing the received data
        """
        if not self.is_connected:
            raise RuntimeError("WebSocket is not connected")
        
        if hasattr(self._websocket, 'receive_text'):
            data = await self._websocket.receive_text()
            self._message_count_in += 1
            self._bytes_in += len(data.encode('utf-8'))
            return WebSocketMessage.from_json(data)
        elif hasattr(self._websocket, 'receive'):
            data = await self._websocket.receive()
            if isinstance(data, dict):
                # Starlette-style receive
                if 'text' in data:
                    self._message_count_in += 1
                    self._bytes_in += len(data['text'].encode('utf-8'))
                    return WebSocketMessage.from_json(data['text'])
                elif 'bytes' in data:
                    self._message_count_in += 1
                    self._bytes_in += len(data['bytes'])
                    return WebSocketMessage(type="binary", data=data['bytes'])
            return WebSocketMessage(type="text", data=data)
        
        raise RuntimeError("WebSocket does not support receive")
    
    async def __aiter__(self) -> AsyncIterator[WebSocketMessage]:
        """
        Iterate over incoming messages.
        
        Example:
            async for message in websocket:
                print(message.data)
        """
        while self.is_connected:
            try:
                message = await self.receive()
                yield message
            except Exception as e:
                logger.debug(f"WebSocket receive error: {e}")
                break
    
    async def send_stream(
        self,
        generator: AsyncIterator[Any],
        event_type: str = "message"
    ):
        """
        Stream data from an async generator.
        
        Args:
            generator: Async generator yielding data
            event_type: Event type to include in messages
        
        Example:
            async def generate():
                for i in range(10):
                    yield f"message {i}"
            
            await ws.send_stream(generate())
        """
        index = 0
        try:
            async for item in generator:
                await self.send({
                    "event": event_type,
                    "data": item,
                    "index": index
                })
                index += 1
            
            await self.send({
                "event": "done",
                "total_items": index
            })
        except Exception as e:
            await self.send({
                "event": "error",
                "error": str(e)
            })
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        stats = {
            "state": self._state.value,
            "messages_in": self._message_count_in,
            "messages_out": self._message_count_out,
            "bytes_in": self._bytes_in,
            "bytes_out": self._bytes_out,
        }
        
        if self._connected_at:
            duration = (datetime.utcnow() - self._connected_at).total_seconds()
            stats["duration_seconds"] = round(duration, 2)
        
        return stats


class WebSocketManager:
    """
    Manages multiple WebSocket connections.
    
    Useful for broadcasting messages to multiple clients
    and managing connection pools.
    
    Example:
        ```python
        manager = WebSocketManager()
        
        @app.websocket("/ws")
        async def websocket_endpoint(websocket):
            ws = StreamingWebSocket(websocket)
            await manager.connect(ws)
            try:
                async for message in ws:
                    # Broadcast to all connected clients
                    await manager.broadcast(message.data)
            finally:
                await manager.disconnect(ws)
        ```
    """
    
    def __init__(self, max_connections: Optional[int] = None):
        self._connections: Set[StreamingWebSocket] = set()
        self._connection_groups: Dict[str, Set[StreamingWebSocket]] = {}
        self._max_connections = max_connections
        self._lock = asyncio.Lock()
    
    @property
    def connection_count(self) -> int:
        """Get number of active connections."""
        return len(self._connections)
    
    async def connect(
        self,
        websocket: StreamingWebSocket,
        group: Optional[str] = None
    ):
        """
        Add a WebSocket connection.
        
        Args:
            websocket: WebSocket to add
            group: Optional group name for the connection
        """
        async with self._lock:
            if self._max_connections and len(self._connections) >= self._max_connections:
                raise RuntimeError("Maximum connections reached")
            
            self._connections.add(websocket)
            
            if group:
                if group not in self._connection_groups:
                    self._connection_groups[group] = set()
                self._connection_groups[group].add(websocket)
        
        logger.debug(f"WebSocket connected. Total: {len(self._connections)}")
    
    async def disconnect(
        self,
        websocket: StreamingWebSocket,
        group: Optional[str] = None
    ):
        """
        Remove a WebSocket connection.
        
        Args:
            websocket: WebSocket to remove
            group: Optional group name
        """
        async with self._lock:
            self._connections.discard(websocket)
            
            if group and group in self._connection_groups:
                self._connection_groups[group].discard(websocket)
                if not self._connection_groups[group]:
                    del self._connection_groups[group]
        
        logger.debug(f"WebSocket disconnected. Total: {len(self._connections)}")
    
    async def broadcast(
        self,
        message: Any,
        exclude: Optional[Set[StreamingWebSocket]] = None
    ):
        """
        Broadcast message to all connections.
        
        Args:
            message: Message to broadcast
            exclude: Set of connections to exclude
        """
        exclude = exclude or set()
        
        async with self._lock:
            connections = self._connections - exclude
        
        send_tasks = [
            ws.send(message) for ws in connections
            if ws.is_connected
        ]
        
        if send_tasks:
            results = await asyncio.gather(*send_tasks, return_exceptions=True)
            errors = [r for r in results if isinstance(r, Exception)]
            if errors:
                logger.warning(f"Broadcast had {len(errors)} errors")
    
    async def broadcast_to_group(
        self,
        group: str,
        message: Any,
        exclude: Optional[Set[StreamingWebSocket]] = None
    ):
        """
        Broadcast message to a specific group.
        
        Args:
            group: Group name
            message: Message to broadcast
            exclude: Set of connections to exclude
        """
        exclude = exclude or set()
        
        async with self._lock:
            if group not in self._connection_groups:
                return
            connections = self._connection_groups[group] - exclude
        
        send_tasks = [
            ws.send(message) for ws in connections
            if ws.is_connected
        ]
        
        if send_tasks:
            await asyncio.gather(*send_tasks, return_exceptions=True)
    
    async def close_all(self, code: int = 1000, reason: str = ""):
        """Close all connections."""
        async with self._lock:
            connections = list(self._connections)
        
        close_tasks = [ws.close(code, reason) for ws in connections]
        await asyncio.gather(*close_tasks, return_exceptions=True)
        
        async with self._lock:
            self._connections.clear()
            self._connection_groups.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        return {
            "total_connections": len(self._connections),
            "groups": {
                name: len(conns) 
                for name, conns in self._connection_groups.items()
            },
            "max_connections": self._max_connections,
        }
