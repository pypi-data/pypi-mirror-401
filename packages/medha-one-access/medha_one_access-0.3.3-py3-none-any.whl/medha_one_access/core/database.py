"""
MedhaOne Access Control Database Management (Async)

Async database connection, session management, and configuration utilities.
"""

import os
from contextlib import asynccontextmanager
from typing import Optional, AsyncGenerator, Dict, Any
from urllib.parse import urlparse

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import text

from medha_one_access.core.base import Base
from medha_one_access.core.exceptions import DatabaseConnectionError, ConfigurationError


def convert_to_async_url(sync_url: str) -> str:
    """Convert sync database URL to async URL."""
    if sync_url.startswith('postgresql://'):
        return sync_url.replace('postgresql://', 'postgresql+asyncpg://')
    elif sync_url.startswith('sqlite:///'):
        return sync_url.replace('sqlite:///', 'sqlite+aiosqlite:///')
    elif sync_url.startswith('mysql://'):
        return sync_url.replace('mysql://', 'mysql+aiomysql://')
    return sync_url


class AsyncDatabaseManager:
    """
    Async database connection and session management.

    Handles async database connections, session creation, and schema management.
    Supports PostgreSQL (asyncpg), SQLite (aiosqlite), and MySQL (aiomysql).
    """

    def __init__(self, database_url: str, **kwargs):
        """
        Initialize the async database manager.

        Args:
            database_url: Database connection URL
            **kwargs: Additional SQLAlchemy engine options
        """
        self.sync_database_url = database_url
        self.database_url = convert_to_async_url(database_url)
        self.engine_kwargs = kwargs
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None
        self._setup_engine()

    def _setup_engine(self) -> None:
        """Set up the async SQLAlchemy engine with appropriate configuration."""
        try:
            # Parse database URL to determine database type
            parsed = urlparse(self.database_url)
            db_type = parsed.scheme.split("+")[
                0
            ]  # Handle schemes like 'postgresql+asyncpg'

            # Default engine arguments
            engine_kwargs = {
                "pool_pre_ping": True,  # Enable connection health checks
                **self.engine_kwargs,
            }

            # Database-specific configurations
            if db_type == "postgresql":
                # PostgreSQL specific settings
                engine_kwargs.setdefault("connect_args", {}).update(
                    {"server_settings": {"jit": "off"}}  # Disable JIT for better performance
                )
                if "azure" in self.database_url.lower():
                    # Azure PostgreSQL requires SSL
                    engine_kwargs["connect_args"]["ssl"] = "require"

            elif db_type == "sqlite":
                # SQLite specific settings
                engine_kwargs.update(
                    {
                        "poolclass": StaticPool,
                        "connect_args": {
                            "check_same_thread": False,  # Allow multi-threading
                            **engine_kwargs.get("connect_args", {}),
                        },
                    }
                )

            # Create async engine
            self._engine = create_async_engine(self.database_url, **engine_kwargs)

            # Create async session factory
            self._session_factory = async_sessionmaker(
                bind=self._engine, 
                class_=AsyncSession,
                autocommit=False, 
                autoflush=False,
                expire_on_commit=False  # Important for async usage
            )

        except Exception as e:
            raise DatabaseConnectionError(
                self.database_url, f"Failed to setup async database engine: {str(e)}"
            )

    async def _test_connection(self) -> None:
        """Test async database connection."""
        try:
            async with self._engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as e:
            raise DatabaseConnectionError(
                self.database_url, f"Async database connection test failed: {str(e)}"
            )

    @property
    def engine(self) -> AsyncEngine:
        """Get the async SQLAlchemy engine."""
        if self._engine is None:
            raise DatabaseConnectionError(
                self.database_url, "Async database engine not initialized"
            )
        return self._engine

    def get_session(self) -> AsyncSession:
        """
        Create a new async database session.

        Returns:
            New async database session

        Note:
            Remember to close the session when done or use session_scope() context manager.
        """
        if self._session_factory is None:
            raise DatabaseConnectionError(
                self.database_url, "Async session factory not initialized"
            )
        return self._session_factory()

    @asynccontextmanager
    async def session_scope(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Provide a transactional scope around async database operations.

        Yields:
            Async database session

        Example:
            async with db_manager.session_scope() as session:
                user = await session.get(User, user_id)
                session.add(new_user)
                # Automatically commits on success, rolls back on exception
        """
        session = self.get_session()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def initialize(self) -> None:
        """Initialize the database manager and test connection."""
        await self._test_connection()

    async def create_all(self) -> None:
        """
        Create all database tables.

        This will create all tables defined in the models if they don't exist.
        """
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            raise DatabaseConnectionError(
                self.database_url, f"Failed to create database tables: {str(e)}"
            )

    async def drop_all(self) -> None:
        """
        Drop all database tables.

        WARNING: This will delete all data in the database!
        """
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
        except Exception as e:
            raise DatabaseConnectionError(
                self.database_url, f"Failed to drop database tables: {str(e)}"
            )

    async def get_table_names(self) -> list[str]:
        """
        Get list of existing table names.

        Returns:
            List of table names in the database
        """
        try:
            async with self.engine.begin() as conn:
                result = await conn.run_sync(lambda sync_conn: self.engine.dialect.get_table_names(sync_conn))
                return result
        except Exception as e:
            raise DatabaseConnectionError(
                self.database_url, f"Failed to get table names: {str(e)}"
            )

    async def check_tables_exist(self) -> bool:
        """
        Check if all required tables exist.

        Returns:
            True if all tables exist, False otherwise
        """
        try:
            required_tables = {"users", "artifacts", "access_rules", "access_summaries"}
            existing_tables = set(await self.get_table_names())
            return required_tables.issubset(existing_tables)
        except Exception:
            return False

    async def get_database_info(self) -> Dict[str, Any]:
        """
        Get database information and statistics.

        Returns:
            Dictionary with database information
        """
        try:
            info = {
                "database_url": self._mask_password(self.database_url),
                "sync_database_url": self._mask_password(self.sync_database_url),
                "engine": str(self.engine),
                "tables_exist": await self.check_tables_exist(),
            }

            # Get table counts if tables exist
            if info["tables_exist"]:
                async with self.session_scope() as session:
                    from medha_one_access.core.models import (
                        User,
                        Artifact,
                        AccessRule,
                        AccessSummary,
                    )
                    from sqlalchemy import select, func

                    # Count all tables concurrently
                    user_count_result = await session.execute(select(func.count()).select_from(User))
                    artifact_count_result = await session.execute(select(func.count()).select_from(Artifact))
                    rule_count_result = await session.execute(select(func.count()).select_from(AccessRule))
                    summary_count_result = await session.execute(select(func.count()).select_from(AccessSummary))

                    info["table_counts"] = {
                        "users": user_count_result.scalar(),
                        "artifacts": artifact_count_result.scalar(),
                        "access_rules": rule_count_result.scalar(),
                        "access_summaries": summary_count_result.scalar(),
                    }

            return info

        except Exception as e:
            return {
                "database_url": self._mask_password(self.database_url),
                "sync_database_url": self._mask_password(self.sync_database_url),
                "error": str(e),
            }

    def _mask_password(self, url: str) -> str:
        """Mask password in database URL for logging."""
        try:
            parsed = urlparse(url)
            if parsed.password:
                masked_netloc = parsed.netloc.replace(parsed.password, "***")
                return url.replace(parsed.netloc, masked_netloc)
            return url
        except Exception:
            return url

    async def close(self) -> None:
        """Close database connections and cleanup resources."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
        self._session_factory = None


class DatabaseConfig:
    """
    Database configuration management.

    Handles environment variables, configuration validation, and URL building.
    """

    @staticmethod
    def from_env() -> str:
        """
        Create database URL from environment variables.

        Environment variables:
            DATABASE_URL: Full database URL (takes precedence)
            DB_HOST: Database host
            DB_PORT: Database port
            DB_NAME: Database name
            DB_USER: Database username
            DB_PASSWORD: Database password
            DB_DRIVER: Database driver (postgresql, sqlite, etc.)

        Returns:
            Database connection URL

        Raises:
            ConfigurationError: If required configuration is missing
        """
        # Check for full URL first
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return database_url

        # Build URL from components
        driver = os.getenv("DB_DRIVER", "postgresql")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        name = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        if driver == "sqlite":
            # SQLite URL
            db_path = name or "medha_access.db"
            return f"sqlite:///{db_path}"

        # PostgreSQL or other databases
        if not all([host, name, user]):
            raise ConfigurationError(
                "database",
                "Missing required database configuration. Set DATABASE_URL or DB_HOST, DB_NAME, DB_USER",
            )

        # Build URL
        url_parts = [f"{driver}://"]

        if user:
            url_parts.append(user)
            if password:
                url_parts.append(f":{password}")
            url_parts.append("@")

        url_parts.append(host)

        if port:
            url_parts.append(f":{port}")

        url_parts.append(f"/{name}")

        return "".join(url_parts)

    @staticmethod
    def validate_url(database_url: str) -> None:
        """
        Validate database URL format.

        Args:
            database_url: Database URL to validate

        Raises:
            ConfigurationError: If URL format is invalid
        """
        try:
            parsed = urlparse(database_url)

            if not parsed.scheme:
                raise ConfigurationError(
                    "database_url", "Missing database driver/scheme"
                )

            # Check for async-compatible schemes
            async_schemes = ["postgresql+asyncpg", "sqlite+aiosqlite", "mysql+aiomysql"]
            if parsed.scheme not in async_schemes and not any(parsed.scheme.startswith(scheme.split('+')[0]) for scheme in async_schemes):
                # Allow but warn about unknown schemes
                pass

            if not parsed.scheme.startswith("sqlite") and not parsed.netloc:
                raise ConfigurationError("database_url", "Missing database host/netloc")

        except Exception as e:
            raise ConfigurationError("database_url", f"Invalid URL format: {str(e)}")


# Convenience function for creating async database manager from environment
async def create_async_database_manager(**kwargs) -> AsyncDatabaseManager:
    """
    Create async database manager from environment variables.

    Args:
        **kwargs: Additional engine options

    Returns:
        Configured AsyncDatabaseManager instance
    """
    database_url = DatabaseConfig.from_env()
    DatabaseConfig.validate_url(database_url)
    manager = AsyncDatabaseManager(database_url, **kwargs)
    await manager.initialize()
    return manager


# Export classes and functions
__all__ = [
    "AsyncDatabaseManager",
    "DatabaseConfig",
    "create_async_database_manager",
    "convert_to_async_url",
]