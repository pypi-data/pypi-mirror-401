"""
Database module exports.
"""

from .manager import DatabaseManager
from .base import Base
from typing import Optional
from contextlib import asynccontextmanager

# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_database_manager() -> DatabaseManager:
    """
    Get singleton DatabaseManager instance.
    
    This ensures only one DatabaseManager is created per application,
    preventing connection leaks and session cleanup warnings.
    
    Returns:
        DatabaseManager: Singleton database manager instance
    """
    global _db_manager

    if _db_manager is None:
        from neuralforge.config import get_settings
        settings = get_settings()

        _db_manager = DatabaseManager(
            database_url=settings.database_url,
            echo=settings.db_echo,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow
        )

    return _db_manager


@asynccontextmanager
async def get_db_session():
    """
    Database session dependency with automatic management.
    
    Features:
    - Automatic session creation
    - Auto-commit on success
    - Auto-rollback on error
    - Auto-close session (cleanup)
    
    Usage:
        from neuralforge.dependencies import Depends
        from neuralforge.db import get_db_session
        
        @app.endpoint("/users", methods=["POST"])
        async def create_user(db = Depends(get_db_session)):
            # db session is automatically managed
            user = User(name="John")
            db.add(user)
            # Commit happens automatically on success
            # Rollback happens automatically on error
            # Session cleanup happens automatically
            return {"id": user.id}
    
    Yields:
        AsyncSession: Database session
    
    Raises:
        Exception: Re-raises any exception after rollback
    """
    db_manager = get_database_manager()
    session = db_manager.get_session()

    try:
        yield session
        # Commit on success
        await session.commit()
    except Exception:
        # Rollback on error
        await session.rollback()
        raise
    finally:
        # Always cleanup
        await session.close()


__all__ = ["DatabaseManager", "Base", "get_database_manager", "get_db_session"]
