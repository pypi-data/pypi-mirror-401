"""Unit tests for FastMCP Feedback database models."""

import pytest
from datetime import datetime
from typing import Dict, Any

from fastmcp_feedback.models import (
    Feedback, 
    FeedbackType, 
    FeedbackStatus,
    SubmitFeedbackRequest,
    FeedbackResponse,
    FeedbackListResponse
)


@pytest.mark.unit
class TestFeedbackModel:
    """Test the Feedback database model."""
    
    def test_feedback_creation_with_valid_data(self, sample_feedback_data):
        """Test creating a feedback item with valid data."""
        feedback = Feedback(**sample_feedback_data)
        
        assert feedback.type == "bug"
        assert feedback.title == "Application crashes on startup"
        assert feedback.description == "The app crashes immediately after launching on iOS 17"
        assert feedback.submitter == "test_user"
        assert feedback.contact_info == "test@example.com"
        assert feedback.status == FeedbackStatus.OPEN  # Default status
        assert feedback.created_at is not None
        assert feedback.updated_at is not None
    
    def test_feedback_creation_with_minimal_data(self):
        """Test creating feedback with only required fields."""
        feedback = Feedback(
            type="feature",
            title="Add dark mode",
            description="Please add dark mode support",
            submitter="user123"
        )
        
        assert feedback.type == "feature"
        assert feedback.title == "Add dark mode"
        assert feedback.contact_info is None
        assert feedback.status == FeedbackStatus.OPEN
    
    def test_feedback_type_validation(self):
        """Test feedback type validation."""
        valid_types = ["bug", "feature", "improvement", "question"]
        
        for feedback_type in valid_types:
            feedback = Feedback(
                type=feedback_type,
                title="Test feedback",
                description="Test description",
                submitter="test_user"
            )
            assert feedback.type == feedback_type
    
    def test_feedback_status_updates(self, sample_feedback_data):
        """Test feedback status transitions."""
        feedback = Feedback(**sample_feedback_data)
        
        # Test status transitions
        feedback.status = FeedbackStatus.IN_PROGRESS
        assert feedback.status == FeedbackStatus.IN_PROGRESS
        
        feedback.status = FeedbackStatus.RESOLVED
        assert feedback.status == FeedbackStatus.RESOLVED
        
        feedback.status = FeedbackStatus.CLOSED
        assert feedback.status == FeedbackStatus.CLOSED
    
    def test_feedback_string_representation(self, sample_feedback_data):
        """Test string representation of feedback."""
        feedback = Feedback(**sample_feedback_data)
        feedback.id = 1
        
        str_repr = str(feedback)
        assert "Feedback" in str_repr
        assert "Application crashes on startup" in str_repr
        assert "bug" in str_repr
    
    def test_feedback_to_dict(self, sample_feedback_data):
        """Test converting feedback to dictionary."""
        feedback = Feedback(**sample_feedback_data)
        feedback.id = 1
        
        feedback_dict = feedback.to_dict()
        
        assert feedback_dict["id"] == 1
        assert feedback_dict["type"] == "bug"
        assert feedback_dict["title"] == "Application crashes on startup"
        assert feedback_dict["status"] == "open"
        assert "created_at" in feedback_dict
        assert "updated_at" in feedback_dict


