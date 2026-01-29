"""Comprehensive tests for feedback.py server factory functions.

This module tests all server creation functions with comprehensive error handling,
configuration validation, and edge case testing to boost coverage to 90%+.
"""

import pytest
import pytest_asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock, PropertyMock
from fastmcp import FastMCP

from fastmcp_feedback.feedback import (
    create_feedback_server,
    create_submission_server,
    create_management_server,
    create_analytics_server,
    compose_feedback_services,
    create_distributed_feedback_system,
    get_server_health,
    monitor_feedback_servers,
    get_server_templates,
    validate_server_config,
    _add_analytics_tools
)
from fastmcp_feedback.insights import FeedbackInsights


@pytest.mark.unit
class TestFeedbackServerFactories:
    """Test server creation factory functions."""

    @pytest.mark.asyncio
    async def test_create_feedback_server_success(self, memory_db_url, test_insights):
        """Test successful feedback server creation with all parameters."""
        with patch('fastmcp_feedback.feedback.add_feedback_tools') as mock_add_tools:
            server = create_feedback_server(
                name="Test Feedback Server",
                database_url=memory_db_url,
                insights=test_insights,
                description="Custom test description"
            )

            # Verify server creation
            assert isinstance(server, FastMCP)
            assert server.name == "Test Feedback Server"
            assert server.description == "Custom test description"

            # Verify add_feedback_tools was called with correct parameters
            mock_add_tools.assert_called_once_with(
                server,
                database_url=memory_db_url,
                insights=test_insights
            )

    @pytest.mark.asyncio
    async def test_create_feedback_server_defaults(self):
        """Test feedback server creation with default parameters."""
        with patch('fastmcp_feedback.feedback.add_feedback_tools') as mock_add_tools:
            server = create_feedback_server()

            # Verify defaults are applied
            assert server.name == "FastMCP Feedback Server"
            assert server.description == "Comprehensive feedback collection and management system"

            # Verify insights were created as default
            mock_add_tools.assert_called_once()
            call_args = mock_add_tools.call_args
            assert call_args[0][0] == server  # First arg is server
            assert call_args[1]['database_url'] is None
            assert isinstance(call_args[1]['insights'], FeedbackInsights)

    @pytest.mark.asyncio
    async def test_create_feedback_server_error_handling(self):
        """Test error handling in feedback server creation."""
        with patch('fastmcp_feedback.feedback.add_feedback_tools', side_effect=Exception("Database connection failed")):
            with pytest.raises(Exception, match="Database connection failed"):
                create_feedback_server("Test Server")

    @pytest.mark.asyncio
    async def test_create_submission_server_success(self, memory_db_url):
        """Test successful submission server creation."""
        with patch('fastmcp_feedback.tools.add_submission_tools') as mock_add_submission:
            server = create_submission_server(
                name="Submission Server",
                database_url=memory_db_url,
                insights=None
            )

            assert isinstance(server, FastMCP)
            assert server.name == "Submission Server"
            assert server.description == "Feedback submission service"

            # Verify add_submission_tools was called
            mock_add_submission.assert_called_once()
            call_args = mock_add_submission.call_args
            assert call_args[0][0] == server
            assert call_args[0][1] == memory_db_url
            assert isinstance(call_args[0][2], FeedbackInsights)

    @pytest.mark.asyncio
    async def test_create_submission_server_default_name(self):
        """Test submission server creation with default name."""
        with patch('fastmcp_feedback.tools.add_submission_tools'):
            server = create_submission_server()
            assert server.name == "Feedback Submission Server"

    @pytest.mark.asyncio
    async def test_create_submission_server_error_handling(self):
        """Test error handling in submission server creation."""
        with patch('fastmcp_feedback.tools.add_submission_tools', side_effect=RuntimeError("Tool registration failed")):
            with pytest.raises(RuntimeError, match="Tool registration failed"):
                create_submission_server("Test Server")

    @pytest.mark.asyncio
    async def test_create_management_server_success(self, memory_db_url):
        """Test successful management server creation."""
        with patch('fastmcp_feedback.tools.add_retrieval_tools') as mock_retrieval, \
             patch('fastmcp_feedback.tools.add_management_tools') as mock_management:
            
            server = create_management_server(
                name="Management Server",
                database_url=memory_db_url
            )

            assert isinstance(server, FastMCP)
            assert server.name == "Management Server"
            assert server.description == "Feedback management and analytics service"

            # Verify both tool sets were added
            mock_retrieval.assert_called_once()
            mock_management.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_management_server_defaults(self):
        """Test management server creation with defaults."""
        with patch('fastmcp_feedback.tools.add_retrieval_tools'), \
             patch('fastmcp_feedback.tools.add_management_tools'):
            
            server = create_management_server()
            assert server.name == "Feedback Management Server"

    @pytest.mark.asyncio
    async def test_create_management_server_error_handling(self):
        """Test error handling in management server creation."""
        with patch('fastmcp_feedback.tools.add_retrieval_tools', side_effect=ValueError("Invalid configuration")):
            with pytest.raises(ValueError, match="Invalid configuration"):
                create_management_server("Test Server")

    @pytest.mark.asyncio
    async def test_create_analytics_server_success(self, memory_db_url):
        """Test successful analytics server creation."""
        with patch('fastmcp_feedback.tools.add_retrieval_tools') as mock_retrieval, \
             patch('fastmcp_feedback.feedback._add_analytics_tools') as mock_analytics:
            
            server = create_analytics_server(
                name="Analytics Server",
                database_url=memory_db_url,
                enable_insights=True,
                retention_days=60
            )

            assert isinstance(server, FastMCP)
            assert server.name == "Analytics Server"
            assert server.description == "Feedback analytics and reporting service"

            # Verify insights configuration
            mock_retrieval.assert_called_once()
            mock_analytics.assert_called_once()

            # Check insights configuration from call
            retrieval_call_args = mock_retrieval.call_args
            insights = retrieval_call_args[0][2]  # Third argument is insights
            assert insights.enabled is True
            assert insights.retention_days == 60

    @pytest.mark.asyncio
    async def test_create_analytics_server_defaults(self):
        """Test analytics server creation with default parameters."""
        with patch('fastmcp_feedback.tools.add_retrieval_tools'), \
             patch('fastmcp_feedback.feedback._add_analytics_tools'):
            
            server = create_analytics_server()
            assert server.name == "Feedback Analytics Server"

    @pytest.mark.asyncio
    async def test_create_analytics_server_error_handling(self):
        """Test error handling in analytics server creation."""
        with patch('fastmcp_feedback.tools.add_retrieval_tools'), \
             patch('fastmcp_feedback.feedback._add_analytics_tools', side_effect=ConnectionError("Analytics service unavailable")):
            
            with pytest.raises(ConnectionError, match="Analytics service unavailable"):
                create_analytics_server("Test Server")


