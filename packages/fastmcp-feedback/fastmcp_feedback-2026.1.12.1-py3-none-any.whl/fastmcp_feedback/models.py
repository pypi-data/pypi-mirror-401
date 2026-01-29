"""Database models and Pydantic schemas for FastMCP Feedback."""

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class FeedbackType(str, Enum):
    """Enumeration of feedback types."""

    BUG = "bug"
    FEATURE = "feature"
    IMPROVEMENT = "improvement"
    QUESTION = "question"


class FeedbackStatus(str, Enum):
    """Enumeration of feedback statuses."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Feedback(Base):
    """Database model for feedback items."""

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(SQLEnum(FeedbackType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    submitter = Column(String(255), nullable=False)
    contact_info = Column(String(255), nullable=True)
    status = Column(
        SQLEnum(FeedbackStatus), nullable=False, default=FeedbackStatus.OPEN
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __init__(self, **kwargs):
        """Initialize feedback with defaults."""
        if "status" not in kwargs:
            kwargs["status"] = FeedbackStatus.OPEN
        if "created_at" not in kwargs or "updated_at" not in kwargs:
            now = datetime.now(UTC)
            if "created_at" not in kwargs:
                kwargs["created_at"] = now
            if "updated_at" not in kwargs:
                kwargs["updated_at"] = now
        super().__init__(**kwargs)

    def __str__(self) -> str:
        """String representation of feedback."""
        return f"Feedback(id={self.id}, type={self.type}, title='{self.title}', status={self.status})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return self.__str__()

    def to_dict(self) -> dict[str, Any]:
        """Convert feedback to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value
            if isinstance(self.type, FeedbackType)
            else self.type,
            "title": self.title,
            "description": self.description,
            "submitter": self.submitter,
            "contact_info": self.contact_info,
            "status": self.status.value
            if isinstance(self.status, FeedbackStatus)
            else self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# Pydantic Models for API validation


class SubmitFeedbackRequest(BaseModel):
    """Request model for feedback submission about MCP server/tool experience."""

    type: str = Field(
        ...,
        description="Type of feedback: 'bug' (something doesn't work), 'feature' (request new capability), 'improvement' (suggest enhancement), 'question' (unclear behavior)",
    )
    title: str = Field(
        ...,
        description="Brief descriptive title summarizing the feedback (e.g., 'Tool X returns incorrect data', 'Need Y functionality for Z use case')",
    )
    description: str = Field(
        ...,
        description="Detailed description including: what happened, what you expected, how it impacts the MCP session. PRIVACY: Only include information already shared in this session. Ask human permission before including sensitive data not previously disclosed.",
    )
    submitter: str = Field(
        ...,
        description="Your identifier (e.g., 'Claude-3.5-Sonnet', 'GPT-4', 'Human-User', or generic session ID - avoid specific personal identifiers)",
    )
    contact_info: str | None = Field(
        None,
        max_length=255,
        description="Optional contact info for follow-up (generic session ID, public handles only - avoid personal details)",
    )

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate feedback type with helpful guidance."""
        valid_types = [t.value for t in FeedbackType]
        if v not in valid_types:
            raise ValueError(
                f"Invalid feedback type. Must be one of: {', '.join(valid_types)}. Use 'bug' for broken functionality, 'feature' for new capabilities, 'improvement' for enhancements, 'question' for clarification."
            )
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        if len(v) > 255:
            raise ValueError("Title too long (maximum 255 characters)")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Validate description is not empty."""
        if not v or not v.strip():
            raise ValueError("Description cannot be empty")
        if len(v) > 10000:
            raise ValueError("Description too long (maximum 10000 characters)")
        return v.strip()

    @field_validator("submitter")
    @classmethod
    def validate_submitter(cls, v: str) -> str:
        """Validate submitter is not empty."""
        if not v or not v.strip():
            raise ValueError("Submitter cannot be empty")
        return v.strip()


