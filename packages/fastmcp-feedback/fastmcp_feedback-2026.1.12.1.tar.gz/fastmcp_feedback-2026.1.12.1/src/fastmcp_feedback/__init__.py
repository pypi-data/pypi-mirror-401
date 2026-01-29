"""FastMCP Feedback - Comprehensive feedback collection system for FastMCP servers.

This package provides a complete feedback collection and management system
that integrates seamlessly with FastMCP servers. It supports multiple
integration patterns, privacy-compliant analytics, and production-ready
database management.

Key Features:
- Modular mixin architecture for selective tool integration
- Privacy-compliant analytics with configurable data retention
- Support for SQLite (development) and PostgreSQL (production)
- Comprehensive error handling and logging
- Multiple server composition patterns
- Production-ready with connection pooling and health checks

Quick Start:
    Basic integration with existing FastMCP server:

    >>> from fastmcp import FastMCP
    >>> from fastmcp_feedback import add_feedback_tools
    >>>
    >>> app = FastMCP("My App")
    >>> add_feedback_tools(app, database_url="sqlite:///feedback.db")

    Create dedicated feedback server:

    >>> from fastmcp_feedback import create_feedback_server
    >>>
    >>> feedback_server = create_feedback_server("Feedback Service")
    >>> # feedback_server now has all feedback tools ready

    Selective tool integration using mixins:

    >>> from fastmcp_feedback import SubmissionMixin, RetrievalMixin
    >>> from fastmcp_feedback import FeedbackDatabase, FeedbackInsights
    >>>
    >>> db = FeedbackDatabase("postgresql://user:pass@host:5432/db")
    >>> insights = FeedbackInsights(enabled=True, retention_days=90)
    >>>
    >>> submission = SubmissionMixin(db, insights)
    >>> submission.register_tools(app, prefix="support")
"""

import logging

# Version information - CalVer YYYY.MM.DD
__version__ = "2026.01.12.1"
__author__ = "Ryan Malloy"
__email__ = "ryan@supported.systems"

# Core models and types
# Database management
from .database import (
    DatabaseConnectionError,
    DatabaseOperationError,
    FeedbackDatabase,
    create_feedback_database,
    get_connection_pool_status,
    get_database_session,
    get_database_stats,
    get_database_type,
    handle_database_error,
    is_memory_database,
    test_database_connection,
)

# Server factories
from .feedback import (
    # Composition helpers
    compose_feedback_services,
    create_analytics_server,
    create_distributed_feedback_system,
    # Server creation functions
    create_feedback_server,
    create_management_server,
    create_submission_server,
    # Monitoring
    get_server_health,
    # Configuration
    get_server_templates,
    monitor_feedback_servers,
    validate_server_config,
)

# Analytics and insights
from .insights import (
    AnalyticsData,
    FeedbackInsights,
    InsightMetric,
    is_insights_enabled,
    record_feedback_retrieval,
    record_feedback_status_change,
    # Helper functions
    record_feedback_submission,
    record_statistics_view,
    record_tool_usage,
    setup_insights_from_environment,
)

# Tool mixins
from .mixins import ManagementMixin, RetrievalMixin, SubmissionMixin
from .models import (
    FEEDBACK_STATUSES,
    # Constants
    FEEDBACK_TYPES,
    MODEL_METADATA,
    BulkUpdateStatusRequest,
    DeleteFeedbackRequest,
    # Database models
    Feedback,
    FeedbackListResponse,
    FeedbackResponse,
    FeedbackStatsResponse,
    FeedbackStatus,
    FeedbackType,
    # Pydantic models
    SubmitFeedbackRequest,
    UpdateStatusRequest,
    # Utility functions
    create_feedback_from_request,
    feedback_to_dict,
    validate_feedback_status,
    validate_feedback_type,
)

# Integration functions
from .tools import (
    # Main integration functions
    add_feedback_tools,
    add_management_tools,
    add_retrieval_tools,
    add_submission_tools,
    # Health and diagnostics
    check_tools_health,
    # Configuration helpers
    configure_feedback_tools,
    # Advanced patterns
    create_multi_tenant_tools,
    create_role_based_tools,
    get_tool_info,
    migrate_tools_to_mixins,
    validate_tool_configuration,
)

# Package metadata
PACKAGE_INFO = {
    "name": "fastmcp-feedback",
    "version": __version__,
    "description": "Comprehensive feedback collection system for FastMCP servers",
    "author": __author__,
    "email": __email__,
    "keywords": ["fastmcp", "feedback", "mcp", "analytics", "database"],
    "classifiers": [
        "Development Status :: 5 - Production/Ready",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    "dependencies": ["fastmcp>=2.12.2", "sqlalchemy>=2.0.43", "pydantic>=2.11.7"],
    "optional_dependencies": {
        "postgresql": ["psycopg2-binary>=2.9.0"],
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-html>=3.2.0",
            "pytest-cov>=4.1.0",
            "ruff>=0.1.0",
        ],
    },
}