@pytest.mark.unit
class TestAnalyticsTools:
    """Test analytics-specific tool creation."""

    @pytest.mark.asyncio
    async def test_add_analytics_tools_success(self, memory_db_url):
        """Test successful analytics tools addition."""
        server = Mock()
        server.add_tool = Mock()
        insights = Mock()
        insights.generate_report.return_value = {"total_feedback": 10}
        insights.export_data.return_value = {"data": "test"}

        # Test the internal function
        _add_analytics_tools(server, memory_db_url, insights)

        # Verify add_tool was called twice (for both analytics tools)
        assert server.add_tool.call_count == 2

    @pytest.mark.asyncio
    async def test_analytics_report_tool_success(self):
        """Test analytics report tool with date parameters."""
        # Test the analytics report function directly
        insights = Mock()
        insights.generate_report.return_value = {"total_feedback": 5, "period": "test"}

        # Create a mock server to capture the tool functions
        captured_tools = []
        
        def mock_add_tool(func):
            captured_tools.append(func)
        
        server = Mock()
        server.add_tool = mock_add_tool

        _add_analytics_tools(server, None, insights)

        # Find the analytics report tool
        report_tool = None
        for tool in captured_tools:
            if hasattr(tool, '__name__') and 'analytics_report' in tool.__name__:
                report_tool = tool
                break

        assert report_tool is not None

        # Test the tool function directly
        result = await report_tool("2024-01-01", "2024-01-31")
        insights.generate_report.assert_called_once()
        assert result == {"total_feedback": 5, "period": "test"}

    @pytest.mark.asyncio
    async def test_analytics_report_tool_error_handling(self):
        """Test analytics report tool error handling."""
        insights = Mock()
        insights.generate_report.side_effect = ValueError("Invalid date format")

        # Create a mock server to capture the tool functions
        captured_tools = []
        
        def mock_add_tool(func):
            captured_tools.append(func)
        
        server = Mock()
        server.add_tool = mock_add_tool

        _add_analytics_tools(server, None, insights)

        # Find the analytics report tool
        report_tool = None
        for tool in captured_tools:
            if hasattr(tool, '__name__') and 'analytics_report' in tool.__name__:
                report_tool = tool
                break

        assert report_tool is not None

        # Test error handling
        result = await report_tool("invalid-date", "2024-01-31")
        assert "error" in result
        assert "Invalid" in result["error"]  # More flexible assertion to handle different error messages

    @pytest.mark.asyncio
    async def test_export_analytics_tool_success(self):
        """Test export analytics data tool."""
        insights = Mock()
        insights.export_data.return_value = {"exported_data": "success"}

        # Create a mock server to capture the tool functions
        captured_tools = []
        
        def mock_add_tool(func):
            captured_tools.append(func)
        
        server = Mock()
        server.add_tool = mock_add_tool

        _add_analytics_tools(server, None, insights)

        # Find the export tool
        export_tool = None
        for tool in captured_tools:
            if hasattr(tool, '__name__') and 'export_analytics_data' in tool.__name__:
                export_tool = tool
                break

        assert export_tool is not None

        # Test the tool function
        result = await export_tool(include_metrics=True)
        insights.export_data.assert_called_once_with(True)
        assert result == {"exported_data": "success"}

    @pytest.mark.asyncio
    async def test_export_analytics_tool_error_handling(self):
        """Test export analytics tool error handling."""
        insights = Mock()
        insights.export_data.side_effect = PermissionError("Access denied")

        # Create a mock server to capture the tool functions
        captured_tools = []
        
        def mock_add_tool(func):
            captured_tools.append(func)
        
        server = Mock()
        server.add_tool = mock_add_tool

        _add_analytics_tools(server, None, insights)

        # Find the export tool
        export_tool = None
        for tool in captured_tools:
            if hasattr(tool, '__name__') and 'export_analytics_data' in tool.__name__:
                export_tool = tool
                break

        assert export_tool is not None

        # Test error handling
        result = await export_tool(include_metrics=False)
        assert "error" in result
        assert "Access denied" in result["error"]


