import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from sxd_core.ops.temporal import (
    get_workers,
    get_workflow_status,
    cancel_workflow,
    terminate_workflow,
)


@pytest.fixture
def mock_temporal_client():
    with (
        patch("sxd_core.ops.temporal.get_config") as mock_conf,
        patch(
            "temporalio.client.Client.connect", new_callable=AsyncMock
        ) as mock_connect,
        patch("sxd_core.simulation.in_simulation", return_value=False),
    ):

        mock_conf.return_value.get_temporal_config.return_value = {
            "host": "localhost",
            "port": 7233,
            "namespace": "default",
            "task_queue": "q1",
        }

        client = AsyncMock()
        mock_connect.return_value = client
        # get_workflow_handle is synchronous in real client
        client.get_workflow_handle = MagicMock()
        yield client


def test_get_workers(mock_temporal_client):
    # Mock describe_task_queue responses
    wf_desc = MagicMock()
    wf_desc.pollers = [MagicMock(identity="p1", last_access_time=None)]

    act_desc = MagicMock()
    act_desc.pollers = [MagicMock(identity="p2")]

    mock_temporal_client.workflow_service.describe_task_queue.side_effect = [
        wf_desc,
        act_desc,
    ]

    info = get_workers("q1")
    assert info.task_queue == "q1"
    assert len(info.workflow_pollers) == 1
    assert len(info.activity_pollers) == 1
    assert info.workflow_pollers[0].identity == "p1"


def test_get_workflow_status(mock_temporal_client):
    handle = MagicMock()
    mock_temporal_client.get_workflow_handle.return_value = handle

    # Mock describe
    desc = MagicMock()
    desc.status.name = "COMPLETED"
    desc.run_id = "run-1"
    desc.start_time = None
    desc.close_time = None
    handle.describe = AsyncMock(return_value=desc)
    handle.result = AsyncMock(return_value="res")

    status = get_workflow_status("wf-1")
    assert status.workflow_id == "wf-1"
    assert status.status == "COMPLETED"
    assert status.result == "res"


def test_cancel_workflow(mock_temporal_client):
    handle = MagicMock()
    mock_temporal_client.get_workflow_handle.return_value = handle
    handle.cancel = AsyncMock()

    res = cancel_workflow("wf-1")
    assert res is True
    handle.cancel.assert_awaited_once()


def test_terminate_workflow(mock_temporal_client):
    handle = MagicMock()
    mock_temporal_client.get_workflow_handle.return_value = handle
    handle.terminate = AsyncMock()

    res = terminate_workflow("wf-1", reason="foo")
    assert res is True
    handle.terminate.assert_awaited_once_with(reason="foo")
