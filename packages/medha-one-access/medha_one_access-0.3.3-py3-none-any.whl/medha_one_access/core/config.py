"""
MedhaOne Access Control Library Configuration

Configuration management for the access control library.
Supports both programmatic configuration and environment variables.
"""

from typing import Optional, Dict, Any
from pydantic import Field
from .compatibility import BaseSettings
from pydantic import PostgresDsn
import os


class AccessControlConfig(BaseSettings):
    """Configuration class for MedhaOne Access Control Library."""

    # Database configuration
    database_url: PostgresDsn = Field(..., description="PostgreSQL database URL")

    # Security configuration
    secret_key: str = Field(
        ..., description="Secret key for token encryption/decryption"
    )

    # API configuration (for FastAPI integration)
    api_prefix: str = Field("/oneAccess", description="API route prefix")

    # Application settings
    project_name: str = Field("MedhaOne Access Control", description="Project name")
    debug: bool = Field(False, description="Debug mode")

    class Config:
        env_file = ".env"
        case_sensitive = False
        env_prefix = "MEDHA_"


class LibraryConfig:
    """Simple configuration class for library usage."""

    def __init__(
        self,
        database_url: str,
        secret_key: str,
        api_prefix: str = "/oneAccess",
        application_name: Optional[str] = None,
        debug: bool = False,
        # Performance optimization settings
        enable_caching: bool = True,
        cache_ttl: int = 300,
        enable_bulk_queries: bool = True,
        enable_audit_trail: bool = False,  # Disabled by default for performance
        max_pool_size: int = 20,
        pool_recycle_time: int = 3600,
        # Auto-recalculation settings
        enable_auto_recalculation: bool = True,  # Enable automatic recalculation on data changes
        auto_recalc_mode: str = "immediate",  # "immediate", "batched", or "disabled"
        auto_recalc_batch_size: int = 50,  # Max users to recalculate in one batch
        auto_recalc_batch_delay: int = 5,  # Seconds to wait before processing batch
        **kwargs,
    ):
        self.database_url = database_url
        self.secret_key = secret_key
        self.api_prefix = api_prefix
        self.application_name = application_name
        self.debug = debug
        
        # Performance settings
        self.enable_caching = enable_caching
        self.cache_ttl = cache_ttl
        self.enable_bulk_queries = enable_bulk_queries
        self.enable_audit_trail = enable_audit_trail
        self.max_pool_size = max_pool_size
        self.pool_recycle_time = pool_recycle_time
        
        # Auto-recalculation settings
        self.enable_auto_recalculation = enable_auto_recalculation
        self.auto_recalc_mode = auto_recalc_mode
        self.auto_recalc_batch_size = auto_recalc_batch_size
        self.auto_recalc_batch_delay = auto_recalc_batch_delay
        
        self.extra_config = kwargs

    @classmethod
    def from_env(cls, env_prefix: str = "MEDHA_") -> "LibraryConfig":
        """Create configuration from environment variables."""
        database_url = os.getenv(f"{env_prefix}DATABASE_URL")
        secret_key = os.getenv(f"{env_prefix}SECRET_KEY")

        if not database_url:
            raise ValueError(
                f"Environment variable {env_prefix}DATABASE_URL is required"
            )
        if not secret_key:
            raise ValueError(f"Environment variable {env_prefix}SECRET_KEY is required")

        return cls(
            database_url=database_url,
            secret_key=secret_key,
            api_prefix=os.getenv(f"{env_prefix}API_PREFIX", "/oneAccess"),
            application_name=os.getenv(f"{env_prefix}APPLICATION_NAME"),
            debug=os.getenv(f"{env_prefix}DEBUG", "false").lower() == "true",
            # Performance settings from environment
            enable_caching=os.getenv(f"{env_prefix}ENABLE_CACHING", "true").lower() == "true",
            cache_ttl=int(os.getenv(f"{env_prefix}CACHE_TTL", "300")),
            enable_bulk_queries=os.getenv(f"{env_prefix}ENABLE_BULK_QUERIES", "true").lower() == "true",
            enable_audit_trail=os.getenv(f"{env_prefix}ENABLE_AUDIT_TRAIL", "false").lower() == "true",
            max_pool_size=int(os.getenv(f"{env_prefix}MAX_POOL_SIZE", "20")),
            pool_recycle_time=int(os.getenv(f"{env_prefix}POOL_RECYCLE_TIME", "3600")),
            # Auto-recalculation settings from environment
            enable_auto_recalculation=os.getenv(f"{env_prefix}ENABLE_AUTO_RECALC", "true").lower() == "true",
            auto_recalc_mode=os.getenv(f"{env_prefix}AUTO_RECALC_MODE", "immediate"),
            auto_recalc_batch_size=int(os.getenv(f"{env_prefix}AUTO_RECALC_BATCH_SIZE", "50")),
            auto_recalc_batch_delay=int(os.getenv(f"{env_prefix}AUTO_RECALC_BATCH_DELAY", "5")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "database_url": self.database_url,
            "secret_key": self.secret_key,
            "api_prefix": self.api_prefix,
            "application_name": self.application_name,
            "debug": self.debug,
            "enable_caching": self.enable_caching,
            "cache_ttl": self.cache_ttl,
            "enable_bulk_queries": self.enable_bulk_queries,
            "enable_audit_trail": self.enable_audit_trail,
            "max_pool_size": self.max_pool_size,
            "pool_recycle_time": self.pool_recycle_time,
            "enable_auto_recalculation": self.enable_auto_recalculation,
            "auto_recalc_mode": self.auto_recalc_mode,
            "auto_recalc_batch_size": self.auto_recalc_batch_size,
            "auto_recalc_batch_delay": self.auto_recalc_batch_delay,
            **self.extra_config,
        }