@pytest.mark.unit
class TestServerComposition:
    """Test server composition and distributed systems."""

    @pytest.mark.asyncio
    async def test_compose_feedback_services_success(self):
        """Test successful service composition."""
        main_server = Mock()
        main_server.import_server = Mock()

        services = {
            "service1": {
                "database_url": "sqlite:///service1.db",
                "type": "submission"
            },
            "service2": {
                "database_url": "sqlite:///service2.db", 
                "type": "management"
            },
            "service3": {
                "database_url": "sqlite:///service3.db",
                "type": "full"
            }
        }

        with patch('fastmcp_feedback.feedback.create_submission_server') as mock_submission, \
             patch('fastmcp_feedback.feedback.create_management_server') as mock_management, \
             patch('fastmcp_feedback.feedback.create_feedback_server') as mock_feedback:

            mock_submission.return_value = Mock(name="SubmissionServer")
            mock_management.return_value = Mock(name="ManagementServer")
            mock_feedback.return_value = Mock(name="FeedbackServer")

            compose_feedback_services(main_server, services)

            # Verify all servers were created and imported
            mock_submission.assert_called_once()
            mock_management.assert_called_once()
            mock_feedback.assert_called_once()
            assert main_server.import_server.call_count == 3

    @pytest.mark.asyncio
    async def test_compose_feedback_services_with_shared_insights(self):
        """Test service composition with shared insights."""
        main_server = Mock()
        main_server.import_server = Mock()
        shared_insights = Mock()

        services = {
            "test_service": {
                "database_url": "sqlite:///test.db",
                "type": "submission"
            }
        }

        with patch('fastmcp_feedback.feedback.create_submission_server') as mock_submission:
            mock_submission.return_value = Mock()

            compose_feedback_services(main_server, services, shared_insights)

            # Verify shared insights was passed
            mock_submission.assert_called_once()
            call_args = mock_submission.call_args[0]
            assert call_args[2] == shared_insights  # Third argument is insights

    @pytest.mark.asyncio
    async def test_compose_feedback_services_error_handling(self):
        """Test error handling in service composition."""
        main_server = Mock()
        services = {"bad_service": {"database_url": "invalid://url"}}

        with patch('fastmcp_feedback.feedback.create_feedback_server', side_effect=RuntimeError("Server creation failed")):
            with pytest.raises(RuntimeError, match="Server creation failed"):
                compose_feedback_services(main_server, services)

    @pytest.mark.asyncio
    async def test_create_distributed_feedback_system_success(self):
        """Test successful distributed system creation."""
        services = {
            "submission": {
                "database_url": "sqlite:///submission.db",
                "type": "submission"
            },
            "analytics": {
                "database_url": "sqlite:///analytics.db",
                "type": "analytics",
                "enable_insights": False,
                "retention_days": 30
            },
            "management": {
                "database_url": "sqlite:///management.db",
                "type": "management"
            },
            "full": {
                "database_url": "sqlite:///full.db",
                "type": "full"
            }
        }

        with patch('fastmcp_feedback.feedback.create_submission_server') as mock_submission, \
             patch('fastmcp_feedback.feedback.create_analytics_server') as mock_analytics, \
             patch('fastmcp_feedback.feedback.create_management_server') as mock_management, \
             patch('fastmcp_feedback.feedback.create_feedback_server') as mock_feedback:

            mock_submission.return_value = Mock(name="SubmissionServer")
            mock_analytics.return_value = Mock(name="AnalyticsServer")
            mock_management.return_value = Mock(name="ManagementServer")
            mock_feedback.return_value = Mock(name="FeedbackServer")

            result = create_distributed_feedback_system(services)

            # Verify all servers were created
            assert len(result) == 4
            assert "submission" in result
            assert "analytics" in result
            assert "management" in result
            assert "full" in result

            # Verify analytics server was called with custom config
            mock_analytics.assert_called_once_with(
                "analytics Analytics Service",
                "sqlite:///analytics.db",
                False,  # enable_insights
                30      # retention_days
            )

    @pytest.mark.asyncio
    async def test_create_distributed_feedback_system_with_shared_insights(self):
        """Test distributed system creation with shared insights."""
        services = {"test": {"database_url": "sqlite:///test.db"}}
        shared_insights = Mock()

        with patch('fastmcp_feedback.feedback.create_feedback_server') as mock_feedback:
            mock_feedback.return_value = Mock()

            result = create_distributed_feedback_system(services, shared_insights)

            # Verify shared insights was used
            mock_feedback.assert_called_once()
            call_args = mock_feedback.call_args[0]
            assert call_args[2] == shared_insights

    @pytest.mark.asyncio
    async def test_create_distributed_feedback_system_error_handling(self):
        """Test error handling in distributed system creation."""
        services = {"failing_service": {"database_url": "invalid://url"}}

        with patch('fastmcp_feedback.feedback.create_feedback_server', side_effect=ConnectionError("Connection failed")):
            with pytest.raises(ConnectionError, match="Connection failed"):
                create_distributed_feedback_system(services)


