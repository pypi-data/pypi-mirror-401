"""
Authentication Manager - Multi-provider authentication and authorization.
"""

from typing import Optional, List, Dict, Any, Callable, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging
import hashlib
import secrets

if TYPE_CHECKING:
    from neuralforge import NeuralForge

logger = logging.getLogger(__name__)


# ============================================================================
# Data Models
# ============================================================================

class Permission(str, Enum):
    """Standard permissions."""
    READ_DATA = "read:data"
    WRITE_DATA = "write:data"
    READ_MODELS = "read:models"
    DEPLOY_MODELS = "deploy:models"
    VIEW_METRICS = "view:metrics"
    ADMIN = "admin"
    ALL = "*"


@dataclass
class AuthUser:
    """Authenticated user."""
    id: str
    username: str
    email: Optional[str] = None
    roles: List[str] = None
    permissions: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.roles is None:
            self.roles = []
        if self.permissions is None:
            self.permissions = []
        if self.metadata is None:
            self.metadata = {}

    def has_role(self, role: str) -> bool:
        """Check if user has role."""
        return role in self.roles

    def has_permission(self, permission: str) -> bool:
        """Check if user has permission."""
        return (
            permission in self.permissions or
            Permission.ALL.value in self.permissions or
            "admin" in self.roles
        )


# ============================================================================
# Authentication Providers
# ============================================================================

class AuthProvider:
    """Base class for authentication providers."""

    async def authenticate(self, request: Any) -> Optional[AuthUser]:
        """
        Authenticate request and return user.

        Args:
            request: Request object

        Returns:
            AuthUser if authenticated, None otherwise
        """
        raise NotImplementedError


class APIKeyAuth(AuthProvider):
    """
    API Key authentication provider with database persistence.

    Features:
    - Loads keys from database (survives restart)
    - In-memory caching for performance
    - Key prefix validation ("nf_")
    - Expiration checking
    - Usage tracking
    """

    KEY_PREFIX = "nf_"

    def __init__(
        self,
        header_name: str = "X-API-Key",
        query_param: str = "api_key",
        validate_fn: Optional[Callable[[str], bool]] = None,
        db_session_factory = None
    ):
        self.header_name = header_name
        self.query_param = query_param
        self.validate_fn = validate_fn
        self.db_session_factory = db_session_factory
        self.api_keys: Dict[str, AuthUser] = {}  # key_hash -> user

    def add_api_key(self, key: str, user: AuthUser):
        """Add API key to cache (stores by hash for security)."""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        self.api_keys[key_hash] = user
        logger.info(f"Added API key to cache for user: {user.username}")

    def remove_api_key(self, key: str):
        """Remove API key."""
        if key in self.api_keys:
            del self.api_keys[key]
            logger.info("Removed API key")

    async def authenticate(self, request: Any) -> Optional[AuthUser]:
        """
        Authenticate using API key with database fallback.

        Process:
        1. Extract key from header/query
        2. Validate prefix
        3. Check cache (fast)
        4. Load from DB (slow)
        5. Update usage stats
        """
        # Extract API key
        api_key = None
        if hasattr(request, 'headers'):
            api_key = request.headers.get(self.header_name)
        if not api_key and hasattr(request, 'query_params'):
            api_key = request.query_params.get(self.query_param)

        if not api_key:
            return None

        # Validate prefix
        if not api_key.startswith(self.KEY_PREFIX):
            logger.warning("Invalid API key prefix")
            return None

        # Hash for lookup
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # Check cache first
        if key_hash in self.api_keys:
            user = self.api_keys[key_hash]
            if "expires_at" in user.metadata:
                expires_at = datetime.fromisoformat(user.metadata["expires_at"])
                if datetime.utcnow() > expires_at:
                    del self.api_keys[key_hash]
                    return None
            return user

        # Load from database
        if self.db_session_factory:
            from neuralforge.db.models import APIKey
            from sqlalchemy import select

            try:
                async with self.db_session_factory() as session:
                    result = await session.execute(
                        select(APIKey).where(
                            APIKey.key_hash == key_hash,
                            APIKey.is_active.is_(True)
                        )
                    )
                    db_key = result.scalar_one_or_none()

                    if not db_key or datetime.utcnow() > db_key.expires_at:
                        return None

                    # Update usage
                    db_key.last_used_at = datetime.utcnow()
                    db_key.usage_count += 1
                    await session.commit()

                    # Create and cache user
                    user = AuthUser(
                        id=db_key.user_id,
                        username=db_key.username,
                        email=db_key.email,
                        permissions=db_key.scopes,
                        metadata={
                            "key_hash": key_hash,
                            "expires_at": db_key.expires_at.isoformat(),
                            "rate_limit": db_key.rate_limit_per_minute
                        }
                    )
                    self.api_keys[key_hash] = user
                    logger.info(f"Authenticated from DB: {user.username}")
                    return user
            except Exception as e:
                logger.error(f"DB auth error: {e}")

        return None


