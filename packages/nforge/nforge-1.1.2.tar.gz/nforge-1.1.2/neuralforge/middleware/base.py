"""
Base Middleware Class - Foundation for all middleware.
"""

from typing import Callable
import logging

logger = logging.getLogger(__name__)


class BaseMiddleware:
    """
    Base class for all middleware.
    
    Middleware process requests and responses in the ASGI application.
    They can modify requests before they reach the application and
    modify responses before they are sent to the client.
    """

    async def __call__(self, scope: dict, receive: Callable, send: Callable, app: Callable):
        """
        Process request through middleware.
        
        Args:
            scope: ASGI scope dictionary
            receive: ASGI receive callable
            send: ASGI send callable
            app: Next application/middleware in chain
        """
        # Default implementation: pass through to next middleware/app
        await app(scope, receive, send)

    def __repr__(self) -> str:
        """String representation of middleware."""
        return f"<{self.__class__.__name__}>"


# Legacy classes for backwards compatibility
class Middleware(BaseMiddleware):
    """Legacy middleware class (deprecated, use BaseMiddleware)."""

    async def process(self, request, call_next):
        """Process request (legacy method)."""
        return await call_next(request)


class MiddlewareStack:
    """
    Middleware stack manager.
    
    Handles both class-based and functional middlewares.
    """

    def __init__(self):
        self.middlewares = []
        logger.info("Initialized MiddlewareStack")

    def add(self, middleware):
        """Add middleware instance to stack."""
        self.middlewares.append(middleware)

    def add_function(self, func, middleware_type="http"):
        """Add middleware function to stack."""
        self.middlewares.append(func)

    async def __call__(self, scope, receive, send, app):
        """Execute middleware stack."""
        if not self.middlewares:
            return await app(scope, receive, send)

        # Build the chain
        wrapped_app = app
        
        for middleware in reversed(self.middlewares):
            current_app = wrapped_app
            current_mw = middleware
            
            async def wrapper(s, r, sn, mw=current_mw, next_app=current_app):
                # Only process HTTP
                if s["type"] != "http":
                    return await next_app(s, r, sn)

                import inspect
                from neuralforge.http.request import Request
                
                # Check signature
                try:
                    sig = inspect.signature(mw)
                    is_functional = len(sig.parameters) == 2
                except Exception:
                    is_functional = False

                if is_functional:
                    # Capture response state
                    resp_state = {
                        "status": 200,
                        "headers": {}, # dict for uniqueness
                        "body": b""
                    }

                    class ResponseProxy:
                        def __init__(self, state):
                            self._state = state
                            self.headers = state["headers"]
                            self.status_code = state["status"]
                        
                        async def __call__(self, scope, receive, send_func):
                            # Finalize headers
                            final_headers = []
                            for k, v in self.headers.items():
                                final_headers.append((str(k).encode(), str(v).encode()))
                            
                            await send_func({
                                "type": "http.response.start",
                                "status": self.status_code,
                                "headers": final_headers
                            })
                            await send_func({
                                "type": "http.response.body",
                                "body": self._state["body"]
                            })

                    resp_proxy = ResponseProxy(resp_state)
                    
                    async def middleware_send(message):
                        if message["type"] == "http.response.start":
                            resp_state["status"] = message["status"]
                            for k, v in message.get("headers", []):
                                key = k.decode().lower() if isinstance(k, bytes) else k.lower()
                                resp_state["headers"][key] = v.decode() if isinstance(v, bytes) else v
                        elif message["type"] == "http.response.body":
                            resp_state["body"] += message.get("body", b"")

                    async def call_next(request_obj):
                        await next_app(s, r, middleware_send)
                        # Sync status_code in case it was modified
                        resp_proxy.status_code = resp_state["status"]
                        return resp_proxy

                    # Run middleware
                    result = await mw(Request(s, r, sn), call_next)
                    
                    # Send final response
                    if isinstance(result, ResponseProxy):
                        await result(s, r, sn)
                    else:
                        # Fallback if middleware didn't return the proxy
                        await resp_proxy(s, r, sn)
                else:
                    # Standard ASGI middleware
                    await mw(s, r, sn, next_app)

            wrapped_app = wrapper

        return await wrapped_app(scope, receive, send)
