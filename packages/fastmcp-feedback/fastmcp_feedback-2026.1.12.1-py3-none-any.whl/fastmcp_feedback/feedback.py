"""Standalone server factory for FastMCP Feedback."""

import logging

from fastmcp import FastMCP

from .insights import FeedbackInsights
from .tools import add_feedback_tools

logger = logging.getLogger(__name__)


def create_feedback_server(
    name: str = "FastMCP Feedback Server",
    database_url: str | None = None,
    insights: FeedbackInsights | None = None,
    description: str | None = None,
) -> FastMCP:
    """Create a standalone FastMCP server dedicated to feedback functionality.

    This factory function creates a complete FastMCP server with all feedback
    tools pre-configured. Ideal for microservice architectures or when you
    want a dedicated feedback service.

    Args:
        name: Name of the FastMCP server.
        database_url: Database connection URL. Defaults to SQLite in-memory.
        insights: Optional insights instance. Creates default if not provided.
        description: Optional server description.

    Returns:
        Configured FastMCP server with feedback tools.
    """
    try:
        # Create FastMCP server
        server = FastMCP(name)

        # Set description if provided
        if description:
            server.description = description
        else:
            server.description = (
                "Comprehensive feedback collection and management system"
            )

        # Initialize insights if not provided
        if insights is None:
            insights = FeedbackInsights()

        # Add all feedback tools
        add_feedback_tools(server, database_url=database_url, insights=insights)

        logger.info(f"Created feedback server '{name}' successfully")

        return server

    except Exception as e:
        logger.error(f"Failed to create feedback server: {e}")
        raise


def create_submission_server(
    name: str = "Feedback Submission Server",
    database_url: str | None = None,
    insights: FeedbackInsights | None = None,
) -> FastMCP:
    """Create a server with only submission tools.

    Args:
        name: Name of the server.
        database_url: Database connection URL.
        insights: Optional insights instance.

    Returns:
        FastMCP server with submission tools only.
    """
    from .tools import add_submission_tools

    try:
        server = FastMCP(name)
        server.description = "Feedback submission service"

        insights = insights or FeedbackInsights()
        add_submission_tools(server, database_url, insights)

        logger.info(f"Created submission server '{name}'")
        return server

    except Exception as e:
        logger.error(f"Failed to create submission server: {e}")
        raise


def create_management_server(
    name: str = "Feedback Management Server",
    database_url: str | None = None,
    insights: FeedbackInsights | None = None,
) -> FastMCP:
    """Create a server with management and retrieval tools.

    Args:
        name: Name of the server.
        database_url: Database connection URL.
        insights: Optional insights instance.

    Returns:
        FastMCP server with management tools.
    """
    from .tools import add_management_tools, add_retrieval_tools

    try:
        server = FastMCP(name)
        server.description = "Feedback management and analytics service"

        insights = insights or FeedbackInsights()
        add_retrieval_tools(server, database_url, insights)
        add_management_tools(server, database_url, insights)

        logger.info(f"Created management server '{name}'")
        return server

    except Exception as e:
        logger.error(f"Failed to create management server: {e}")
        raise


def create_analytics_server(
    name: str = "Feedback Analytics Server",
    database_url: str | None = None,
    enable_insights: bool = True,
    retention_days: int = 90,
) -> FastMCP:
    """Create a server focused on analytics and reporting.

    Args:
        name: Name of the server.
        database_url: Database connection URL.
        enable_insights: Whether to enable analytics.
        retention_days: Days to retain analytics data.

    Returns:
        FastMCP server with analytics-focused tools.
    """
    from .tools import add_retrieval_tools

    try:
        server = FastMCP(name)
        server.description = "Feedback analytics and reporting service"

        insights = FeedbackInsights(
            enabled=enable_insights, retention_days=retention_days
        )

        # Add retrieval tools with enhanced analytics
        add_retrieval_tools(server, database_url, insights)

        # Add analytics-specific tools
        _add_analytics_tools(server, database_url, insights)

        logger.info(f"Created analytics server '{name}'")
        return server

    except Exception as e:
        logger.error(f"Failed to create analytics server: {e}")
        raise


def _add_analytics_tools(
    server: FastMCP, database_url: str | None, insights: FeedbackInsights
) -> None:
    """Add analytics-specific tools to a server.

    Args:
        server: FastMCP server instance.
        database_url: Database connection URL.
        insights: Insights instance.
    """

    async def get_analytics_report(
        start_date: str | None = None, end_date: str | None = None
    ) -> dict:
        """Get comprehensive analytics report.

        Args:
            start_date: Start date in ISO format.
            end_date: End date in ISO format.

        Returns:
            Analytics report dictionary.
        """
        try:
            from datetime import datetime

            start_dt = None
            end_dt = None

            if start_date:
                start_dt = datetime.fromisoformat(start_date)
            if end_date:
                end_dt = datetime.fromisoformat(end_date)

            report = insights.generate_report(start_dt, end_dt)
            return report

        except Exception as e:
            logger.error(f"Failed to generate analytics report: {e}")
            return {"error": str(e)}

    async def export_analytics_data(include_metrics: bool = False) -> dict:
        """Export analytics data for external analysis.

        Args:
            include_metrics: Whether to include individual metrics.

        Returns:
            Exported data dictionary.
        """
        try:
            return insights.export_data(include_metrics)

        except Exception as e:
            logger.error(f"Failed to export analytics data: {e}")
            return {"error": str(e)}

    # Register tools with the server
    server.add_tool(get_analytics_report)
    server.add_tool(export_analytics_data)


