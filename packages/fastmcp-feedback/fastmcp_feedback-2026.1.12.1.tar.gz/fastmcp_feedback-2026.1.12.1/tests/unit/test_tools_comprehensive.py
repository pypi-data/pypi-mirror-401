"""Comprehensive unit tests for FastMCP Feedback tools.py module.

This test suite targets the uncovered lines in tools.py to boost coverage from 27% to 90%+.
Focuses on error handling, edge cases, and advanced integration patterns.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from fastmcp import FastMCP

from fastmcp_feedback.tools import (
    add_submission_tools,
    add_retrieval_tools, 
    add_management_tools,
    configure_feedback_tools,
    get_tool_info,
    create_multi_tenant_tools,
    create_role_based_tools,
    migrate_tools_to_mixins,
    check_tools_health,
    validate_tool_configuration
)
from fastmcp_feedback.database import FeedbackDatabase
from fastmcp_feedback.insights import FeedbackInsights


@pytest.mark.unit
@pytest.mark.asyncio
class TestSubmissionTools:
    """Test the add_submission_tools function and error scenarios."""
    
    async def test_add_submission_tools_basic(self, mock_fastmcp_server, memory_db_url):
        """Test adding submission tools with basic configuration."""
        add_submission_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have submission-related tools
        assert "submit_feedback" in tool_names
        # Should not have retrieval or management tools
        assert "list_feedback" not in tool_names
        assert "update_feedback_status" not in tool_names
    
    async def test_add_submission_tools_with_prefix(self, mock_fastmcp_server, memory_db_url):
        """Test adding submission tools with prefix."""
        add_submission_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            prefix="user"
        )
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        assert "user_submit_feedback" in tool_names
        assert "submit_feedback" not in tool_names
    
    async def test_add_submission_tools_with_insights(self, mock_fastmcp_server, memory_db_url, test_insights):
        """Test adding submission tools with custom insights."""
        add_submission_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            insights=test_insights
        )
        
        tools = await mock_fastmcp_server.get_tools()
        assert len(tools) > 0
    
    async def test_add_submission_tools_without_database_url(self, mock_fastmcp_server):
        """Test adding submission tools without database URL (uses default)."""
        add_submission_tools(mock_fastmcp_server)
        
        tools = await mock_fastmcp_server.get_tools()
        assert "submit_feedback" in tools
    
    @patch('fastmcp_feedback.tools.FeedbackDatabase')
    async def test_add_submission_tools_database_error(self, mock_db_class, mock_fastmcp_server):
        """Test handling of database initialization errors."""
        mock_db_class.side_effect = Exception("Database connection failed")
        
        with pytest.raises(Exception) as exc_info:
            add_submission_tools(mock_fastmcp_server, database_url="sqlite:///invalid.db")
        
        assert "Database connection failed" in str(exc_info.value)
    
    @patch('fastmcp_feedback.tools.SubmissionMixin')
    async def test_add_submission_tools_mixin_error(self, mock_mixin_class, mock_fastmcp_server, memory_db_url):
        """Test handling of mixin registration errors."""
        mock_mixin = Mock()
        mock_mixin.register_tools.side_effect = Exception("Registration failed")
        mock_mixin_class.return_value = mock_mixin
        
        with pytest.raises(Exception) as exc_info:
            add_submission_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        assert "Registration failed" in str(exc_info.value)
    
    async def test_add_submission_tools_prefix_stripping(self, mock_fastmcp_server, memory_db_url):
        """Test prefix stripping behavior."""
        add_submission_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            prefix="api_"  # With trailing underscore
        )
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should strip trailing underscore
        assert "api_submit_feedback" in tool_names


@pytest.mark.unit
@pytest.mark.asyncio
class TestRetrievalTools:
    """Test the add_retrieval_tools function and error scenarios."""
    
    async def test_add_retrieval_tools_basic(self, mock_fastmcp_server, memory_db_url):
        """Test adding retrieval tools with basic configuration."""
        add_retrieval_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have retrieval-related tools
        assert "list_feedback" in tool_names
        assert "get_feedback_statistics" in tool_names
        # Should not have submission or management tools
        assert "submit_feedback" not in tool_names
        assert "update_feedback_status" not in tool_names
    
    async def test_add_retrieval_tools_with_prefix(self, mock_fastmcp_server, memory_db_url):
        """Test adding retrieval tools with prefix."""
        add_retrieval_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            prefix="public"
        )
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        assert "public_list_feedback" in tool_names
        assert "public_get_feedback_statistics" in tool_names
        assert "list_feedback" not in tool_names
    
    async def test_add_retrieval_tools_with_insights(self, mock_fastmcp_server, memory_db_url, test_insights):
        """Test adding retrieval tools with custom insights."""
        add_retrieval_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            insights=test_insights
        )
        
        tools = await mock_fastmcp_server.get_tools()
        assert len(tools) > 0
    
    async def test_add_retrieval_tools_without_database_url(self, mock_fastmcp_server):
        """Test adding retrieval tools without database URL (uses default)."""
        add_retrieval_tools(mock_fastmcp_server)
        
        tools = await mock_fastmcp_server.get_tools()
        assert "list_feedback" in tools
        assert "get_feedback_statistics" in tools
    
    @patch('fastmcp_feedback.tools.FeedbackDatabase')
    async def test_add_retrieval_tools_database_error(self, mock_db_class, mock_fastmcp_server):
        """Test handling of database initialization errors."""
        mock_db_class.side_effect = Exception("Database connection failed")
        
        with pytest.raises(Exception) as exc_info:
            add_retrieval_tools(mock_fastmcp_server, database_url="sqlite:///invalid.db")
        
        assert "Database connection failed" in str(exc_info.value)
    
    @patch('fastmcp_feedback.tools.RetrievalMixin')
    async def test_add_retrieval_tools_mixin_error(self, mock_mixin_class, mock_fastmcp_server, memory_db_url):
        """Test handling of mixin registration errors."""
        mock_mixin = Mock()
        mock_mixin.register_tools.side_effect = Exception("Registration failed")
        mock_mixin_class.return_value = mock_mixin
        
        with pytest.raises(Exception) as exc_info:
            add_retrieval_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        assert "Registration failed" in str(exc_info.value)


@pytest.mark.unit
@pytest.mark.asyncio
class TestManagementTools:
    """Test the add_management_tools function and error scenarios."""
    
    async def test_add_management_tools_basic(self, mock_fastmcp_server, memory_db_url):
        """Test adding management tools with basic configuration."""
        add_management_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have management-related tools
        assert "update_feedback_status" in tool_names
        assert "delete_feedback" in tool_names
        # Should not have submission or retrieval tools
        assert "submit_feedback" not in tool_names
        assert "list_feedback" not in tool_names
    
    async def test_add_management_tools_with_prefix(self, mock_fastmcp_server, memory_db_url):
        """Test adding management tools with prefix."""
        add_management_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            prefix="admin"
        )
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        assert "admin_update_feedback_status" in tool_names
        assert "admin_delete_feedback" in tool_names
        assert "update_feedback_status" not in tool_names
    
    async def test_add_management_tools_with_insights(self, mock_fastmcp_server, memory_db_url, test_insights):
        """Test adding management tools with custom insights."""
        add_management_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            insights=test_insights
        )
        
        tools = await mock_fastmcp_server.get_tools()
        assert len(tools) > 0
    
    async def test_add_management_tools_without_database_url(self, mock_fastmcp_server):
        """Test adding management tools without database URL (uses default)."""
        add_management_tools(mock_fastmcp_server)
        
        tools = await mock_fastmcp_server.get_tools()
        assert "update_feedback_status" in tools
        assert "delete_feedback" in tools
    
    @patch('fastmcp_feedback.tools.FeedbackDatabase')
    async def test_add_management_tools_database_error(self, mock_db_class, mock_fastmcp_server):
        """Test handling of database initialization errors."""
        mock_db_class.side_effect = Exception("Database connection failed")
        
        with pytest.raises(Exception) as exc_info:
            add_management_tools(mock_fastmcp_server, database_url="sqlite:///invalid.db")
        
        assert "Database connection failed" in str(exc_info.value)
    
    @patch('fastmcp_feedback.tools.ManagementMixin')
    async def test_add_management_tools_mixin_error(self, mock_mixin_class, mock_fastmcp_server, memory_db_url):
        """Test handling of mixin registration errors."""
        mock_mixin = Mock()
        mock_mixin.register_tools.side_effect = Exception("Registration failed")
        mock_mixin_class.return_value = mock_mixin
        
        with pytest.raises(Exception) as exc_info:
            add_management_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        assert "Registration failed" in str(exc_info.value)


@pytest.mark.unit
class TestConfigurationTools:
    """Test configuration and information functions."""
    
    def test_configure_feedback_tools_basic(self):
        """Test basic configuration function."""
        config = configure_feedback_tools()
        
        assert "database_url" in config
        assert config["database_url"] == "sqlite:///:memory:"
        assert "insights" in config
        assert isinstance(config["insights"], FeedbackInsights)
        assert config["insights"].enabled is True
    
    def test_configure_feedback_tools_custom_database(self):
        """Test configuration with custom database URL."""
        config = configure_feedback_tools(database_url="sqlite:///custom.db")
        
        assert config["database_url"] == "sqlite:///custom.db"
        assert isinstance(config["insights"], FeedbackInsights)
    
    def test_configure_feedback_tools_disable_insights(self):
        """Test configuration with insights disabled."""
        config = configure_feedback_tools(enable_insights=False)
        
        assert config["insights"].enabled is False
    
    def test_configure_feedback_tools_custom_retention(self):
        """Test configuration with custom retention period."""
        config = configure_feedback_tools(insights_retention_days=30)
        
        assert config["insights"].retention_days == 30
    
    def test_get_tool_info(self):
        """Test get_tool_info function returns complete information."""
        info = get_tool_info()
        
        assert "available_tools" in info
        assert "mixin_classes" in info
        assert "integration_functions" in info
        assert "supported_databases" in info
        assert "features" in info
        
        # Check specific tools are listed
        assert "submit_feedback" in info["available_tools"]
        assert "list_feedback" in info["available_tools"]
        assert "get_feedback_statistics" in info["available_tools"]
        assert "update_feedback_status" in info["available_tools"]
        assert "delete_feedback" in info["available_tools"]
        
        # Check mixins are listed
        assert "SubmissionMixin" in info["mixin_classes"]
        assert "RetrievalMixin" in info["mixin_classes"]
        assert "ManagementMixin" in info["mixin_classes"]
        
        # Check integration functions
        assert "add_feedback_tools" in info["integration_functions"]
        assert "add_submission_tools" in info["integration_functions"]
        assert "add_retrieval_tools" in info["integration_functions"]
        assert "add_management_tools" in info["integration_functions"]
        
        # Check supported databases
        assert "sqlite" in info["supported_databases"]
        assert "postgresql" in info["supported_databases"]
        
        # Check features
        assert len(info["features"]) > 0


@pytest.mark.unit
@pytest.mark.asyncio
class TestAdvancedIntegrationPatterns:
    """Test advanced integration patterns like multi-tenant and role-based tools."""
    
    async def test_create_multi_tenant_tools_basic(self, mock_fastmcp_server):
        """Test creating multi-tenant tools."""
        tenants = {
            "tenant1": "sqlite:///tenant1.db",
            "tenant2": "sqlite:///tenant2.db"
        }
        
        create_multi_tenant_tools(mock_fastmcp_server, tenants)
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have tools for each tenant with prefixes
        assert "tenant1_submit_feedback" in tool_names
        assert "tenant2_submit_feedback" in tool_names
        assert "tenant1_list_feedback" in tool_names
        assert "tenant2_list_feedback" in tool_names
    
    async def test_create_multi_tenant_tools_with_insights(self, mock_fastmcp_server, test_insights):
        """Test creating multi-tenant tools with shared insights."""
        tenants = {
            "org1": "sqlite:///org1.db",
            "org2": "sqlite:///org2.db"
        }
        
        create_multi_tenant_tools(mock_fastmcp_server, tenants, insights=test_insights)
        
        tools = await mock_fastmcp_server.get_tools()
        assert len(tools) >= 10  # At least 5 tools per tenant
    
    async def test_create_multi_tenant_tools_empty_tenants(self, mock_fastmcp_server):
        """Test creating multi-tenant tools with empty tenants dict."""
        tenants = {}
        
        create_multi_tenant_tools(mock_fastmcp_server, tenants)
        
        tools = await mock_fastmcp_server.get_tools()
        # Should complete without error but not add any tools
        assert len(tools) == 0
    
    @patch('fastmcp_feedback.tools.add_feedback_tools')
    async def test_create_multi_tenant_tools_error(self, mock_add_tools, mock_fastmcp_server):
        """Test handling errors in multi-tenant tool creation."""
        mock_add_tools.side_effect = Exception("Failed to add tools")
        tenants = {"tenant1": "sqlite:///tenant1.db"}
        
        with pytest.raises(Exception) as exc_info:
            create_multi_tenant_tools(mock_fastmcp_server, tenants)
        
        # The error should be re-raised with logging
        assert "Failed to add tools" in str(exc_info.value)
    
    async def test_create_role_based_tools_basic(self, mock_fastmcp_server, memory_db_url):
        """Test creating role-based tools."""
        create_role_based_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have public tools (submission and retrieval)
        assert "public_submit_feedback" in tool_names
        assert "public_list_feedback" in tool_names
        assert "public_get_feedback_statistics" in tool_names
        
        # Should have admin tools (all tools)
        assert "admin_submit_feedback" in tool_names
        assert "admin_list_feedback" in tool_names
        assert "admin_update_feedback_status" in tool_names
        assert "admin_delete_feedback" in tool_names
    
    async def test_create_role_based_tools_with_insights(self, mock_fastmcp_server, memory_db_url, test_insights):
        """Test creating role-based tools with insights."""
        create_role_based_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            insights=test_insights
        )
        
        tools = await mock_fastmcp_server.get_tools()
        assert len(tools) >= 7  # Public + admin tools
    
    async def test_create_role_based_tools_without_database(self, mock_fastmcp_server):
        """Test creating role-based tools without database URL."""
        create_role_based_tools(mock_fastmcp_server)
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        assert "public_submit_feedback" in tool_names
        assert "admin_submit_feedback" in tool_names
    
    @patch('fastmcp_feedback.tools.add_submission_tools')
    async def test_create_role_based_tools_error(self, mock_add_submission, mock_fastmcp_server, memory_db_url):
        """Test handling errors in role-based tool creation."""
        mock_add_submission.side_effect = Exception("Failed to add submission tools")
        
        with pytest.raises(Exception) as exc_info:
            create_role_based_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        # The error should be re-raised with logging
        assert "Failed to add submission tools" in str(exc_info.value)


@pytest.mark.unit
@pytest.mark.asyncio
class TestMigrationHelpers:
    """Test migration and upgrade helper functions."""
    
    async def test_migrate_tools_to_mixins_basic(self, mock_fastmcp_server, memory_db_url):
        """Test migrating from old tools to mixin-based architecture."""
        old_tools = ["old_submit_tool", "old_list_tool"]
        
        # Mock the server to have remove_tool method
        mock_fastmcp_server.remove_tool = Mock()
        
        migrate_tools_to_mixins(
            mock_fastmcp_server,
            old_tools,
            database_url=memory_db_url
        )
        
        # Should have called remove_tool for each old tool
        assert mock_fastmcp_server.remove_tool.call_count == 2
        mock_fastmcp_server.remove_tool.assert_any_call("old_submit_tool")
        mock_fastmcp_server.remove_tool.assert_any_call("old_list_tool")
        
        # Should have new tools added
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        assert "submit_feedback" in tool_names
        assert "list_feedback" in tool_names
    
    async def test_migrate_tools_to_mixins_no_remove_method(self, memory_db_url):
        """Test migration when server doesn't have remove_tool method."""
        # Create a mock server without remove_tool method
        mock_server = Mock()
        mock_server.name = "Test Server"
        # Don't add remove_tool method to the mock
        
        old_tools = ["old_tool"]
        
        migrate_tools_to_mixins(
            mock_server,
            old_tools,
            database_url=memory_db_url
        )
        
        # Should complete without error (just skip the removal part)
        # Since we can't verify tool addition with a basic mock, 
        # the important thing is that no exception was raised
    
    async def test_migrate_tools_to_mixins_with_insights(self, mock_fastmcp_server, memory_db_url, test_insights):
        """Test migration with custom insights."""
        old_tools = ["old_tool"]
        mock_fastmcp_server.remove_tool = Mock()
        
        migrate_tools_to_mixins(
            mock_fastmcp_server,
            old_tools,
            database_url=memory_db_url,
            insights=test_insights
        )
        
        tools = await mock_fastmcp_server.get_tools()
        assert len(tools) >= 5
    
    async def test_migrate_tools_to_mixins_empty_list(self, mock_fastmcp_server, memory_db_url):
        """Test migration with empty old tools list."""
        old_tools = []
        
        migrate_tools_to_mixins(
            mock_fastmcp_server,
            old_tools,
            database_url=memory_db_url
        )
        
        # Should still add new tools
        tools = await mock_fastmcp_server.get_tools()
        assert len(tools) >= 5
    
    @patch('fastmcp_feedback.tools.add_feedback_tools')
    async def test_migrate_tools_to_mixins_error(self, mock_add_tools, mock_fastmcp_server, memory_db_url):
        """Test handling errors during migration."""
        # Create a dummy tool first so removal doesn't fail
        @mock_fastmcp_server.tool(description="Dummy tool for migration test")
        def old_tool():
            return "dummy"
        
        mock_add_tools.side_effect = Exception("Failed to add new tools")
        old_tools = ["old_tool"]
        
        with pytest.raises(Exception) as exc_info:
            migrate_tools_to_mixins(
                mock_fastmcp_server,
                old_tools,
                database_url=memory_db_url
            )
        
        # The original exception should be re-raised after logging
        assert "Failed to add new tools" in str(exc_info.value)