@pytest.mark.unit
class TestSubmitFeedbackRequest:
    """Test the SubmitFeedbackRequest Pydantic model."""
    
    def test_valid_request_creation(self):
        """Test creating a valid feedback request."""
        request = SubmitFeedbackRequest(
            type="bug",
            title="Test bug report",
            description="This is a test bug report",
            submitter="test_user",
            contact_info="test@example.com"
        )
        
        assert request.type == "bug"
        assert request.title == "Test bug report"
        assert request.description == "This is a test bug report"
        assert request.submitter == "test_user"
        assert request.contact_info == "test@example.com"
    
    def test_request_with_minimal_fields(self):
        """Test request with only required fields."""
        request = SubmitFeedbackRequest(
            type="feature",
            title="Feature request",
            description="Please add this feature",
            submitter="user123"
        )
        
        assert request.type == "feature"
        assert request.contact_info is None
    
    def test_invalid_feedback_type(self):
        """Test validation with invalid feedback type."""
        with pytest.raises(ValueError, match="Invalid feedback type"):
            SubmitFeedbackRequest(
                type="invalid_type",
                title="Test",
                description="Test description",
                submitter="test_user"
            )
    
    def test_empty_title_validation(self):
        """Test validation with empty title."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            SubmitFeedbackRequest(
                type="bug",
                title="",
                description="Test description",
                submitter="test_user"
            )
    
    def test_empty_description_validation(self):
        """Test validation with empty description."""
        with pytest.raises(ValueError, match="Description cannot be empty"):
            SubmitFeedbackRequest(
                type="bug",
                title="Test title",
                description="",
                submitter="test_user"
            )
    
    def test_empty_submitter_validation(self):
        """Test validation with empty submitter."""
        with pytest.raises(ValueError, match="Submitter cannot be empty"):
            SubmitFeedbackRequest(
                type="bug",
                title="Test title",
                description="Test description",
                submitter=""
            )
    
    def test_title_length_validation(self):
        """Test title length validation."""
        long_title = "x" * 256  # Exceeds 255 character limit
        
        with pytest.raises(ValueError, match="Title too long"):
            SubmitFeedbackRequest(
                type="bug",
                title=long_title,
                description="Test description",
                submitter="test_user"
            )
    
    def test_description_length_validation(self):
        """Test description length validation."""
        long_description = "x" * 10001  # Exceeds 10000 character limit
        
        with pytest.raises(ValueError, match="Description too long"):
            SubmitFeedbackRequest(
                type="bug",
                title="Test title",
                description=long_description,
                submitter="test_user"
            )


@pytest.mark.unit
class TestFeedbackResponse:
    """Test the FeedbackResponse Pydantic model."""
    
    def test_successful_response_creation(self):
        """Test creating a successful feedback response."""
        response = FeedbackResponse(
            success=True,
            feedback_id="12345",
            message="Feedback submitted successfully"
        )
        
        assert response.success is True
        assert response.feedback_id == "12345"
        assert response.message == "Feedback submitted successfully"
        assert response.error is None
    
    def test_error_response_creation(self):
        """Test creating an error feedback response."""
        response = FeedbackResponse(
            success=False,
            error="Validation failed: Title cannot be empty"
        )
        
        assert response.success is False
        assert response.feedback_id is None
        assert response.error == "Validation failed: Title cannot be empty"


@pytest.mark.unit
class TestFeedbackListResponse:
    """Test the FeedbackListResponse Pydantic model."""
    
    def test_feedback_list_response(self, multiple_feedback_data):
        """Test creating a feedback list response."""
        # Convert sample data to feedback objects
        feedback_items = []
        for i, data in enumerate(multiple_feedback_data):
            feedback_dict = {**data, "id": i + 1, "status": "open"}
            feedback_items.append(feedback_dict)
        
        response = FeedbackListResponse(
            feedback=feedback_items,
            total_count=len(feedback_items),
            page=1,
            per_page=10
        )
        
        assert len(response.feedback) == 3
        assert response.total_count == 3
        assert response.page == 1
        assert response.per_page == 10
    
    def test_empty_feedback_list_response(self):
        """Test creating an empty feedback list response."""
        response = FeedbackListResponse(
            feedback=[],
            total_count=0,
            page=1,
            per_page=10
        )
        
        assert len(response.feedback) == 0
        assert response.total_count == 0


@pytest.mark.unit
class TestModelValidation:
    """Test model validation and edge cases."""
    
    def test_feedback_with_special_characters(self):
        """Test feedback with special characters in text fields."""
        special_chars_data = {
            "type": "bug",
            "title": "Bug with émojis 🐛 and spëcial chars",
            "description": "Testing with special characters: @#$%^&*()[]{}|\\:;\"'<>?/~`",
            "submitter": "user_with-special.chars@example.com"
        }
        
        feedback = Feedback(**special_chars_data)
        assert "émojis 🐛" in feedback.title
        assert "@#$%^&*()" in feedback.description
    
    def test_feedback_with_unicode_content(self):
        """Test feedback with unicode content."""
        unicode_data = {
            "type": "feature",
            "title": "支持中文输入法",
            "description": "希望应用能够支持中文输入法，包括拼音、五笔等输入方式。",
            "submitter": "中文用户"
        }
        
        feedback = Feedback(**unicode_data)
        assert feedback.title == "支持中文输入法"
        assert "拼音" in feedback.description
    
    def test_feedback_timestamps(self, sample_feedback_data):
        """Test feedback timestamp behavior."""
        feedback = Feedback(**sample_feedback_data)
        
        # Check that timestamps are set
        assert feedback.created_at is not None
        assert feedback.updated_at is not None
        assert isinstance(feedback.created_at, datetime)
        assert isinstance(feedback.updated_at, datetime)
        
        # Initially, created_at and updated_at should be the same
        assert feedback.created_at == feedback.updated_at


@pytest.mark.unit
class TestEnumValidation:
    """Test enum validation for feedback types and statuses."""
    
    def test_feedback_type_enum_values(self):
        """Test all valid feedback type enum values."""
        valid_types = [
            FeedbackType.BUG,
            FeedbackType.FEATURE,
            FeedbackType.IMPROVEMENT,
            FeedbackType.QUESTION
        ]
        
        for feedback_type in valid_types:
            feedback = Feedback(
                type=feedback_type.value,
                title="Test feedback",
                description="Test description",
                submitter="test_user"
            )
            assert feedback.type == feedback_type.value
    
    def test_feedback_status_enum_values(self):
        """Test all valid feedback status enum values."""
        feedback = Feedback(
            type="bug",
            title="Test feedback",
            description="Test description",
            submitter="test_user"
        )
        
        valid_statuses = [
            FeedbackStatus.OPEN,
            FeedbackStatus.IN_PROGRESS,
            FeedbackStatus.RESOLVED,
            FeedbackStatus.CLOSED
        ]
        
        for status in valid_statuses:
            feedback.status = status
            assert feedback.status == status


@pytest.mark.unit 
class TestModelSerialization:
    """Test model serialization and deserialization."""
    
    def test_feedback_json_serialization(self, sample_feedback_data):
        """Test feedback model JSON serialization."""
        feedback = Feedback(**sample_feedback_data)
        feedback.id = 1
        
        # Test dictionary conversion
        feedback_dict = feedback.to_dict()
        
        required_fields = [
            'id', 'type', 'title', 'description', 'submitter',
            'contact_info', 'status', 'created_at', 'updated_at'
        ]
        
        for field in required_fields:
            assert field in feedback_dict
        
        # Test that datetime objects are properly handled
        assert isinstance(feedback_dict['created_at'], datetime)
        assert isinstance(feedback_dict['updated_at'], datetime)
    
    def test_request_model_validation(self):
        """Test Pydantic request model validation."""
        # Valid request data
        valid_data = {
            "type": "bug",
            "title": "Valid feedback",
            "description": "This is a valid feedback description",
            "submitter": "valid_user"
        }
        
        request = SubmitFeedbackRequest(**valid_data)
        assert request.type == "bug"
        
        # Test model_dump for serialization
        dumped = request.model_dump()
        assert dumped["type"] == "bug"
        assert dumped["title"] == "Valid feedback"
    
    def test_response_model_creation(self):
        """Test response model creation and validation."""
        # Success response
        success_response = FeedbackResponse(
            success=True,
            feedback_id="abc123",
            message="Feedback created successfully"
        )
        
        assert success_response.success is True
        assert success_response.feedback_id == "abc123"
        assert success_response.error is None
        
        # Error response
        error_response = FeedbackResponse(
            success=False,
            error="Database connection failed"
        )
        
        assert error_response.success is False
        assert error_response.feedback_id is None
        assert error_response.error == "Database connection failed"