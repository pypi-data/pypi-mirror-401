from unittest.mock import patch

# Import the module to test
from sxd_core.ops.node_metrics import collect_remote_metrics


def test_collect_remote_metrics_success():
    with (
        patch("sxd_core.io.run") as mock_run,
        patch(
            "sxd_core.ops.node_metrics._get_queue_stats_for_node", return_value=(0, 0)
        ),
    ):

        # Mock SSH output: "total available" newline "cpu_count"
        # df -B1 output example: "1000 500"
        # nproc output: "8"
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "1000 500\n8\n"

        metrics = collect_remote_metrics("remote-host")

        assert metrics is not None
        assert metrics.hostname == "remote-host"
        assert metrics.disk_total_bytes == 1000
        assert metrics.disk_available_bytes == 500
        assert metrics.cpu_cores == 8