@pytest.mark.unit
class TestServerHealthMonitoring:
    """Test server health monitoring functions."""

    def test_get_server_health_success(self):
        """Test successful server health check."""
        server = Mock()
        server.name = "Test Server"

        result = get_server_health(server)

        assert result["server_name"] == "Test Server"
        assert result["status"] == "healthy"
        assert result["message"] == "Feedback server is healthy"

    def test_get_server_health_error_handling(self):
        """Test server health check with errors."""
        # Create a server that will trigger an exception in the try block 
        # but allow getattr to work in the except block
        class ProblematicServer:
            def __init__(self):
                self._name = "Crashed Server"
                self._access_count = 0
            
            @property 
            def name(self):
                self._access_count += 1
                if self._access_count == 1:  # First access in try block
                    raise RuntimeError("Server crashed")
                return self._name  # Second access via getattr works
        
        server = ProblematicServer()
        result = get_server_health(server)

        # The function should catch the exception and return error status
        assert result["status"] == "unhealthy"
        assert "error" in result
        assert "Server crashed" in result["error"]
        assert result["server_name"] == "Crashed Server"

    def test_get_server_health_unknown_server(self):
        """Test health check for server without name."""
        server = Mock(spec=[])  # Empty spec means no attributes

        result = get_server_health(server)

        # Should handle missing name gracefully
        assert result["server_name"] == "unknown"
        assert result["status"] == "unhealthy"

    def test_monitor_feedback_servers_all_healthy(self):
        """Test monitoring multiple healthy servers."""
        servers = {
            "server1": Mock(name="Server1"),
            "server2": Mock(name="Server2")
        }

        with patch('fastmcp_feedback.feedback.get_server_health') as mock_health:
            mock_health.side_effect = [
                {"server_name": "server1", "status": "healthy", "total_tools": 5},
                {"server_name": "server2", "status": "healthy", "total_tools": 3}
            ]

            result = monitor_feedback_servers(servers)

            assert result["overall_status"] == "healthy"
            assert result["summary"]["total_servers"] == 2
            assert result["summary"]["healthy_servers"] == 2
            assert result["summary"]["unhealthy_servers"] == 0
            assert result["summary"]["total_tools"] == 8

    def test_monitor_feedback_servers_mixed_health(self):
        """Test monitoring servers with mixed health status."""
        servers = {
            "healthy_server": Mock(),
            "unhealthy_server": Mock()
        }

        with patch('fastmcp_feedback.feedback.get_server_health') as mock_health:
            mock_health.side_effect = [
                {"server_name": "healthy_server", "status": "healthy", "total_tools": 4},
                {"server_name": "unhealthy_server", "status": "unhealthy", "error": "Connection lost"}
            ]

            result = monitor_feedback_servers(servers)

            assert result["overall_status"] == "degraded"
            assert result["summary"]["total_servers"] == 2
            assert result["summary"]["healthy_servers"] == 1
            assert result["summary"]["unhealthy_servers"] == 1
            assert result["summary"]["total_tools"] == 4

    def test_monitor_feedback_servers_empty(self):
        """Test monitoring with no servers."""
        result = monitor_feedback_servers({})

        assert result["overall_status"] == "healthy"
        assert result["summary"]["total_servers"] == 0
        assert result["summary"]["healthy_servers"] == 0
        assert result["summary"]["unhealthy_servers"] == 0
        assert result["summary"]["total_tools"] == 0


