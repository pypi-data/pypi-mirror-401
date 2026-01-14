"""
Middleware Chain Manager - Manages middleware execution order and configuration.
"""

from typing import List, Tuple, Callable
import logging

from .base import BaseMiddleware

logger = logging.getLogger(__name__)


class MiddlewareChain:
    """
    Manages middleware execution order and configuration.
    
    Middleware are executed in priority order (lower priority = earlier execution).
    Default priorities:
    - Security Headers: 10
    - CORS: 20
    - Rate Limiting: 30
    - Logging: 40
    """

    def __init__(self):
        """Initialize middleware chain."""
        self.middleware: List[Tuple[int, BaseMiddleware]] = []
        logger.info("Middleware chain initialized")

    def add(self, middleware: BaseMiddleware, priority: int = 50):
        """
        Add middleware to the chain.
        
        Args:
            middleware: Middleware instance to add
            priority: Execution priority (lower = earlier, default: 50)
        """
        self.middleware.append((priority, middleware))
        self.middleware.sort(key=lambda x: x[0])

        middleware_name = middleware.__class__.__name__
        logger.info(f"Added middleware: {middleware_name} (priority: {priority})")

    def remove(self, middleware_class: type):
        """
        Remove middleware by class type.
        
        Args:
            middleware_class: Class of middleware to remove
        """
        self.middleware = [
            (p, m) for p, m in self.middleware
            if not isinstance(m, middleware_class)
        ]
        logger.info(f"Removed middleware: {middleware_class.__name__}")

    def clear(self):
        """Remove all middleware from chain."""
        self.middleware.clear()
        logger.info("Cleared all middleware")

    def build(self, app: Callable) -> Callable:
        """
        Build the middleware chain around the application.
        
        Middleware are wrapped in reverse order so that the first middleware
        in the list is the outermost (executes first).
        
        Args:
            app: ASGI application callable
        
        Returns:
            Wrapped application with middleware chain
        """
        if not self.middleware:
            logger.debug("No middleware in chain, returning app as-is")
            return app

        # Wrap middleware in reverse order
        wrapped_app = app
        for priority, middleware in reversed(self.middleware):
            middleware_name = middleware.__class__.__name__
            logger.debug(f"Wrapping app with {middleware_name} (priority: {priority})")

            # Capture current wrapped_app in closure
            current_app = wrapped_app

            # Create wrapper function
            async def make_wrapper(scope, receive, send, mw=middleware, inner_app=current_app):
                await mw(scope, receive, send, inner_app)

            wrapped_app = make_wrapper

        logger.info(f"Built middleware chain with {len(self.middleware)} middleware")
        return wrapped_app

    def get_middleware_list(self) -> List[str]:
        """
        Get list of middleware names in execution order.
        
        Returns:
            List of middleware class names
        """
        return [m.__class__.__name__ for _, m in self.middleware]

    def __len__(self) -> int:
        """Get number of middleware in chain."""
        return len(self.middleware)

    def __repr__(self) -> str:
        """String representation of middleware chain."""
        middleware_names = self.get_middleware_list()
        return f"<MiddlewareChain({len(self)} middleware: {', '.join(middleware_names)})>"
