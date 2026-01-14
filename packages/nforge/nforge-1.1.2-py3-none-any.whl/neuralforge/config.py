"""
Configuration management for NeuralForge.
"""

from typing import List, Optional, Any
from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    Settings can be loaded from:
    1. Environment variables
    2. .env file
    3. Direct instantiation
    
    Example:
        >>> settings = Settings(app_name="my-api", debug=True)
        >>> # Or from environment:
        >>> # export APP_NAME="my-api"
        >>> settings = Settings()
    """

    # ========================================================================
    # Application Settings
    # ========================================================================

    app_name: str = Field(
        default="neuralforge-app",
        description="Application name"
    )

    environment: str = Field(
        default="development",
        description="Environment: development, staging, production"
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )

    version: str = Field(
        default="1.0.0",
        description="Application version"
    )

    # ========================================================================
    # Server Settings
    # ========================================================================

    host: str = Field(
        default="0.0.0.0",
        description="Server host"
    )

    port: int = Field(
        default=8000,
        description="Server port"
    )

    workers: int = Field(
        default=4,
        description="Number of worker processes"
    )

    reload: bool = Field(
        default=False,
        description="Enable auto-reload (development only)"
    )

    # ========================================================================
    # Security Settings
    # ========================================================================

    secret_key: str = Field(
        default="change-this-in-production",
        description="Secret key for signing tokens"
    )

    allowed_origins: List[str] = Field(
        default_factory=lambda: ["*"],
        description="CORS allowed origins"
    )

    allowed_methods: List[str] = Field(
        default_factory=lambda: ["*"],
        description="CORS allowed methods"
    )

    allowed_headers: List[str] = Field(
        default_factory=lambda: ["*"],
        description="CORS allowed headers"
    )

    # ========================================================================
    # Database Settings
    # ========================================================================

    database_url: str = Field(
        default="sqlite+aiosqlite:///./neuralforge.db",
        description="Database connection URL"
    )

    db_pool_size: int = Field(
        default=20,
        description="Database connection pool size"
    )

    db_max_overflow: int = Field(
        default=10,
        description="Database connection pool overflow"
    )

    db_echo: bool = Field(
        default=False,
        description="Echo SQL statements (debug)"
    )

    # ========================================================================
    # Redis/Cache Settings
    # ========================================================================

    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL"
    )

    cache_ttl: int = Field(
        default=300,
        description="Default cache TTL in seconds"
    )

    cache_max_size_mb: int = Field(
        default=1024,
        description="Maximum cache size in MB"
    )

    # ========================================================================
    # Model Settings
    # ========================================================================

    model_storage_path: str = Field(
        default="/models",
        description="Path to model storage directory"
    )

    model_cache_size_gb: float = Field(
        default=10.0,
        description="Maximum size for model cache in GB"
    )

    model_load_timeout: float = Field(
        default=300.0,
        description="Model loading timeout in seconds"
    )

    # ========================================================================
    # GPU/Resource Settings
    # ========================================================================

    gpu_devices: List[int] = Field(
        default_factory=list,
        description="GPU device IDs to use (empty = use all available)"
    )

    gpu_memory_fraction: float = Field(
        default=0.9,
        description="Fraction of GPU memory to use (0.0-1.0)"
    )

    max_concurrent_requests: int = Field(
        default=100,
        description="Maximum concurrent requests"
    )

    request_timeout: float = Field(
        default=30.0,
        description="Request timeout in seconds"
    )

    max_request_size_mb: int = Field(
        default=100,
        description="Maximum request size in MB"
    )

    # ========================================================================
    # Observability Settings
    # ========================================================================

    log_level: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )

    log_format: str = Field(
        default="json",
        description="Log format: json or text"
    )

    metrics_enabled: bool = Field(
        default=True,
        description="Enable metrics collection"
    )

    metrics_port: int = Field(
        default=9090,
        description="Port for metrics endpoint"
    )

    tracing_enabled: bool = Field(
        default=False,
        description="Enable distributed tracing"
    )

    tracing_sample_rate: float = Field(
        default=0.1,
        description="Tracing sample rate (0.0-1.0)"
    )

    jaeger_endpoint: Optional[str] = Field(
        default=None,
        description="Jaeger collector endpoint"
    )

    # ========================================================================
    # Feature Flags
    # ========================================================================

    enable_docs: bool = Field(
        default=True,
        description="Enable API documentation"
    )

    enable_cors: bool = Field(
        default=True,
        description="Enable CORS middleware"
    )

    enable_compression: bool = Field(
        default=True,
        description="Enable response compression"
    )

    enable_rate_limiting: bool = Field(
        default=True,
        description="Enable rate limiting"
    )

    # ========================================================================
    # External Services
    # ========================================================================

    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key"
    )

    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key"
    )

    pinecone_api_key: Optional[str] = Field(
        default=None,
        description="Pinecone API key"
    )

    datadog_api_key: Optional[str] = Field(
        default=None,
        description="DataDog API key"
    )

    slack_webhook_url: Optional[str] = Field(
        default=None,
        description="Slack webhook URL for alerts"
    )

    # ========================================================================
    # Pydantic Config
    # ========================================================================

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow"  # Allow extra fields for extensibility
    }

    # ========================================================================
    # Helper Methods
    # ========================================================================

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"

    @property
    def is_testing(self) -> bool:
        """Check if running in test environment."""
        return self.environment.lower() in ["test", "testing"]

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        return getattr(self, key, default)

    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        setattr(self, key, value)

    def to_dict(self) -> dict:
        """Convert settings to dictionary."""
        return self.model_dump()

    def __repr__(self) -> str:
        """Return string representation of Settings."""
        return f"<Settings(app_name='{self.app_name}', environment='{self.environment}')>"


# ============================================================================
# Environment-Specific Settings
# ============================================================================

class DevelopmentSettings(Settings):
    """Settings optimized for development."""

    environment: str = "development"
    debug: bool = True
    reload: bool = True
    db_echo: bool = True
    log_level: str = "DEBUG"
    workers: int = 1

    model_config = {
        "env_file": ".env.development",
        "env_file_encoding": "utf-8"
    }


class ProductionSettings(Settings):
    """Settings optimized for production."""

    environment: str = "production"
    debug: bool = False
    reload: bool = False
    db_echo: bool = False
    log_level: str = "INFO"
    workers: int = 4

    # Security
    allowed_origins: List[str] = Field(
        default_factory=list,  # Must be explicitly set in production
        description="CORS allowed origins"
    )

    model_config = {
        "env_file": ".env.production",
        "env_file_encoding": "utf-8"
    }

    def __init__(self, **kwargs):
        """Initialize ProductionSettings with validation.
        
        Args:
            **kwargs: Configuration overrides
            
        Raises:
            ValueError: If required production settings are not configured
        """
        super().__init__(**kwargs)

        # Validate production requirements
        if self.secret_key == "change-this-in-production":
            raise ValueError("SECRET_KEY must be set in production")

        # Check for both wildcard and empty origins
        if not self.allowed_origins or self.allowed_origins == ["*"]:
            raise ValueError("CORS origins must be explicitly set in production")


class TestSettings(Settings):
    """Settings optimized for testing."""

    environment: str = "test"
    debug: bool = True

    # Use in-memory databases for testing
    database_url: str = "sqlite:///:memory:"
    redis_url: str = "redis://localhost:6379/1"  # Use different Redis DB

    # Disable external services
    metrics_enabled: bool = False
    tracing_enabled: bool = False

    model_config = {
        "env_file": ".env.test",
        "env_file_encoding": "utf-8"
    }


# ============================================================================
# Settings Factory
# ============================================================================

def get_settings(environment: Optional[str] = None) -> Settings:
    """
    Get settings for the specified environment.
    
    Args:
        environment: Environment name (development, production, test)
                    If None, uses ENVIRONMENT env var or defaults to development
    
    Returns:
        Settings object for the environment
    
    Example:
        >>> settings = get_settings("production")
        >>> settings = get_settings()  # Uses ENVIRONMENT env var
    """
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")

    environment = environment.lower()

    settings_map = {
        "development": DevelopmentSettings,
        "dev": DevelopmentSettings,
        "production": ProductionSettings,
        "prod": ProductionSettings,
        "test": TestSettings,
        "testing": TestSettings,
    }

    settings_class = settings_map.get(environment, Settings)
    return settings_class()
