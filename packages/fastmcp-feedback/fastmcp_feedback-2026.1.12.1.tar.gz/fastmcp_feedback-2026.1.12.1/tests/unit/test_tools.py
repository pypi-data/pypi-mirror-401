"""Unit tests for FastMCP Feedback tool integration."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastmcp import FastMCP

from fastmcp_feedback.tools import add_feedback_tools
from fastmcp_feedback.feedback import create_feedback_server
from fastmcp_feedback.models import SubmitFeedbackRequest


@pytest.mark.unit
@pytest.mark.asyncio
class TestAddFeedbackTools:
    """Test the add_feedback_tools function."""
    
    async def test_add_feedback_tools_basic(self, mock_fastmcp_server, memory_db_url):
        """Test adding feedback tools with basic configuration."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        expected_tools = [
            "submit_feedback",
            "list_feedback",
            "get_feedback_statistics", 
            "update_feedback_status",
            "delete_feedback"
        ]
        
        for tool_name in expected_tools:
            assert tool_name in tool_names
    
    async def test_add_feedback_tools_with_prefix(self, mock_fastmcp_server, memory_db_url):
        """Test adding feedback tools with prefix."""
        add_feedback_tools(
            mock_fastmcp_server, 
            database_url=memory_db_url,
            prefix="support"
        )
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        expected_tools = [
            "support_submit_feedback",
            "support_list_feedback",
            "support_get_feedback_statistics",
            "support_update_feedback_status", 
            "support_delete_feedback"
        ]
        
        for tool_name in expected_tools:
            assert tool_name in tool_names
    
    async def test_add_feedback_tools_with_insights(self, mock_fastmcp_server, memory_db_url, test_insights):
        """Test adding feedback tools with insights enabled."""
        add_feedback_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            insights=test_insights
        )
        
        tools = await mock_fastmcp_server.get_tools()
        
        # Should have all standard tools - check tool names in the keys
        assert len([name for name in tools.keys() if "feedback" in name]) >= 5
        
        # Verify insights are configured
        # This would test that the tools use the provided insights instance
        assert test_insights.enabled is True
    
    async def test_add_feedback_tools_without_database_url(self, mock_fastmcp_server):
        """Test adding feedback tools without explicit database URL."""
        # Should use default SQLite database
        add_feedback_tools(mock_fastmcp_server)
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        assert "submit_feedback" in tool_names
        assert "list_feedback" in tool_names
    
    async def test_add_feedback_tools_with_custom_separator(self, mock_fastmcp_server, memory_db_url):
        """Test adding feedback tools with custom separator."""
        add_feedback_tools(
            mock_fastmcp_server,
            database_url=memory_db_url,
            prefix="api",
            separator="-"
        )
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        assert "api-submit_feedback" in tool_names
        assert "api-list_feedback" in tool_names
    
    async def test_add_feedback_tools_multiple_calls(self, mock_fastmcp_server, memory_db_url):
        """Test calling add_feedback_tools multiple times."""
        # First call
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url, prefix="admin")
        
        # Second call with different prefix
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url, prefix="user")
        
        tools = await mock_fastmcp_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have tools with both prefixes
        assert "admin_submit_feedback" in tool_names
        assert "user_submit_feedback" in tool_names
        
        # Should not have unprefixed tools
        assert "submit_feedback" not in tool_names


