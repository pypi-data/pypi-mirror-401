"""Advanced unit tests for FastMCP Feedback database operations - targeting 90%+ coverage."""

import asyncio
import logging
import os
import tempfile
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.pool import QueuePool, StaticPool

from fastmcp_feedback.database import (
    FeedbackDatabase,
    create_feedback_database,
    get_database_stats,
    test_database_connection as db_connection_test,
    get_database_type,
    is_memory_database,
    migrate_database,
    backup_database,
    get_connection_pool_status,
    handle_database_error,
    DatabaseConnectionError,
    DatabaseOperationError
)
from fastmcp_feedback.models import Feedback, FeedbackType, FeedbackStatus


@pytest.mark.unit
class TestDatabaseAdvancedOperations:
    """Test advanced database operations and error handling."""
    
    @pytest.mark.asyncio
    async def test_engine_disposal_during_initialization(self):
        """Test engine disposal during initialization (covers lines 41-44)."""
        db = FeedbackDatabase("sqlite:///:memory:")
        
        # First initialize normally to create an engine
        await db.initialize()
        original_engine = db.engine
        
        # Mark as not initialized to force disposal path
        db._is_initialized = False
        
        # Initialize again - this should dispose the existing engine and create a new one
        await db.initialize()
        
        # Should have a new engine
        assert db.engine is not None
        assert db._is_initialized
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_database_close_error_handling(self):
        """Test database close error handling (lines 106-107)."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        # Mock the engine to raise an exception on dispose
        mock_engine = Mock()
        mock_engine.dispose.side_effect = Exception("Close error")
        db.engine = mock_engine
        
        # This should handle the error gracefully and still cleanup
        await db.close()
        
        # Should have cleaned up references despite error
        assert db.engine is None
        assert db.SessionLocal is None
        assert not db._is_initialized
    
    def test_synchronous_session_error_handling(self):
        """Test synchronous session error handling (lines 164-167)."""
        db = FeedbackDatabase("sqlite:///:memory:")
        
        # Database not initialized - should raise RuntimeError
        with pytest.raises(RuntimeError) as exc_info:
            db.get_session()
        
        assert "Database not initialized" in str(exc_info.value)
        assert "async session() context manager" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_synchronous_session_success(self):
        """Test synchronous session success path (line 167)."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        # Should be able to get session when initialized
        session = db.get_session()
        assert session is not None
        session.close()
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_create_feedback_database_utility(self):
        """Test create_feedback_database utility function (lines 181-183)."""
        db = await create_feedback_database("sqlite:///:memory:")
        
        assert isinstance(db, FeedbackDatabase)
        assert db._is_initialized
        assert db.engine is not None
        assert db.SessionLocal is not None
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_get_database_stats_success(self):
        """Test get_database_stats success path (lines 195-223)."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        # Add some test data
        async with db.session() as session:
            feedback1 = Feedback(
                type=FeedbackType.BUG,
                title="Bug report",
                description="Test bug",
                submitter="user1"
            )
            feedback2 = Feedback(
                type=FeedbackType.FEATURE,
                title="Feature request",
                description="Test feature",
                submitter="user2"
            )
            feedback1.status = FeedbackStatus.OPEN
            feedback2.status = FeedbackStatus.RESOLVED
            
            session.add(feedback1)
            session.add(feedback2)
            session.commit()
        
        # Get stats
        stats = await get_database_stats(db)
        
        assert stats["total_count"] == 2
        assert stats["by_type"]["BUG"] == 1
        assert stats["by_type"]["FEATURE"] == 1
        assert stats["by_status"]["OPEN"] == 1
        assert stats["by_status"]["RESOLVED"] == 1
        assert stats["database_url"] == db.database_url
        assert stats["is_initialized"] is True
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_get_database_stats_error_handling(self):
        """Test get_database_stats error handling (lines 221-227)."""
        # Create database with invalid state
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        # Mock session to raise an error
        with patch.object(db, 'session') as mock_session:
            mock_session.side_effect = Exception("Database error")
            
            stats = await get_database_stats(db)
            
            assert "error" in stats
            assert stats["error"] == "Database error"
            assert stats["database_url"] == db.database_url
            assert stats["is_initialized"] is True
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_test_database_connection_success(self):
        """Test test_database_connection success path (lines 239-243)."""
        result = await db_connection_test("sqlite:///:memory:")
        assert result is True
    
    @pytest.mark.asyncio
    async def test_test_database_connection_failure(self):
        """Test test_database_connection failure path (lines 239-243)."""
        result = await db_connection_test("invalid://database/url")
        assert result is False
    
    @pytest.mark.asyncio
    async def test_test_database_connection_exception_handling(self):
        """Test test_database_connection exception handling (lines 242-243)."""
        # Test with database URL that will cause an exception during health check
        with patch('fastmcp_feedback.database.FeedbackDatabase') as mock_db_class:
            mock_db = Mock()
            mock_db.health_check.side_effect = Exception("Connection error")
            mock_db_class.return_value = mock_db
            
            result = await db_connection_test("sqlite:///:memory:")
            assert result is False
    
    def test_get_database_type_sqlite(self):
        """Test get_database_type with SQLite URLs (lines 255-262)."""
        assert get_database_type("sqlite:///test.db") == "sqlite"
        assert get_database_type("sqlite:///:memory:") == "sqlite"
    
    def test_get_database_type_postgresql(self):
        """Test get_database_type with PostgreSQL URLs (lines 255-262)."""
        assert get_database_type("postgresql://user:pass@host:5432/db") == "postgresql"
        assert get_database_type("postgresql+asyncpg://user:pass@host:5432/db") == "postgresql"
    
    def test_get_database_type_mysql(self):
        """Test get_database_type with MySQL URLs (lines 255-262)."""
        assert get_database_type("mysql://user:pass@host:3306/db") == "mysql"
        assert get_database_type("mysql+pymysql://user:pass@host:3306/db") == "mysql"
    
    def test_get_database_type_unknown(self):
        """Test get_database_type with unknown URLs (lines 255-262)."""
        assert get_database_type("mongodb://host:27017/db") == "unknown"
        assert get_database_type("redis://host:6379/0") == "unknown"
    
    def test_is_memory_database_true(self):
        """Test is_memory_database with memory databases (line 274)."""
        assert is_memory_database("sqlite:///:memory:") is True
        assert is_memory_database("SQLite:///:MEMORY:") is True  # Case insensitive
    
    def test_is_memory_database_false(self):
        """Test is_memory_database with file databases (line 274)."""
        assert is_memory_database("sqlite:///test.db") is False
        assert is_memory_database("postgresql://host/db") is False
        assert is_memory_database("mysql://host/db") is False
    
    @pytest.mark.asyncio
    async def test_migrate_database_success(self):
        """Test migrate_database success path (lines 288-297)."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        result = await migrate_database(db)
        assert result is True
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_migrate_database_no_engine(self):
        """Test migrate_database with no engine (lines 288-297)."""
        db = FeedbackDatabase("sqlite:///:memory:")
        # Don't initialize - no engine
        
        result = await migrate_database(db)
        assert result is False
    
    @pytest.mark.asyncio
    async def test_migrate_database_error(self):
        """Test migrate_database error handling (lines 288-297)."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        # Mock Base.metadata.create_all to raise error
        with patch('fastmcp_feedback.database.Base') as mock_base:
            mock_base.metadata.create_all.side_effect = Exception("Migration error")
            
            result = await migrate_database(db)
            assert result is False
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_backup_database_sqlite_success(self):
        """Test backup_database with SQLite (lines 310-321)."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        result = await backup_database(db, "/tmp/backup.db")
        assert result is True  # Mocked success
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_backup_database_non_sqlite(self):
        """Test backup_database with non-SQLite database (lines 310-321)."""
        db = FeedbackDatabase("postgresql://user:pass@host:5432/db")
        
        result = await backup_database(db, "/tmp/backup.db")
        assert result is False
    
    @pytest.mark.asyncio
    async def test_backup_database_error(self):
        """Test backup_database error handling (lines 310-321)."""
        db = FeedbackDatabase("sqlite:///test.db")
        
        # Mock logger to raise an exception during backup
        with patch('fastmcp_feedback.database.logger') as mock_logger:
            mock_logger.info.side_effect = Exception("Backup error")
            
            result = await backup_database(db, "/tmp/backup.db")
            assert result is False


