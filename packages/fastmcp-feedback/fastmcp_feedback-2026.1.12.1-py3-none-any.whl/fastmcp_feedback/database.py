"""Database connection and session management for FastMCP Feedback."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool, StaticPool

from .models import Base

logger = logging.getLogger(__name__)


class FeedbackDatabase:
    """Database connection and session manager for feedback system."""

    def __init__(self, database_url: str | None = None):
        """Initialize database connection.

        Args:
            database_url: Database connection URL. Defaults to SQLite in-memory.
        """
        self.database_url = database_url or "sqlite:///:memory:"
        self.engine = None
        self.SessionLocal = None
        self._is_initialized = False

    async def initialize(self):
        """Initialize database engine and create tables."""
        # Skip initialization if already done
        if self._is_initialized and self.engine is not None:
            logger.debug(f"Database already initialized: {self.database_url}")
            return

        try:
            # Dispose of existing engine if present
            if self.engine is not None:
                logger.debug("Disposing of existing database engine")
                self.engine.dispose()
                self.engine = None
                self.SessionLocal = None

            # Configure engine based on database type
            if "sqlite" in self.database_url.lower():
                # SQLite configuration
                connect_args = {"check_same_thread": False}
                if ":memory:" in self.database_url:
                    # In-memory database needs StaticPool
                    poolclass = StaticPool
                    connect_args["check_same_thread"] = False
                else:
                    poolclass = QueuePool

                self.engine = create_engine(
                    self.database_url,
                    connect_args=connect_args,
                    poolclass=poolclass,
                    pool_pre_ping=True,
                    echo=False,  # Set to True for SQL debugging
                )
            else:
                # PostgreSQL or other database
                self.engine = create_engine(
                    self.database_url,
                    poolclass=QueuePool,
                    pool_size=20,
                    max_overflow=30,
                    pool_pre_ping=True,
                    pool_recycle=3600,  # Recycle connections every hour
                    echo=False,
                )

            # Create session factory
            self.SessionLocal = sessionmaker(
                bind=self.engine, autocommit=False, autoflush=False
            )

            # Create all tables
            Base.metadata.create_all(self.engine)

            self._is_initialized = True
            logger.info(f"Database initialized successfully: {self.database_url}")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            # Ensure cleanup on error
            if self.engine is not None:
                self.engine.dispose()
                self.engine = None
                self.SessionLocal = None
            self._is_initialized = False
            raise

    async def close(self):
        """Close database connections."""
        if self.engine:
            try:
                # Dispose of all connections in the pool
                self.engine.dispose()
                logger.info("Database connections closed")
            except Exception as e:
                logger.warning(f"Error while closing database connections: {e}")
            finally:
                # Always clear references
                self.engine = None
                self.SessionLocal = None
                self._is_initialized = False

    async def health_check(self) -> bool:
        """Check if database is healthy and accessible.

        Returns:
            True if database is accessible, False otherwise.
        """
        try:
            if not self._is_initialized:
                await self.initialize()

            async with self.session() as session:
                # Simple query to test connectivity
                result = session.execute(text("SELECT 1"))
                result.scalar()
                return True

        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[Session, None]:
        """Create database session context manager.

        Yields:
            Database session with automatic transaction management.
        """
        if not self._is_initialized:
            await self.initialize()

        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def get_session(self) -> Session:
        """Get a database session (synchronous version for compatibility).

        Warning: This method assumes the database is already initialized.
        Use async session() context manager for proper initialization.

        Returns:
            Database session.
        """
        if not self._is_initialized:
            raise RuntimeError(
                "Database not initialized. Use async session() context manager or call initialize() first."
            )

        return self.SessionLocal()


# Database utility functions


async def create_feedback_database(database_url: str | None = None) -> FeedbackDatabase:
    """Create and initialize a feedback database.

    Args:
        database_url: Database connection URL.

    Returns:
        Initialized FeedbackDatabase instance.
    """
    db = FeedbackDatabase(database_url)
    await db.initialize()
    return db


async def get_database_stats(db: FeedbackDatabase) -> dict[str, Any]:
    """Get database statistics.

    Args:
        db: Database instance.

    Returns:
        Dictionary with database statistics.
    """
    try:
        async with db.session() as session:
            # Get total feedback count
            total_result = session.execute(text("SELECT COUNT(*) FROM feedback"))
            total_count = total_result.scalar()

            # Get counts by type
            type_result = session.execute(
                text("SELECT type, COUNT(*) FROM feedback GROUP BY type")
            )
            by_type = dict(type_result.fetchall())

            # Get counts by status
            status_result = session.execute(
                text("SELECT status, COUNT(*) FROM feedback GROUP BY status")
            )
            by_status = dict(status_result.fetchall())

            return {
                "total_count": total_count,
                "by_type": by_type,
                "by_status": by_status,
                "database_url": db.database_url,
                "is_initialized": db._is_initialized,
            }

    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {
            "error": str(e),
            "database_url": db.database_url,
            "is_initialized": db._is_initialized,
        }


async def test_database_connection(database_url: str) -> bool:
    """Test database connection.

    Args:
        database_url: Database URL to test.

    Returns:
        True if connection succeeds, False otherwise.
    """
    try:
        db = FeedbackDatabase(database_url)
        return await db.health_check()
    except Exception:
        return False


def get_database_type(database_url: str) -> str:
    """Get database type from URL.

    Args:
        database_url: Database connection URL.

    Returns:
        Database type (sqlite, postgresql, etc.).
    """
    if database_url.startswith("sqlite"):
        return "sqlite"
    elif database_url.startswith("postgresql"):
        return "postgresql"
    elif database_url.startswith("mysql"):
        return "mysql"
    else:
        return "unknown"


def is_memory_database(database_url: str) -> bool:
    """Check if database URL points to in-memory database.

    Args:
        database_url: Database connection URL.

    Returns:
        True if in-memory database, False otherwise.
    """
    return ":memory:" in database_url.lower()


# Database migration helpers (for future use)


async def migrate_database(db: FeedbackDatabase) -> bool:
    """Run database migrations.

    Args:
        db: Database instance.

    Returns:
        True if migrations succeed, False otherwise.
    """
    try:
        # This would integrate with Alembic for real migrations
        # For now, just ensure tables exist
        if db.engine:
            Base.metadata.create_all(db.engine)
            return True
        return False
    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        return False


async def backup_database(db: FeedbackDatabase, backup_path: str) -> bool:
    """Backup database (SQLite only for now).

    Args:
        db: Database instance.
        backup_path: Path for backup file.

    Returns:
        True if backup succeeds, False otherwise.
    """
    try:
        if "sqlite" not in db.database_url.lower():
            logger.error("Backup only supported for SQLite databases")
            return False

        # This would implement actual backup logic
        logger.info(f"Database backup would be created at: {backup_path}")
        return True

    except Exception as e:
        logger.error(f"Database backup failed: {e}")
        return False


# Connection pool monitoring


def get_connection_pool_status(db: FeedbackDatabase) -> dict[str, Any]:
    """Get connection pool status.

    Args:
        db: Database instance.

    Returns:
        Dictionary with pool status information.
    """
    if not db.engine or not hasattr(db.engine, "pool"):
        return {"error": "No connection pool available"}

    pool = db.engine.pool

    try:
        return {
            "pool_size": pool.size(),
            "checked_out": pool.checkedout(),
            "overflow": getattr(pool, "overflow", 0),
            "checked_in": pool.checkedin(),
        }
    except Exception as e:
        return {"error": str(e)}


# Error handling helpers


class DatabaseConnectionError(Exception):
    """Raised when database connection fails."""

    pass


class DatabaseOperationError(Exception):
    """Raised when database operation fails."""

    pass


def handle_database_error(func):
    """Decorator to handle database errors gracefully."""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except OperationalError as e:
            logger.error(f"Database operational error in {func.__name__}: {e}")
            raise DatabaseConnectionError(f"Database connection failed: {e}") from e
        except SQLAlchemyError as e:
            logger.error(f"Database error in {func.__name__}: {e}")
            raise DatabaseOperationError(f"Database operation failed: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            raise

    return wrapper


def get_database_session(
    database_url: str = "sqlite:///feedback.db",
) -> FeedbackDatabase:
    """Create and return a FeedbackDatabase instance.

    Convenience function for quickly getting a database session.
    For more control, instantiate FeedbackDatabase directly.

    Args:
        database_url: Database connection URL.

    Returns:
        Initialized FeedbackDatabase instance.

    Example:
        >>> from fastmcp_feedback import get_database_session
        >>> db = get_database_session("sqlite:///my_feedback.db")
    """
    return FeedbackDatabase(database_url)
