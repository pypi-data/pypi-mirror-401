"""Retrieval mixin for feedback querying and statistics."""

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import text

from ..insights import record_feedback_retrieval, record_statistics_view
from .base import BaseFeedbackMixin, Feedback, feedback_to_dict, logger, mcp_tool


class RetrievalMixin(BaseFeedbackMixin):
    """Mixin for feedback retrieval functionality."""

    @mcp_tool(description="List feedback items with optional filtering")
    async def list_feedback(
        self,
        type_filter: str | None = None,
        status_filter: str | None = None,
        page: int = 1,
        per_page: int = 10,
    ) -> dict[str, Any]:
        """List feedback items with filtering and pagination.

        Args:
            type_filter: Filter by feedback type.
            status_filter: Filter by feedback status.
            page: Page number (1-based).
            per_page: Number of items per page.

        Returns:
            Dictionary with feedback list and metadata.
        """
        start_time = datetime.now(UTC)

        try:
            async with self.database.session() as session:
                # Build query
                query = session.query(Feedback)

                # Apply filters
                if type_filter:
                    query = query.filter(Feedback.type == type_filter)
                if status_filter:
                    query = query.filter(Feedback.status == status_filter)

                # Get total count
                total_count = query.count()

                # Apply pagination
                offset = (page - 1) * per_page
                feedback_items = (
                    query.order_by(Feedback.created_at.desc())
                    .offset(offset)
                    .limit(per_page)
                    .all()
                )

                # Convert to dictionaries
                feedback_list = [feedback_to_dict(item) for item in feedback_items]

            # Record analytics
            if self.insights.enabled:
                record_feedback_retrieval(
                    self.insights,
                    count=len(feedback_list),
                    has_filters=bool(type_filter or status_filter),
                    page_size=per_page,
                )

            self._record_tool_usage("list_feedback", start_time, True)

            return {
                "feedback": feedback_list,
                "total_count": total_count,
                "page": page,
                "per_page": per_page,
            }

        except Exception as e:
            logger.error(f"Failed to list feedback: {e}")
            self._record_tool_usage(
                "list_feedback", start_time, False, type(e).__name__
            )

            return {
                "feedback": [],
                "total_count": 0,
                "page": page,
                "per_page": per_page,
                "error": str(e),
            }

    @mcp_tool(description="Get feedback statistics and analytics")
    async def get_feedback_statistics(self) -> dict[str, Any]:
        """Get comprehensive feedback statistics.

        Returns:
            Dictionary with statistics.
        """
        start_time = datetime.now(UTC)

        try:
            async with self.database.session() as session:
                # Total count
                total_result = session.execute(text("SELECT COUNT(*) FROM feedback"))
                total_count = total_result.scalar() or 0

                # Count by type
                type_result = session.execute(
                    text("SELECT type, COUNT(*) FROM feedback GROUP BY type")
                )
                by_type = dict(type_result.fetchall()) if total_count > 0 else {}

                # Count by status
                status_result = session.execute(
                    text("SELECT status, COUNT(*) FROM feedback GROUP BY status")
                )
                by_status = dict(status_result.fetchall()) if total_count > 0 else {}

                # Recent count (last 7 days)
                week_ago = datetime.now(UTC) - timedelta(days=7)
                recent_result = session.execute(
                    text("SELECT COUNT(*) FROM feedback WHERE created_at >= :week_ago"),
                    {"week_ago": week_ago},
                )
                recent_count = recent_result.scalar() or 0

            stats = {
                "total_count": total_count,
                "by_type": by_type,
                "by_status": by_status,
                "recent_count": recent_count,
            }

            # Record analytics
            if self.insights.enabled:
                record_statistics_view(
                    self.insights,
                    total_feedback=total_count,
                    types_count=len(by_type),
                    statuses_count=len(by_status),
                )

            self._record_tool_usage("get_feedback_statistics", start_time, True)
            return stats

        except Exception as e:
            logger.error(f"Failed to get feedback statistics: {e}")
            self._record_tool_usage(
                "get_feedback_statistics", start_time, False, type(e).__name__
            )

            return {
                "total_count": 0,
                "by_type": {},
                "by_status": {},
                "recent_count": 0,
                "error": str(e),
            }

    async def get_feedback_by_id(self, feedback_id: str) -> dict[str, Any] | None:
        """Get specific feedback by ID.

        Args:
            feedback_id: ID of feedback to retrieve.

        Returns:
            Feedback dictionary or None if not found.
        """
        try:
            async with self.database.session() as session:
                feedback = session.get(Feedback, int(feedback_id))

                if feedback:
                    return feedback_to_dict(feedback)
                return None

        except Exception as e:
            logger.error(f"Failed to get feedback by ID {feedback_id}: {e}")
            return None
