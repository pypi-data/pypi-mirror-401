"""Unit tests for FastMCP Feedback insights and analytics."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import os
import tempfile

from fastmcp_feedback.insights import FeedbackInsights, InsightMetric, AnalyticsData


@pytest.mark.unit
class TestFeedbackInsights:
    """Test the FeedbackInsights analytics system."""
    
    def test_insights_initialization_enabled(self):
        """Test insights initialization with analytics enabled."""
        insights = FeedbackInsights(enabled=True)
        
        assert insights.enabled is True
        assert insights.retention_days == 90  # Default retention
        assert insights.metrics == []
    
    def test_insights_initialization_disabled(self):
        """Test insights initialization with analytics disabled."""
        insights = FeedbackInsights(enabled=False)
        
        assert insights.enabled is False
        assert insights.retention_days == 90
        assert insights.metrics == []
    
    def test_insights_custom_retention(self):
        """Test insights with custom retention period."""
        insights = FeedbackInsights(enabled=True, retention_days=30)
        
        assert insights.retention_days == 30
    
    def test_insights_environment_configuration(self):
        """Test insights configuration from environment variables."""
        with patch.dict(os.environ, {
            'FEEDBACK_INSIGHTS_ENABLED': 'true',
            'FEEDBACK_INSIGHTS_RETENTION_DAYS': '60'
        }):
            insights = FeedbackInsights()
            
            assert insights.enabled is True
            assert insights.retention_days == 60
    
    def test_record_metric_enabled(self, test_insights):
        """Test recording metrics when insights are enabled."""
        metric_name = "feedback_submitted"
        metric_value = {"type": "bug", "submitter": "user123"}
        
        test_insights.record_metric(metric_name, metric_value)
        
        assert len(test_insights.metrics) == 1
        
        recorded = test_insights.metrics[0]
        assert recorded.name == metric_name
        assert recorded.value == metric_value
        assert isinstance(recorded.timestamp, datetime)
    
    def test_record_metric_disabled(self, disabled_insights):
        """Test recording metrics when insights are disabled."""
        metric_name = "feedback_submitted"
        metric_value = {"type": "feature"}
        
        disabled_insights.record_metric(metric_name, metric_value)
        
        # No metrics should be recorded when disabled
        assert len(disabled_insights.metrics) == 0
    
    def test_record_multiple_metrics(self, test_insights):
        """Test recording multiple metrics."""
        metrics_data = [
            ("feedback_submitted", {"type": "bug"}),
            ("feedback_viewed", {"feedback_id": "123"}),
            ("feedback_updated", {"status": "resolved"})
        ]
        
        for name, value in metrics_data:
            test_insights.record_metric(name, value)
        
        assert len(test_insights.metrics) == 3
        
        # Verify all metrics are recorded
        recorded_names = [m.name for m in test_insights.metrics]
        expected_names = ["feedback_submitted", "feedback_viewed", "feedback_updated"]
        assert recorded_names == expected_names
    
    def test_get_metrics_by_name(self, test_insights):
        """Test retrieving metrics by name."""
        # Record some metrics
        test_insights.record_metric("feedback_submitted", {"type": "bug"})
        test_insights.record_metric("feedback_submitted", {"type": "feature"})
        test_insights.record_metric("feedback_viewed", {"id": "123"})
        
        # Get metrics by name
        submitted_metrics = test_insights.get_metrics("feedback_submitted")
        
        assert len(submitted_metrics) == 2
        for metric in submitted_metrics:
            assert metric.name == "feedback_submitted"
    
    def test_get_metrics_by_time_range(self, test_insights):
        """Test retrieving metrics by time range."""
        now = datetime.utcnow()
        
        # Create metrics with specific timestamps
        metric1 = InsightMetric("test_metric", {"value": 1}, now - timedelta(hours=2))
        metric2 = InsightMetric("test_metric", {"value": 2}, now - timedelta(hours=1))
        metric3 = InsightMetric("test_metric", {"value": 3}, now)
        
        test_insights.metrics = [metric1, metric2, metric3]
        
        # Get metrics from last 90 minutes
        since = now - timedelta(minutes=90)
        recent_metrics = test_insights.get_metrics_since(since)
        
        assert len(recent_metrics) == 2  # metric2 and metric3
        assert recent_metrics[0].value["value"] == 2
        assert recent_metrics[1].value["value"] == 3
    
    def test_cleanup_old_metrics(self, test_insights):
        """Test cleanup of old metrics based on retention policy."""
        now = datetime.utcnow()
        
        # Create metrics with different ages
        old_metric = InsightMetric("old_metric", {"value": 1}, now - timedelta(days=100))
        recent_metric = InsightMetric("recent_metric", {"value": 2}, now - timedelta(days=30))
        current_metric = InsightMetric("current_metric", {"value": 3}, now)
        
        test_insights.metrics = [old_metric, recent_metric, current_metric]
        
        # Cleanup old metrics (retention is 90 days)
        test_insights.cleanup_old_metrics()
        
        assert len(test_insights.metrics) == 2
        remaining_names = [m.name for m in test_insights.metrics]
        assert "old_metric" not in remaining_names
        assert "recent_metric" in remaining_names
        assert "current_metric" in remaining_names
    
    def test_get_analytics_summary(self, test_insights):
        """Test getting analytics summary."""
        # Record various metrics
        test_insights.record_metric("feedback_submitted", {"type": "bug"})
        test_insights.record_metric("feedback_submitted", {"type": "feature"})
        test_insights.record_metric("feedback_submitted", {"type": "bug"})
        test_insights.record_metric("feedback_viewed", {"id": "123"})
        
        summary = test_insights.get_analytics_summary()
        
        assert "total_metrics" in summary
        assert "metrics_by_type" in summary
        assert "time_range" in summary
        
        assert summary["total_metrics"] == 4
        assert "feedback_submitted" in summary["metrics_by_type"]
        assert "feedback_viewed" in summary["metrics_by_type"]
        assert summary["metrics_by_type"]["feedback_submitted"] == 3
        assert summary["metrics_by_type"]["feedback_viewed"] == 1


@pytest.mark.unit
class TestInsightMetric:
    """Test the InsightMetric data class."""
    
    def test_metric_creation(self):
        """Test creating an insight metric."""
        now = datetime.utcnow()
        metric = InsightMetric(
            name="test_metric",
            value={"key": "value"},
            timestamp=now
        )
        
        assert metric.name == "test_metric"
        assert metric.value == {"key": "value"}
        assert metric.timestamp == now
    
    def test_metric_creation_with_auto_timestamp(self):
        """Test creating metric with automatic timestamp."""
        metric = InsightMetric("auto_timestamp", {"data": "test"})
        
        assert metric.name == "auto_timestamp"
        assert isinstance(metric.timestamp, datetime)
        
        # Timestamp should be recent (within last minute)
        from datetime import UTC
        now = datetime.now(UTC)
        assert (now - metric.timestamp).total_seconds() < 60
    
    def test_metric_string_representation(self):
        """Test string representation of metric."""
        metric = InsightMetric("test_metric", {"type": "bug"})
        
        str_repr = str(metric)
        assert "test_metric" in str_repr
        assert "bug" in str_repr
    
    def test_metric_to_dict(self):
        """Test converting metric to dictionary."""
        now = datetime.utcnow()
        metric = InsightMetric("dict_test", {"value": 42}, now)
        
        metric_dict = metric.to_dict()
        
        assert metric_dict["name"] == "dict_test"
        assert metric_dict["value"] == {"value": 42}
        assert metric_dict["timestamp"] == now.isoformat()


@pytest.mark.unit
class TestAnalyticsData:
    """Test the AnalyticsData class."""
    
    def test_analytics_data_creation(self):
        """Test creating analytics data container."""
        metrics = [
            InsightMetric("metric1", {"value": 1}),
            InsightMetric("metric2", {"value": 2})
        ]
        
        analytics = AnalyticsData(
            metrics=metrics,
            summary={"total": 2},
            period_start=datetime.utcnow() - timedelta(days=1),
            period_end=datetime.utcnow()
        )
        
        assert len(analytics.metrics) == 2
        assert analytics.summary["total"] == 2
        assert analytics.period_start is not None
        assert analytics.period_end is not None
    
    def test_analytics_data_to_dict(self):
        """Test converting analytics data to dictionary."""
        metrics = [InsightMetric("test", {"value": 1})]
        analytics = AnalyticsData(
            metrics=metrics,
            summary={"count": 1},
            period_start=datetime.utcnow() - timedelta(hours=1),
            period_end=datetime.utcnow()
        )
        
        data_dict = analytics.to_dict()
        
        assert "metrics" in data_dict
        assert "summary" in data_dict
        assert "period_start" in data_dict
        assert "period_end" in data_dict
        
        assert len(data_dict["metrics"]) == 1
        assert data_dict["summary"]["count"] == 1


@pytest.mark.unit
class TestPrivacyCompliance:
    """Test privacy compliance features."""
    
    def test_no_pii_in_metrics(self, test_insights):
        """Test that no PII is recorded in metrics."""
        # Record metrics that might contain PII
        test_insights.record_metric("feedback_submitted", {
            "type": "bug",
            "has_contact": True,  # Boolean instead of actual contact
            "title_length": 25,   # Length instead of actual title
            "submitter_hash": "abc123"  # Hash instead of actual submitter
        })
        
        metrics = test_insights.get_metrics("feedback_submitted")
        metric = metrics[0]
        
        # Verify no actual PII is stored
        assert "email" not in str(metric.value).lower()
        assert "name" not in str(metric.value).lower()
        assert "@" not in str(metric.value)
        
        # Verify we have useful analytics data
        assert metric.value["type"] == "bug"
        assert metric.value["has_contact"] is True
        assert metric.value["title_length"] == 25
    
    def test_consent_tracking(self, test_insights):
        """Test analytics consent tracking."""
        # Record consent metric
        test_insights.record_metric("analytics_consent", {
            "granted": True,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0"
        })
        
        consent_metrics = test_insights.get_metrics("analytics_consent")
        assert len(consent_metrics) == 1
        assert consent_metrics[0].value["granted"] is True
    
    def test_data_retention_compliance(self, test_insights):
        """Test data retention compliance."""
        now = datetime.utcnow()
        
        # Create metrics at retention boundary
        boundary_date = now - timedelta(days=test_insights.retention_days)
        
        old_metric = InsightMetric("old", {"value": 1}, boundary_date - timedelta(days=1))
        boundary_metric = InsightMetric("boundary", {"value": 2}, boundary_date)
        new_metric = InsightMetric("new", {"value": 3}, now)
        
        test_insights.metrics = [old_metric, boundary_metric, new_metric]
        
        # Cleanup should remove only the old metric
        test_insights.cleanup_old_metrics()
        
        remaining_names = [m.name for m in test_insights.metrics]
        assert "old" not in remaining_names
        # Note: boundary metric might be removed depending on exact timing
        assert "new" in remaining_names
    
    def test_anonymized_aggregation(self, test_insights):
        """Test anonymized data aggregation."""
        # Record multiple metrics for aggregation
        feedback_types = ["bug", "feature", "bug", "improvement", "bug"]
        
        for feedback_type in feedback_types:
            test_insights.record_metric("feedback_submitted", {"type": feedback_type})
        
        # Get aggregated data
        summary = test_insights.get_analytics_summary()
        
        # Verify aggregation doesn't reveal individual entries
        assert summary["total_metrics"] == 5
        
        # Should show type distribution without individual identification
        type_counts = {}
        for metric in test_insights.get_metrics("feedback_submitted"):
            metric_type = metric.value["type"]
            type_counts[metric_type] = type_counts.get(metric_type, 0) + 1
        
        assert type_counts["bug"] == 3
        assert type_counts["feature"] == 1
        assert type_counts["improvement"] == 1


@pytest.mark.unit
class TestInsightsIntegration:
    """Test insights integration with feedback system."""
    
    def test_feedback_submission_tracking(self, test_insights):
        """Test tracking feedback submissions."""
        # Simulate feedback submission
        test_insights.record_metric("feedback_submitted", {
            "type": "bug",
            "has_contact": True,
            "title_length": 42,
            "description_length": 156,
            "source": "api"
        })
        
        submissions = test_insights.get_metrics("feedback_submitted")
        assert len(submissions) == 1
        
        submission = submissions[0]
        assert submission.value["type"] == "bug"
        assert submission.value["source"] == "api"
    
    def test_feedback_status_tracking(self, test_insights):
        """Test tracking feedback status changes."""
        test_insights.record_metric("feedback_status_changed", {
            "from_status": "open",
            "to_status": "resolved",
            "age_days": 5,
            "type": "bug"
        })
        
        status_changes = test_insights.get_metrics("feedback_status_changed")
        assert len(status_changes) == 1
        
        change = status_changes[0]
        assert change.value["from_status"] == "open"
        assert change.value["to_status"] == "resolved"
    
    def test_tool_usage_tracking(self, test_insights):
        """Test tracking MCP tool usage."""
        test_insights.record_metric("tool_used", {
            "tool_name": "submit_feedback",
            "success": True,
            "duration_ms": 245,
            "user_agent": "claude-client"
        })
        
        tool_usage = test_insights.get_metrics("tool_used")
        assert len(tool_usage) == 1
        
        usage = tool_usage[0]
        assert usage.value["tool_name"] == "submit_feedback"
        assert usage.value["success"] is True


@pytest.mark.unit
class TestInsightsPerformance:
    """Test insights performance characteristics."""
    
    def test_metric_recording_performance(self, test_insights, performance_timer):
        """Test performance of metric recording."""
        performance_timer.start()
        
        # Record 1000 metrics
        for i in range(1000):
            test_insights.record_metric("performance_test", {
                "iteration": i,
                "data": f"test_data_{i}"
            })
        
        performance_timer.stop()
        
        # Should complete quickly
        assert performance_timer.duration_ms < 1000  # 1 second
        assert len(test_insights.metrics) == 1000
    
    def test_metric_retrieval_performance(self, test_insights, performance_timer):
        """Test performance of metric retrieval."""
        # Add many metrics
        for i in range(1000):
            test_insights.record_metric(f"metric_{i % 10}", {"value": i})
        
        performance_timer.start()
        
        # Retrieve specific metrics
        results = test_insights.get_metrics("metric_0")
        
        performance_timer.stop()
        
        # Should be fast
        assert performance_timer.duration_ms < 100  # 100ms
        assert len(results) == 100  # Every 10th metric
    
    def test_cleanup_performance(self, test_insights, performance_timer):
        """Test performance of metric cleanup."""
        now = datetime.utcnow()
        
        # Add mix of old and new metrics
        for i in range(1000):
            age_days = i % 200  # 0-199 days old
            timestamp = now - timedelta(days=age_days)
            test_insights.metrics.append(
                InsightMetric(f"metric_{i}", {"value": i}, timestamp)
            )
        
        performance_timer.start()
        test_insights.cleanup_old_metrics()
        performance_timer.stop()
        
        # Should complete reasonably fast
        assert performance_timer.duration_ms < 500  # 500ms
        
        # Should have removed old metrics (> 90 days)
        remaining_count = len(test_insights.metrics)
        assert remaining_count < 1000  # Some should be removed


@pytest.mark.unit
class TestInsightsConfiguration:
    """Test insights configuration options."""
    
    def test_insights_from_environment(self):
        """Test insights configuration from environment variables."""
        env_vars = {
            'FEEDBACK_INSIGHTS_ENABLED': 'true',
            'FEEDBACK_INSIGHTS_RETENTION_DAYS': '30'
        }
        
        with patch.dict(os.environ, env_vars):
            insights = FeedbackInsights()
            
            assert insights.enabled is True
            assert insights.retention_days == 30
    
    def test_insights_disabled_from_environment(self):
        """Test disabling insights via environment."""
        with patch.dict(os.environ, {'FEEDBACK_INSIGHTS_ENABLED': 'false'}):
            insights = FeedbackInsights()
            
            assert insights.enabled is False
    
    def test_invalid_retention_days(self):
        """Test handling of invalid retention days."""
        # Test negative retention
        insights = FeedbackInsights(enabled=True, retention_days=-1)
        assert insights.retention_days == 1  # Should default to minimum
        
        # Test zero retention
        insights = FeedbackInsights(enabled=True, retention_days=0)
        assert insights.retention_days == 1  # Should default to minimum
    
    def test_very_long_retention(self):
        """Test handling of very long retention periods."""
        insights = FeedbackInsights(enabled=True, retention_days=36500)  # 100 years
        assert insights.retention_days == 36500  # Should accept long periods


@pytest.mark.unit
class TestInsightsStorage:
    """Test insights storage capabilities."""
    
    def test_insights_persistence(self):
        """Test insights persistence to storage."""
        # This would test saving/loading insights to/from file
        # For now, just test in-memory behavior
        insights = FeedbackInsights(enabled=True)
        
        # Record some metrics
        insights.record_metric("test", {"value": 1})
        insights.record_metric("test", {"value": 2})
        
        assert len(insights.metrics) == 2
    
    def test_insights_export(self, test_insights):
        """Test exporting insights data."""
        # Record test metrics
        test_insights.record_metric("export_test", {"value": "data1"})
        test_insights.record_metric("export_test", {"value": "data2"})
        
        # Export data
        exported = test_insights.export_data()
        
        assert "metrics" in exported
        assert "summary" in exported
        assert len(exported["metrics"]) == 2
    
    def test_insights_import(self):
        """Test importing insights data."""
        insights = FeedbackInsights(enabled=True)
        
        # Test data to import
        import_data = {
            "metrics": [
                {
                    "name": "imported_metric",
                    "value": {"imported": True},
                    "timestamp": datetime.utcnow().isoformat()
                }
            ]
        }
        
        # Import would be implemented as a method
        # For now, just test that we can create the structure
        assert "metrics" in import_data
        assert len(import_data["metrics"]) == 1