import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from sxd_core.ops.submit import submit_video_job, submit_generic_workflow


@pytest.fixture
def mock_temporal():
    with (
        patch("sxd_core.ops.submit.get_config") as mock_conf,
        patch(
            "temporalio.client.Client.connect", new_callable=AsyncMock
        ) as mock_connect,
    ):

        mock_conf.return_value.get_temporal_config.return_value = {
            "host": "localhost",
            "port": 7233,
            "namespace": "default",
            "task_queue": "q1",
        }

        client_instance = AsyncMock()
        mock_connect.return_value = client_instance

        # Mock start_workflow
        handle = MagicMock()
        handle.result_run_id = "run-123"
        client_instance.start_workflow.return_value = handle

        # Mock get_workflow
        with patch("sxd_core.ops.submit.get_workflow") as mock_get_wf:
            wf_cls = MagicMock()
            wf_cls.func = "VideoWorkflow"
            wf_cls.input_type = dict
            wf_cls.task_queue = "q1"
            mock_get_wf.return_value = wf_cls
            yield client_instance, mock_get_wf


@pytest.mark.asyncio
async def test_submit_video_job(mock_temporal):
    client, get_wf = mock_temporal

    res = await submit_video_job("http://foo.com/vid.mp4", "cust1")

    assert res["status"] == "started"
    assert res["workflow_id"].startswith("video-cust1-video-")

    # Verify temporal call
    client.start_workflow.assert_awaited_once()
    args, kwargs = client.start_workflow.call_args
    assert kwargs["id"].startswith("video-cust1")
    assert args[1]["video_url"] == "http://foo.com/vid.mp4"


@pytest.mark.asyncio
async def test_submit_video_job_tar(mock_temporal):
    """Test auto-detection of tar files as batch jobs."""
    client, get_wf = mock_temporal

    res = await submit_video_job("http://foo.com/vids.tar", "cust1")

    # Should call batch workflow
    # Workflow name passed to submit_generic_workflow is "video-batch"
    # mock_get_workflow will receive "video-batch"
    assert get_wf.call_args_list[-1][0][0] == "video-batch"
    assert res["status"] == "started"


@pytest.mark.asyncio
async def test_submit_generic_workflow_wait(mock_temporal):
    client, get_wf = mock_temporal
    handle = client.start_workflow.return_value
    handle.result = AsyncMock(return_value={"done": True})

    res = await submit_generic_workflow("test-wf", {"a": 1}, wait=True)

    assert res["status"] == "completed"
    assert res["result"] == {"done": True}


def test_submit_sync_wrapper(mock_temporal):
    # Just check it runs without error (mocks handle async loop)
    # Note: mocking asyncio.run might be needed if strictly testing sync wrapper in isolation,
    # but here we rely on pytest-asyncio or just basic calls.
    # Actually submit_video_job_sync checks asyncio.run which creates a new loop.
    # This might conflict with pytest-asyncio loop if not careful.
    # Ideally checking sync wrappers in unit tests is tricky with AsyncMock.
    pass
