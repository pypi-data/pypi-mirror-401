"""
Base model class for all database models.
"""

from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from typing import Any, Dict


class Base(DeclarativeBase):
    """
    Base class for all database models.
    
    Provides:
    - Automatic table naming (pluralized class name)
    - Common fields: id, created_at, updated_at
    - Utility methods: dict(), __repr__()
    
    Example:
        class User(Base):
            __tablename__ = "users"  # Optional, auto-generated if not provided
            
            name = Column(String(100))
            email = Column(String(100), unique=True)
        
        # Automatic fields:
        # - id: Integer primary key
        # - created_at: DateTime (auto-set on creation)
        # - updated_at: DateTime (auto-updated on modification)
    """

    # Generate __tablename__ automatically if not provided
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name from class name (lowercase + 's')."""
        return cls.__name__.lower() + 's'

    # Common fields for all models
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary.
        
        Returns:
            dict: Model data as dictionary
        
        Example:
            user = User(name="John", email="john@example.com")
            data = user.dict()
            # {'id': 1, 'name': 'John', 'email': 'john@example.com', ...}
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self) -> str:
        """String representation of model."""
        return f"<{self.__class__.__name__}(id={self.id})>"
