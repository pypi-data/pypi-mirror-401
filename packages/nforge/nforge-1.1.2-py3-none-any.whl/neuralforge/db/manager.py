"""
Database Manager - Async SQLAlchemy 2.0 implementation.

Provides:
- Async database engine and session management
- Connection pooling
- Transaction support
- Health checks
- Support for PostgreSQL, MySQL, and SQLite
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool, QueuePool
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Async database manager using SQLAlchemy 2.0.
    
    Supports:
    - PostgreSQL (asyncpg): postgresql+asyncpg://user:pass@host/db
    - MySQL (aiomysql): mysql+aiomysql://user:pass@host/db
    - SQLite (aiosqlite): sqlite+aiosqlite:///path/to/db.sqlite
    
    Features:
    - Connection pooling (except SQLite)
    - Async session management
    - Transaction support
    - Health checks
    
    Example:
        db_manager = DatabaseManager("sqlite+aiosqlite:///./app.db")
        
        # Using context manager
        async with db_manager.session() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
        
        # For dependency injection
        session = await db_manager.get_session()
    """

    def __init__(
        self,
        database_url: str,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_pre_ping: bool = True,
        pool_recycle: int = 3600
    ):
        """
        Initialize database manager.
        
        Args:
            database_url: Database connection URL
            echo: Log all SQL statements
            pool_size: Number of connections to maintain
            max_overflow: Max connections beyond pool_size
            pool_pre_ping: Test connections before using
            pool_recycle: Recycle connections after N seconds
        """
        self.database_url = database_url
        self.echo = echo

        # Determine if SQLite (no pooling needed)
        is_sqlite = "sqlite" in database_url.lower()

        # Create async engine
        if is_sqlite:
            self.engine: AsyncEngine = create_async_engine(
                database_url,
                echo=echo,
                poolclass=NullPool,  # SQLite doesn't need pooling
                connect_args={"check_same_thread": False}
            )
        else:
            self.engine: AsyncEngine = create_async_engine(
                database_url,
                echo=echo,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_pre_ping=pool_pre_ping,
                pool_recycle=pool_recycle,
                poolclass=QueuePool
            )

        # Create session factory
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

        # Log successful initialization
        db_type = "SQLite" if is_sqlite else "PostgreSQL/MySQL"
        logger.info(f"DatabaseManager initialized: {db_type} at {database_url}")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get async database session with automatic commit/rollback.
        
        Usage:
            async with db_manager.session() as session:
                result = await session.execute(select(User))
                users = result.scalars().all()
                # Automatically commits on success, rolls back on error
        
        Yields:
            AsyncSession: SQLAlchemy async session
        """
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def get_session(self) -> AsyncSession:
        """
        Get a new async session (for dependency injection).
        
        Note: Caller is responsible for closing the session.
        
        Returns:
            AsyncSession: New database session
        """
        return self.async_session_maker()

    async def close(self):
        """Close database engine and all connections."""
        await self.engine.dispose()
        logger.info("Database engine closed")

    async def health_check(self) -> bool:
        """
        Check database connection health.
        
        Returns:
            bool: True if database is accessible, False otherwise
        """
        try:
            async with self.session() as session:
                await session.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    async def create_all_tables(self, base):
        """
        Create all tables defined in Base metadata.
        
        Args:
            base: SQLAlchemy DeclarativeBase class
        
        Note: For development/testing only. Use Alembic for production.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)
        logger.info("All tables created")

    async def drop_all_tables(self, base):
        """
        Drop all tables defined in Base metadata.
        
        Args:
            base: SQLAlchemy DeclarativeBase class
        
        Warning: This will delete all data!
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.drop_all)
        logger.info("All tables dropped")
