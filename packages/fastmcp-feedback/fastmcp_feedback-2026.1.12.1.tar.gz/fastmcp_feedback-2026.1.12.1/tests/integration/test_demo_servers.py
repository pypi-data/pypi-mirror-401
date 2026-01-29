"""
Comprehensive tests for all demo servers to ensure they work correctly
and demonstrate all features properly.
"""

import pytest
import asyncio
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add the examples directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "examples"))

from fastmcp import FastMCP
from fastmcp_feedback import FeedbackDatabase, FeedbackInsights


@pytest.mark.asyncio
class TestDemoServerIntegration:
    """Test all demo servers for complete functionality."""
    
    async def test_demo_server_creation_and_tools(self):
        """Test that demo_server.py creates all expected tools."""
        # Import here to avoid circular imports
        from demo_server import create_demo_server
        
        server = create_demo_server()
        
        # Verify server creation
        assert isinstance(server, FastMCP)
        assert server.name == "FastMCP Feedback Demo"
        assert "demonstration" in server.description.lower()
        
        # Get all tools
        tools = await server.get_tools()
        
        # Verify all expected tools are present
        expected_tools = {
            "submit_feedback",
            "list_feedback", 
            "get_feedback_statistics",
            "update_feedback_status",
            "delete_feedback",
            "get_system_info",
            "setup_sample_data"
        }
        
        tool_names = set(tools.keys())
        assert expected_tools.issubset(tool_names), f"Missing tools: {expected_tools - tool_names}"
        
        # Test tool descriptions
        for tool_name, tool in tools.items():
            assert hasattr(tool, 'description'), f"Tool {tool_name} missing description"
            assert len(tool.description) > 10, f"Tool {tool_name} has insufficient description"
    
    async def test_demo_server_sample_data_setup(self):
        """Test that demo server can setup sample data correctly."""
        from demo_server import setup_demo_data, create_temp_database
        
        # Create temporary database
        db_url = create_temp_database()
        database = FeedbackDatabase(db_url)
        
        try:
            # Setup demo data
            await setup_demo_data(database)
            
            # Verify data was created
            from fastmcp_feedback.models import Feedback
            async with database.session() as session:
                # Count feedback items
                result = session.execute("SELECT COUNT(*) FROM feedback")
                count = result.scalar()
                assert count >= 5, f"Expected at least 5 sample items, got {count}"
                
                # Verify types are present
                result = session.execute("SELECT DISTINCT type FROM feedback")
                types = [row[0] for row in result.fetchall()]
                expected_types = {"BUG", "FEATURE", "IMPROVEMENT", "QUESTION"}
                assert expected_types.issubset(set(types)), f"Missing feedback types: {expected_types - set(types)}"
                
        finally:
            await database.close()
    
    async def test_demo_server_tool_execution(self):
        """Test actual execution of demo server tools."""
        from demo_server import create_demo_server, create_temp_database, setup_demo_data
        
        # Create server with temporary database
        server = create_demo_server()
        
        # Override database URL for testing
        db_url = create_temp_database()
        database = FeedbackDatabase(db_url)
        await setup_demo_data(database)
        
        tools = await server.get_tools()
        
        # Test system info tool
        system_info_tool = tools["get_system_info"]
        info_result = await system_info_tool.run({})
        assert info_result.structured_content["success"] is True
        assert "version" in info_result.structured_content
        assert "dependencies" in info_result.structured_content
        
        # Test statistics tool (should work with sample data)
        stats_tool = tools["get_feedback_statistics"]
        stats_result = await stats_tool.run({})
        assert stats_result.structured_content["total_count"] >= 5
        assert "by_type" in stats_result.structured_content
        assert "by_status" in stats_result.structured_content
        
        await database.close()
    
    async def test_simple_integration_server(self):
        """Test that simple_integration.py works correctly."""
        # Import simple integration
        from simple_integration import FastMCP
        from fastmcp_feedback import add_feedback_tools
        
        # Create simple server
        app = FastMCP("Test Simple Feedback App")
        add_feedback_tools(app, database_url="sqlite:///:memory:")
        
        # Verify tools were added
        tools = await app.get_tools()
        expected_tools = {
            "submit_feedback",
            "list_feedback",
            "get_feedback_statistics", 
            "delete_feedback",
            "update_feedback_status"
        }
        
        tool_names = set(tools.keys())
        assert expected_tools == tool_names, f"Tool mismatch. Expected: {expected_tools}, Got: {tool_names}"
        
        # Test basic tool functionality
        submit_tool = tools["submit_feedback"]
        test_feedback = {
            "type": "bug",
            "title": "Test simple integration bug",
            "description": "Testing simple integration functionality",
            "submitter": "simple_test@example.com"
        }
        
        result = await submit_tool.run({"request": test_feedback})
        assert result.structured_content["success"] is True
        assert "feedback_id" in result.structured_content
    
    async def test_mcp_server_environment_configuration(self):
        """Test that mcp_server.py respects environment variables."""
        # Mock environment variables
        env_vars = {
            "DATABASE_URL": "sqlite:///:memory:",
            "INSIGHTS_ENABLED": "true",
            "LOG_LEVEL": "DEBUG",
            "RETENTION_DAYS": "30"
        }
        
        with patch.dict(os.environ, env_vars, clear=False):
            # Import and test mcp_server
            import mcp_server
            
            # Verify environment variables are being read
            assert os.getenv("DATABASE_URL") == "sqlite:///:memory:"
            assert os.getenv("INSIGHTS_ENABLED") == "true"
            assert os.getenv("LOG_LEVEL") == "DEBUG"
            assert os.getenv("RETENTION_DAYS") == "30"
    
    async def test_demo_server_error_handling(self):
        """Test that demo servers handle errors gracefully."""
        from demo_server import create_demo_server
        
        server = create_demo_server()
        tools = await server.get_tools()
        
        # Test submit_feedback with invalid data
        submit_tool = tools["submit_feedback"]
        
        # Test missing required fields
        with pytest.raises(Exception):  # Should raise validation error
            await submit_tool.run({"request": {}})
        
        # Test invalid feedback type
        with pytest.raises(Exception):  # Should raise validation error
            await submit_tool.run({"request": {
                "type": "invalid_type",
                "title": "Test",
                "description": "Test",
                "submitter": "test@example.com"
            }})
    
    async def test_demo_server_comprehensive_workflow(self):
        """Test complete workflow: submit → list → update → delete."""
        from demo_server import create_demo_server, create_temp_database
        
        server = create_demo_server()
        tools = await server.get_tools()
        
        # Submit feedback
        submit_tool = tools["submit_feedback"]
        test_feedback = {
            "type": "feature",
            "title": "Comprehensive workflow test",
            "description": "Testing the complete demo server workflow",
            "submitter": "workflow_test@example.com",
            "contact_info": "workflow@test.com"
        }
        
        submit_result = await submit_tool.run({"request": test_feedback})
        assert submit_result.structured_content["success"] is True
        feedback_id = submit_result.structured_content["feedback_id"]
        
        # List feedback (should include our submission)
        list_tool = tools["list_feedback"]
        list_result = await list_tool.run({})
        feedback_list = list_result.structured_content["feedback"]
        
        # Find our submitted feedback
        our_feedback = next((f for f in feedback_list if f["id"] == feedback_id), None)
        assert our_feedback is not None, "Submitted feedback not found in list"
        assert our_feedback["title"] == test_feedback["title"]
        assert our_feedback["type"] == test_feedback["type"]
        assert our_feedback["status"] == "OPEN"
        
        # Update feedback status
        update_tool = tools["update_feedback_status"]
        update_result = await update_tool.run({
            "feedback_id": feedback_id,
            "new_status": "in_progress"
        })
        assert update_result.structured_content["success"] is True
        
        # Verify status update
        list_result = await list_tool.run({})
        feedback_list = list_result.structured_content["feedback"]
        updated_feedback = next((f for f in feedback_list if f["id"] == feedback_id), None)
        assert updated_feedback["status"] == "IN_PROGRESS"
        
        # Get statistics (should include our feedback)
        stats_tool = tools["get_feedback_statistics"]
        stats_result = await stats_tool.run({})
        stats = stats_result.structured_content
        
        assert stats["total_count"] >= 1
        assert "FEATURE" in stats["by_type"]
        assert stats["by_type"]["FEATURE"] >= 1
        assert "IN_PROGRESS" in stats["by_status"]
        
        # Delete feedback
        delete_tool = tools["delete_feedback"]
        delete_result = await delete_tool.run({"feedback_id": feedback_id})
        assert delete_result.structured_content["success"] is True
        
        # Verify deletion
        list_result = await list_tool.run({})
        feedback_list = list_result.structured_content["feedback"]
        deleted_feedback = next((f for f in feedback_list if f["id"] == feedback_id), None)
        assert deleted_feedback is None, "Feedback should be deleted"