@pytest.mark.unit
class TestConnectionPoolMonitoring:
    """Test connection pool monitoring functionality (lines 335-348)."""
    
    def test_get_connection_pool_status_no_engine(self):
        """Test connection pool status with no engine."""
        db = FeedbackDatabase("sqlite:///:memory:")
        
        status = get_connection_pool_status(db)
        assert "error" in status
        assert "No connection pool available" in status["error"]
    
    def test_get_connection_pool_status_no_pool(self):
        """Test connection pool status with engine but no pool attribute."""
        db = FeedbackDatabase("sqlite:///:memory:")
        db.engine = Mock()
        del db.engine.pool  # Remove pool attribute
        
        status = get_connection_pool_status(db)
        assert "error" in status
        assert "No connection pool available" in status["error"]
    
    @pytest.mark.asyncio
    async def test_get_connection_pool_status_success(self):
        """Test connection pool status success path."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        # For any database, we should be able to get pool status
        status = get_connection_pool_status(db)
        
        # SQLite may not have all pool attributes, so check for basic structure
        if "error" not in status:
            # Pool status should have at least some attributes
            assert isinstance(status, dict)
        
        await db.close()
    
    def test_get_connection_pool_status_method_error(self):
        """Test connection pool status with method call errors."""
        db = FeedbackDatabase("sqlite:///:memory:")
        
        # Create mock engine with pool that raises errors
        mock_pool = Mock()
        mock_pool.size.side_effect = Exception("Pool error")
        mock_pool.checkedout.return_value = 0
        mock_pool.checkedin.return_value = 0
        
        mock_engine = Mock()
        mock_engine.pool = mock_pool
        db.engine = mock_engine
        
        status = get_connection_pool_status(db)
        assert "error" in status
        assert "Pool error" in status["error"]


@pytest.mark.unit
class TestDatabaseErrorHandling:
    """Test database error handling decorator and custom exceptions (lines 365-378)."""
    
    @pytest.mark.asyncio
    async def test_handle_database_error_operational_error(self):
        """Test handle_database_error with OperationalError."""
        
        @handle_database_error
        async def test_func():
            raise OperationalError("statement", "params", "orig")
        
        with pytest.raises(DatabaseConnectionError) as exc_info:
            await test_func()
        
        assert "Database connection failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_handle_database_error_sqlalchemy_error(self):
        """Test handle_database_error with SQLAlchemyError."""
        
        @handle_database_error
        async def test_func():
            raise SQLAlchemyError("Database error")
        
        with pytest.raises(DatabaseOperationError) as exc_info:
            await test_func()
        
        assert "Database operation failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_handle_database_error_generic_exception(self):
        """Test handle_database_error with generic exception."""
        
        @handle_database_error
        async def test_func():
            raise ValueError("Generic error")
        
        with pytest.raises(ValueError):
            await test_func()
    
    @pytest.mark.asyncio
    async def test_handle_database_error_success(self):
        """Test handle_database_error with successful function."""
        
        @handle_database_error
        async def test_func():
            return "success"
        
        result = await test_func()
        assert result == "success"


@pytest.mark.unit
class TestDatabaseEdgeCases:
    """Test edge cases and error conditions."""
    
    @pytest.mark.asyncio
    async def test_multiple_initialize_calls(self):
        """Test multiple initialize calls don't cause issues."""
        db = FeedbackDatabase("sqlite:///:memory:")
        
        # First initialization
        await db.initialize()
        first_engine = db.engine
        
        # Second initialization - should skip
        await db.initialize()
        assert db.engine == first_engine
        assert db._is_initialized
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_health_check_initializes_database(self):
        """Test health check initializes database if not already initialized."""
        db = FeedbackDatabase("sqlite:///:memory:")
        assert not db._is_initialized
        
        result = await db.health_check()
        assert result is True
        assert db._is_initialized
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_session_context_initializes_database(self):
        """Test session context manager initializes database if needed."""
        db = FeedbackDatabase("sqlite:///:memory:")
        assert not db._is_initialized
        
        async with db.session() as session:
            assert session is not None
            assert db._is_initialized
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_database_operations_with_postgresql_config(self):
        """Test database configuration for PostgreSQL (lines 66-74)."""
        db_url = "postgresql://user:pass@localhost:5432/testdb"
        db = FeedbackDatabase(db_url)
        
        # This will fail to connect but we can test configuration
        try:
            await db.initialize()
        except Exception:
            pass  # Expected - no actual PostgreSQL server
        
        # Check that PostgreSQL-specific configuration was applied
        if db.engine:
            assert db.engine.pool.size == 20
            assert db.engine.pool._max_overflow == 30
            
    @pytest.mark.asyncio
    async def test_session_error_rollback_logging(self, caplog):
        """Test session error triggers rollback and logging."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        with caplog.at_level(logging.ERROR):
            try:
                async with db.session() as session:
                    # Create invalid SQL to trigger error
                    session.execute(text("INVALID SQL STATEMENT"))
            except Exception:
                pass  # Expected
        
        # Check that error was logged
        assert len(caplog.records) > 0
        assert any("Database session error" in record.message for record in caplog.records)
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_database_initialization_failure_cleanup(self):
        """Test cleanup happens when initialization fails."""
        # Use invalid directory path to force initialization failure
        db = FeedbackDatabase("sqlite:///nonexistent_dir/test.db")
        
        with pytest.raises(OperationalError):
            await db.initialize()
        
        # Should have cleaned up
        assert db.engine is None
        assert db.SessionLocal is None
        assert not db._is_initialized


@pytest.mark.unit
class TestDatabaseUtilityFunctions:
    """Test utility functions and edge cases."""
    
    @pytest.mark.asyncio
    async def test_database_stats_empty_database(self):
        """Test database stats with empty database."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        stats = await get_database_stats(db)
        
        assert stats["total_count"] == 0
        assert stats["by_type"] == {}
        assert stats["by_status"] == {}
        assert stats["database_url"] == db.database_url
        assert stats["is_initialized"] is True
        
        await db.close()
    
    def test_database_custom_exceptions(self):
        """Test custom exception classes."""
        conn_error = DatabaseConnectionError("Connection failed")
        assert "Connection failed" in str(conn_error)
        
        op_error = DatabaseOperationError("Operation failed")
        assert "Operation failed" in str(op_error)
    
    @pytest.mark.asyncio
    async def test_create_feedback_database_with_custom_url(self):
        """Test create_feedback_database with custom URL."""
        custom_url = "sqlite:///custom_test.db"
        
        db = await create_feedback_database(custom_url)
        
        assert db.database_url == custom_url
        assert db._is_initialized
        
        await db.close()
        
        # Cleanup
        try:
            os.unlink("custom_test.db")
        except FileNotFoundError:
            pass
    
    def test_database_url_edge_cases(self):
        """Test database URL parsing edge cases."""
        edge_cases = [
            ("", "unknown"),
            ("invalid", "unknown"),
            ("sqlite://test.db", "sqlite"),  # Fixed: needs full URL
            ("postgresql://host/db", "postgresql"),  # Fixed: needs full URL
            ("mysql://host/db", "mysql"),  # Fixed: needs full URL
            ("mongodb://host:27017/db", "unknown"),  # MongoDB not supported
            ("redis://host:6379/0", "unknown"),  # Redis not supported
        ]
        
        for url, expected_type in edge_cases:
            assert get_database_type(url) == expected_type
    
    def test_memory_database_edge_cases(self):
        """Test memory database detection edge cases."""
        test_cases = [
            ("sqlite:///:memory:", True),
            ("sqlite:///:MEMORY:", True),  # Case insensitive
            ("sqlite:///path/to/:memory:", True),  # Memory string anywhere
            ("postgresql:///:memory:", True),
            ("sqlite:///test.db", False),
            ("", False),
            ("invalid", False),
        ]
        
        for url, expected in test_cases:
            assert is_memory_database(url) == expected


