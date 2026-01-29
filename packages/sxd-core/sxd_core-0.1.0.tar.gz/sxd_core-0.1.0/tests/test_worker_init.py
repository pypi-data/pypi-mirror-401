import pytest
from unittest.mock import MagicMock, patch, AsyncMock

from sxd_core.worker import start_worker


@pytest.mark.asyncio
async def test_start_worker_success():
    # Setup Mocks
    mock_client = MagicMock()
    mock_connect = AsyncMock(return_value=mock_client)
    mock_worker_cls = MagicMock()
    mock_worker_instance = MagicMock()
    mock_worker_instance.run = AsyncMock()
    mock_worker_cls.return_value = mock_worker_instance

    mock_list_wf = MagicMock(
        return_value={"wf1": MagicMock(task_queue="q1", workflow_class="cls1")}
    )
    mock_list_act = MagicMock(return_value={"act1": MagicMock(func="func1")})

    with (
        patch("sxd_core.worker.Client.connect", mock_connect),
        patch("sxd_core.worker.Worker", mock_worker_cls),
        patch("sxd_core.worker.list_workflows", mock_list_wf),
        patch("sxd_core.worker.list_activities", mock_list_act),
        patch("concurrent.futures.ThreadPoolExecutor"),
    ):

        await start_worker(
            worker_count=2,
            temporal_host="localhost",
            temporal_port=7233,
            pipeline_loader=MagicMock(),
        )

        # Verify connect
        mock_connect.assert_called_with("localhost:7233", namespace="default")

        # Verify worker creation
        assert mock_worker_cls.call_count >= 1
        # Should create worker for "q1" and possibly "default" or node-specific if env var set

        # Verify run
        mock_worker_instance.run.assert_called()


@pytest.mark.asyncio
async def test_start_worker_connect_fail():
    with patch(
        "sxd_core.worker.Client.connect", side_effect=Exception("Connection failed")
    ):
        with pytest.raises(Exception):
            await start_worker(1, "host", 1234)
