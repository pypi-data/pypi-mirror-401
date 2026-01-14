"""
API Key Model - Persistent storage for API keys.
"""

from sqlalchemy import Column, String, DateTime, JSON, Integer, Boolean
from neuralforge.db.base import Base
from datetime import datetime


class APIKey(Base):
    """
    API Key model for persistent storage.
    
    Stores API keys securely with hashing, expiration, and usage tracking.
    Keys are never stored in plaintext - only SHA256 hashes are persisted.
    """
    __tablename__ = "api_keys"

    # Primary key is the short key_id (first 16 chars of hash)
    id = Column(String(16), primary_key=True)

    # Full SHA256 hash of the API key (for verification)
    key_hash = Column(String(64), unique=True, nullable=False, index=True)

    # User information
    user_id = Column(String(100), nullable=False, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255))

    # Permissions (JSON array of scope strings)
    scopes = Column(JSON, default=list, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    last_used_at = Column(DateTime)

    # Usage tracking
    usage_count = Column(Integer, default=0, nullable=False)

    # Rate limiting
    rate_limit_per_minute = Column(Integer, default=100, nullable=False)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)

    # Additional metadata (JSON object) - renamed from 'metadata' to avoid SQLAlchemy conflict
    extra_metadata = Column(JSON, default=dict)

    def __repr__(self):
        return f"<APIKey {self.id} user={self.user_id} active={self.is_active}>"

    def is_expired(self) -> bool:
        """Check if API key has expired."""
        return datetime.utcnow() > self.expires_at

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "key_id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "scopes": self.scopes,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "usage_count": self.usage_count,
            "rate_limit_per_minute": self.rate_limit_per_minute,
            "is_active": self.is_active,
            "is_expired": self.is_expired()
        }