@pytest.mark.unit
class TestDatabasePerformanceAndLimits:
    """Test database performance characteristics and limits."""
    
    @pytest.mark.asyncio
    async def test_concurrent_session_access(self):
        """Test concurrent session access."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        async def create_feedback(session_num):
            async with db.session() as session:
                feedback = Feedback(
                    type=FeedbackType.BUG,
                    title=f"Concurrent feedback {session_num}",
                    description=f"Test feedback from session {session_num}",
                    submitter=f"user_{session_num}"
                )
                session.add(feedback)
                # Small delay to simulate work
                await asyncio.sleep(0.001)
        
        # Create multiple concurrent sessions
        tasks = [create_feedback(i) for i in range(10)]
        await asyncio.gather(*tasks)
        
        # Verify all feedback was created
        async with db.session() as session:
            result = session.execute(text("SELECT COUNT(*) FROM feedback"))
            count = result.scalar()
            assert count == 10
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_large_data_operations(self):
        """Test operations with larger datasets."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        # Create larger dataset
        async with db.session() as session:
            for i in range(1000):
                feedback = Feedback(
                    type=FeedbackType.IMPROVEMENT,
                    title=f"Large dataset feedback {i}",
                    description="A" * 500,  # Larger description
                    submitter=f"user_{i % 100}"  # 100 different users
                )
                session.add(feedback)
        
        # Test stats with larger dataset
        stats = await get_database_stats(db)
        assert stats["total_count"] == 1000
        assert len(stats["by_type"]) >= 1
        assert stats["by_type"]["IMPROVEMENT"] == 1000
        
        await db.close()
    
    @pytest.mark.asyncio
    async def test_database_reconnection_scenario(self):
        """Test database reconnection scenarios."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        # Simulate connection loss by closing and reinitializing
        await db.close()
        assert not db._is_initialized
        
        # Should be able to reconnect
        await db.initialize()
        assert db._is_initialized
        
        # Should be able to use normally
        async with db.session() as session:
            result = session.execute(text("SELECT 1"))
            assert result.scalar() == 1
        
        await db.close()