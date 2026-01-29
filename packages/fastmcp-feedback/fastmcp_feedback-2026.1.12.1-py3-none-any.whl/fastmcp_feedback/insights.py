"""Privacy-compliant analytics and insights for FastMCP Feedback."""

import logging
import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class InsightMetric:
    """Individual insight metric data point."""

    name: str
    value: dict[str, Any]
    timestamp: datetime = None

    def __post_init__(self):
        """Set default timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now(UTC)

    def __str__(self) -> str:
        """String representation of metric."""
        return f"InsightMetric(name='{self.name}', value={self.value}, timestamp={self.timestamp})"

    def to_dict(self) -> dict[str, Any]:
        """Convert metric to dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class AnalyticsData:
    """Container for analytics data with metadata."""

    metrics: list[InsightMetric]
    summary: dict[str, Any]
    period_start: datetime
    period_end: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert analytics data to dictionary."""
        return {
            "metrics": [metric.to_dict() for metric in self.metrics],
            "summary": self.summary,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
        }


class FeedbackInsights:
    """Privacy-compliant analytics and insights system."""

    def __init__(self, enabled: bool | None = None, retention_days: int = 90):
        """Initialize insights system.

        Args:
            enabled: Whether analytics are enabled. Defaults to environment variable.
            retention_days: Number of days to retain metrics data.
        """
        # Check environment variables for configuration
        env_enabled = os.getenv("FEEDBACK_INSIGHTS_ENABLED", "false").lower()
        env_retention = os.getenv("FEEDBACK_INSIGHTS_RETENTION_DAYS", "90")

        self.enabled = enabled if enabled is not None else env_enabled == "true"

        try:
            self.retention_days = (
                int(env_retention) if enabled is None else retention_days
            )
        except ValueError:
            self.retention_days = retention_days

        # Ensure minimum retention period
        if self.retention_days < 1:
            self.retention_days = 1

        self.metrics: list[InsightMetric] = []

        logger.info(
            f"FeedbackInsights initialized: enabled={self.enabled}, retention={self.retention_days} days"
        )

    def record_metric(self, name: str, value: dict[str, Any]) -> None:
        """Record an analytics metric.

        Args:
            name: Name of the metric.
            value: Metric value data (should not contain PII).
        """
        if not self.enabled:
            return

        try:
            metric = InsightMetric(name=name, value=value)
            self.metrics.append(metric)

            logger.debug(f"Recorded metric: {name} with {len(value)} data points")

            # Periodically clean up old metrics to manage memory
            if len(self.metrics) % 100 == 0:
                self.cleanup_old_metrics()

        except Exception as e:
            logger.error(f"Failed to record metric {name}: {e}")
            # Don't raise exception - insights should not break main functionality

    def get_metrics(self, metric_name: str | None = None) -> list[InsightMetric]:
        """Get metrics, optionally filtered by name.

        Args:
            metric_name: Name of metrics to filter by.

        Returns:
            List of matching metrics.
        """
        if not self.enabled:
            return []

        if metric_name is None:
            return self.metrics.copy()

        return [metric for metric in self.metrics if metric.name == metric_name]

    def get_metrics_since(self, since: datetime) -> list[InsightMetric]:
        """Get metrics since a specific timestamp.

        Args:
            since: Timestamp to filter from.

        Returns:
            List of metrics since the timestamp.
        """
        if not self.enabled:
            return []

        return [metric for metric in self.metrics if metric.timestamp >= since]

    def cleanup_old_metrics(self) -> int:
        """Remove metrics older than retention period.

        Returns:
            Number of metrics removed.
        """
        if not self.enabled:
            return 0

        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
        initial_count = len(self.metrics)

        self.metrics = [
            metric for metric in self.metrics if metric.timestamp >= cutoff_date
        ]

        removed_count = initial_count - len(self.metrics)

        if removed_count > 0:
            logger.info(
                f"Cleaned up {removed_count} old metrics (retention: {self.retention_days} days)"
            )

        return removed_count

    def get_analytics_summary(self) -> dict[str, Any]:
        """Get summary analytics.

        Returns:
            Dictionary with analytics summary.
        """
        if not self.enabled:
            return {"enabled": False, "message": "Analytics disabled"}

        total_metrics = len(self.metrics)

        # Count metrics by type
        metrics_by_type = defaultdict(int)
        for metric in self.metrics:
            metrics_by_type[metric.name] += 1

        # Calculate time range
        if self.metrics:
            timestamps = [metric.timestamp for metric in self.metrics]
            time_range = {
                "earliest": min(timestamps).isoformat(),
                "latest": max(timestamps).isoformat(),
            }
        else:
            time_range = {"earliest": None, "latest": None}

        return {
            "enabled": True,
            "total_metrics": total_metrics,
            "metrics_by_type": dict(metrics_by_type),
            "time_range": time_range,
            "retention_days": self.retention_days,
        }

    def export_data(self, include_metrics: bool = True) -> dict[str, Any]:
        """Export analytics data.

        Args:
            include_metrics: Whether to include individual metrics.

        Returns:
            Dictionary with exported data.
        """
        if not self.enabled:
            return {"enabled": False, "data": None}

        export_data = {
            "enabled": True,
            "summary": self.get_analytics_summary(),
            "export_timestamp": datetime.utcnow().isoformat(),
        }

        if include_metrics:
            export_data["metrics"] = [metric.to_dict() for metric in self.metrics]

        return export_data

    def import_data(self, data: dict[str, Any]) -> bool:
        """Import analytics data.

        Args:
            data: Data dictionary to import.

        Returns:
            True if import successful, False otherwise.
        """
        if not self.enabled:
            return False

        try:
            if "metrics" in data:
                imported_metrics = []
                for metric_data in data["metrics"]:
                    metric = InsightMetric(
                        name=metric_data["name"],
                        value=metric_data["value"],
                        timestamp=datetime.fromisoformat(metric_data["timestamp"]),
                    )
                    imported_metrics.append(metric)

                self.metrics.extend(imported_metrics)
                logger.info(f"Imported {len(imported_metrics)} metrics")
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to import analytics data: {e}")
            return False

    def generate_report(
        self, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> dict[str, Any]:
        """Generate analytics report for a time period.

        Args:
            start_date: Start of report period. Defaults to 7 days ago.
            end_date: End of report period. Defaults to now.

        Returns:
            Analytics report dictionary.
        """
        if not self.enabled:
            return {"enabled": False, "report": None}

        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=7)

        # Filter metrics by time period
        period_metrics = [
            metric
            for metric in self.metrics
            if start_date <= metric.timestamp <= end_date
        ]

        # Generate report
        report = {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": (end_date - start_date).days,
            },
            "total_events": len(period_metrics),
            "events_by_type": defaultdict(int),
            "daily_activity": defaultdict(int),
            "insights": [],
        }

        # Analyze metrics
        for metric in period_metrics:
            report["events_by_type"][metric.name] += 1
            day_key = metric.timestamp.strftime("%Y-%m-%d")
            report["daily_activity"][day_key] += 1

        # Convert defaultdicts to regular dicts
        report["events_by_type"] = dict(report["events_by_type"])
        report["daily_activity"] = dict(report["daily_activity"])

        # Generate insights
        if report["total_events"] > 0:
            most_active_day = max(
                report["daily_activity"], key=report["daily_activity"].get
            )
            most_common_event = max(
                report["events_by_type"], key=report["events_by_type"].get
            )

            report["insights"] = [
                f"Most active day: {most_active_day} ({report['daily_activity'][most_active_day]} events)",
                f"Most common event: {most_common_event} ({report['events_by_type'][most_common_event]} occurrences)",
                f"Average events per day: {report['total_events'] / max(1, report['period']['days']):.1f}",
            ]

        return report


# Privacy-compliant metric recording helpers


def record_feedback_submission(
    insights: FeedbackInsights,
    feedback_type: str,
    has_contact: bool = False,
    title_length: int = 0,
    description_length: int = 0,
    source: str = "api",
) -> None:
    """Record feedback submission metric without PII.

    Args:
        insights: Insights instance.
        feedback_type: Type of feedback.
        has_contact: Whether contact info was provided.
        title_length: Length of title (not actual title).
        description_length: Length of description.
        source: Source of submission.
    """
    insights.record_metric(
        "feedback_submitted",
        {
            "type": feedback_type,
            "has_contact": has_contact,
            "title_length": title_length,
            "description_length": description_length,
            "source": source,
        },
    )


def record_feedback_status_change(
    insights: FeedbackInsights,
    from_status: str,
    to_status: str,
    feedback_type: str,
    age_hours: float | None = None,
) -> None:
    """Record feedback status change metric.

    Args:
        insights: Insights instance.
        from_status: Original status.
        to_status: New status.
        feedback_type: Type of feedback.
        age_hours: Age of feedback in hours.
    """
    metric_data = {
        "from_status": from_status,
        "to_status": to_status,
        "type": feedback_type,
    }

    if age_hours is not None:
        metric_data["age_hours"] = age_hours

    insights.record_metric("feedback_status_updated", metric_data)


def record_tool_usage(
    insights: FeedbackInsights,
    tool_name: str,
    success: bool,
    duration_ms: float | None = None,
    error_type: str | None = None,
) -> None:
    """Record tool usage metric.

    Args:
        insights: Insights instance.
        tool_name: Name of the tool used.
        success: Whether the operation was successful.
        duration_ms: Operation duration in milliseconds.
        error_type: Type of error if unsuccessful.
    """
    metric_data = {"tool_name": tool_name, "success": success}

    if duration_ms is not None:
        metric_data["duration_ms"] = duration_ms

    if error_type is not None:
        metric_data["error_type"] = error_type

    insights.record_metric("tool_used", metric_data)


def record_feedback_retrieval(
    insights: FeedbackInsights,
    count: int,
    has_filters: bool = False,
    page_size: int = 10,
) -> None:
    """Record feedback retrieval metric.

    Args:
        insights: Insights instance.
        count: Number of feedback items retrieved.
        has_filters: Whether filters were applied.
        page_size: Page size used.
    """
    insights.record_metric(
        "feedback_listed",
        {"count": count, "has_filters": has_filters, "page_size": page_size},
    )


def record_statistics_view(
    insights: FeedbackInsights,
    total_feedback: int,
    types_count: int,
    statuses_count: int,
) -> None:
    """Record statistics view metric.

    Args:
        insights: Insights instance.
        total_feedback: Total number of feedback items.
        types_count: Number of different types.
        statuses_count: Number of different statuses.
    """
    insights.record_metric(
        "feedback_statistics_viewed",
        {
            "total_feedback": total_feedback,
            "types_count": types_count,
            "statuses_count": statuses_count,
        },
    )


# Configuration helpers


def setup_insights_from_environment() -> FeedbackInsights:
    """Set up insights from environment variables.

    Returns:
        Configured FeedbackInsights instance.
    """
    return FeedbackInsights()


def is_insights_enabled() -> bool:
    """Check if insights are enabled via environment.

    Returns:
        True if enabled, False otherwise.
    """
    return os.getenv("FEEDBACK_INSIGHTS_ENABLED", "false").lower() == "true"
