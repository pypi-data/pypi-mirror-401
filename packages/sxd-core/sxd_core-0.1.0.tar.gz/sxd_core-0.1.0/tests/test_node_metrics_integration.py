from unittest.mock import patch
from sxd_core.ops.node_metrics import (
    get_all_node_metrics,
    cache_metrics_to_clickhouse,
    get_cached_metrics_from_clickhouse,
    NodeMetrics,
)
from datetime import datetime, timezone


@patch("sxd_core.ops.node_metrics._get_config")
@patch("sxd_core.ops.node_metrics.collect_local_metrics")
@patch("sxd_core.ops.node_metrics.collect_remote_metrics")
def test_get_all_node_metrics(mock_remote, mock_local, mock_config):
    # Setup config
    mock_config.return_value.get_nodes_config.return_value = {
        "node1": {"user": "u1", "port": 22},
        "node2": {"user": "u2", "port": 2222, "cpu_cores": 16},
    }
    mock_config.return_value.get_ssh_key_path.return_value = "/key"

    # Mock implementations
    nm1 = NodeMetrics("node1", 100, 50, 4, 0, 0, datetime.now(timezone.utc))
    nm2 = NodeMetrics("node2", 200, 100, 8, 0, 0, datetime.now(timezone.utc))

    # Simulate node1 is local, node2 is remote
    with patch(
        "sxd_core.ops.node_metrics._is_local_node", side_effect=lambda h: h == "node1"
    ):
        mock_local.return_value = nm1
        mock_remote.return_value = nm2

        # Call
        metrics = get_all_node_metrics(force_refresh=True)

        assert len(metrics) == 2
        assert metrics["node1"] == nm1

        # Check node2 overrides
        assert metrics["node2"].cpu_cores == 16  # Overridden by config
        assert metrics["node2"].hostname == "node2"

        # Verify calls
        mock_local.assert_called_with("node1")
        mock_remote.assert_called_with("node2", 2222, "u2", "/key")


@patch("sxd_core.ops.node_metrics._get_clickhouse_manager")
def test_cache_metrics_to_clickhouse(mock_get_ch):
    mock_ch = mock_get_ch.return_value

    metrics = {"n1": NodeMetrics("n1", 100, 50, 4, 10, 20, datetime.now(timezone.utc))}

    cache_metrics_to_clickhouse(metrics)

    mock_ch.insert_telemetry.assert_called_once()
    rows = mock_ch.insert_telemetry.call_args[0][0]
    assert len(rows) == 5  # 5 metrics per node
    assert rows[0][1] == "node.disk_available"
    assert rows[0][3] == {"node": "n1"}


@patch("sxd_core.ops.node_metrics._get_clickhouse_manager")
def test_get_cached_metrics(mock_get_ch):
    mock_ch = mock_get_ch.return_value
    mock_ch.database = "default"

    # Mock result rows: hostname, metric_name, value, timestamp
    ts = datetime.now(timezone.utc)
    mock_ch.execute_query.return_value = [
        {
            "hostname": "n1",
            "metric_name": "node.disk_total",
            "value": 100,
            "timestamp": ts,
        },
        {
            "hostname": "n1",
            "metric_name": "node.cpu_cores",
            "value": 4,
            "timestamp": ts,
        },
    ]

    metrics = get_cached_metrics_from_clickhouse()

    assert "n1" in metrics
    assert metrics["n1"].disk_total_bytes == 100
    assert metrics["n1"].cpu_cores == 4
    assert metrics["n1"].disk_available_bytes == 0  # Default if missing
