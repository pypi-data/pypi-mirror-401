"""
Comprehensive tests for validation edge cases in FastMCP Feedback models.

This test suite specifically targets the uncovered validation code paths
to achieve 100% coverage while ensuring robust input validation.
"""

import pytest
from datetime import datetime, UTC
from typing import Dict, Any

from fastmcp_feedback.models import (
    Feedback,
    SubmitFeedbackRequest,
    UpdateStatusRequest,
    BulkUpdateStatusRequest,
    DeleteFeedbackRequest,
    FeedbackType,
    FeedbackStatus,
    validate_feedback_type,
    validate_feedback_status,
    FEEDBACK_TYPES,
    FEEDBACK_STATUSES
)


class TestStatusValidationEdgeCases:
    """Test status validation error paths that are currently uncovered."""
    
    def test_update_status_request_invalid_status(self):
        """Test UpdateStatusRequest with invalid status value."""
        with pytest.raises(ValueError, match="Invalid status. Must be one of"):
            UpdateStatusRequest(
                feedback_id="123",
                new_status="invalid_status_value"  # This should trigger validation error
            )
    
    def test_bulk_update_request_invalid_status(self):
        """Test BulkUpdateStatusRequest with invalid status value."""
        with pytest.raises(ValueError, match="Invalid status. Must be one of"):
            BulkUpdateStatusRequest(
                feedback_ids=["1", "2", "3"],
                new_status="completely_invalid_status",  # This should trigger validation error
                note="Testing invalid status"
            )
    
    def test_status_validation_with_enum_name_instead_of_value(self):
        """Test validation fails when using enum name instead of value."""
        # Enum names are like "OPEN", "IN_PROGRESS" but values are "open", "in_progress"
        with pytest.raises(ValueError, match="Invalid status"):
            UpdateStatusRequest(
                feedback_id="123", 
                new_status="OPEN"  # Should be "open", not "OPEN"
            )
    
    def test_status_validation_case_sensitivity(self):
        """Test that status validation is case-sensitive."""
        with pytest.raises(ValueError, match="Invalid status"):
            UpdateStatusRequest(
                feedback_id="123",
                new_status="Open"  # Should be "open", not "Open"
            )
    
    def test_status_validation_with_whitespace(self):
        """Test validation fails with whitespace around valid status."""
        with pytest.raises(ValueError, match="Invalid status"):
            UpdateStatusRequest(
                feedback_id="123",
                new_status=" open "  # Valid status with spaces should fail
            )
    
    def test_status_validation_with_empty_string(self):
        """Test validation fails with empty status."""
        with pytest.raises(ValueError, match="Invalid status"):
            UpdateStatusRequest(
                feedback_id="123",
                new_status=""  # Empty string should fail
            )
    
    def test_status_validation_with_none_converted_to_string(self):
        """Test validation fails when None gets converted to string."""
        with pytest.raises(ValueError, match="Invalid status"):
            UpdateStatusRequest(
                feedback_id="123",
                new_status="None"  # String "None" should fail
            )