# Public API - these are the main exports users should use
__all__ = [
    # Core models
    "Feedback",
    "FeedbackType",
    "FeedbackStatus",
    "SubmitFeedbackRequest",
    "FeedbackResponse",
    "FeedbackListResponse",
    # Database
    "FeedbackDatabase",
    "create_feedback_database",
    "get_database_session",
    # Analytics
    "FeedbackInsights",
    "InsightMetric",
    # Mixins
    "SubmissionMixin",
    "RetrievalMixin",
    "ManagementMixin",
    # Integration functions (most commonly used)
    "add_feedback_tools",
    "create_feedback_server",
    # Advanced integration
    "add_submission_tools",
    "add_retrieval_tools",
    "add_management_tools",
    "create_submission_server",
    "create_management_server",
    "create_analytics_server",
    # Configuration
    "configure_feedback_tools",
    "get_tool_info",
    # Constants
    "FEEDBACK_TYPES",
    "FEEDBACK_STATUSES",
    "PACKAGE_INFO",
]

# Integration examples for documentation
INTEGRATION_EXAMPLES = {
    "basic": """
from fastmcp import FastMCP
from fastmcp_feedback import add_feedback_tools

app = FastMCP("My Application")
add_feedback_tools(app, database_url="sqlite:///feedback.db")
""",
    "with_analytics": """
from fastmcp import FastMCP
from fastmcp_feedback import add_feedback_tools, FeedbackInsights

app = FastMCP("Analytics App")
insights = FeedbackInsights(enabled=True, retention_days=30)
add_feedback_tools(app, database_url="postgresql://user:pass@host/db", insights=insights)
""",
    "mixin_based": """
from fastmcp import FastMCP
from fastmcp_feedback import SubmissionMixin, FeedbackDatabase, FeedbackInsights

app = FastMCP("Custom App")
db = FeedbackDatabase("sqlite:///feedback.db")
insights = FeedbackInsights(enabled=True)

submission = SubmissionMixin(db, insights)
submission.register_tools(app, prefix="support")
""",
    "dedicated_server": """
from fastmcp_feedback import create_feedback_server

# Create standalone feedback service
feedback_server = create_feedback_server(
    "Customer Feedback Service",
    database_url="postgresql://user:pass@host/feedback",
    description="Dedicated customer feedback collection service"
)
""",
    "server_composition": """
from fastmcp import FastMCP
from fastmcp_feedback import create_feedback_server

main_app = FastMCP("Main Application")
feedback_service = create_feedback_server("Feedback Service")

# Import feedback service with prefix
main_app.import_server(feedback_service, prefix="feedback")
""",
    "multi_tenant": """
from fastmcp import FastMCP
from fastmcp_feedback import create_multi_tenant_tools

app = FastMCP("Multi-tenant App")
tenants = {
    "tenant_a": "postgresql://user:pass@host/tenant_a_feedback",
    "tenant_b": "postgresql://user:pass@host/tenant_b_feedback"
}
create_multi_tenant_tools(app, tenants)
""",
}

# Logging configuration


def setup_logging(level: str = "INFO") -> None:
    """Set up logging for FastMCP Feedback.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR).
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger("fastmcp_feedback")
    logger.info(f"FastMCP Feedback v{__version__} initialized")


# Auto-setup logging if not already configured
if not logging.getLogger().handlers:
    setup_logging()


def get_version_info() -> dict:
    """Get version and dependency information.

    Returns:
        Dictionary with version information.
    """
    import sys

    try:
        import fastmcp

        fastmcp_version = fastmcp.__version__
    except (ImportError, AttributeError):
        fastmcp_version = "unknown"

    try:
        import sqlalchemy

        sqlalchemy_version = sqlalchemy.__version__
    except (ImportError, AttributeError):
        sqlalchemy_version = "unknown"

    try:
        import pydantic

        pydantic_version = pydantic.VERSION
    except (ImportError, AttributeError):
        pydantic_version = "unknown"

    return {
        "fastmcp_feedback": __version__,
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "fastmcp": fastmcp_version,
        "sqlalchemy": sqlalchemy_version,
        "pydantic": pydantic_version,
    }


def check_dependencies() -> dict:
    """Check if all required dependencies are available.

    Returns:
        Dictionary with dependency status.
    """
    dependencies = {
        "fastmcp": ">=2.12.2",
        "sqlalchemy": ">=2.0.43",
        "pydantic": ">=2.11.7",
    }

    status = {"all_available": True, "details": {}}

    for package, required_version in dependencies.items():
        try:
            __import__(package)
            status["details"][package] = {
                "available": True,
                "required": required_version,
            }
        except ImportError:
            status["details"][package] = {
                "available": False,
                "required": required_version,
            }
            status["all_available"] = False

    return status
