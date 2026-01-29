"""Management mixin for feedback status updates and deletion."""

from datetime import UTC, datetime
from typing import Any

from ..insights import record_feedback_status_change
from .base import (
    BaseFeedbackMixin,
    Feedback,
    FeedbackStatus,
    FeedbackType,
    logger,
    mcp_tool,
)


class ManagementMixin(BaseFeedbackMixin):
    """Mixin for feedback management functionality."""

    @mcp_tool(description="Update feedback status")
    async def update_feedback_status(
        self, feedback_id: str, new_status: FeedbackStatus, note: str | None = None
    ) -> dict[str, Any]:
        """Update the status of a feedback item.

        Args:
            feedback_id: ID of feedback to update.
            new_status: New status for the feedback.
            note: Optional note about the status change.

        Returns:
            Dictionary with update result.
        """
        start_time = datetime.now(UTC)

        try:
            async with self.database.session() as session:
                feedback = session.get(Feedback, int(feedback_id))

                if not feedback:
                    return {
                        "success": False,
                        "error": f"Feedback with ID {feedback_id} not found",
                    }

                old_status = feedback.status
                old_type = feedback.type

                # Calculate feedback age for analytics
                age_hours = None
                if feedback.created_at:
                    # Assume stored datetime is UTC (SQLite stores without timezone info)
                    created_utc = (
                        feedback.created_at.replace(tzinfo=UTC)
                        if feedback.created_at.tzinfo is None
                        else feedback.created_at
                    )
                    age_hours = (datetime.now(UTC) - created_utc).total_seconds() / 3600

                # Update status
                feedback.status = new_status
                feedback.updated_at = datetime.now(UTC)

                session.commit()

            # Record analytics
            if self.insights.enabled:
                record_feedback_status_change(
                    self.insights,
                    from_status=old_status.value
                    if isinstance(old_status, FeedbackStatus)
                    else old_status,
                    to_status=new_status.value
                    if isinstance(new_status, FeedbackStatus)
                    else new_status,
                    feedback_type=old_type.value
                    if isinstance(old_type, FeedbackType)
                    else old_type,
                    age_hours=age_hours,
                )

                # Record additional metric if note provided
                if note:
                    self.insights.record_metric(
                        "feedback_status_updated",
                        {
                            "feedback_id_hash": hash(feedback_id) % 10000,
                            "has_note": True,
                            "note_length": len(note),
                        },
                    )

            self._record_tool_usage("update_feedback_status", start_time, True)
            logger.info(
                f"Feedback {feedback_id} status updated: {old_status} -> {new_status}"
            )

            return {"success": True, "message": "Feedback status updated successfully"}

        except Exception as e:
            logger.error(f"Failed to update feedback status: {e}")
            self._record_tool_usage(
                "update_feedback_status", start_time, False, type(e).__name__
            )

            return {"success": False, "error": str(e)}

    @mcp_tool(description="Delete feedback item")
    async def delete_feedback(self, feedback_id: str) -> dict[str, Any]:
        """Delete a feedback item.

        Args:
            feedback_id: ID of feedback to delete.

        Returns:
            Dictionary with deletion result.
        """
        start_time = datetime.now(UTC)

        try:
            async with self.database.session() as session:
                feedback = session.get(Feedback, int(feedback_id))

                if not feedback:
                    return {
                        "success": False,
                        "error": f"Feedback with ID {feedback_id} not found",
                    }

                feedback_type = feedback.type

                session.delete(feedback)
                session.commit()

            # Record analytics
            if self.insights.enabled:
                self.insights.record_metric(
                    "feedback_deleted",
                    {
                        "type": feedback_type.value
                        if isinstance(feedback_type, FeedbackType)
                        else feedback_type,
                        "feedback_id_hash": hash(feedback_id) % 10000,
                    },
                )

            self._record_tool_usage("delete_feedback", start_time, True)
            logger.info(f"Feedback {feedback_id} deleted successfully")

            return {"success": True, "message": "Feedback deleted successfully"}

        except Exception as e:
            logger.error(f"Failed to delete feedback: {e}")
            self._record_tool_usage(
                "delete_feedback", start_time, False, type(e).__name__
            )

            return {"success": False, "error": str(e)}

    async def bulk_update_status(
        self, feedback_ids: list[str], new_status: FeedbackStatus
    ) -> dict[str, Any]:
        """Update status of multiple feedback items.

        Args:
            feedback_ids: List of feedback IDs to update.
            new_status: New status for all items.

        Returns:
            Dictionary with bulk update result.
        """
        try:
            updated_count = 0

            for feedback_id in feedback_ids:
                result = await self.update_feedback_status(feedback_id, new_status)
                if result.get("success"):
                    updated_count += 1

            return {
                "success": True,
                "updated_count": updated_count,
                "total_requested": len(feedback_ids),
                "message": f"Updated {updated_count} of {len(feedback_ids)} feedback items",
            }

        except Exception as e:
            logger.error(f"Failed bulk status update: {e}")
            return {"success": False, "error": str(e)}
