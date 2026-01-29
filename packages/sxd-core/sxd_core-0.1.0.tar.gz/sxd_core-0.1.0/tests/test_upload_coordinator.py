import pytest
from unittest.mock import patch
from sxd_core.workflows.upload_coordinator import UploadCoordinatorWorkflow


@pytest.mark.asyncio
async def test_upload_coordinator_flow():
    """Test UploadCoordinatorWorkflow logic via mocked workflow module.
    
    Note: Uses workflow module patching since @workflow.defn classes
    require Temporal runtime for proper integration testing.
    """
    assignments_result = {
        "assignments": {"node1": {"files": ["f1"]}, "node2": {"files": ["f2"]}}
    }

    # Capture calls
    activity_calls = []

    async def mock_execute_activity(func, args, **kwargs):
        activity_calls.append((func, args))
        if func.__name__ == "compute_upload_assignments":
            return assignments_result
        return "triggered"

    async def mock_wait_condition(condition):
        # Simulate condition becoming true immediately
        return True

    # Patch workflow module to bypass @workflow.defn runtime requirements
    with patch("sxd_core.workflows.upload_coordinator.workflow") as mock_wf:

        mock_wf.execute_activity = mock_execute_activity
        mock_wf.wait_condition = mock_wait_condition

        wf = UploadCoordinatorWorkflow()
        wf.s_requested = False
        wf.is_completed = (
            True  # Helper to pass wait condition if lambda checked immediately
        )

        req = {
            "session_id": "sess-1",
            "customer_id": "cust-1",
            "files": [],
            "worker_nodes": ["node1"],
        }

        result = await wf.run(req)

        # Verify result
        assert result["status"] == "PROCESSING"
        assert len(result["assignments"]) == 2

        # Verify activities called
        assert len(activity_calls) == 3  # 1 compute + 2 triggers
        assert activity_calls[0][0].__name__ == "compute_upload_assignments"
        assert activity_calls[1][0].__name__ == "trigger_worker_ingest"


def test_upload_coordinator_signal():
    """Test the signal handler coverage."""
    wf = UploadCoordinatorWorkflow()
    assert wf.is_completed is False
    wf.complete_upload()
    assert wf.is_completed is True