class TestModelInitializationEdgeCases:
    """Test Feedback model initialization edge cases."""
    
    def test_feedback_constructor_with_explicit_created_at_only(self):
        """Test constructor when only created_at is provided."""
        explicit_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        
        feedback = Feedback(
            type=FeedbackType.BUG,
            title="Test Bug",
            description="Test description",
            submitter="tester",
            created_at=explicit_time  # Provide created_at but not updated_at
            # This should trigger the updated_at default assignment
        )
        
        assert feedback.created_at == explicit_time
        assert feedback.updated_at is not None
        assert feedback.updated_at != explicit_time  # Should be current time
        assert feedback.status == FeedbackStatus.OPEN  # Default status
    
    def test_feedback_constructor_with_explicit_updated_at_only(self):
        """Test constructor when only updated_at is provided."""
        explicit_time = datetime(2024, 6, 15, 14, 30, 0, tzinfo=UTC)
        
        feedback = Feedback(
            type=FeedbackType.FEATURE,
            title="Test Feature",
            description="Test description", 
            submitter="tester",
            updated_at=explicit_time  # Provide updated_at but not created_at
            # This should trigger the created_at default assignment
        )
        
        assert feedback.updated_at == explicit_time
        assert feedback.created_at is not None
        assert feedback.created_at != explicit_time  # Should be current time
        assert feedback.status == FeedbackStatus.OPEN  # Default status
    
    def test_feedback_constructor_with_explicit_status_and_timestamps(self):
        """Test constructor when all optional fields are explicitly provided."""
        created_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=UTC)
        updated_time = datetime(2024, 1, 1, 11, 0, 0, tzinfo=UTC)
        
        feedback = Feedback(
            type=FeedbackType.IMPROVEMENT,
            title="Test Improvement",
            description="Test description",
            submitter="tester",
            status=FeedbackStatus.IN_PROGRESS,  # Explicit status
            created_at=created_time,            # Explicit created_at
            updated_at=updated_time             # Explicit updated_at
            # No defaults should be applied
        )
        
        assert feedback.status == FeedbackStatus.IN_PROGRESS
        assert feedback.created_at == created_time
        assert feedback.updated_at == updated_time
    
    def test_feedback_constructor_minimal_required_fields(self):
        """Test constructor with only required fields."""
        feedback = Feedback(
            type=FeedbackType.QUESTION,
            title="Test Question",
            description="Test description",
            submitter="tester"
            # All optional fields should get defaults
        )
        
        assert feedback.status == FeedbackStatus.OPEN
        assert feedback.created_at is not None
        assert feedback.updated_at is not None
        assert feedback.contact_info is None  # Should remain None
        assert isinstance(feedback.created_at, datetime)
        assert isinstance(feedback.updated_at, datetime)


class TestUtilityValidationFunctions:
    """Test standalone validation utility functions."""
    
    def test_validate_feedback_type_valid_cases(self):
        """Test validate_feedback_type with all valid types."""
        for feedback_type in FEEDBACK_TYPES:
            assert validate_feedback_type(feedback_type) is True
    
    def test_validate_feedback_type_invalid_cases(self):
        """Test validate_feedback_type with invalid types."""
        invalid_types = [
            "invalid_type",
            "BUG",  # Enum name instead of value
            "Bug",  # Wrong case
            " bug ",  # With whitespace
            "",     # Empty string
            "null", # String null
            "undefined"
        ]
        
        for invalid_type in invalid_types:
            assert validate_feedback_type(invalid_type) is False
    
    def test_validate_feedback_status_valid_cases(self):
        """Test validate_feedback_status with all valid statuses."""
        for status in FEEDBACK_STATUSES:
            assert validate_feedback_status(status) is True
    
    def test_validate_feedback_status_invalid_cases(self):
        """Test validate_feedback_status with invalid statuses."""
        invalid_statuses = [
            "invalid_status",
            "OPEN",  # Enum name instead of value
            "Open",  # Wrong case
            " open ",  # With whitespace
            "",      # Empty string
            "null",  # String null
            "pending",  # Doesn't exist
            "completed"  # Doesn't exist
        ]
        
        for invalid_status in invalid_statuses:
            assert validate_feedback_status(invalid_status) is False


