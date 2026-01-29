"""Tool mixins for modular FastMCP Feedback functionality.

This module maintains backward compatibility while providing a cleaner
modular structure for feedback tool mixins.
"""

# Import all mixins from their new locations
from .management import ManagementMixin
from .retrieval import RetrievalMixin
from .submission import SubmissionMixin

# Re-export for backward compatibility
__all__ = ["SubmissionMixin", "RetrievalMixin", "ManagementMixin"]

# Legacy import support - ensures existing imports continue to work
# Users can still do: from fastmcp_feedback.mixins import SubmissionMixin
