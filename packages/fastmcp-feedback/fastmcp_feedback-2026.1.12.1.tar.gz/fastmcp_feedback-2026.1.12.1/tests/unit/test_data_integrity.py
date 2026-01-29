"""
Comprehensive data integrity tests for FastMCP Feedback.

This test suite validates that ALL submitted data is correctly stored,
retrieved, and preserved through the complete lifecycle.
"""

import pytest
from datetime import datetime, UTC
from fastmcp_feedback.models import Feedback, FeedbackType, FeedbackStatus, SubmitFeedbackRequest


class TestDataIntegrity:
    """Test complete data integrity through the full pipeline."""
    
    @pytest.mark.asyncio
    async def test_complete_data_roundtrip_validation(self, test_database):
        """Test that ALL fields are correctly stored and retrieved exactly as submitted."""
        
        # Complex test data with edge cases
        original_data = {
            "type": "bug",
            "title": "  🐛 Critical Bug with Special Characters: émojis & symbols @#$%  ",
            "description": "Line 1: Detailed description\nLine 2: With newlines\nLine 3: And unicode: 测试中文 🎯",
            "submitter": "  test.user+123@example.com  ",  # With whitespace
            "contact_info": "Discord: user#1234, Slack: @testuser"
        }
        
        # 1. Submit through validation pipeline
        request = SubmitFeedbackRequest(**original_data)
        
        # 2. Store in database
        feedback_id = None
        async with test_database.session() as session:
            feedback = Feedback(
                type=FeedbackType(request.type),
                title=request.title,
                description=request.description,
                submitter=request.submitter,
                contact_info=request.contact_info,
                status=FeedbackStatus.OPEN
            )
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            feedback_id = feedback.id
            
            # Capture creation timestamp for later validation
            created_timestamp = feedback.created_at
        
        # 3. Retrieve from database
        async with test_database.session() as session:
            retrieved = session.get(Feedback, feedback_id)
            
            # 4. Validate ALL fields are preserved exactly
            assert retrieved is not None, "Feedback should be retrievable"
            
            # Core field validation
            assert retrieved.type == FeedbackType.BUG, f"Type mismatch: {retrieved.type} != {FeedbackType.BUG}"
            assert retrieved.status == FeedbackStatus.OPEN, f"Status mismatch: {retrieved.status} != {FeedbackStatus.OPEN}"
            
            # Text field validation (should preserve exact content after validation)
            assert retrieved.title == request.title, f"Title mismatch:\nExpected: {repr(request.title)}\nActual: {repr(retrieved.title)}"
            assert retrieved.description == request.description, f"Description mismatch:\nExpected: {repr(request.description)}\nActual: {repr(retrieved.description)}"
            assert retrieved.submitter == request.submitter, f"Submitter mismatch:\nExpected: {repr(request.submitter)}\nActual: {repr(retrieved.submitter)}"
            assert retrieved.contact_info == request.contact_info, f"Contact info mismatch:\nExpected: {repr(request.contact_info)}\nActual: {repr(retrieved.contact_info)}"
            
            # Timestamp validation
            assert retrieved.created_at is not None, "Created timestamp should be set"
            assert retrieved.updated_at is not None, "Updated timestamp should be set"
            assert retrieved.created_at == created_timestamp, "Created timestamp should be preserved"
            assert isinstance(retrieved.created_at, datetime), "Created timestamp should be datetime object"
            
            # Validate to_dict() method preserves data correctly
            feedback_dict = retrieved.to_dict()
            assert feedback_dict["title"] == request.title, "to_dict() should preserve title"
            assert feedback_dict["description"] == request.description, "to_dict() should preserve description"
            assert feedback_dict["submitter"] == request.submitter, "to_dict() should preserve submitter"
            assert feedback_dict["contact_info"] == request.contact_info, "to_dict() should preserve contact_info"
            assert feedback_dict["type"] == "bug", "to_dict() should return string enum values"
            assert feedback_dict["status"] == "open", "to_dict() should return string enum values"
    
    @pytest.mark.asyncio
    async def test_optional_fields_data_integrity(self, test_database):
        """Test data integrity with optional fields (None values)."""
        
        minimal_data = {
            "type": "feature",
            "title": "Essential feature request",
            "description": "This is the minimum required data",
            "submitter": "minimal@user.com"
            # contact_info is intentionally omitted
        }
        
        request = SubmitFeedbackRequest(**minimal_data)
        
        async with test_database.session() as session:
            feedback = Feedback(
                type=FeedbackType(request.type),
                title=request.title,
                description=request.description,
                submitter=request.submitter,
                contact_info=request.contact_info,  # Should be None
                status=FeedbackStatus.OPEN
            )
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            feedback_id = feedback.id
        
        # Retrieve and validate None handling
        async with test_database.session() as session:
            retrieved = session.get(Feedback, feedback_id)
            
            assert retrieved.contact_info is None, f"Optional field should be None, got: {retrieved.contact_info}"
            
            # Validate to_dict() handles None correctly
            feedback_dict = retrieved.to_dict()
            assert feedback_dict["contact_info"] is None, "to_dict() should preserve None values"
    
    @pytest.mark.asyncio
    async def test_whitespace_handling_consistency(self, test_database):
        """Test that whitespace trimming is applied consistently."""
        
        whitespace_data = {
            "type": "improvement",
            "title": "   Title with leading/trailing spaces   ",
            "description": "  \n  Description with various whitespace  \t  ",
            "submitter": "  \t whitespace@example.com \n ",
            "contact_info": "   Extra spaces in contact   "
        }
        
        request = SubmitFeedbackRequest(**whitespace_data)
        
        # Pydantic validation should trim whitespace
        assert request.title == "Title with leading/trailing spaces", "Title should be trimmed"
        assert request.submitter == "whitespace@example.com", "Submitter should be trimmed"
        
        # Store and retrieve
        async with test_database.session() as session:
            feedback = Feedback(
                type=FeedbackType(request.type),
                title=request.title,
                description=request.description,
                submitter=request.submitter,
                contact_info=request.contact_info,
                status=FeedbackStatus.OPEN
            )
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            feedback_id = feedback.id
        
        async with test_database.session() as session:
            retrieved = session.get(Feedback, feedback_id)
            
            # Validate trimmed data is preserved
            assert retrieved.title == request.title, "Trimmed title should be preserved"
            assert retrieved.submitter == request.submitter, "Trimmed submitter should be preserved"
            
            # Ensure no double-trimming occurred
            assert "Title with leading/trailing spaces" in retrieved.title
            assert "whitespace@example.com" in retrieved.submitter
    
    @pytest.mark.asyncio
    async def test_timezone_aware_datetime_integrity(self, test_database):
        """Test that datetime objects are stored and retrieved with proper timezone awareness."""
        
        test_data = {
            "type": "question",
            "title": "Timezone test",
            "description": "Testing datetime storage",
            "submitter": "timezone@test.com"
        }
        
        request = SubmitFeedbackRequest(**test_data)
        
        # Record the time of submission
        submission_time = datetime.now(UTC)
        
        async with test_database.session() as session:
            feedback = Feedback(
                type=FeedbackType(request.type),
                title=request.title,
                description=request.description,
                submitter=request.submitter,
                status=FeedbackStatus.OPEN
            )
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            feedback_id = feedback.id
        
        async with test_database.session() as session:
            retrieved = session.get(Feedback, feedback_id)
            
            # Validate timestamp integrity
            assert retrieved.created_at is not None, "Created timestamp should exist"
            assert retrieved.updated_at is not None, "Updated timestamp should exist"
            
            # Handle timezone-naive stored dates (SQLite stores without timezone info)
            stored_time = retrieved.created_at
            if stored_time.tzinfo is None:
                stored_time = stored_time.replace(tzinfo=UTC)
            
            # Timestamps should be close to submission time (within 1 second)
            time_diff = abs((stored_time - submission_time).total_seconds())
            assert time_diff < 1.0, f"Created timestamp should be close to submission time, diff: {time_diff}s"
            
            # created_at and updated_at should be the same for new records
            assert retrieved.created_at == retrieved.updated_at, "Initial created_at should equal updated_at"
    
    @pytest.mark.asyncio
    async def test_enum_storage_consistency(self, test_database):
        """Test that enums are stored and retrieved consistently."""
        
        for feedback_type in ["bug", "feature", "improvement", "question"]:
            for feedback_status in ["open", "in_progress", "resolved", "closed"]:
                test_data = {
                    "type": feedback_type,
                    "title": f"Test {feedback_type} - {feedback_status}",
                    "description": f"Testing enum storage for {feedback_type}/{feedback_status}",
                    "submitter": "enum@test.com"
                }
                
                request = SubmitFeedbackRequest(**test_data)
                
                async with test_database.session() as session:
                    feedback = Feedback(
                        type=FeedbackType(request.type),
                        title=request.title,
                        description=request.description,
                        submitter=request.submitter,
                        status=FeedbackStatus(feedback_status)
                    )
                    session.add(feedback)
                    session.commit()
                    session.refresh(feedback)
                    feedback_id = feedback.id
                
                async with test_database.session() as session:
                    retrieved = session.get(Feedback, feedback_id)
                    
                    # Validate enum integrity
                    assert retrieved.type.value == feedback_type, f"Type enum mismatch: {retrieved.type.value} != {feedback_type}"
                    assert retrieved.status.value == feedback_status, f"Status enum mismatch: {retrieved.status.value} != {feedback_status}"
                    
                    # Validate to_dict() returns string values
                    feedback_dict = retrieved.to_dict()
                    assert feedback_dict["type"] == feedback_type, "to_dict() should return enum values as strings"
                    assert feedback_dict["status"] == feedback_status, "to_dict() should return enum values as strings"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])