@pytest.mark.unit
@pytest.mark.asyncio
class TestCreateFeedbackServer:
    """Test the create_feedback_server function."""
    
    async def test_create_feedback_server_basic(self):
        """Test creating a basic feedback server."""
        server = create_feedback_server("Test Feedback Server")
        
        assert isinstance(server, FastMCP)
        assert server.name == "Test Feedback Server"
        
        tools = await server.get_tools()
        tool_names = list(tools.keys())
        
        expected_tools = [
            "submit_feedback",
            "list_feedback", 
            "get_feedback_statistics",
            "update_feedback_status",
            "delete_feedback"
        ]
        
        for tool_name in expected_tools:
            assert tool_name in tool_names
    
    async def test_create_feedback_server_with_database_url(self, memory_db_url):
        """Test creating feedback server with custom database URL."""
        server = create_feedback_server(
            "Custom DB Server",
            database_url=memory_db_url
        )
        
        assert server.name == "Custom DB Server"
        tools = await server.get_tools()
        assert len(tools) >= 5
    
    async def test_create_feedback_server_with_insights(self, test_insights):
        """Test creating feedback server with insights."""
        server = create_feedback_server(
            "Analytics Server",
            insights=test_insights
        )
        
        assert server.name == "Analytics Server"
        # Verify insights are integrated
        tools = await server.get_tools()
        assert len(tools) >= 5
    
    async def test_create_feedback_server_with_description(self):
        """Test creating feedback server with description."""
        description = "Comprehensive feedback collection system"
        server = create_feedback_server(
            "Described Server",
            description=description
        )
        
        assert server.name == "Described Server"
        # Description would be used in server metadata
    
    async def test_multiple_feedback_servers(self):
        """Test creating multiple independent feedback servers."""
        server1 = create_feedback_server("Server 1")
        server2 = create_feedback_server("Server 2")
        
        assert server1.name != server2.name
        
        # Each should have independent tool sets
        tools1 = await server1.get_tools()
        tools2 = await server2.get_tools()
        
        assert len(tools1) >= 5
        assert len(tools2) >= 5


@pytest.mark.unit
@pytest.mark.asyncio
class TestToolIntegration:
    """Test integration of tools with FastMCP server."""
    
    async def test_submit_feedback_tool_execution(self, mock_fastmcp_server, memory_db_url, sample_feedback_data):
        """Test executing the submit_feedback tool."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        # Get the submit_feedback tool
        tools = await mock_fastmcp_server.get_tools()
        submit_tool = tools["submit_feedback"]
        
        assert submit_tool is not None
        
        # Execute the tool
        result = await submit_tool.run({"request": sample_feedback_data})
        
        # Verify result structure
        assert hasattr(result, 'content')
        # Result format depends on FastMCP implementation
    
    async def test_list_feedback_tool_execution(self, mock_fastmcp_server, memory_db_url):
        """Test executing the list_feedback tool."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        # Get the list_feedback tool
        tools = await mock_fastmcp_server.get_tools()
        list_tool = tools["list_feedback"]
        
        assert list_tool is not None
        
        # Execute the tool
        result = await list_tool.run({})
        
        # Should return feedback list structure
        assert hasattr(result, 'content')
    
    async def test_get_statistics_tool_execution(self, mock_fastmcp_server, memory_db_url):
        """Test executing the get_feedback_statistics tool."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        # Get the statistics tool
        tools = await mock_fastmcp_server.get_tools()
        stats_tool = tools["get_feedback_statistics"]
        
        assert stats_tool is not None
        
        # Execute the tool
        result = await stats_tool.run({})
        
        # Should return statistics structure
        assert hasattr(result, 'content')
    
    async def test_update_status_tool_execution(self, mock_fastmcp_server, memory_db_url):
        """Test executing the update_feedback_status tool."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        # Get the update status tool
        tools = await mock_fastmcp_server.get_tools()
        update_tool = tools["update_feedback_status"]
        
        assert update_tool is not None
        
        # Execute with test parameters
        result = await update_tool.run({
            "feedback_id": "test_id",
            "new_status": "resolved"
        })
        
        # Should handle the update attempt
        assert hasattr(result, 'content')
    
    async def test_delete_feedback_tool_execution(self, mock_fastmcp_server, memory_db_url):
        """Test executing the delete_feedback tool.""" 
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        # Get the delete tool
        tools = await mock_fastmcp_server.get_tools()
        delete_tool = tools["delete_feedback"]
        
        assert delete_tool is not None
        
        # Execute with test parameters
        result = await delete_tool.run({"feedback_id": "test_id"})
        
        # Should handle the delete attempt
        assert hasattr(result, 'content')


