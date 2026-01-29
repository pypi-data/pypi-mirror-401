"""Integration tests for complete FastMCP Feedback workflows."""

import pytest
import asyncio
from datetime import datetime, timedelta

from fastmcp import FastMCP
from fastmcp_feedback import add_feedback_tools
from fastmcp_feedback.feedback import create_feedback_server
from fastmcp_feedback.models import SubmitFeedbackRequest, FeedbackStatus
from fastmcp_feedback.database import FeedbackDatabase
from fastmcp_feedback.insights import FeedbackInsights


@pytest.mark.integration
@pytest.mark.asyncio
class TestCompleteWorkflow:
    """Test complete feedback submission and management workflow."""
    
    async def test_submit_list_update_workflow(self, memory_db_url):
        """Test complete feedback lifecycle: submit -> list -> update -> verify."""
        # Setup
        server = FastMCP("Workflow Test Server")
        insights = FeedbackInsights(enabled=True)
        add_feedback_tools(server, database_url=memory_db_url, insights=insights)
        
        # Get tools
        tools = await server.get_tools()
        submit_tool = tools["submit_feedback"]
        list_tool = tools["list_feedback"]
        update_tool = tools["update_feedback_status"]
        stats_tool = tools["get_feedback_statistics"]
        
        # 1. Submit feedback
        feedback_request = {
            "type": "bug",
            "title": "Integration test bug report",
            "description": "This is a comprehensive test of the feedback system workflow",
            "submitter": "integration_tester",
            "contact_info": "test@integration.com"
        }
        
        submit_result = await submit_tool.run({"request": feedback_request})
        assert submit_result.structured_content["success"] is True
        feedback_id = submit_result.structured_content["feedback_id"]
        
        # 2. List feedback and verify submission
        list_result = await list_tool.run({})
        feedback_list = list_result.structured_content["feedback"]
        
        assert len(feedback_list) >= 1
        submitted_feedback = next((f for f in feedback_list if f["id"] == feedback_id), None)
        assert submitted_feedback is not None
        assert submitted_feedback["type"] == "bug"
        assert submitted_feedback["status"] == "open"
        assert submitted_feedback["title"] == feedback_request["title"]
        
        # 3. Get statistics and verify counts
        stats_result = await stats_tool.run({})
        stats = stats_result.structured_content
        
        assert stats["total_count"] >= 1
        assert "BUG" in stats["by_type"]
        assert stats["by_type"]["BUG"] >= 1
        assert "OPEN" in stats["by_status"]
        assert stats["by_status"]["OPEN"] >= 1
        
        # 4. Update feedback status
        update_result = await update_tool.run({
            "feedback_id": feedback_id,
            "new_status": "in_progress",
            "note": "Started working on this issue"
        })
        assert update_result.structured_content["success"] is True
        
        # 5. Verify status update
        updated_list_result = await list_tool.run({})
        updated_feedback_list = updated_list_result.structured_content["feedback"]
        
        updated_feedback = next((f for f in updated_feedback_list if f["id"] == feedback_id), None)
        assert updated_feedback is not None
        assert updated_feedback["status"] == "in_progress"
        
        # 6. Update to resolved
        resolve_result = await update_tool.run({
            "feedback_id": feedback_id,
            "new_status": "resolved",
            "note": "Issue has been fixed"
        })
        assert resolve_result.structured_content["success"] is True
        
        # 7. Final verification
        final_stats_result = await stats_tool.run({})
        final_stats = final_stats_result.structured_content
        
        assert "RESOLVED" in final_stats["by_status"]
        assert final_stats["by_status"]["RESOLVED"] >= 1
        
        # 8. Verify insights were recorded
        assert len(insights.get_metrics("feedback_submitted")) >= 1
        assert len(insights.get_metrics("feedback_listed")) >= 2  # Called multiple times
        assert len(insights.get_metrics("feedback_status_updated")) >= 2  # Two updates
    
    async def test_multiple_feedback_types_workflow(self, memory_db_url):
        """Test workflow with multiple feedback types and filtering."""
        server = FastMCP("Multi-Type Test Server")
        add_feedback_tools(server, database_url=memory_db_url)
        
        tools = await server.get_tools()
        submit_tool = tools["submit_feedback"]
        list_tool = tools["list_feedback"]
        
        # Submit different types of feedback
        feedback_types = [
            {
                "type": "bug",
                "title": "Critical bug in login",
                "description": "Users cannot log in",
                "submitter": "user1"
            },
            {
                "type": "feature",
                "title": "Add dark mode",
                "description": "Please add dark mode support",
                "submitter": "user2"
            },
            {
                "type": "improvement",
                "title": "Optimize loading speed",
                "description": "App loads slowly on mobile",
                "submitter": "user3"
            }
        ]
        
        submitted_ids = []
        
        # Submit all feedback
        for feedback_data in feedback_types:
            result = await submit_tool.run({"request": feedback_data})
            assert result.structured_content["success"] is True
            submitted_ids.append(result.structured_content["feedback_id"])
        
        # Test filtering by type
        bug_result = await list_tool.run({"type_filter": "bug"})
        bug_feedback = bug_result.structured_content["feedback"]
        
        assert len(bug_feedback) >= 1
        for feedback in bug_feedback:
            assert feedback["type"] == "bug"
        
        # Test filtering by status (all should be open)
        open_result = await list_tool.run({"status_filter": "open"})
        open_feedback = open_result.structured_content["feedback"]
        
        assert len(open_feedback) >= 3
        for feedback in open_feedback:
            assert feedback["status"] == "open"
        
        # Test pagination
        page1_result = await list_tool.run({"page": 1, "per_page": 2})
        page1_feedback = page1_result.structured_content["feedback"]
        
        assert len(page1_feedback) <= 2
        assert page1_result.structured_content["page"] == 1
        assert page1_result.structured_content["per_page"] == 2
        
        # If there are more than 2 items, test second page
        if page1_result.structured_content["total_count"] > 2:
            page2_result = await list_tool.run({"page": 2, "per_page": 2})
            page2_feedback = page2_result.structured_content["feedback"]
            
            # Pages should have different items
            page1_ids = {f["id"] for f in page1_feedback}
            page2_ids = {f["id"] for f in page2_feedback}
            assert page1_ids.isdisjoint(page2_ids)
    
    async def test_error_handling_workflow(self, memory_db_url):
        """Test workflow error handling scenarios."""
        server = FastMCP("Error Test Server")
        add_feedback_tools(server, database_url=memory_db_url)
        
        tools = await server.get_tools()
        submit_tool = tools["submit_feedback"]
        update_tool = tools["update_feedback_status"]
        delete_tool = tools["delete_feedback"]
        
        # 1. Test invalid feedback submission
        invalid_feedback = {
            "type": "invalid_type",
            "title": "",  # Empty title
            "description": "Test description",
            "submitter": ""  # Empty submitter
        }
        
        with pytest.raises(Exception):  # Should fail validation
            await submit_tool.run({"request": invalid_feedback})
        
        # 2. Test updating non-existent feedback
        update_result = await update_tool.run({
            "feedback_id": "99999",  # Use valid integer format
            "new_status": "resolved"
        })
        assert update_result.structured_content["success"] is False
        assert "not found" in update_result.structured_content["error"].lower()
        
        # 3. Test deleting non-existent feedback
        delete_result = await delete_tool.run({"feedback_id": "99999"})
        assert delete_result.structured_content["success"] is False
        assert "not found" in delete_result.structured_content["error"].lower()
        
        # 4. Test invalid status update
        # First submit valid feedback
        valid_feedback = {
            "type": "bug",
            "title": "Valid feedback for error test",
            "description": "This feedback will be used for error testing",
            "submitter": "error_tester"
        }
        
        submit_result = await submit_tool.run({"request": valid_feedback})
        feedback_id = submit_result.structured_content["feedback_id"]
        
        # Try to update with invalid status
        with pytest.raises(Exception):  # Should fail validation
            await update_tool.run({
                "feedback_id": feedback_id,
                "new_status": "invalid_status"
            })
    
    async def test_concurrent_operations_workflow(self, memory_db_url):
        """Test concurrent operations in the workflow."""
        server = FastMCP("Concurrent Test Server")
        insights = FeedbackInsights(enabled=True)
        add_feedback_tools(server, database_url=memory_db_url, insights=insights)
        
        tools = await server.get_tools()
        submit_tool = tools["submit_feedback"]
        list_tool = tools["list_feedback"]
        
        # Prepare multiple feedback submissions
        feedback_data = [
            {
                "type": "bug",
                "title": f"Concurrent bug report {i}",
                "description": f"This is concurrent bug report number {i}",
                "submitter": f"user_{i}"
            }
            for i in range(10)
        ]
        
        # Submit all feedback concurrently
        submit_tasks = []
        for data in feedback_data:
            task = submit_tool.run({"request": data})
            submit_tasks.append(task)
        
        submit_results = await asyncio.gather(*submit_tasks)
        
        # All submissions should succeed
        for result in submit_results:
            assert result.structured_content["success"] is True
        
        # All feedback IDs should be unique
        feedback_ids = [r.structured_content["feedback_id"] for r in submit_results]
        assert len(set(feedback_ids)) == len(feedback_ids)
        
        # Concurrent list operations
        list_tasks = [list_tool.run({}) for _ in range(5)]
        list_results = await asyncio.gather(*list_tasks)
        
        # All list operations should succeed
        for result in list_results:
            feedback_list = result.structured_content["feedback"]
            assert len(feedback_list) >= 10  # Should see all submitted feedback
        
        # Verify insights recorded all operations
        submit_metrics = insights.get_metrics("feedback_submitted")
        assert len(submit_metrics) >= 10
        
        list_metrics = insights.get_metrics("feedback_listed")
        assert len(list_metrics) >= 5
    
    async def test_bulk_operations_workflow(self, memory_db_url):
        """Test bulk operations workflow."""
        server = FastMCP("Bulk Test Server")
        add_feedback_tools(server, database_url=memory_db_url)
        
        tools = await server.get_tools()
        submit_tool = tools["submit_feedback"]
        list_tool = tools["list_feedback"]
        update_tool = tools["update_feedback_status"]
        
        # Submit bulk feedback
        bulk_feedback = [
            {
                "type": "improvement",
                "title": f"Bulk improvement {i}",
                "description": f"Bulk improvement suggestion number {i}",
                "submitter": f"bulk_user_{i}"
            }
            for i in range(20)
        ]
        
        submitted_ids = []
        
        # Submit all feedback (sequential for reliability)
        for feedback_data in bulk_feedback:
            result = await submit_tool.run({"request": feedback_data})
            assert result.structured_content["success"] is True
            submitted_ids.append(result.structured_content["feedback_id"])
        
        # Verify all were submitted
        list_result = await list_tool.run({})
        total_count = list_result.structured_content["total_count"]
        assert total_count >= 20
        
        # Bulk status updates (update first 10 to in_progress)
        for feedback_id in submitted_ids[:10]:
            update_result = await update_tool.run({
                "feedback_id": feedback_id,
                "new_status": "in_progress"
            })
            assert update_result.structured_content["success"] is True
        
        # Verify status updates
        in_progress_result = await list_tool.run({"status_filter": "in_progress"})
        in_progress_feedback = in_progress_result.structured_content["feedback"]
        assert len(in_progress_feedback) >= 10
        
        # Update remaining to resolved
        for feedback_id in submitted_ids[10:]:
            update_result = await update_tool.run({
                "feedback_id": feedback_id,
                "new_status": "resolved"
            })
            assert update_result.structured_content["success"] is True
        
        # Final verification
        resolved_result = await list_tool.run({"status_filter": "resolved"})
        resolved_feedback = resolved_result.structured_content["feedback"]
        assert len(resolved_feedback) >= 10