@pytest.mark.unit
class TestConfigurationHelpers:
    """Test configuration and template helper functions."""

    def test_get_server_templates(self):
        """Test server template definitions."""
        templates = get_server_templates()

        # Verify all expected templates exist
        assert "basic" in templates
        assert "submission_only" in templates
        assert "management" in templates
        assert "analytics" in templates

        # Verify template structure
        basic_template = templates["basic"]
        assert "description" in basic_template
        assert "factory" in basic_template
        assert "features" in basic_template
        assert basic_template["factory"] == create_feedback_server

        # Verify analytics template
        analytics_template = templates["analytics"]
        assert analytics_template["factory"] == create_analytics_server
        assert "analytics" in analytics_template["features"]

    def test_validate_server_config_valid(self):
        """Test validation of valid server configuration."""
        config = {
            "name": "Test Server",
            "database_url": "sqlite:///test.db",
            "insights": {
                "enabled": True,
                "retention_days": 30
            }
        }

        result = validate_server_config(config)

        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 0

    def test_validate_server_config_missing_name(self):
        """Test validation with missing server name."""
        config = {}

        result = validate_server_config(config)

        assert result["valid"] is False
        assert "Server name is required" in result["errors"]

    def test_validate_server_config_memory_database_warning(self):
        """Test validation with in-memory database warning."""
        config = {
            "name": "Test Server",
            "database_url": "sqlite:///:memory:"
        }

        result = validate_server_config(config)

        assert result["valid"] is True
        assert any("in-memory database" in warning.lower() for warning in result["warnings"])

    def test_validate_server_config_no_database_url(self):
        """Test validation without database URL."""
        config = {
            "name": "Test Server"
        }

        result = validate_server_config(config)

        assert result["valid"] is True
        assert any("no database url specified" in warning.lower() for warning in result["warnings"])

    def test_validate_server_config_invalid_insights(self):
        """Test validation with invalid insights configuration."""
        config = {
            "name": "Test Server",
            "insights": {
                "enabled": True,
                "retention_days": 0  # Invalid: must be at least 1
            }
        }

        result = validate_server_config(config)

        assert result["valid"] is False
        assert any("retention days must be at least 1" in error.lower() for error in result["errors"])

    def test_validate_server_config_negative_retention_days(self):
        """Test validation with negative retention days."""
        config = {
            "name": "Test Server",
            "insights": {
                "enabled": True,
                "retention_days": -5
            }
        }

        result = validate_server_config(config)

        assert result["valid"] is False
        assert any("retention days must be at least 1" in error.lower() for error in result["errors"])

    def test_validate_server_config_disabled_insights(self):
        """Test validation with disabled insights (should be valid)."""
        config = {
            "name": "Test Server",
            "insights": {
                "enabled": False,
                "retention_days": 0  # Should be ignored when disabled
            }
        }

        result = validate_server_config(config)

        assert result["valid"] is True