class JWTAuth(AuthProvider):
    """JWT (JSON Web Token) authentication provider."""

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        token_location: List[str] = None,
        header_name: str = "Authorization",
        header_type: str = "Bearer"
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_location = token_location or ["headers"]
        self.header_name = header_name
        self.header_type = header_type

    async def authenticate(self, request: Any) -> Optional[AuthUser]:
        """Authenticate using JWT."""
        try:
            import jwt
        except ImportError:
            raise ImportError(
                "PyJWT is required for JWT authentication. "
                "Install with: pip install pyjwt"
            )

        # Extract token
        token = None

        if "headers" in self.token_location and hasattr(request, 'headers'):
            auth_header = request.headers.get(self.header_name, "")
            if auth_header.startswith(f"{self.header_type} "):
                token = auth_header[len(f"{self.header_type} "):]

        if not token and "cookies" in self.token_location and hasattr(request, 'cookies'):
            token = request.cookies.get("access_token")

        if not token:
            return None

        try:
            # Decode token
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            # Create user from payload
            user = AuthUser(
                id=payload.get("sub"),
                username=payload.get("username", payload.get("sub")),
                email=payload.get("email"),
                roles=payload.get("roles", []),
                permissions=payload.get("permissions", []),
                metadata=payload
            )

            logger.debug(f"Authenticated user via JWT: {user.username}")

            return user

        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None

    def create_token(
        self,
        user: AuthUser,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT token for user.

        Args:
            user: User to create token for
            expires_delta: Token expiration time

        Returns:
            JWT token string
        """
        try:
            import jwt
        except ImportError:
            raise ImportError("PyJWT is required")

        if expires_delta is None:
            expires_delta = timedelta(days=7)

        expire = datetime.utcnow() + expires_delta

        payload = {
            "sub": user.id,
            "username": user.username,
            "email": user.email,
            "roles": user.roles,
            "permissions": user.permissions,
            "exp": expire,
            "iat": datetime.utcnow()
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        return token


class OAuth2(AuthProvider):
    """OAuth2 authentication provider."""

    def __init__(
        self,
        provider: str,  # google, github, etc.
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: List[str] = None
    ):
        self.provider = provider
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes or []

    async def authenticate(self, request: Any) -> Optional[AuthUser]:
        """Authenticate using OAuth2."""
        # OAuth2 flow implementation would go here
        # This is a simplified placeholder
        logger.info(f"OAuth2 authentication with {self.provider}")
        return None


# ============================================================================
# Authorization
# ============================================================================

class RBACPolicy:
    """Role-Based Access Control policy."""

    def __init__(
        self,
        roles: List[str] = None,
        permissions: List[str] = None,
        check_resource_ownership: bool = False
    ):
        self.roles = roles or []
        self.permissions = permissions or []
        self.check_resource_ownership = check_resource_ownership

    async def evaluate(self, user: AuthUser, resource: Any = None) -> bool:
        """
        Evaluate if user has access.

        Args:
            user: User to check
            resource: Resource being accessed (optional)

        Returns:
            True if access granted, False otherwise
        """
        # Check roles
        if self.roles:
            if not any(user.has_role(role) for role in self.roles):
                return False

        # Check permissions
        if self.permissions:
            if not any(user.has_permission(perm) for perm in self.permissions):
                return False

        # Check resource ownership
        if self.check_resource_ownership and resource:
            if hasattr(resource, 'owner_id'):
                if resource.owner_id != user.id and not user.has_role("admin"):
                    return False

        return True


# ============================================================================
# Authentication Manager
# ============================================================================

class AuthManager:
    """
    Central authentication and authorization manager.

    Supports:
    - Multiple authentication providers
    - Role-based access control (RBAC)
    - Permission management
    - API key management
    """

    def __init__(self, app: "NeuralForge"):
        self.app = app
        self.providers: List[AuthProvider] = []
        self.roles: Dict[str, List[str]] = {}  # role -> permissions
        self.policies: Dict[str, Any] = {}

        logger.info("Initialized AuthManager")

    # ========================================================================
    # Provider Management
    # ========================================================================

    def add_provider(self, provider: AuthProvider):
        """Add authentication provider."""
        self.providers.append(provider)
        logger.info(f"Added auth provider: {provider.__class__.__name__}")

    async def authenticate(self, request: Any) -> Optional[AuthUser]:
        """
        Authenticate request using all providers.

        Args:
            request: Request to authenticate

        Returns:
            AuthUser if authenticated, None otherwise
        """
        for provider in self.providers:
            try:
                user = await provider.authenticate(request)
                if user:
                    return user
            except Exception as e:
                logger.error(f"Error in auth provider {provider.__class__.__name__}: {e}")

        return None

    # ========================================================================
    # Role Management
    # ========================================================================

    def define_role(self, role: str, permissions: List[str]):
        """
        Define a role with permissions.

        Args:
            role: Role name
            permissions: List of permissions

        Example:
            >>> auth.define_role("ml_engineer", [
            >>>     Permission.READ_MODELS,
            >>>     Permission.DEPLOY_MODELS
            >>> ])
        """
        self.roles[role] = permissions
        logger.info(f"Defined role '{role}' with {len(permissions)} permissions")

    def get_role_permissions(self, role: str) -> List[str]:
        """Get permissions for a role."""
        return self.roles.get(role, [])

    def user_has_permission(self, user: AuthUser, permission: str) -> bool:
        """Check if user has permission."""
        # Direct permission check
        if user.has_permission(permission):
            return True

        # Check via roles
        for role in user.roles:
            role_perms = self.get_role_permissions(role)
            if permission in role_perms or Permission.ALL.value in role_perms:
                return True

        return False

    # ========================================================================
    # Policy Management
    # ========================================================================

    def add_policy(self, name: str, policy: Any):
        """Add authorization policy."""
        self.policies[name] = policy
        logger.info(f"Added policy: {name}")

    async def evaluate_policy(
        self,
        policy_name: str,
        user: AuthUser,
        resource: Any = None
    ) -> bool:
        """Evaluate policy for user and resource."""
        if policy_name not in self.policies:
            logger.warning(f"Policy not found: {policy_name}")
            return False

        policy = self.policies[policy_name]

        if hasattr(policy, 'evaluate'):
            return await policy.evaluate(user, resource)

        return False

    async def can_access_resource(
        self,
        user: AuthUser,
        resource: Any
    ) -> bool:
        """Check if user can access resource."""
        # Admin can access everything
        if user.has_role("admin"):
            return True

        # Check resource ownership
        if hasattr(resource, 'owner_id'):
            if resource.owner_id == user.id:
                return True

        # Check resource-specific permissions
        if hasattr(resource, 'required_permission'):
            return self.user_has_permission(user, resource.required_permission)

        return False

    async def create_api_key(
        self,
        user_id: str,
        username: str = None,
        email: str = None,
        expires_days: int = 365,
        scopes: List[str] = None,
        rate_limit_per_minute: int = 100,
        db_session = None
    ) -> Dict[str, str]:
        """
        Create a new API key for a user with database persistence.

        This method generates a secure API key, stores it in the database as a hash,
        and caches it in memory for fast lookups. Keys are never stored in plaintext.

        Args:
            user_id: Unique user identifier
            username: Username (defaults to user_id if not provided)
            email: User email address (optional)
            expires_days: Days until key expires (default: 365)
            scopes: List of permission scopes (default: all permissions)
            rate_limit_per_minute: Rate limit for this key (default: 100)
            db_session: Database session for persistence (optional but recommended)

        Returns:
            Dict containing:
            - key: Full API key (ONLY shown once! Store it securely!)
            - key_id: Short identifier for listing/revoking
            - expires_at: ISO format expiration date
            - user_id: User ID
            - username: Username
            - scopes: List of granted scopes
            - rate_limit_per_minute: Rate limit setting

        Example:
            >>> from neuralforge import NeuralForge
            >>> from neuralforge.auth import AuthManager
            >>> from neuralforge.dependencies import Depends
            >>> from neuralforge.db import get_db_session
            >>>
            >>> app = NeuralForge()
            >>> auth = AuthManager(app)
            >>>
            >>> # Create API key with database persistence
            >>> @app.endpoint("/admin/create-key", methods=["POST"])
            >>> async def create_key(
            ...     user_id: str,
            ...     db = Depends(get_db_session)
            ... ):
            ...     result = await auth.create_api_key(
            ...         user_id=user_id,
            ...         username="john_doe",
            ...         email="john@example.com",
            ...         scopes=["predict", "models:read"],
            ...         db_session=db
            ...     )
            ...     return result
            >>>
            >>> # Response:
            >>> # {
            >>> #   "key": "nf_abc123def456...",  # ONLY shown once!
            >>> #   "key_id": "a1b2c3d4e5f6",
            >>> #   "expires_at": "2026-12-28T13:55:00",
            >>> #   "user_id": "user_123",
            >>> #   "username": "john_doe",
            >>> #   "scopes": ["predict", "models:read"],
            >>> #   "rate_limit_per_minute": 100
            >>> # }

        Warning:
            The full API key is returned ONLY ONCE. It cannot be retrieved later.
            Store it securely! Only the hash is persisted in the database.

        Security:
            - Keys are generated using secrets.token_urlsafe (cryptographically secure)
            - Only SHA256 hashes are stored in database (never plaintext)
            - Keys have configurable expiration
            - Rate limiting per key
        """
        from neuralforge.db.models import APIKey

        # Generate secure random key with prefix
        api_key = f"nf_{secrets.token_urlsafe(32)}"

        # Hash the key for storage (NEVER store plaintext!)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        key_id = key_hash[:16]  # Short identifier for listing

        # Calculate expiration
        expires_at = datetime.utcnow() + timedelta(days=expires_days)

        # Persist to database if session provided
        if db_session:
            try:
                db_key = APIKey(
                    id=key_id,
                    key_hash=key_hash,
                    user_id=user_id,
                    username=username or user_id,
                    email=email,
                    scopes=scopes or [Permission.ALL.value],
                    expires_at=expires_at,
                    rate_limit_per_minute=rate_limit_per_minute,
                    is_active=True,
                    extra_metadata={
                        "created_by": "AuthManager",
                        "created_at": datetime.utcnow().isoformat()
                    }
                )
                db_session.add(db_key)
                await db_session.commit()

                logger.info(f"Created and persisted API key {key_id} for user: {user_id}")
            except Exception as e:
                logger.error(f"Failed to persist API key to database: {e}")
                await db_session.rollback()
                raise
        else:
            logger.warning(
                f"No database session provided for API key creation (user: {user_id}). "
                "Key will only be stored in memory and lost on restart!"
            )

        # Create user object for in-memory cache
        user = AuthUser(
            id=user_id,
            username=username or user_id,
            email=email,
            permissions=scopes or [Permission.ALL.value],
            metadata={
                "key_hash": key_hash,
                "key_id": key_id,
                "expires_at": expires_at.isoformat(),
                "rate_limit": rate_limit_per_minute
            }
        )

        # Add to APIKeyAuth provider (create if needed)
        api_key_provider = None
        for provider in self.providers:
            if isinstance(provider, APIKeyAuth):
                api_key_provider = provider
                break

        if not api_key_provider:
            api_key_provider = APIKeyAuth()
            self.providers.append(api_key_provider)
            logger.info("Created APIKeyAuth provider")

        # Store by hash in memory cache, not plaintext!
        api_key_provider.api_keys[key_hash] = user

        # Return comprehensive information
        return {
            "key": api_key,  # Full key - ONLY returned once!
            "key_id": key_id,  # For listing/revoking
            "expires_at": expires_at.isoformat(),
            "user_id": user_id,
            "username": username or user_id,
            "scopes": scopes or [Permission.ALL.value],
            "rate_limit_per_minute": rate_limit_per_minute
        }

    async def list_api_keys(
        self,
        user_id: str,
        db_session = None
    ) -> List[Dict[str, Any]]:
        """
        List all API keys for a user.

        Args:
            user_id: User ID to list keys for
            db_session: Database session

        Returns:
            List of API key information (without the actual keys)
        """
        if not db_session:
            logger.warning("No database session provided for listing API keys")
            return []

        from neuralforge.db.models import APIKey
        from sqlalchemy import select

        try:
            result = await db_session.execute(
                select(APIKey).where(APIKey.user_id == user_id)
            )
            keys = result.scalars().all()

            return [key.to_dict() for key in keys]
        except Exception as e:
            logger.error(f"Failed to list API keys: {e}")
            return []

    async def revoke_api_key(
        self,
        key_id: str,
        db_session = None
    ) -> bool:
        """
        Revoke an API key.

        Args:
            key_id: Key ID to revoke
            db_session: Database session

        Returns:
            True if revoked successfully
        """
        if not db_session:
            logger.warning("No database session provided for revoking API key")
            return False

        from neuralforge.db.models import APIKey
        from sqlalchemy import select

        try:
            result = await db_session.execute(
                select(APIKey).where(APIKey.id == key_id)
            )
            key = result.scalar_one_or_none()

            if not key:
                logger.warning(f"API key not found: {key_id}")
                return False

            key.is_active = False
            await db_session.commit()

            # Remove from cache
            for provider in self.providers:
                if isinstance(provider, APIKeyAuth):
                    if key.key_hash in provider.api_keys:
                        del provider.api_keys[key.key_hash]

            logger.info(f"Revoked API key: {key_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to revoke API key: {e}")
            await db_session.rollback()
            return False

    async def get_api_key_info(
        self,
        key_id: str,
        db_session = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get information about an API key.

        Args:
            key_id: Key ID
            db_session: Database session

        Returns:
            API key information or None
        """
        if not db_session:
            logger.warning("No database session provided")
            return None

        from neuralforge.db.models import APIKey
        from sqlalchemy import select

        try:
            result = await db_session.execute(
                select(APIKey).where(APIKey.id == key_id)
            )
            key = result.scalar_one_or_none()

            if not key:
                return None

            return key.to_dict()
        except Exception as e:
            logger.error(f"Failed to get API key info: {e}")
            return None


# ============================================================================
# Decorators
# ============================================================================

def require_auth(func: Callable = None, *, roles: List[str] = None, permissions: List[str] = None):
    """
    Decorator to require authentication.

    Example:
        >>> @require_auth
        >>> async def protected_endpoint():
        >>>     pass
        >>>
        >>> @require_auth(roles=["admin"])
        >>> async def admin_only():
        >>>     pass
    """
    def decorator(f: Callable):
        async def wrapper(*args, **kwargs):
            # This would be integrated with the request handling system
            # For now, it's a placeholder
            logger.debug(f"Auth check for {f.__name__}")
            return await f(*args, **kwargs)

        wrapper.__auth_required__ = True
        wrapper.__required_roles__ = roles or []
        wrapper.__required_permissions__ = permissions or []

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


async def get_current_user(request: Any = None, optional: bool = False) -> Optional[AuthUser]:
    """
    Dependency to get current authenticated user.

    This would be used with dependency injection:

    Example:
        >>> @app.endpoint("/profile")
        >>> async def get_profile(user = Depends(get_current_user)):
        >>>     return {"username": user.username}
    """
    # This would extract user from request context
    # Placeholder implementation
    if optional:
        return None

    # In real implementation, would raise 401 if not authenticated
    return AuthUser(id="test", username="test_user")


# ============================================================================
# API Key Management
# ============================================================================

class APIKeyManager:
    """Manager for API keys."""

    def __init__(self):
        self.keys: Dict[str, Dict[str, Any]] = {}

    async def generate(
        self,
        user_id: str,
        name: str,
        scopes: List[str] = None,
        expires_in_days: int = 90,
        rate_limit: Optional[Any] = None
    ) -> Dict[str, str]:
        """
        Generate new API key.

        Args:
            user_id: User ID
            name: Key name/description
            scopes: List of scopes
            expires_in_days: Expiration time
            rate_limit: Rate limit for this key

        Returns:
            Dict with key and key_id
        """
        # Generate secure random key
        key = f"nf_{secrets.token_urlsafe(32)}"
        key_id = hashlib.sha256(key.encode()).hexdigest()[:16]

        # Store key info
        self.keys[key] = {
            "key_id": key_id,
            "user_id": user_id,
            "name": name,
            "scopes": scopes or [],
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=expires_in_days),
            "rate_limit": rate_limit,
            "last_used": None,
            "usage_count": 0
        }

        logger.info(f"Generated API key for user {user_id}: {key_id}")

        return {
            "key": key,
            "key_id": key_id
        }

    async def validate(self, key: str) -> Optional[Dict[str, Any]]:
        """Validate API key."""
        if key not in self.keys:
            return None

        key_info = self.keys[key]

        # Check expiration
        if datetime.utcnow() > key_info["expires_at"]:
            logger.warning(f"API key expired: {key_info['key_id']}")
            return None

        # Update usage
        key_info["last_used"] = datetime.utcnow()
        key_info["usage_count"] += 1

        return key_info

    async def revoke(self, key_id: str):
        """Revoke API key."""
        # Find and remove key
        for key, info in list(self.keys.items()):
            if info["key_id"] == key_id:
                del self.keys[key]
                logger.info(f"Revoked API key: {key_id}")
                return

        logger.warning(f"API key not found: {key_id}")

    async def list(self, user_id: str) -> List[Dict[str, Any]]:
        """List API keys for user."""
        return [
            {
                "key_id": info["key_id"],
                "name": info["name"],
                "scopes": info["scopes"],
                "created_at": info["created_at"],
                "expires_at": info["expires_at"],
                "last_used": info["last_used"],
                "usage_count": info["usage_count"]
            }
            for info in self.keys.values()
            if info["user_id"] == user_id
        ]
