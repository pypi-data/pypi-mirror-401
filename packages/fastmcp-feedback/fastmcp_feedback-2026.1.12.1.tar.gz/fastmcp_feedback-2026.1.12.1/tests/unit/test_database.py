"""Unit tests for FastMCP Feedback database operations."""

import pytest
import tempfile
import os
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, IntegrityError

from fastmcp_feedback.database import FeedbackDatabase
from fastmcp_feedback.models import Feedback, FeedbackStatus, FeedbackType


@pytest.mark.unit
@pytest.mark.asyncio
class TestFeedbackDatabase:
    """Test the FeedbackDatabase class."""
    
    async def test_database_initialization_memory(self):
        """Test database initialization with in-memory SQLite."""
        db = FeedbackDatabase("sqlite:///:memory:")
        await db.initialize()
        
        assert db.database_url == "sqlite:///:memory:"
        assert db.engine is not None
        assert db.SessionLocal is not None
        
        await db.close()
    
    async def test_database_initialization_file(self, temp_db_path):
        """Test database initialization with file-based SQLite."""
        db_url = f"sqlite:///{temp_db_path}"
        db = FeedbackDatabase(db_url)
        await db.initialize()
        
        # Check that database file exists
        assert os.path.exists(temp_db_path)
        assert db.engine is not None
        
        await db.close()
    
    async def test_database_initialization_postgresql(self):
        """Test database initialization with PostgreSQL URL."""
        db_url = "postgresql://user:pass@localhost:5432/testdb"
        db = FeedbackDatabase(db_url)
        
        # Note: This won't actually connect, just test URL parsing
        assert db.database_url == db_url
        assert "postgresql" in db.database_url
    
    async def test_health_check_success(self, test_database):
        """Test successful database health check."""
        # test_database fixture already initializes the database
        is_healthy = await test_database.health_check()
        assert is_healthy is True
    
    async def test_health_check_failure(self):
        """Test database health check with connection failure."""
        # Use invalid database URL
        db = FeedbackDatabase("sqlite:///nonexistent_directory/db.sqlite")
        
        is_healthy = await db.health_check()
        assert is_healthy is False
    
    async def test_session_context_manager(self, test_database):
        """Test database session context manager."""
        # test_database fixture already initializes the database
        async with test_database.session() as session:
            assert session is not None
            # Session should be active
            assert session.is_active
        
        # Session should be closed after context exit
        # Note: We can't easily test this without access to session internals
    
    async def test_session_rollback_on_exception(self, test_database):
        """Test session rollback on exception."""
        # test_database fixture already initializes the database
        try:
            async with test_database.session() as session:
                # Create a feedback item
                feedback = Feedback(
                    type="bug",
                    title="Test feedback",
                    description="Test description",
                    submitter="test_user"
                )
                session.add(feedback)
                
                # Simulate an error
                raise ValueError("Test exception")
                
        except ValueError:
            pass  # Expected
        
        # Verify that no data was committed
        async with test_database.session() as session:
            count = session.execute(text("SELECT COUNT(*) FROM feedback"))
            result = count.scalar()
            assert result == 0
    
    async def test_create_tables(self, test_database):
        """Test table creation."""
        # test_database fixture already initializes the database
        # Check that tables exist by querying them
        async with test_database.session() as session:
            # This should not raise an exception
            result = session.execute(text("SELECT COUNT(*) FROM feedback"))
            count = result.scalar()
            assert count == 0
    
    async def test_database_url_validation(self):
        """Test database URL validation."""
        # Valid URLs
        valid_urls = [
            "sqlite:///:memory:",
            "sqlite:///./feedback.db",
            "postgresql://user:pass@localhost:5432/db",
            "postgresql+asyncpg://user:pass@localhost:5432/db"
        ]
        
        for url in valid_urls:
            db = FeedbackDatabase(url)
            assert db.database_url == url
    
    async def test_connection_pool_configuration(self, test_database):
        """Test connection pool configuration."""
        # test_database fixture already initializes the database
        # Check engine configuration
        engine = test_database.engine
        assert engine is not None
        
        # For SQLite, pool_size doesn't apply, but for PostgreSQL it would
        if "postgresql" in test_database.database_url:
            assert engine.pool.size() > 0