@pytest.mark.unit
@pytest.mark.integration
class TestEndToEndServerCreation:
    """Integration tests for complete server creation workflows."""

    @pytest.mark.asyncio
    async def test_full_server_creation_workflow(self, memory_db_url):
        """Test complete server creation and validation workflow."""
        # Test configuration validation
        config = {
            "name": "Integration Test Server",
            "database_url": memory_db_url,
            "insights": {
                "enabled": True,
                "retention_days": 7
            }
        }

        validation_result = validate_server_config(config)
        assert validation_result["valid"]

        # Create server using validated config
        with patch('fastmcp_feedback.feedback.add_feedback_tools'):
            server = create_feedback_server(
                name=config["name"],
                database_url=config["database_url"]
            )

            # Verify server health
            health = get_server_health(server)
            assert health["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_distributed_system_with_health_monitoring(self):
        """Test distributed system creation with health monitoring."""
        services_config = {
            "frontend": {"database_url": "sqlite:///frontend.db", "type": "submission"},
            "backend": {"database_url": "sqlite:///backend.db", "type": "management"},
            "analytics": {"database_url": "sqlite:///analytics.db", "type": "analytics"}
        }

        with patch('fastmcp_feedback.feedback.create_submission_server') as mock_submission, \
             patch('fastmcp_feedback.feedback.create_management_server') as mock_management, \
             patch('fastmcp_feedback.feedback.create_analytics_server') as mock_analytics:

            mock_submission.return_value = Mock(name="FrontendServer")
            mock_management.return_value = Mock(name="BackendServer")
            mock_analytics.return_value = Mock(name="AnalyticsServer")

            # Create distributed system
            servers = create_distributed_feedback_system(services_config)

            # Monitor health of all servers
            health_status = monitor_feedback_servers(servers)

            assert len(servers) == 3
            assert health_status["summary"]["total_servers"] == 3
            assert health_status["overall_status"] == "healthy"

    def test_template_based_server_creation(self):
        """Test server creation using templates."""
        templates = get_server_templates()
        
        # Test creating servers from each template
        for template_name, template_config in templates.items():
            factory_function = template_config["factory"]
            
            # Create appropriate patches based on the factory function
            patches = ['fastmcp_feedback.feedback.add_feedback_tools']
            
            if factory_function in [create_submission_server, create_management_server, create_analytics_server]:
                patches.extend([
                    'fastmcp_feedback.tools.add_submission_tools',
                    'fastmcp_feedback.tools.add_retrieval_tools', 
                    'fastmcp_feedback.tools.add_management_tools',
                    'fastmcp_feedback.feedback._add_analytics_tools'
                ])
            
            # Apply all patches
            with patch('fastmcp_feedback.feedback.add_feedback_tools'), \
                 patch('fastmcp_feedback.tools.add_submission_tools'), \
                 patch('fastmcp_feedback.tools.add_retrieval_tools'), \
                 patch('fastmcp_feedback.tools.add_management_tools'), \
                 patch('fastmcp_feedback.feedback._add_analytics_tools'):
                
                # Create server using template factory
                server = factory_function(f"Template {template_name.title()} Server")
                
                # Verify server was created successfully
                assert isinstance(server, FastMCP)
                assert template_name.title() in server.name or "Server" in server.name