@pytest.mark.unit
class TestHealthAndDiagnostics:
    """Test health check and diagnostic functions."""
    
    def test_check_tools_health_healthy_server(self, mock_fastmcp_server):
        """Test health check with healthy server."""
        health = check_tools_health(mock_fastmcp_server)
        
        assert health["status"] == "healthy"
        assert "server_name" in health
        assert health["server_name"] == "Test Feedback Server"
        assert "message" in health
    
    def test_check_tools_health_server_without_name(self):
        """Test health check with server that doesn't have name attribute."""
        mock_server = Mock(spec=[])  # No name attribute
        
        health = check_tools_health(mock_server)
        
        assert health["status"] == "healthy"
        assert health["server_name"] == "unknown"
    
    @patch('fastmcp_feedback.tools.getattr')
    def test_check_tools_health_exception(self, mock_getattr, mock_fastmcp_server):
        """Test health check when exception occurs."""
        mock_getattr.side_effect = Exception("Health check failed")
        
        health = check_tools_health(mock_fastmcp_server)
        
        assert health["status"] == "unhealthy"
        assert "error" in health
        assert "Health check failed" in health["error"]
    
    def test_validate_tool_configuration_valid_config(self):
        """Test configuration validation with valid config."""
        config = {
            "database_url": "postgresql://user:pass@localhost/db",
            "insights": FeedbackInsights(enabled=True, retention_days=30)
        }
        
        result = validate_tool_configuration(config)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 0
    
    def test_validate_tool_configuration_no_database_url(self):
        """Test configuration validation without database URL."""
        config = {}
        
        result = validate_tool_configuration(config)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 1
        assert "No database URL specified" in result["warnings"][0]
    
    def test_validate_tool_configuration_memory_database(self):
        """Test configuration validation with memory database."""
        config = {
            "database_url": "sqlite:///:memory:"
        }
        
        result = validate_tool_configuration(config)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 1
        assert "in-memory database" in result["warnings"][0]
    
    def test_validate_tool_configuration_invalid_retention_days(self):
        """Test configuration validation with invalid retention days."""
        # Create insights with minimum retention and then manually set to invalid value
        insights = FeedbackInsights(enabled=True, retention_days=1)
        # Manually set to invalid value to test validation logic
        insights.retention_days = 0
        
        config = {
            "database_url": "sqlite:///test.db",
            "insights": insights
        }
        
        result = validate_tool_configuration(config)
        
        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert "retention days must be at least 1" in result["errors"][0]
    
    def test_validate_tool_configuration_disabled_insights(self):
        """Test configuration validation with disabled insights."""
        insights = FeedbackInsights(enabled=False)
        config = {
            "database_url": "sqlite:///test.db",
            "insights": insights
        }
        
        result = validate_tool_configuration(config)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_tool_configuration_no_insights(self):
        """Test configuration validation without insights."""
        config = {
            "database_url": "sqlite:///test.db"
        }
        
        result = validate_tool_configuration(config)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0


