"""
Dependency Resolver - Resolves and caches dependencies.
"""

from typing import Dict, Set, Any, Callable
from inspect import signature, iscoroutinefunction
import logging

from .core import Depends, DependencyScope

logger = logging.getLogger(__name__)


class CircularDependencyError(Exception):
    """Raised when a circular dependency is detected."""
    pass


class DependencyResolver:
    """
    Resolves and caches dependencies.
    
    Handles:
    - Dependency resolution
    - Circular dependency detection
    - Caching based on scope (request/singleton/transient)
    - Sub-dependency resolution (dependencies of dependencies)
    - Both async and sync dependencies
    
    Example:
        resolver = DependencyResolver()
        
        def get_config():
            return {"db_url": "sqlite:///db.sqlite"}
        
        result = await resolver.resolve(get_config, DependencyScope.REQUEST)
    """

    def __init__(self):
        self._request_cache: Dict[Callable, Any] = {}
        self._singleton_cache: Dict[Callable, Any] = {}
        self._resolving: Set[Callable] = set()

    async def resolve(
        self,
        dependency: Callable,
        scope: DependencyScope,
        **context
    ) -> Any:
        """
        Resolve a dependency.
        
        Args:
            dependency: Function to call
            scope: Dependency scope (REQUEST/SINGLETON/TRANSIENT)
            **context: Additional context (request, scope, etc.)
        
        Returns:
            Resolved dependency value
        
        Raises:
            CircularDependencyError: If circular dependency detected
        """
        # Check for circular dependencies
        if dependency in self._resolving:
            dep_chain = " -> ".join([d.__name__ for d in self._resolving])
            raise CircularDependencyError(
                f"Circular dependency detected: {dep_chain} -> {dependency.__name__}"
            )

        # Check cache based on scope
        if scope == DependencyScope.SINGLETON:
            if dependency in self._singleton_cache:
                logger.debug(f"Using cached singleton: {dependency.__name__}")
                return self._singleton_cache[dependency]
        elif scope == DependencyScope.REQUEST:
            if dependency in self._request_cache:
                logger.debug(f"Using cached request dependency: {dependency.__name__}")
                return self._request_cache[dependency]

        # Mark as resolving
        self._resolving.add(dependency)

        try:
            # Get dependency's own dependencies
            sig = signature(dependency)
            dep_kwargs = {}

            for param_name, param in sig.parameters.items():
                if isinstance(param.default, Depends):
                    # Recursively resolve sub-dependency
                    sub_dep = param.default.dependency
                    sub_scope = param.default.scope

                    logger.debug(
                        f"Resolving sub-dependency: {param_name} = {sub_dep.__name__}"
                    )

                    dep_kwargs[param_name] = await self.resolve(
                        sub_dep,
                        sub_scope,
                        **context
                    )
                elif param_name in context:
                    # Use provided context value
                    dep_kwargs[param_name] = context[param_name]

            # Call dependency
            logger.debug(f"Calling dependency: {dependency.__name__}")

            if iscoroutinefunction(dependency):
                result = await dependency(**dep_kwargs)
            else:
                result = dependency(**dep_kwargs)

            # Handle generator dependencies (like database sessions)
            import inspect
            if inspect.isasyncgen(result):
                # Async generator - get first value
                result = await result.__anext__()
            elif inspect.isgenerator(result):
                # Regular generator - get first value
                result = next(result)

            # Cache based on scope
            if scope == DependencyScope.SINGLETON:
                self._singleton_cache[dependency] = result
                logger.debug(f"Cached singleton: {dependency.__name__}")
            elif scope == DependencyScope.REQUEST:
                self._request_cache[dependency] = result
                logger.debug(f"Cached request dependency: {dependency.__name__}")

            return result

        finally:
            self._resolving.remove(dependency)

    def clear_request_cache(self):
        """Clear request-scoped cache."""
        logger.debug(f"Clearing request cache ({len(self._request_cache)} items)")
        self._request_cache.clear()

    def clear_singleton_cache(self):
        """Clear singleton cache."""
        logger.debug(f"Clearing singleton cache ({len(self._singleton_cache)} items)")
        self._singleton_cache.clear()

    def clear_all_caches(self):
        """Clear all caches."""
        self.clear_request_cache()
        self.clear_singleton_cache()

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "request_cache_size": len(self._request_cache),
            "singleton_cache_size": len(self._singleton_cache),
            "total_cached": len(self._request_cache) + len(self._singleton_cache)
        }