@pytest.mark.integration
@pytest.mark.asyncio
class TestServerCompositionWorkflow:
    """Test server composition workflows."""
    
    async def test_dedicated_feedback_server_workflow(self):
        """Test workflow with dedicated feedback server."""
        # Create dedicated feedback server
        feedback_server = create_feedback_server(
            "Dedicated Feedback Service",
            database_url="sqlite:///:memory:"
        )
        
        # Get tools from dedicated server
        tools = await feedback_server.get_tools()
        submit_tool = tools["submit_feedback"]
        list_tool = tools["list_feedback"]
        
        # Test basic workflow
        feedback_data = {
            "type": "feature",
            "title": "Server composition test",
            "description": "Testing dedicated feedback server",
            "submitter": "composition_tester"
        }
        
        submit_result = await submit_tool.run({"request": feedback_data})
        assert submit_result.structured_content["success"] is True
        
        list_result = await list_tool.run({})
        feedback_list = list_result.structured_content["feedback"]
        assert len(feedback_list) >= 1
    
    async def test_multi_server_import_workflow(self):
        """Test workflow with multiple imported feedback servers."""
        # Main server
        main_server = FastMCP("Main Application Server")
        
        # Create specialized feedback servers
        user_feedback = create_feedback_server("User Feedback", database_url="sqlite:///:memory:")
        admin_feedback = create_feedback_server("Admin Feedback", database_url="sqlite:///:memory:")
        
        # Import servers with different prefixes
        await main_server.import_server(user_feedback, prefix="user")
        await main_server.import_server(admin_feedback, prefix="admin")
        
        # Get tools
        tools = await main_server.get_tools()
        
        user_submit = tools["user_submit_feedback"]
        admin_submit = tools["admin_submit_feedback"]
        user_list = tools["user_list_feedback"]
        admin_list = tools["admin_list_feedback"]
        
        # Submit to user feedback
        user_feedback_data = {
            "type": "bug",
            "title": "User reported bug",
            "description": "Bug reported by regular user",
            "submitter": "regular_user"
        }
        
        user_result = await user_submit.run({"request": user_feedback_data})
        assert user_result.structured_content["success"] is True
        
        # Submit to admin feedback
        admin_feedback_data = {
            "type": "improvement",
            "title": "Admin improvement suggestion",
            "description": "Improvement suggested by admin",
            "submitter": "admin_user"
        }
        
        admin_result = await admin_submit.run({"request": admin_feedback_data})
        assert admin_result.structured_content["success"] is True
        
        # Verify isolation - user feedback should only see user submissions
        user_list_result = await user_list.run({})
        user_feedback_list = user_list_result.structured_content["feedback"]
        
        assert len(user_feedback_list) == 1
        assert user_feedback_list[0]["title"] == "User reported bug"
        
        # Admin feedback should only see admin submissions
        admin_list_result = await admin_list.run({})
        admin_feedback_list = admin_list_result.structured_content["feedback"]
        
        assert len(admin_feedback_list) == 1
        assert admin_feedback_list[0]["title"] == "Admin improvement suggestion"
    
    async def test_prefix_isolation_workflow(self, memory_db_url):
        """Test prefix isolation in composed servers."""
        server = FastMCP("Prefix Test Server")
        
        # Add feedback tools with different prefixes
        add_feedback_tools(server, database_url=memory_db_url, prefix="public")
        add_feedback_tools(server, database_url=memory_db_url, prefix="internal")
        
        tools = await server.get_tools()
        
        public_submit = tools["public_submit_feedback"]
        internal_submit = tools["internal_submit_feedback"]
        public_list = tools["public_list_feedback"]
        internal_list = tools["internal_list_feedback"]
        
        # Submit to both systems
        public_data = {
            "type": "feature",
            "title": "Public feature request",
            "description": "Feature requested by public user",
            "submitter": "public_user"
        }
        
        internal_data = {
            "type": "bug",
            "title": "Internal bug report",
            "description": "Bug reported by internal team",
            "submitter": "internal_user"
        }
        
        public_result = await public_submit.run({"request": public_data})
        internal_result = await internal_submit.run({"request": internal_data})
        
        assert public_result.structured_content["success"] is True
        assert internal_result.structured_content["success"] is True
        
        # Both should be accessible through their respective interfaces
        public_list_result = await public_list.run({})
        internal_list_result = await internal_list.run({})
        
        public_feedback = public_list_result.structured_content["feedback"]
        internal_feedback = internal_list_result.structured_content["feedback"]
        
        # Each system should see its own submission (they use separate databases in this test)
        assert len(public_feedback) >= 1  # Should see public submission
        assert len(internal_feedback) >= 1  # Should see internal submission