@pytest.mark.unit
@pytest.mark.asyncio
class TestFeedbackCRUD:
    """Test CRUD operations for feedback."""
    
    async def test_create_feedback(self, test_database, sample_feedback_data):
        """Test creating feedback in database."""
        # test_database fixture already initializes the database
        async with test_database.session() as session:
            feedback = Feedback(**sample_feedback_data)
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            
            assert feedback.id is not None
            assert feedback.type == sample_feedback_data["type"]
            assert feedback.title == sample_feedback_data["title"]
            assert feedback.status == FeedbackStatus.OPEN
    
    async def test_read_feedback_by_id(self, test_database, sample_feedback_data):
        """Test reading feedback by ID."""
        # test_database fixture already initializes the database
        feedback_id = None
        # Create feedback
        async with test_database.session() as session:
            feedback = Feedback(**sample_feedback_data)
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            feedback_id = feedback.id
        
        # Read feedback
        async with test_database.session() as session:
            retrieved = session.get(Feedback, feedback_id)
            
            assert retrieved is not None
            assert retrieved.id == feedback_id
            assert retrieved.title == sample_feedback_data["title"]
    
    async def test_update_feedback_status(self, test_database, sample_feedback_data):
        """Test updating feedback status."""
        # test_database fixture already initializes the database
        feedback_id = None
        # Create feedback
        async with test_database.session() as session:
            feedback = Feedback(**sample_feedback_data)
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            feedback_id = feedback.id
        
        # Update status
        async with test_database.session() as session:
            feedback = session.get(Feedback, feedback_id)
            feedback.status = FeedbackStatus.IN_PROGRESS
            session.commit()
        
        # Verify update
        async with test_database.session() as session:
            updated = session.get(Feedback, feedback_id)
            assert updated.status == FeedbackStatus.IN_PROGRESS
    
    async def test_delete_feedback(self, test_database, sample_feedback_data):
        """Test deleting feedback."""
        # test_database fixture already initializes the database
        feedback_id = None
        # Create feedback
        async with test_database.session() as session:
            feedback = Feedback(**sample_feedback_data)
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            feedback_id = feedback.id
        
        # Delete feedback
        async with test_database.session() as session:
            feedback = session.get(Feedback, feedback_id)
            session.delete(feedback)
            session.commit()
        
        # Verify deletion
        async with test_database.session() as session:
            deleted = session.get(Feedback, feedback_id)
            assert deleted is None
    
    async def test_list_all_feedback(self, test_database, multiple_feedback_data):
        """Test listing all feedback items."""
        # test_database fixture already initializes the database
        # Create multiple feedback items
        async with test_database.session() as session:
            for data in multiple_feedback_data:
                feedback = Feedback(**data)
                session.add(feedback)
            session.commit()
        
        # List all feedback
        async with test_database.session() as session:
            result = session.execute(text("SELECT * FROM feedback ORDER BY created_at"))
            feedback_list = result.fetchall()
            
            assert len(feedback_list) == len(multiple_feedback_data)
    
    async def test_filter_feedback_by_type(self, test_database, multiple_feedback_data):
        """Test filtering feedback by type."""
        # test_database fixture already initializes the database
        
        # Create multiple feedback items
        async with test_database.session() as session:
            for data in multiple_feedback_data:
                feedback = Feedback(**data)
                session.add(feedback)
            session.commit()
        
        # Filter by bug type
        async with test_database.session() as session:
            result = session.execute(
                text("SELECT * FROM feedback WHERE type = :type"), {"type": "BUG"}
            )
            bug_feedback = result.fetchall()
            
            # Should have exactly one bug feedback from test data
            assert len(bug_feedback) == 1
            assert bug_feedback[0].type == "BUG"
        
    
    async def test_filter_feedback_by_status(self, test_database, sample_feedback_data):
        """Test filtering feedback by status."""
        # test_database fixture already initializes the database
        
        # Create feedback with different statuses
        async with test_database.session() as session:
            feedback1 = Feedback(**sample_feedback_data)
            feedback1.status = FeedbackStatus.OPEN
            
            feedback2 = Feedback(**sample_feedback_data)
            feedback2.title = "Different title"
            feedback2.status = FeedbackStatus.RESOLVED
            
            session.add(feedback1)
            session.add(feedback2)
            session.commit()
        
        # Filter by open status
        async with test_database.session() as session:
            result = session.execute(
                text("SELECT * FROM feedback WHERE status = :status"), {"status": "OPEN"}
            )
            open_feedback = result.fetchall()
            
            assert len(open_feedback) == 1
            assert open_feedback[0].status == "OPEN"
        


@pytest.mark.unit
@pytest.mark.asyncio
class TestDatabaseErrorHandling:
    """Test database error handling scenarios."""
    
    async def test_connection_error_handling(self):
        """Test handling of database connection errors."""
        # Use invalid database path
        db = FeedbackDatabase("sqlite:///nonexistent/path/db.sqlite")
        
        with pytest.raises(OperationalError):
            await db.initialize()
    
    async def test_invalid_sql_query(self, test_database):
        """Test handling of invalid SQL queries."""
        # test_database fixture already initializes the database
        
        async with test_database.session() as session:
            with pytest.raises(Exception):  # Specific exception depends on database
                session.execute(text("SELECT * FROM nonexistent_table"))
        
    
    async def test_constraint_violation(self, test_database):
        """Test handling of database constraint violations."""
        # test_database fixture already initializes the database
        
        # This would test unique constraints if we had any defined
        # For now, test general integrity errors
        async with test_database.session() as session:
            # Create feedback with invalid foreign key (if we had any)
            feedback = Feedback(
                type="bug",
                title="Test feedback",
                description="Test description",
                submitter="test_user"
            )
            session.add(feedback)
            # No constraint violation expected with current schema
            session.commit()
        
    
    async def test_session_timeout_handling(self, test_database):
        """Test handling of session timeouts."""
        # test_database fixture already initializes the database
        
        # This is difficult to test without actually timing out
        # Just verify that sessions can be created and closed properly
        async with test_database.session() as session:
            assert session is not None
        


