"""Main integration functions for FastMCP Feedback tools."""

import logging

from fastmcp import FastMCP

from .database import FeedbackDatabase
from .insights import FeedbackInsights
from .mixins import ManagementMixin, RetrievalMixin, SubmissionMixin

logger = logging.getLogger(__name__)


def add_feedback_tools(
    mcp: FastMCP,
    database_url: str | None = None,
    insights: FeedbackInsights | None = None,
    prefix: str = "",
    separator: str = "_",
) -> None:
    """Add all feedback tools to a FastMCP server.

    This is the main integration function that adds all feedback functionality
    to an existing FastMCP server using the mixin architecture.

    Args:
        mcp: FastMCP server instance to add tools to.
        database_url: Database connection URL. Defaults to SQLite in-memory.
        insights: Optional insights instance. Creates default if not provided.
        prefix: Optional prefix for tool names.
        separator: Separator between prefix and tool name.
    """
    try:
        # Initialize database
        database = FeedbackDatabase(database_url)

        # Initialize insights if not provided
        if insights is None:
            insights = FeedbackInsights()

        # Create mixin instances
        submission_mixin = SubmissionMixin(database, insights)
        retrieval_mixin = RetrievalMixin(database, insights)
        management_mixin = ManagementMixin(database, insights)

        # Register tools with proper prefix handling
        if prefix:
            clean_prefix = prefix.rstrip(separator)
            submission_mixin.register_tools(
                mcp, prefix=clean_prefix, separator=separator
            )
            retrieval_mixin.register_tools(
                mcp, prefix=clean_prefix, separator=separator
            )
            management_mixin.register_tools(
                mcp, prefix=clean_prefix, separator=separator
            )
        else:
            submission_mixin.register_tools(mcp)
            retrieval_mixin.register_tools(mcp)
            management_mixin.register_tools(mcp)

        logger.info(
            f"Feedback tools added to server '{mcp.name}' with prefix '{prefix}'"
        )

    except Exception as e:
        logger.error(f"Failed to add feedback tools: {e}")
        raise


def add_submission_tools(
    mcp: FastMCP,
    database_url: str | None = None,
    insights: FeedbackInsights | None = None,
    prefix: str = "",
) -> None:
    """Add only submission tools to a FastMCP server.

    Args:
        mcp: FastMCP server instance.
        database_url: Database connection URL.
        insights: Optional insights instance.
        prefix: Optional prefix for tool names.
    """
    try:
        database = FeedbackDatabase(database_url)
        insights = insights or FeedbackInsights()

        submission_mixin = SubmissionMixin(database, insights)

        if prefix:
            submission_mixin.register_tools(mcp, prefix=prefix.rstrip("_"))
        else:
            submission_mixin.register_tools(mcp)

        logger.info(f"Submission tools added to server '{mcp.name}'")

    except Exception as e:
        logger.error(f"Failed to add submission tools: {e}")
        raise


def add_retrieval_tools(
    mcp: FastMCP,
    database_url: str | None = None,
    insights: FeedbackInsights | None = None,
    prefix: str = "",
) -> None:
    """Add only retrieval tools to a FastMCP server.

    Args:
        mcp: FastMCP server instance.
        database_url: Database connection URL.
        insights: Optional insights instance.
        prefix: Optional prefix for tool names.
    """
    try:
        database = FeedbackDatabase(database_url)
        insights = insights or FeedbackInsights()

        retrieval_mixin = RetrievalMixin(database, insights)

        if prefix:
            retrieval_mixin.register_tools(mcp, prefix=prefix.rstrip("_"))
        else:
            retrieval_mixin.register_tools(mcp)

        logger.info(f"Retrieval tools added to server '{mcp.name}'")

    except Exception as e:
        logger.error(f"Failed to add retrieval tools: {e}")
        raise


def add_management_tools(
    mcp: FastMCP,
    database_url: str | None = None,
    insights: FeedbackInsights | None = None,
    prefix: str = "",
) -> None:
    """Add only management tools to a FastMCP server.

    Args:
        mcp: FastMCP server instance.
        database_url: Database connection URL.
        insights: Optional insights instance.
        prefix: Optional prefix for tool names.
    """
    try:
        database = FeedbackDatabase(database_url)
        insights = insights or FeedbackInsights()

        management_mixin = ManagementMixin(database, insights)

        if prefix:
            management_mixin.register_tools(mcp, prefix=prefix.rstrip("_"))
        else:
            management_mixin.register_tools(mcp)

        logger.info(f"Management tools added to server '{mcp.name}'")

    except Exception as e:
        logger.error(f"Failed to add management tools: {e}")
        raise


# Tool configuration helpers