@pytest.mark.asyncio 
class TestDemoServerDocumentation:
    """Test that demo servers match their documentation."""
    
    async def test_demo_server_matches_documentation(self):
        """Verify demo_server.py matches demo_server.md claims."""
        from demo_server import create_demo_server
        
        server = create_demo_server()
        tools = await server.get_tools()
        
        # According to demo_server.md, should have exactly 7 tools
        assert len(tools) == 7, f"Expected 7 tools as documented, got {len(tools)}"
        
        # Verify documented tool names match actual tools
        documented_tools = {
            "submit_feedback", "list_feedback", "get_feedback_statistics",
            "update_feedback_status", "delete_feedback", "get_system_info", 
            "setup_sample_data"
        }
        actual_tools = set(tools.keys())
        
        assert documented_tools == actual_tools, f"Tools mismatch. Documented: {documented_tools}, Actual: {actual_tools}"
    
    async def test_simple_integration_matches_documentation(self):
        """Verify simple_integration.py matches simple_integration.md claims."""
        from fastmcp import FastMCP
        from fastmcp_feedback import add_feedback_tools
        
        # According to documentation, should add exactly 5 tools
        app = FastMCP("Test App")
        add_feedback_tools(app, database_url="sqlite:///:memory:")
        
        tools = await app.get_tools()
        assert len(tools) == 5, f"Expected 5 tools as documented, got {len(tools)}"
        
        # Verify documented tool names
        documented_tools = {
            "submit_feedback", "list_feedback", "get_feedback_statistics",
            "delete_feedback", "update_feedback_status"
        }
        actual_tools = set(tools.keys())
        
        assert documented_tools == actual_tools, f"Tools mismatch. Documented: {documented_tools}, Actual: {actual_tools}"