@pytest.mark.unit
class TestErrorHandlingAndEdgeCases:
    """Test comprehensive error handling and edge cases."""
    
    @pytest.mark.asyncio
    @patch('fastmcp_feedback.tools.logger')
    async def test_logging_in_submission_tools(self, mock_logger, mock_fastmcp_server, memory_db_url):
        """Test that logging works correctly in submission tools."""
        add_submission_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        # Should have logged successful addition
        mock_logger.info.assert_called()
        log_calls = mock_logger.info.call_args_list
        assert any("Submission tools added" in str(call) for call in log_calls)
    
    @pytest.mark.asyncio
    @patch('fastmcp_feedback.tools.logger')
    async def test_logging_in_retrieval_tools(self, mock_logger, mock_fastmcp_server, memory_db_url):
        """Test that logging works correctly in retrieval tools."""
        add_retrieval_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        # Should have logged successful addition
        mock_logger.info.assert_called()
        log_calls = mock_logger.info.call_args_list
        assert any("Retrieval tools added" in str(call) for call in log_calls)
    
    @pytest.mark.asyncio
    @patch('fastmcp_feedback.tools.logger')
    async def test_logging_in_management_tools(self, mock_logger, mock_fastmcp_server, memory_db_url):
        """Test that logging works correctly in management tools."""
        add_management_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        # Should have logged successful addition
        mock_logger.info.assert_called()
        log_calls = mock_logger.info.call_args_list
        assert any("Management tools added" in str(call) for call in log_calls)
    
    @patch('fastmcp_feedback.tools.logger')
    def test_logging_in_configure_feedback_tools(self, mock_logger):
        """Test logging in configure_feedback_tools."""
        configure_feedback_tools(
            database_url="sqlite:///test.db",
            enable_insights=True,
            insights_retention_days=60
        )
        
        mock_logger.info.assert_called()
        log_call = mock_logger.info.call_args[0][0]
        assert "Feedback tools configured" in log_call
        assert "db=sqlite:///test.db" in log_call
        assert "insights=True" in log_call
    
    @pytest.mark.asyncio
    @patch('fastmcp_feedback.tools.logger')
    async def test_logging_in_multi_tenant_tools(self, mock_logger, mock_fastmcp_server):
        """Test logging in create_multi_tenant_tools."""
        tenants = {"tenant1": "sqlite:///t1.db", "tenant2": "sqlite:///t2.db"}
        
        create_multi_tenant_tools(mock_fastmcp_server, tenants)
        
        mock_logger.info.assert_called()
        log_call = mock_logger.info.call_args[0][0]
        assert "Multi-tenant feedback tools created" in log_call
        assert "2 tenants" in log_call
    
    @pytest.mark.asyncio
    @patch('fastmcp_feedback.tools.logger')
    async def test_logging_in_role_based_tools(self, mock_logger, mock_fastmcp_server, memory_db_url):
        """Test logging in create_role_based_tools."""
        create_role_based_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        mock_logger.info.assert_called()
        log_calls = mock_logger.info.call_args_list
        assert any("Role-based feedback tools created" in str(call) for call in log_calls)
    
    @pytest.mark.asyncio
    @patch('fastmcp_feedback.tools.logger')
    async def test_logging_in_migration(self, mock_logger, mock_fastmcp_server, memory_db_url):
        """Test logging in migrate_tools_to_mixins."""
        old_tools = ["old_tool1", "old_tool2"]
        mock_fastmcp_server.remove_tool = Mock()
        
        migrate_tools_to_mixins(mock_fastmcp_server, old_tools, database_url=memory_db_url)
        
        mock_logger.info.assert_called()
        log_call = mock_logger.info.call_args[0][0]
        assert "Migrated 2 old tools" in log_call
    
    @pytest.mark.asyncio
    async def test_concurrent_tool_additions(self, memory_db_url):
        """Test adding tools concurrently to different servers."""
        servers = [FastMCP(f"Server {i}") for i in range(3)]
        
        async def add_tools_to_server(server):
            add_submission_tools(server, database_url=memory_db_url)
            add_retrieval_tools(server, database_url=memory_db_url, prefix="public")
            add_management_tools(server, database_url=memory_db_url, prefix="admin")
        
        # Add tools concurrently
        tasks = [add_tools_to_server(server) for server in servers]
        await asyncio.gather(*tasks)
        
        # Verify all servers have tools
        for server in servers:
            tools = await server.get_tools()
            assert "submit_feedback" in tools
            assert "public_list_feedback" in tools
            assert "admin_update_feedback_status" in tools
    
    @pytest.mark.asyncio
    async def test_prefix_edge_cases(self, mock_fastmcp_server, memory_db_url):
        """Test edge cases with prefixes."""
        # Empty prefix
        add_submission_tools(mock_fastmcp_server, database_url=memory_db_url, prefix="")
        
        # Whitespace prefix
        add_retrieval_tools(mock_fastmcp_server, database_url=memory_db_url, prefix="   ")
        
        # Multiple underscores
        add_management_tools(mock_fastmcp_server, database_url=memory_db_url, prefix="admin___")
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should handle edge cases gracefully
        assert "submit_feedback" in tool_names  # Empty prefix
        assert len([name for name in tool_names if "feedback" in name]) > 0
    
    def test_insights_configuration_edge_cases(self):
        """Test edge cases in insights configuration."""
        # Very small retention period
        config = configure_feedback_tools(insights_retention_days=1)
        assert config["insights"].retention_days == 1
        
        # Very large retention period
        config = configure_feedback_tools(insights_retention_days=365000)
        assert config["insights"].retention_days == 365000
        
        # Disabled insights with custom retention
        config = configure_feedback_tools(enable_insights=False, insights_retention_days=30)
        assert config["insights"].enabled is False
        assert config["insights"].retention_days == 30


