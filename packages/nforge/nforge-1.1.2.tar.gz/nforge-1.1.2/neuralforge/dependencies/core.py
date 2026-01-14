"""
Dependency Injection Core - Depends class and scope management.
"""

from typing import Callable, TypeVar
from enum import Enum

T = TypeVar('T')


class DependencyScope(Enum):
    """
    Dependency scope types.
    
    - REQUEST: New instance per request (default)
    - SINGLETON: Single instance for app lifetime
    - TRANSIENT: New instance every time (no caching)
    """
    REQUEST = "request"
    SINGLETON = "singleton"
    TRANSIENT = "transient"


class Depends:
    """
    Dependency injection marker.
    
    Marks a function parameter as a dependency that should be
    automatically resolved and injected.
    
    Example:
        def get_db():
            return Database()
        
        @app.get("/users")
        async def get_users(db = Depends(get_db)):
            return await db.query(User).all()
    
    Args:
        dependency: Callable that returns the dependency value
        use_cache: Whether to cache the dependency (default: True)
        scope: Dependency scope (REQUEST, SINGLETON, or TRANSIENT)
    """

    def __init__(
        self,
        dependency: Callable[..., T],
        *,
        use_cache: bool = True,
        scope: DependencyScope = DependencyScope.REQUEST
    ):
        self.dependency = dependency
        self.use_cache = use_cache
        self.scope = scope if use_cache else DependencyScope.TRANSIENT

    def __repr__(self):
        return f"Depends({self.dependency.__name__}, scope={self.scope.value})"

    def __eq__(self, other):
        if not isinstance(other, Depends):
            return False
        return (
            self.dependency == other.dependency and
            self.scope == other.scope
        )

    def __hash__(self):
        return hash((self.dependency, self.scope))