class TestValidationBoundaryConditions:
    """Test edge cases around validation boundaries."""
    
    def test_feedback_type_enum_consistency(self):
        """Ensure FEEDBACK_TYPES constant matches enum values."""
        expected_types = [t.value for t in FeedbackType]
        assert set(FEEDBACK_TYPES) == set(expected_types)
        assert len(FEEDBACK_TYPES) == len(FeedbackType)
    
    def test_feedback_status_enum_consistency(self):
        """Ensure FEEDBACK_STATUSES constant matches enum values."""
        expected_statuses = [s.value for s in FeedbackStatus]
        assert set(FEEDBACK_STATUSES) == set(expected_statuses)
        assert len(FEEDBACK_STATUSES) == len(FeedbackStatus)
    
    def test_bulk_update_minimum_feedback_ids(self):
        """Test BulkUpdateStatusRequest with minimum required feedback IDs."""
        # Should work with exactly 1 ID (min_length=1)
        request = BulkUpdateStatusRequest(
            feedback_ids=["123"],  # Exactly one ID
            new_status="resolved"
        )
        assert len(request.feedback_ids) == 1
    
    def test_bulk_update_empty_feedback_ids_list(self):
        """Test BulkUpdateStatusRequest fails with empty feedback IDs list."""
        with pytest.raises(ValueError, match="at least 1 item"):
            BulkUpdateStatusRequest(
                feedback_ids=[],  # Empty list should fail min_length=1
                new_status="resolved"
            )
    
    def test_bulk_update_note_max_length_boundary(self):
        """Test BulkUpdateStatusRequest note at maximum length boundary."""
        max_note = "x" * 1000  # Exactly at max_length=1000
        
        request = BulkUpdateStatusRequest(
            feedback_ids=["123"],
            new_status="resolved",
            note=max_note
        )
        assert len(request.note) == 1000
    
    def test_bulk_update_note_exceeds_max_length(self):
        """Test BulkUpdateStatusRequest note exceeding maximum length."""
        too_long_note = "x" * 1001  # One character over max_length=1000
        
        with pytest.raises(ValueError, match="at most 1000 characters"):
            BulkUpdateStatusRequest(
                feedback_ids=["123"],
                new_status="resolved",
                note=too_long_note
            )


class TestRequestModelValidation:
    """Test validation in request models."""
    
    def test_delete_feedback_request_validation(self):
        """Test DeleteFeedbackRequest with various ID formats."""
        # Valid cases
        valid_ids = ["123", "abc", "uuid-like-string", "1"]
        for valid_id in valid_ids:
            request = DeleteFeedbackRequest(feedback_id=valid_id)
            assert request.feedback_id == valid_id
    
    def test_submit_feedback_request_with_minimal_data(self):
        """Test SubmitFeedbackRequest with only required fields."""
        request = SubmitFeedbackRequest(
            type="bug",
            title="Minimal Bug Report",
            description="Basic description",
            submitter="minimal_user"
            # contact_info is optional and should default to None
        )
        
        assert request.contact_info is None
        assert request.type == "bug"
        assert len(request.title.strip()) > 0
        assert len(request.description.strip()) > 0


# Performance and edge case stress tests
class TestValidationPerformance:
    """Test validation performance with edge cases."""
    
    def test_status_validation_performance_with_many_requests(self):
        """Test validation performance doesn't degrade with repeated calls."""
        import time
        
        start_time = time.time()
        
        # Create 1000 validation requests
        for i in range(1000):
            try:
                UpdateStatusRequest(
                    feedback_id=f"test_{i}",
                    new_status="invalid_status_that_will_fail"
                )
            except ValueError:
                pass  # Expected validation failure
        
        end_time = time.time()
        validation_time = end_time - start_time
        
        # Validation should complete quickly even with many failures
        assert validation_time < 1.0  # Should complete in under 1 second
    
    def test_enum_validation_consistency_across_models(self):
        """Test that all models use consistent validation logic."""
        invalid_status = "definitely_invalid_status"
        
        # All these should fail with similar validation errors
        models_to_test = [
            lambda: UpdateStatusRequest(feedback_id="123", new_status=invalid_status),
            lambda: BulkUpdateStatusRequest(feedback_ids=["123"], new_status=invalid_status)
        ]
        
        for model_creator in models_to_test:
            with pytest.raises(ValueError, match="Invalid status"):
                model_creator()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])