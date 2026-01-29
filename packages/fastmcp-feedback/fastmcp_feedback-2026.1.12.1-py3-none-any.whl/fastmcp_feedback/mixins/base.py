"""Base mixin functionality and shared utilities for FastMCP Feedback."""

import logging
from datetime import UTC, datetime

from fastmcp.contrib.mcp_mixin import MCPMixin, mcp_tool

from ..database import FeedbackDatabase
from ..insights import (
    FeedbackInsights,
    record_tool_usage,
)
from ..models import Feedback, FeedbackStatus, FeedbackType, feedback_to_dict

logger = logging.getLogger(__name__)

# Explicit re-exports for other mixin modules
__all__ = [
    "BaseFeedbackMixin",
    "Feedback",
    "FeedbackDatabase",
    "FeedbackInsights",
    "FeedbackStatus",
    "FeedbackType",
    "feedback_to_dict",
    "logger",
    "mcp_tool",
    "record_tool_usage",
]


class BaseFeedbackMixin(MCPMixin):
    """Base class for all feedback mixins with shared functionality."""

    def __init__(
        self, database: FeedbackDatabase, insights: FeedbackInsights | None = None
    ):
        """Initialize base mixin.

        Args:
            database: Database instance.
            insights: Optional insights instance.
        """
        self.database = database
        self.insights = insights or FeedbackInsights(enabled=False)
        super().__init__()

    def _record_tool_usage(
        self,
        tool_name: str,
        start_time: datetime,
        success: bool,
        error_type: str | None = None,
    ) -> None:
        """Helper method to record tool usage metrics.

        Args:
            tool_name: Name of the tool being used.
            start_time: When the tool started execution.
            success: Whether the tool executed successfully.
            error_type: Type of error if success is False.
        """
        if self.insights.enabled:
            duration_ms = (datetime.now(UTC) - start_time).total_seconds() * 1000
            record_tool_usage(
                self.insights,
                tool_name=tool_name,
                success=success,
                duration_ms=duration_ms,
                error_type=error_type,
            )