# Server composition helpers


def compose_feedback_services(
    main_server: FastMCP, services: dict, insights: FeedbackInsights | None = None
) -> None:
    """Compose multiple feedback services into a main server.

    Args:
        main_server: Main FastMCP server to import services into.
        services: Dictionary mapping service names to database URLs.
        insights: Shared insights instance.
    """
    try:
        shared_insights = insights or FeedbackInsights()

        for service_name, config in services.items():
            database_url = config.get("database_url")
            service_type = config.get("type", "full")  # full, submission, management

            if service_type == "submission":
                service_server = create_submission_server(
                    f"{service_name} Submission", database_url, shared_insights
                )
            elif service_type == "management":
                service_server = create_management_server(
                    f"{service_name} Management", database_url, shared_insights
                )
            else:
                service_server = create_feedback_server(
                    f"{service_name} Service", database_url, shared_insights
                )

            # Import service with prefix
            main_server.import_server(service_server, prefix=service_name)

        logger.info(f"Composed {len(services)} feedback services into main server")

    except Exception as e:
        logger.error(f"Failed to compose feedback services: {e}")
        raise


def create_distributed_feedback_system(
    services: dict, insights: FeedbackInsights | None = None
) -> dict:
    """Create a distributed feedback system with multiple specialized servers.

    Args:
        services: Configuration for different services.
        insights: Shared insights instance.

    Returns:
        Dictionary of created servers.
    """
    try:
        shared_insights = insights or FeedbackInsights()
        servers = {}

        for service_name, config in services.items():
            database_url = config.get("database_url")
            service_type = config.get("type", "full")

            if service_type == "submission":
                server = create_submission_server(
                    f"{service_name} Submission Service", database_url, shared_insights
                )
            elif service_type == "management":
                server = create_management_server(
                    f"{service_name} Management Service", database_url, shared_insights
                )
            elif service_type == "analytics":
                server = create_analytics_server(
                    f"{service_name} Analytics Service",
                    database_url,
                    config.get("enable_insights", True),
                    config.get("retention_days", 90),
                )
            else:
                server = create_feedback_server(
                    f"{service_name} Service", database_url, shared_insights
                )

            servers[service_name] = server

        logger.info(f"Created distributed feedback system with {len(servers)} services")
        return servers

    except Exception as e:
        logger.error(f"Failed to create distributed system: {e}")
        raise


# Health monitoring for servers


def get_server_health(server: FastMCP) -> dict:
    """Get health status of a feedback server.

    Args:
        server: FastMCP server instance.

    Returns:
        Health status dictionary.
    """
    try:
        return {
            "server_name": server.name,
            "status": "healthy",
            "message": "Feedback server is healthy",
        }

    except Exception as e:
        return {
            "server_name": getattr(server, "name", "unknown"),
            "status": "unhealthy",
            "error": str(e),
        }


def monitor_feedback_servers(servers: dict) -> dict:
    """Monitor health of multiple feedback servers.

    Args:
        servers: Dictionary of server name to FastMCP instance.

    Returns:
        Combined health status.
    """
    health_status = {
        "overall_status": "healthy",
        "servers": {},
        "summary": {
            "total_servers": len(servers),
            "healthy_servers": 0,
            "unhealthy_servers": 0,
            "total_tools": 0,
        },
    }

    for server_name, server in servers.items():
        server_health = get_server_health(server)
        health_status["servers"][server_name] = server_health

        if server_health["status"] == "healthy":
            health_status["summary"]["healthy_servers"] += 1
            health_status["summary"]["total_tools"] += server_health.get(
                "total_tools", 0
            )
        else:
            health_status["summary"]["unhealthy_servers"] += 1
            health_status["overall_status"] = "degraded"

    return health_status


# Configuration helpers


def get_server_templates() -> dict:
    """Get predefined server templates.

    Returns:
        Dictionary of server templates.
    """
    return {
        "basic": {
            "description": "Basic feedback server with all tools",
            "factory": create_feedback_server,
            "features": ["submission", "retrieval", "management", "analytics"],
        },
        "submission_only": {
            "description": "Server for feedback submission only",
            "factory": create_submission_server,
            "features": ["submission"],
        },
        "management": {
            "description": "Server for feedback management and reporting",
            "factory": create_management_server,
            "features": ["retrieval", "management", "analytics"],
        },
        "analytics": {
            "description": "Server focused on analytics and reporting",
            "factory": create_analytics_server,
            "features": ["analytics", "reporting", "insights"],
        },
    }


def validate_server_config(config: dict) -> dict:
    """Validate server configuration.

    Args:
        config: Server configuration.

    Returns:
        Validation result.
    """
    errors = []
    warnings = []

    # Validate required fields
    if not config.get("name"):
        errors.append("Server name is required")

    # Validate database configuration
    database_url = config.get("database_url")
    if database_url:
        if "sqlite:///:memory:" in database_url:
            warnings.append("Using in-memory database - data will be lost on restart")
    else:
        warnings.append("No database URL specified, using default")

    # Validate insights configuration
    insights_config = config.get("insights", {})
    if insights_config.get("enabled") and insights_config.get("retention_days", 90) < 1:
        errors.append("Insights retention days must be at least 1")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}
