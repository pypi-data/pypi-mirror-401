"""Submission mixin for feedback collection."""

from datetime import UTC, datetime
from typing import Any

from ..insights import record_feedback_submission
from ..models import SubmitFeedbackRequest, create_feedback_from_request
from .base import BaseFeedbackMixin, logger, mcp_tool


class SubmissionMixin(BaseFeedbackMixin):
    """Mixin for feedback submission functionality."""

    @mcp_tool(
        description="Submit feedback about your MCP experience - Use this tool when you encounter issues, have suggestions for improvement, or want to report positive experiences. AI models should proactively use this to help improve future MCP sessions. PRIVACY: Only include information you've already shared via previous MCP calls. Ask human permission before including any new sensitive data."
    )
    async def submit_feedback(self, request: SubmitFeedbackRequest) -> dict[str, Any]:
        """Submit feedback about the MCP server, tools, or interaction experience.

        AI models should use this tool to:
        - Report when tools don't work as expected (type='bug')
        - Suggest improvements to tool functionality (type='improvement')
        - Request new capabilities that would be helpful (type='feature')
        - Ask questions about unclear tool behavior (type='question')

        PRIVACY GUIDELINES:
        - Only include information already shared in this MCP session
        - Avoid including sensitive data not previously disclosed
        - When in doubt, ask the human for permission first
        - Focus on the specific technical issue, not broader context

        This helps improve the MCP server and tools for future sessions.

        Args:
            request: Feedback submission request with type, title, description, submitter.

        Returns:
            Dictionary with submission result including feedback_id if successful.
        """
        start_time = datetime.now(UTC)

        try:
            # Create feedback from request
            feedback = create_feedback_from_request(request)

            # Save to database
            async with self.database.session() as session:
                session.add(feedback)
                session.commit()
                session.refresh(feedback)

                feedback_id = str(feedback.id)

            # Record analytics (without PII)
            if self.insights.enabled:
                record_feedback_submission(
                    self.insights,
                    feedback_type=request.type,
                    has_contact=bool(request.contact_info),
                    title_length=len(request.title),
                    description_length=len(request.description),
                    source="mcp_tool",
                )

            self._record_tool_usage("submit_feedback", start_time, True)
            logger.info(f"Feedback submitted successfully: {feedback_id}")

            return {
                "success": True,
                "feedback_id": feedback_id,
                "message": "Feedback submitted successfully",
            }

        except Exception as e:
            logger.error(f"Failed to submit feedback: {e}")
            self._record_tool_usage(
                "submit_feedback", start_time, False, type(e).__name__
            )

            return {"success": False, "error": str(e)}
