import pytest
from unittest.mock import patch
from sxd_core.ops.node_metrics import (
    NodeMetrics,
    collect_local_metrics,
    calculate_node_score,
    select_best_node,
    compute_file_assignments,
)
from datetime import datetime, timezone


@pytest.fixture
def mock_clickhouse():
    with patch("sxd_core.ops.node_metrics._get_clickhouse_manager") as mock_ch:
        mock_ch.return_value.database = "default"
        mock_ch.return_value.execute_query.return_value = []
        yield mock_ch


@pytest.fixture
def mock_io():
    with (
        patch("sxd_core.io.disk_usage") as mock_du,
        patch("sxd_core.io.exists") as mock_exists,
        patch("sxd_core.io.now") as mock_now,
    ):

        mock_du.return_value.total = 1000
        mock_du.return_value.free = 500
        mock_exists.return_value = True
        mock_now.return_value = datetime(2023, 1, 1, tzinfo=timezone.utc)
        yield mock_du


def test_collect_local_metrics(mock_clickhouse, mock_io):
    mock_clickhouse.return_value.execute_query.return_value = [
        {"pending_bytes": 100, "stored_bytes": 200}
    ]

    metrics = collect_local_metrics("local-node")
    assert metrics is not None
    assert metrics.hostname == "local-node"
    assert metrics.disk_total_bytes == 1000
    assert metrics.disk_available_bytes == 500
    assert metrics.pending_queue_bytes == 100
    assert metrics.stored_bytes == 200


def test_calculate_node_score():
    base = NodeMetrics("n1", 1000, 500, 4, 0, 0, datetime.now(timezone.utc))
    all_metrics = {"n1": base}

    score = calculate_node_score(base, all_metrics)
    assert 0 <= score <= 1.0

    # Test preferences
    # Node with full disk should have low score
    full = NodeMetrics("n2", 1000, 0, 4, 0, 0, datetime.now(timezone.utc))
    score_full = calculate_node_score(full, {"n1": base, "n2": full})
    assert score_full < score


def test_select_best_node():
    m1 = NodeMetrics("n1", 1000, 800, 4, 0, 0, datetime.now(timezone.utc))
    m2 = NodeMetrics("n2", 1000, 100, 4, 0, 0, datetime.now(timezone.utc))

    with patch("sxd_core.ops.node_metrics.get_all_node_metrics") as mock_get:
        mock_get.return_value = {"n1": m1, "n2": m2}

        # n1 has more space, should win
        best = select_best_node(["n1", "n2"], episode_size_bytes=50)
        assert best == "n1"

        # Episode too big for n2 (100 avail), n1 (800 avail)
        # 1000 byte episode -> n2 rejected (100 < 1200 needed w/ safety), n1 rejected?
        # 1000 bytes needed -> requires 1200 headroom. n1 has 800.
        best = select_best_node(["n1", "n2"], episode_size_bytes=1000)
        assert best is None


def test_compute_file_assignments():
    m1 = NodeMetrics("n1", 1000, 500, 4, 0, 0, datetime.now(timezone.utc))
    m2 = NodeMetrics("n2", 1000, 500, 4, 0, 0, datetime.now(timezone.utc))

    with patch("sxd_core.ops.node_metrics.get_all_node_metrics") as mock_get:
        mock_get.return_value = {"n1": m1, "n2": m2}

        files = [{"path": "f1", "size": 100}, {"path": "f2", "size": 100}]
        allocations = compute_file_assignments(files, ["n1", "n2"])

        assert len(allocations) == 2
        # Should distribute roughly evenly
        assert len(allocations["n1"].files) == 1
        assert len(allocations["n2"].files) == 1