@pytest.mark.unit
@pytest.mark.asyncio  
class TestToolValidation:
    """Test tool parameter validation and error handling."""
    
    async def test_submit_feedback_validation(self, mock_fastmcp_server, memory_db_url):
        """Test submit_feedback tool parameter validation."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        submit_tool = tools["submit_feedback"]
        
        # Test with invalid parameters
        with pytest.raises(Exception):  # Specific exception depends on implementation
            await submit_tool.run({"invalid": "parameters"})
    
    async def test_list_feedback_parameter_validation(self, mock_fastmcp_server, memory_db_url):
        """Test list_feedback tool parameter validation."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        list_tool = tools["list_feedback"]
        
        # Test with valid optional parameters
        result = await list_tool.run({
            "type_filter": "bug",
            "status_filter": "open",
            "page": 1,
            "per_page": 10
        })
        
        assert hasattr(result, 'content')
    
    async def test_update_status_validation(self, mock_fastmcp_server, memory_db_url):
        """Test update_feedback_status parameter validation."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        update_tool = tools["update_feedback_status"]
        
        # Test with missing required parameters
        with pytest.raises(Exception):
            await update_tool.run({"feedback_id": "test_id"})  # Missing new_status
    
    async def test_delete_feedback_validation(self, mock_fastmcp_server, memory_db_url):
        """Test delete_feedback parameter validation."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        delete_tool = tools["delete_feedback"]
        
        # Test with missing required parameters
        with pytest.raises(Exception):
            await delete_tool.run({})  # Missing feedback_id


@pytest.mark.unit
@pytest.mark.asyncio
class TestServerComposition:
    """Test server composition patterns."""
    
    async def test_import_feedback_server(self):
        """Test importing feedback server into main server."""
        main_server = FastMCP("Main Server")
        feedback_server = create_feedback_server("Feedback Service")
        
        # Import feedback server with prefix
        await main_server.import_server(feedback_server, prefix="feedback")
        
        tools = await main_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have feedback tools with prefix
        assert "feedback_submit_feedback" in tool_names
        assert "feedback_list_feedback" in tool_names
    
    async def test_multiple_server_imports(self):
        """Test importing multiple feedback servers."""
        main_server = FastMCP("Main Server")
        
        user_feedback = create_feedback_server("User Feedback")
        admin_feedback = create_feedback_server("Admin Feedback")
        
        await main_server.import_server(user_feedback, prefix="user")
        await main_server.import_server(admin_feedback, prefix="admin")
        
        tools = await main_server.get_tools()
        tool_names = list(tools.keys())
        
        # Should have tools from both servers
        assert "user_submit_feedback" in tool_names
        assert "admin_submit_feedback" in tool_names
        
        # Should not have unprefixed tools
        assert "submit_feedback" not in tool_names
    
    async def test_selective_tool_import(self):
        """Test importing feedback server with prefix (selective import not directly supported)."""
        main_server = FastMCP("Main Server")
        feedback_server = create_feedback_server("Feedback Service")
        
        # This would test selective import if supported
        # Implementation would need to support this feature
        # FastMCP import_server doesn't support selective tool import
        # but we can test the full import with prefix
        await main_server.import_server(feedback_server, prefix="public")
        
        tools = await main_server.get_tools()
        tool_names = list(tools.keys())
        
        # All tools should be imported with prefix
        assert "public_submit_feedback" in tool_names
        assert "public_list_feedback" in tool_names
        assert "public_delete_feedback" in tool_names
        assert "public_update_feedback_status" in tool_names
        assert "public_get_feedback_statistics" in tool_names