def configure_feedback_tools(
    database_url: str | None = None,
    enable_insights: bool = True,
    insights_retention_days: int = 90,
) -> dict:
    """Configure feedback tools with specified parameters.

    Args:
        database_url: Database connection URL.
        enable_insights: Whether to enable analytics.
        insights_retention_days: Days to retain analytics data.

    Returns:
        Configuration dictionary for tool setup.
    """
    config = {
        "database_url": database_url or "sqlite:///:memory:",
        "insights": FeedbackInsights(
            enabled=enable_insights, retention_days=insights_retention_days
        ),
    }

    logger.info(
        f"Feedback tools configured: db={config['database_url']}, insights={enable_insights}"
    )

    return config


def get_tool_info() -> dict:
    """Get information about available feedback tools.

    Returns:
        Dictionary with tool information.
    """
    return {
        "available_tools": [
            "submit_feedback",
            "list_feedback",
            "get_feedback_statistics",
            "update_feedback_status",
            "delete_feedback",
        ],
        "mixin_classes": ["SubmissionMixin", "RetrievalMixin", "ManagementMixin"],
        "integration_functions": [
            "add_feedback_tools",
            "add_submission_tools",
            "add_retrieval_tools",
            "add_management_tools",
        ],
        "supported_databases": ["sqlite", "postgresql"],
        "features": [
            "Privacy-compliant analytics",
            "Modular mixin architecture",
            "Flexible tool prefixing",
            "Comprehensive error handling",
            "Production-ready database support",
        ],
    }


# Advanced integration patterns


def create_multi_tenant_tools(
    mcp: FastMCP, tenants: dict, insights: FeedbackInsights | None = None
) -> None:
    """Create feedback tools for multiple tenants with isolation.

    Args:
        mcp: FastMCP server instance.
        tenants: Dictionary mapping tenant names to database URLs.
        insights: Shared insights instance.
    """
    try:
        shared_insights = insights or FeedbackInsights()

        for tenant_name, database_url in tenants.items():
            add_feedback_tools(
                mcp,
                database_url=database_url,
                insights=shared_insights,
                prefix=tenant_name,
            )

        logger.info(f"Multi-tenant feedback tools created for {len(tenants)} tenants")

    except Exception as e:
        logger.error(f"Failed to create multi-tenant tools: {e}")
        raise


def create_role_based_tools(
    mcp: FastMCP,
    database_url: str | None = None,
    insights: FeedbackInsights | None = None,
) -> None:
    """Create role-based feedback tools with different access levels.

    Args:
        mcp: FastMCP server instance.
        database_url: Database connection URL.
        insights: Optional insights instance.
    """
    try:
        # Public tools - submission and listing only
        add_submission_tools(mcp, database_url, insights, prefix="public")
        add_retrieval_tools(mcp, database_url, insights, prefix="public")

        # Admin tools - full access
        add_feedback_tools(mcp, database_url, insights, prefix="admin")

        logger.info("Role-based feedback tools created")

    except Exception as e:
        logger.error(f"Failed to create role-based tools: {e}")
        raise


# Migration and upgrade helpers


def migrate_tools_to_mixins(
    mcp: FastMCP,
    old_tools: list,
    database_url: str | None = None,
    insights: FeedbackInsights | None = None,
) -> None:
    """Migrate from old tool structure to mixin-based architecture.

    Args:
        mcp: FastMCP server instance.
        old_tools: List of old tool names to replace.
        database_url: Database connection URL.
        insights: Optional insights instance.
    """
    try:
        # Remove old tools
        for tool_name in old_tools:
            if hasattr(mcp, "remove_tool"):
                mcp.remove_tool(tool_name)

        # Add new mixin-based tools
        add_feedback_tools(mcp, database_url, insights)

        logger.info(f"Migrated {len(old_tools)} old tools to mixin architecture")

    except Exception as e:
        logger.error(f"Failed to migrate tools: {e}")
        raise


# Health check and diagnostics


def check_tools_health(mcp: FastMCP) -> dict:
    """Check health of feedback tools.

    Args:
        mcp: FastMCP server instance.

    Returns:
        Health status dictionary.
    """
    try:
        return {
            "status": "healthy",
            "server_name": getattr(mcp, "name", "unknown"),
            "message": "FastMCP server is healthy",
        }

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}


def validate_tool_configuration(config: dict) -> dict:
    """Validate tool configuration.

    Args:
        config: Configuration dictionary.

    Returns:
        Validation result.
    """
    errors = []
    warnings = []

    # Check database URL
    if not config.get("database_url"):
        warnings.append("No database URL specified, using in-memory SQLite")
    elif "sqlite:///:memory:" in config.get("database_url", ""):
        warnings.append("Using in-memory database - data will be lost on restart")

    # Check insights configuration
    insights = config.get("insights")
    if insights and insights.enabled and insights.retention_days < 1:
        errors.append("Insights retention days must be at least 1")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}