@pytest.mark.integration
@pytest.mark.asyncio
class TestPerformanceWorkflow:
    """Test performance characteristics in real workflows."""
    
    async def test_high_volume_submission_workflow(self, memory_db_url, performance_timer):
        """Test high-volume feedback submission workflow."""
        server = FastMCP("Performance Test Server")
        insights = FeedbackInsights(enabled=True)
        add_feedback_tools(server, database_url=memory_db_url, insights=insights)
        
        tools = await server.get_tools()
        submit_tool = tools["submit_feedback"]
        list_tool = tools["list_feedback"]
        stats_tool = tools["get_feedback_statistics"]
        
        performance_timer.start()
        
        # Submit 100 feedback items
        feedback_ids = []
        for i in range(100):
            feedback_data = {
                "type": "improvement",
                "title": f"Performance test feedback {i}",
                "description": f"Performance testing feedback item number {i}",
                "submitter": f"perf_user_{i}"
            }
            
            result = await submit_tool.run({"request": feedback_data})
            assert result.structured_content["success"] is True
            feedback_ids.append(result.structured_content["feedback_id"])
        
        performance_timer.stop()
        
        # Should complete in reasonable time
        assert performance_timer.duration_ms < 30000  # 30 seconds
        
        # Verify all were submitted
        list_result = await list_tool.run({})
        total_count = list_result.structured_content["total_count"]
        assert total_count >= 100
        
        # Statistics should reflect all submissions
        stats_result = await stats_tool.run({})
        stats = stats_result.structured_content
        assert stats["total_count"] >= 100
        assert "IMPROVEMENT" in stats["by_type"]
        assert stats["by_type"]["IMPROVEMENT"] >= 100
        
        # Insights should have recorded all submissions
        submit_metrics = insights.get_metrics("feedback_submitted")
        assert len(submit_metrics) >= 100
    
    async def test_complex_filtering_workflow(self, memory_db_url, performance_timer):
        """Test performance with complex filtering operations."""
        server = FastMCP("Filter Performance Server")
        add_feedback_tools(server, database_url=memory_db_url)
        
        tools = await server.get_tools()
        submit_tool = tools["submit_feedback"]
        list_tool = tools["list_feedback"]
        update_tool = tools["update_feedback_status"]
        
        # Submit diverse feedback data
        types = ["bug", "feature", "improvement", "question"]
        statuses = ["open", "in_progress", "resolved", "closed"]
        
        feedback_ids = []
        
        # Create 200 feedback items with varied types and statuses
        for i in range(200):
            feedback_type = types[i % len(types)]
            
            feedback_data = {
                "type": feedback_type,
                "title": f"Filter test {feedback_type} {i}",
                "description": f"Filter test feedback of type {feedback_type}",
                "submitter": f"filter_user_{i}"
            }
            
            result = await submit_tool.run({"request": feedback_data})
            feedback_ids.append(result.structured_content["feedback_id"])
            
            # Update some to different statuses
            if i % 4 == 1:
                await update_tool.run({
                    "feedback_id": result.structured_content["feedback_id"],
                    "new_status": "in_progress"
                })
            elif i % 4 == 2:
                await update_tool.run({
                    "feedback_id": result.structured_content["feedback_id"],
                    "new_status": "resolved"
                })
        
        performance_timer.start()
        
        # Perform various filtering operations
        filtering_operations = [
            {"type_filter": "bug"},
            {"type_filter": "feature"},
            {"status_filter": "open"},
            {"status_filter": "resolved"},
            {"type_filter": "bug", "status_filter": "open"},
            {"page": 1, "per_page": 50},
            {"page": 2, "per_page": 50},
            {"page": 3, "per_page": 50},
        ]
        
        for filter_params in filtering_operations:
            result = await list_tool.run(filter_params)
            feedback_list = result.structured_content["feedback"]
            
            # Verify filtering worked
            if "type_filter" in filter_params:
                for feedback in feedback_list:
                    assert feedback["type"] == filter_params["type_filter"]
            
            if "status_filter" in filter_params:
                for feedback in feedback_list:
                    assert feedback["status"] == filter_params["status_filter"]
        
        performance_timer.stop()
        
        # All filtering operations should complete quickly
        assert performance_timer.duration_ms < 10000  # 10 seconds
    
    async def test_concurrent_mixed_operations_workflow(self, memory_db_url, performance_timer):
        """Test concurrent mixed operations (submit, list, update) performance."""
        server = FastMCP("Concurrent Mixed Server")
        add_feedback_tools(server, database_url=memory_db_url)
        
        tools = await server.get_tools()
        submit_tool = tools["submit_feedback"]
        list_tool = tools["list_feedback"]
        update_tool = tools["update_feedback_status"]
        stats_tool = tools["get_feedback_statistics"]
        
        # First, submit some initial feedback
        initial_ids = []
        for i in range(20):
            feedback_data = {
                "type": "question",
                "title": f"Initial feedback {i}",
                "description": f"Initial feedback for concurrent testing {i}",
                "submitter": f"init_user_{i}"
            }
            
            result = await submit_tool.run({"request": feedback_data})
            initial_ids.append(result.structured_content["feedback_id"])
        
        performance_timer.start()
        
        # Create mixed concurrent operations
        tasks = []
        
        # Submit operations
        for i in range(10):
            feedback_data = {
                "type": "bug",
                "title": f"Concurrent submit {i}",
                "description": f"Concurrent submission {i}",
                "submitter": f"concurrent_user_{i}"
            }
            tasks.append(submit_tool.run({"request": feedback_data}))
        
        # List operations with different filters
        for i in range(5):
            tasks.append(list_tool.run({"type_filter": "question"}))
            tasks.append(list_tool.run({"status_filter": "open"}))
        
        # Update operations
        for feedback_id in initial_ids[:10]:
            tasks.append(update_tool.run({
                "feedback_id": feedback_id,
                "new_status": "in_progress"
            }))
        
        # Statistics operations
        for i in range(3):
            tasks.append(stats_tool.run({}))
        
        # Execute all operations concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        performance_timer.stop()
        
        # Should complete in reasonable time
        assert performance_timer.duration_ms < 15000  # 15 seconds
        
        # Verify no exceptions occurred
        exceptions = [r for r in results if isinstance(r, Exception)]
        assert len(exceptions) == 0, f"Got exceptions: {exceptions}"
        
        # Verify operations succeeded
        submit_results = results[:10]  # First 10 were submits
        for result in submit_results:
            assert result.structured_content["success"] is True