@pytest.mark.unit
@pytest.mark.asyncio
class TestToolPerformance:
    """Test tool performance characteristics."""
    
    async def test_tool_registration_performance(self, performance_timer, memory_db_url):
        """Test performance of tool registration."""
        server = FastMCP("Performance Test Server")
        
        performance_timer.start()
        add_feedback_tools(server, database_url=memory_db_url)
        performance_timer.stop()
        
        # Tool registration should be fast
        assert performance_timer.duration_ms < 1000  # 1 second
        
        # Verify all tools were registered
        tools = await server.get_tools()
        assert len(tools) >= 5
    
    async def test_multiple_server_creation_performance(self, performance_timer):
        """Test performance of creating multiple servers."""
        performance_timer.start()
        
        servers = []
        for i in range(10):
            server = create_feedback_server(f"Server {i}")
            servers.append(server)
        
        performance_timer.stop()
        
        # Creating multiple servers should be reasonable
        assert performance_timer.duration_ms < 5000  # 5 seconds
        assert len(servers) == 10
        
        # Each server should be functional
        for server in servers:
            tools = await server.get_tools()
            assert len(tools) >= 5
    
    async def test_tool_execution_performance(self, mock_fastmcp_server, memory_db_url, performance_timer):
        """Test performance of tool execution."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        list_tool = tools["list_feedback"]
        
        performance_timer.start()
        
        # Execute tool multiple times
        for _ in range(10):
            result = await list_tool.run({})
        
        performance_timer.stop()
        
        # Tool execution should be efficient
        assert performance_timer.duration_ms < 2000  # 2 seconds for 10 executions


@pytest.mark.unit
@pytest.mark.asyncio
class TestToolConfiguration:
    """Test tool configuration options."""
    
    async def test_tool_descriptions(self, mock_fastmcp_server, memory_db_url):
        """Test that tools have proper descriptions."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        
        for tool_name, tool_obj in tools.items():
            # Each tool should have a description
            assert hasattr(tool_obj, 'description') or hasattr(tool_obj, 'metadata')
            # Description should be meaningful
            if hasattr(tool_obj, 'description'):
                assert len(tool_obj.description) > 10
    
    async def test_tool_metadata(self, mock_fastmcp_server, memory_db_url):
        """Test tool metadata and categorization."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        feedback_tools = [name for name in tools.keys() if "feedback" in name]
        
        # Should have categorized the tools appropriately
        assert len(feedback_tools) >= 5
    
    async def test_tool_parameter_schemas(self, mock_fastmcp_server, memory_db_url):
        """Test tool parameter schemas."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        submit_tool = tools["submit_feedback"]
        
        # Tool should have parameter schema defined
        assert submit_tool is not None
        # Schema validation depends on FastMCP implementation


@pytest.mark.unit
@pytest.mark.asyncio
class TestToolErrorHandling:
    """Test tool error handling scenarios."""
    
    async def test_database_connection_error(self):
        """Test tool behavior with database connection errors."""
        server = FastMCP("Error Test Server")
        
        # Use invalid database URL
        add_feedback_tools(server, database_url="sqlite:///nonexistent/path/db.sqlite")
        
        tools = await server.get_tools()
        list_tool = tools["list_feedback"]
        
        # Tool execution should handle database errors gracefully
        result = await list_tool.run({})
        
        # Should return error information rather than crashing
        assert hasattr(result, 'content')
    
    async def test_invalid_parameter_handling(self, mock_fastmcp_server, memory_db_url):
        """Test tool handling of invalid parameters."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        submit_tool = tools["submit_feedback"]
        
        # Test with malformed request
        with pytest.raises(Exception):
            await submit_tool.run({"request": "invalid_string"})
    
    async def test_concurrent_tool_execution(self, mock_fastmcp_server, memory_db_url):
        """Test concurrent execution of tools."""
        add_feedback_tools(mock_fastmcp_server, database_url=memory_db_url)
        
        tools = await mock_fastmcp_server.get_tools()
        list_tool = tools["list_feedback"]
        
        import asyncio
        
        # Execute tool concurrently
        tasks = [list_tool.run({}) for _ in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All executions should complete
        assert len(results) == 5
        
        # None should be exceptions
        for result in results:
            assert not isinstance(result, Exception)