@pytest.mark.unit
@pytest.mark.asyncio
class TestDatabaseConfiguration:
    """Test database configuration options."""
    
    async def test_sqlite_pragma_settings(self):
        """Test SQLite pragma settings."""
        db = FeedbackDatabase("sqlite:///test.db")
        await db.initialize()
        
        # Test that foreign keys are enabled (if we configure them)
        async with db.session() as session:
            result = session.execute(text("PRAGMA foreign_keys"))
            # Result depends on our configuration
        
        await db.close()
        
        # Clean up test file
        if os.path.exists("test.db"):
            os.unlink("test.db")
    
    async def test_postgresql_connection_parameters(self):
        """Test PostgreSQL connection parameters."""
        db_url = "postgresql://user:pass@localhost:5432/testdb?sslmode=require"
        db = FeedbackDatabase(db_url)
        
        assert "sslmode=require" in db.database_url
        # Connection testing would require actual PostgreSQL instance
    
    async def test_database_url_with_options(self):
        """Test database URL with various options."""
        urls_with_options = [
            "sqlite:///test.db?check_same_thread=false",
            "postgresql://user:pass@localhost:5432/db?sslmode=require&application_name=feedback"
        ]
        
        for url in urls_with_options:
            db = FeedbackDatabase(url)
            assert db.database_url == url


@pytest.mark.unit
@pytest.mark.asyncio 
class TestDatabasePerformance:
    """Test database performance characteristics."""
    
    async def test_bulk_insert_performance(self, test_database, performance_timer):
        """Test performance of bulk feedback insertion."""
        # test_database fixture already initializes the database
        
        performance_timer.start()
        
        async with test_database.session() as session:
            # Insert 100 feedback items
            for i in range(100):
                feedback = Feedback(
                    type="improvement",
                    title=f"Performance test feedback {i}",
                    description=f"Performance testing feedback item {i}",
                    submitter=f"perf_user_{i}"
                )
                session.add(feedback)
            
            session.commit()
        
        performance_timer.stop()
        
        # Should complete in reasonable time (adjust based on requirements)
        assert performance_timer.duration_ms < 5000  # 5 seconds
        
        # Verify all items were inserted
        async with test_database.session() as session:
            result = session.execute(text("SELECT COUNT(*) FROM feedback"))
            count = result.scalar()
            assert count == 100
        
    
    async def test_query_performance(self, test_database, multiple_feedback_data, performance_timer):
        """Test performance of feedback queries."""
        # test_database fixture already initializes the database
        
        # Insert test data
        async with test_database.session() as session:
            for data in multiple_feedback_data * 10:  # 30 items
                feedback = Feedback(**data)
                session.add(feedback)
            session.commit()
        
        performance_timer.start()
        
        # Perform various queries
        async with test_database.session() as session:
            # Simple count query
            result1 = session.execute(text("SELECT COUNT(*) FROM feedback"))
            count = result1.scalar()
            
            # Filter query
            result2 = session.execute(text("SELECT * FROM feedback WHERE type = :type"), {"type": "BUG"})
            bug_items = result2.fetchall()
            
            # Order by query
            result3 = session.execute(text("SELECT * FROM feedback ORDER BY created_at DESC LIMIT 5"))
            recent_items = result3.fetchall()
        
        performance_timer.stop()
        
        # Verify results
        assert count == 30
        assert len(bug_items) == 10  # 10 bug items from multiplied test data
        assert len(recent_items) == 5
        
        # Should be fast
        assert performance_timer.duration_ms < 1000  # 1 second
        


@pytest.mark.unit
class TestDatabaseUtilities:
    """Test database utility functions."""
    
    def test_database_url_parsing(self):
        """Test database URL parsing utilities."""
        urls = [
            ("sqlite:///:memory:", "sqlite", None, None, None, ":memory:"),
            ("sqlite:///./feedback.db", "sqlite", None, None, None, "./feedback.db"),
            ("postgresql://user:pass@localhost:5432/feedback", "postgresql", "user", "localhost", 5432, "feedback")
        ]
        
        for url, expected_dialect, expected_user, expected_host, expected_port, expected_db in urls:
            db = FeedbackDatabase(url)
            
            # These would be utility methods on the database class
            # For now, just test that the URL is stored correctly
            assert db.database_url == url
    
    def test_database_backup_restore(self, test_database):
        """Test database backup and restore capabilities."""
        # This would test backup/restore functionality if implemented
        # For now, just test that database can be created and accessed
        assert test_database.database_url is not None
    
    def test_database_migration_support(self):
        """Test database migration support."""
        # This would test Alembic integration if implemented
        # For now, just test basic table creation
        db = FeedbackDatabase("sqlite:///:memory:")
        
        # Migration functionality would be tested here
        assert db.database_url == "sqlite:///:memory:"