"""
Common dependencies for NeuralForge applications.
"""

from typing import Optional, AsyncGenerator, Dict


# ============================================================================
# Pagination
# ============================================================================

class Pagination:
    """
    Pagination parameters.
    
    Attributes:
        page: Current page number (1-indexed)
        limit: Items per page (max 100)
        offset: Offset for database queries
    """

    def __init__(self, page: int = 1, limit: int = 10):
        self.page = max(1, page)
        self.limit = min(100, max(1, limit))
        self.offset = (self.page - 1) * self.limit

    def __repr__(self):
        return f"Pagination(page={self.page}, limit={self.limit}, offset={self.offset})"

    def dict(self) -> Dict[str, int]:
        """Convert to dictionary."""
        return {
            "page": self.page,
            "limit": self.limit,
            "offset": self.offset
        }


def get_pagination(page: int = 1, limit: int = 10) -> Pagination:
    """
    Get pagination parameters from query params.
    
    Usage:
        @app.get("/posts")
        async def list_posts(
            pagination = Depends(get_pagination),
            db = Depends(get_db_session)
        ):
            posts = await db.query(Post)\\
                .offset(pagination.offset)\\
                .limit(pagination.limit)\\
                .all()
            return {
                "posts": posts,
                "page": pagination.page,
                "total": await db.query(Post).count()
            }
    
    Args:
        page: Page number (default: 1)
        limit: Items per page (default: 10, max: 100)
    
    Returns:
        Pagination object
    """
    return Pagination(page, limit)


# ============================================================================
# Settings
# ============================================================================

def get_settings():
    """
    Get application settings.
    
    Usage:
        @app.get("/config")
        async def get_config(settings = Depends(get_settings)):
            return {
                "debug": settings.debug,
                "environment": settings.environment
            }
    
    Returns:
        Application settings
    """
    from neuralforge.config import get_settings as _get_settings
    return _get_settings()


# ============================================================================
# Database Session
# ============================================================================

async def get_db_session() -> AsyncGenerator:
    """
    Get async database session.
    
    Uses singleton DatabaseManager to prevent connection leaks.
    
    Usage:
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy import select
        
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db_session)):
            result = await db.execute(select(User))
            users = result.scalars().all()
            return users
    
    Yields:
        AsyncSession: SQLAlchemy async session
    """
    from neuralforge.db import get_database_manager

    db_manager = get_database_manager()

    async with db_manager.session() as session:
        yield session


# ============================================================================
# Authentication
# ============================================================================

async def get_current_user(request: "Request"):
    """
    Get current authenticated user.
    
    Usage:
        @app.get("/me")
        async def get_me(user = Depends(get_current_user)):
            return user
    
    Args:
        request: HTTP request
    
    Returns:
        Authenticated user
    
    Raises:
        UnauthorizedException: If not authenticated
    """
    from neuralforge.auth import AuthManager
    from neuralforge.routing.exceptions import UnauthorizedException

    auth_manager = AuthManager()
    user = await auth_manager.authenticate(request)

    if not user:
        raise UnauthorizedException("Authentication required")

    return user


async def get_current_user_optional(request: "Request"):
    """
    Get current user if authenticated, None otherwise.
    
    Usage:
        @app.get("/posts")
        async def list_posts(user = Depends(get_current_user_optional)):
            if user:
                # Show user-specific posts
                return await get_user_posts(user.id)
            else:
                # Show public posts
                return await get_public_posts()
    
    Args:
        request: HTTP request
    
    Returns:
        Authenticated user or None
    """
    from neuralforge.auth import AuthManager

    auth_manager = AuthManager()
    return await auth_manager.authenticate(request)


# ============================================================================
# Request Context
# ============================================================================

def get_request_id(request: "Request") -> str:
    """
    Get or generate request ID for tracing.
    
    Usage:
        @app.get("/api/data")
        async def get_data(request_id = Depends(get_request_id)):
            logger.info(f"Processing request {request_id}")
            return {"request_id": request_id}
    
    Args:
        request: HTTP request
    
    Returns:
        Request ID
    """
    import uuid

    # Try to get from headers first
    request_id = request.get_header("X-Request-ID")
    if not request_id:
        # Generate new one
        request_id = str(uuid.uuid4())

    return request_id


def get_client_ip(request: "Request") -> Optional[str]:
    """
    Get client IP address.
    
    Usage:
        @app.post("/login")
        async def login(
            credentials: LoginRequest,
            client_ip = Depends(get_client_ip)
        ):
            logger.info(f"Login attempt from {client_ip}")
            return await authenticate(credentials)
    
    Args:
        request: HTTP request
    
    Returns:
        Client IP address or None
    """
    # Check X-Forwarded-For header (for proxies)
    forwarded_for = request.get_header("X-Forwarded-For")
    if forwarded_for:
        # Get first IP in the chain
        return forwarded_for.split(",")[0].strip()

    # Get from client tuple
    if request.client:
        return request.client[0]

    return None
