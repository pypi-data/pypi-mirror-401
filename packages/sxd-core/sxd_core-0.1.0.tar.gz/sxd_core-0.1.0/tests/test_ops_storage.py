import pytest
from unittest.mock import patch, MagicMock
from sxd_core.ops.storage import list_videos, list_batches, VideoInfo, BatchInfo


@pytest.fixture
def mock_ch_manager():
    with patch("sxd_core.ops.storage._get_clickhouse_manager") as mock_get:
        mgr = MagicMock()
        mock_get.return_value = mgr
        yield mgr


def test_list_videos(mock_ch_manager):
    mock_ch_manager.list_videos.return_value = [
        {"id": "v1", "status": "COMPLETED", "size_bytes": 100}
    ]

    videos = list_videos()
    assert len(videos) == 1
    assert isinstance(videos[0], VideoInfo)
    assert videos[0].id == "v1"
    assert videos[0].size_bytes == 100
    assert videos[0].status == "COMPLETED"


def test_list_batches(mock_ch_manager):
    mock_ch_manager.list_batches.return_value = [{"id": "b1", "total_videos": 10}]

    batches = list_batches()
    assert len(batches) == 1
    assert isinstance(batches[0], BatchInfo)
    assert batches[0].id == "b1"
    assert batches[0].total_videos == 10