@pytest.mark.unit
@pytest.mark.asyncio
class TestIntegrationWithExistingTests:
    """Test integration with existing test patterns and ensure compatibility."""
    
    async def test_compatibility_with_existing_add_feedback_tools(self, mock_fastmcp_server, memory_db_url):
        """Test that individual tool functions are compatible with add_feedback_tools."""
        from fastmcp_feedback.tools import add_feedback_tools
        
        # Add individual tools
        add_submission_tools(mock_fastmcp_server, database_url=memory_db_url, prefix="individual")
        
        # Add all tools
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url, prefix="complete")
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have both individual and complete sets
        assert "individual_submit_feedback" in tool_names
        assert "complete_submit_feedback" in tool_names
        assert "complete_list_feedback" in tool_names
        assert "complete_update_feedback_status" in tool_names
    
    async def test_tools_work_with_existing_fixtures(self, mock_fastmcp_server, memory_db_url, test_insights, sample_feedback_data):
        """Test that new tool functions work with existing fixtures."""
        # Use existing fixtures
        add_submission_tools(
            mock_fastmcp_server, 
            database_url=memory_db_url,
            insights=test_insights
        )
        
        tools = await mock_fastmcp_server.get_tools()
        submit_tool = tools["submit_feedback"]
        
        # Should work with existing sample data
        result = await submit_tool.run({"request": sample_feedback_data})
        assert hasattr(result, 'content')
    
    async def test_new_patterns_with_existing_server_composition(self):
        """Test that new patterns work with existing server composition tests."""
        from fastmcp_feedback.feedback import create_feedback_server
        
        main_server = FastMCP("Main Server")
        
        # Create feedback server with individual tools
        feedback_server = create_feedback_server("Individual Tools")
        add_retrieval_tools(feedback_server, prefix="readonly")
        
        # Import with prefix
        await main_server.import_server(feedback_server, prefix="external")
        
        tools = await main_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have properly composed tool names
        assert len([name for name in tool_names if "external" in name]) > 0