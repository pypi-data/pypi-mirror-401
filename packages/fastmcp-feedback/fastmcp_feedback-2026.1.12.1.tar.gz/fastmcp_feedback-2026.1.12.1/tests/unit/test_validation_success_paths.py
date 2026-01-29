"""
Tests for validation success paths to achieve 100% coverage.

This targets the specific success return statements in validators
that were missed by our edge case failure testing.
"""

import pytest
from fastmcp_feedback.models import (
    UpdateStatusRequest,
    BulkUpdateStatusRequest,
    FeedbackStatus
)


class TestValidationSuccessPaths:
    """Test successful validation paths to cover return statements."""
    
    def test_update_status_request_valid_status_success(self):
        """Test UpdateStatusRequest with valid status to cover success return path."""
        # This should succeed and cover the 'return v' line in validate_status
        for status in ["open", "in_progress", "resolved", "closed"]:
            request = UpdateStatusRequest(
                feedback_id="123",
                new_status=status  # Valid status should trigger success path
            )
            assert request.new_status == status
    
    def test_bulk_update_request_valid_status_success(self):
        """Test BulkUpdateStatusRequest with valid status to cover success return path."""
        # This should succeed and cover the 'return v' line in validate_status
        for status in ["open", "in_progress", "resolved", "closed"]:
            request = BulkUpdateStatusRequest(
                feedback_ids=["1", "2"],
                new_status=status,  # Valid status should trigger success path
                note="Valid status test"
            )
            assert request.new_status == status
    
    def test_validation_success_with_all_enum_values(self):
        """Test validation success with all FeedbackStatus enum values."""
        # Cover success paths for every possible valid status
        valid_statuses = [status.value for status in FeedbackStatus]
        
        for status in valid_statuses:
            # Test UpdateStatusRequest
            update_request = UpdateStatusRequest(
                feedback_id="test",
                new_status=status
            )
            assert update_request.new_status == status
            
            # Test BulkUpdateStatusRequest  
            bulk_request = BulkUpdateStatusRequest(
                feedback_ids=["1"],
                new_status=status
            )
            assert bulk_request.new_status == status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])