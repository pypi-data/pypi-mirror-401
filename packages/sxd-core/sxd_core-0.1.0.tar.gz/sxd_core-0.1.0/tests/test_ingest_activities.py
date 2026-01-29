from unittest.mock import MagicMock, patch
from sxd_core.ingest.activities import (
    calculate_checksum,
    discover_and_chunk,
    reassemble_chunks,
    init_episode,
    verify_remote_checksum,
    CHUNK_SIZE,
)


@patch("sxd_core.ingest.activities.io")
@patch("sxd_core.ingest.activities.activity")
def test_calculate_checksum(mock_activity, mock_io):
    mock_io.getsize.return_value = 100
    mock_io.time.return_value = 0
    mock_io.open_file.return_value.__enter__.return_value.read.side_effect = [
        b"data",
        b"",
    ]

    res = calculate_checksum("test_file")

    assert len(res) == 64  # Blake2b digest hex size
    mock_io.open_file.assert_called_with("test_file", "rb")


@patch("sxd_core.ingest.activities.io")
def test_discover_and_chunk_simple(mock_io):
    # Setup
    mock_io.exists.return_value = True
    mock_io.isfile.return_value = True
    mock_io.getsize.return_value = 100  # Small file
    mock_io.link = MagicMock()

    # Mock ClickHouse check
    with patch("sxd_core.ingest.activities._get_completed_chunks", return_value=set()):
        chunks = discover_and_chunk("source.mp4", "ep1")

    assert len(chunks) == 1
    assert chunks[0]["file_name"] == "source.mp4"
    assert chunks[0]["status"] == "pending"


@patch("sxd_core.ingest.activities.io")
def test_discover_and_chunk_split(mock_io):
    # Setup large file
    mock_io.exists.return_value = True
    mock_io.isfile.return_value = True
    mock_io.getsize.return_value = CHUNK_SIZE + 100
    mock_io.run = MagicMock()

    # Mock glob for parts
    mock_io.glob.return_value = ["part.part.00", "part.part.01"]
    mock_io.getsize.side_effect = [
        CHUNK_SIZE + 100,  # Initial check
        CHUNK_SIZE,  # Part 1 check
        100,  # Part 2 check
    ]

    with patch("sxd_core.ingest.activities._get_completed_chunks", return_value=set()):
        chunks = discover_and_chunk("large.mp4", "ep1")

    assert mock_io.run.called  # split command
    assert len(chunks) == 2
    assert chunks[0]["is_part"] is True
    assert chunks[1]["is_part"] is True


@patch("sxd_core.ingest.activities.io")
def test_reassemble_chunks(mock_io):
    mock_io.rglob.return_value = ["p.part.0", "p.part.1"]
    mock_io.getsize.side_effect = [10, 10, 20]
    mock_io.time.return_value = 0
    # Two files, each read once then EOF
    mock_io.open_file.return_value.__enter__.return_value.read.side_effect = [
        b"a",
        b"",
        b"a",
        b"",
    ]

    res = reassemble_chunks("ep1", "orig.mp4", "remote_dir")

    assert "orig.mp4" in res
    assert mock_io.remove.call_count == 2  # Cleanup parts


@patch("sxd_core.clickhouse.ClickHouseManager")
def test_init_episode(MockCH):
    mock_ch = MockCH.return_value
    mock_ch.execute_query.return_value = []  # Episode not exists
    mock_ch.database = "sxd"

    init_episode("ep1", "c1", "src", 100, 1, "node1")

    # Verify cleanup attempt
    mock_ch.execute_query.assert_any_call(
        "ALTER TABLE sxd.chunks DELETE WHERE episode_id = 'ep1'"
    )

    # Verify upsert
    mock_ch.upsert_episode.assert_called_once()
    data = mock_ch.upsert_episode.call_args[0][0]
    assert data["id"] == "ep1"
    assert data["status"] == "UPLOADING"


@patch("sxd_core.ingest.activities.io")
def test_verify_remote_checksum_match(mock_io):
    mock_io.exists.return_value = True
    mock_io.getsize.return_value = 4
    mock_io.time.return_value = 0
    mock_io.open_file.return_value.__enter__.return_value.read.side_effect = [
        b"test",
        b"",
    ]

    import hashlib

    h = hashlib.blake2b(digest_size=32)
    h.update(b"test")
    expected = h.hexdigest()

    res = verify_remote_checksum("path", expected)
    assert res is True


@patch("sxd_core.ingest.activities.io")
def test_verify_remote_checksum_mismatch(mock_io):
    mock_io.exists.return_value = True
    mock_io.getsize.return_value = 4
    mock_io.time.return_value = 0
    mock_io.open_file.return_value.__enter__.return_value.read.side_effect = [
        b"test",
        b"",
    ]

    res = verify_remote_checksum("path", "wrong_hash")
    assert res is False


@patch("sxd_core.ingest.activities.io")
@patch("sxd_core.clickhouse.ClickHouseManager")
@patch("sxd_core.ingest.activities.activity")
def test_transfer_chunk_rsync(mock_activity, MockCH, mock_io):
    mock_ch = MockCH.return_value
    mock_io.time.return_value = 0
    # Mock Popen context manager and communication
    mock_process = MagicMock()
    mock_process.poll.side_effect = [None, 0]  # Run once then finish
    mock_process.communicate.return_value = ("stdout", "")
    mock_process.returncode = 0
    mock_io.Popen.return_value = mock_process

    from sxd_core.ingest.activities import transfer_chunk_rsync

    meta = {
        "episode_id": "ep1",
        "chunk_index": 0,
        "file_name": "f.txt",
        "size_bytes": 100,
        "checksum": "abc",
        "path": "/local/f.txt",
    }
    node_info = {"user": "u", "port": 22}

    remote_path = transfer_chunk_rsync(meta, "node1", node_info)

    assert remote_path == "/home/u/sxd/data/incoming/ep1/f.txt"
    assert mock_io.Popen.called
    assert mock_ch.upsert_chunk.call_count >= 2  # Initial and verifying updates


@patch("sxd_core.ops.node_metrics.get_all_node_metrics")
@patch("sxd_core.ops.node_metrics.cache_metrics_to_clickhouse")
def test_refresh_node_metrics(mock_cache, mock_get):
    mock_get.return_value = {"node1": {}}

    from sxd_core.ingest.activities import refresh_node_metrics

    res = refresh_node_metrics()

    assert res["success"] is True
    assert res["node_count"] == 1
    mock_cache.assert_called_once()