class FeedbackResponse(BaseModel):
    """Response model for feedback operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    feedback_id: str | None = Field(
        None, description="ID of the created/updated feedback"
    )
    message: str | None = Field(None, description="Success message")
    error: str | None = Field(None, description="Error message if operation failed")


class FeedbackItem(BaseModel):
    """Model for individual feedback items in responses."""

    id: str = Field(..., description="Feedback ID")
    type: str = Field(..., description="Feedback type")
    title: str = Field(..., description="Feedback title")
    description: str = Field(..., description="Feedback description")
    submitter: str = Field(..., description="Submitter name/ID")
    contact_info: str | None = Field(None, description="Contact information")
    status: str = Field(..., description="Current status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class FeedbackListResponse(BaseModel):
    """Response model for feedback list operations."""

    feedback: list[dict[str, Any]] = Field(..., description="List of feedback items")
    total_count: int = Field(..., description="Total number of feedback items")
    page: int = Field(1, description="Current page number")
    per_page: int = Field(10, description="Items per page")


class FeedbackStatsResponse(BaseModel):
    """Response model for feedback statistics."""

    total_count: int = Field(..., description="Total number of feedback items")
    by_type: dict[str, int] = Field(..., description="Count by feedback type")
    by_status: dict[str, int] = Field(..., description="Count by status")
    recent_count: int = Field(..., description="Count of recent feedback (last 7 days)")


class UpdateStatusRequest(BaseModel):
    """Request model for updating feedback status."""

    feedback_id: str = Field(..., description="ID of feedback to update")
    new_status: str = Field(..., description="New status for the feedback")
    note: str | None = Field(
        None, max_length=1000, description="Optional note about the status change"
    )

    @field_validator("new_status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate new status."""
        valid_statuses = [s.value for s in FeedbackStatus]
        if v not in valid_statuses:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        return v


class DeleteFeedbackRequest(BaseModel):
    """Request model for deleting feedback."""

    feedback_id: str = Field(..., description="ID of feedback to delete")


class BulkUpdateStatusRequest(BaseModel):
    """Request model for bulk status updates."""

    feedback_ids: list[str] = Field(
        ..., min_length=1, description="List of feedback IDs to update"
    )
    new_status: str = Field(..., description="New status for all feedback items")
    note: str | None = Field(
        None, max_length=1000, description="Optional note about the status change"
    )

    @field_validator("new_status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate new status."""
        valid_statuses = [s.value for s in FeedbackStatus]
        if v not in valid_statuses:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        return v


# Utility functions for model operations


def create_feedback_from_request(request: SubmitFeedbackRequest) -> Feedback:
    """Create a Feedback model instance from a request."""
    return Feedback(
        type=FeedbackType(request.type),
        title=request.title,
        description=request.description,
        submitter=request.submitter,
        contact_info=request.contact_info,
        status=FeedbackStatus.OPEN,
    )


def feedback_to_dict(feedback: Feedback) -> dict[str, Any]:
    """Convert Feedback model to dictionary for API responses."""
    return {
        "id": str(feedback.id),
        "type": feedback.type.value
        if isinstance(feedback.type, FeedbackType)
        else feedback.type,
        "title": feedback.title,
        "description": feedback.description,
        "submitter": feedback.submitter,
        "contact_info": feedback.contact_info,
        "status": feedback.status.value
        if isinstance(feedback.status, FeedbackStatus)
        else feedback.status,
        "created_at": feedback.created_at.isoformat() if feedback.created_at else None,
        "updated_at": feedback.updated_at.isoformat() if feedback.updated_at else None,
    }


def validate_feedback_type(feedback_type: str) -> bool:
    """Validate if feedback type is valid."""
    return feedback_type in [t.value for t in FeedbackType]


def validate_feedback_status(status: str) -> bool:
    """Validate if feedback status is valid."""
    return status in [s.value for s in FeedbackStatus]


# Model metadata for introspection

FEEDBACK_TYPES = [t.value for t in FeedbackType]
FEEDBACK_STATUSES = [s.value for s in FeedbackStatus]

MODEL_METADATA = {
    "feedback_types": FEEDBACK_TYPES,
    "feedback_statuses": FEEDBACK_STATUSES,
    "max_title_length": 255,
    "max_description_length": 10000,
    "max_submitter_length": 255,
    "max_contact_length": 255,
    "max_note_length": 1000,
}