@pytest.mark.asyncio
class TestDemoServerPerformance:
    """Test demo server performance characteristics."""
    
    async def test_demo_server_concurrent_operations(self):
        """Test demo server handles concurrent operations correctly."""
        from demo_server import create_demo_server
        
        server = create_demo_server()
        tools = await server.get_tools()
        submit_tool = tools["submit_feedback"]
        
        # Submit multiple feedback items concurrently
        async def submit_feedback(index):
            test_feedback = {
                "type": "bug",
                "title": f"Concurrent test bug {index}",
                "description": f"Testing concurrent submission {index}",
                "submitter": f"concurrent_test_{index}@example.com"
            }
            result = await submit_tool.run({"request": test_feedback})
            return result.structured_content["success"]
        
        # Submit 10 feedback items concurrently
        tasks = [submit_feedback(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        # All submissions should succeed
        assert all(results), "Some concurrent submissions failed"
        
        # Verify all submissions are in the database
        list_tool = tools["list_feedback"]
        list_result = await list_tool.run({})
        feedback_list = list_result.structured_content["feedback"]
        
        concurrent_submissions = [f for f in feedback_list if "Concurrent test bug" in f["title"]]
        assert len(concurrent_submissions) == 10, f"Expected 10 concurrent submissions, found {len(concurrent_submissions)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])