import pytest
from unittest.mock import patch
from sxd_core.clickhouse import ClickHouseManager
import json


class TestClickHouseAdvanced:

    @pytest.fixture
    def manager(self):
        with patch("sxd_core.clickhouse.clickhouse_connect.get_client") as mock_client:
            mgr = ClickHouseManager(client_override=mock_client.return_value)
            mgr.database = "sxd"
            yield mgr

    def test_upsert_chunk(self, manager):
        chunk = {
            "episode_id": "ep1",
            "chunk_index": 0,
            "status": "pending",
            "metadata": {"key": "val"},
        }

        manager.upsert_chunk(chunk)

        manager.client.insert.assert_called_once()
        call_args = manager.client.insert.call_args
        # args: (table, rows), kwargs: {column_names: ...}
        args, kwargs = call_args

        table = args[0]
        rows = args[1]
        col_names = kwargs.get("column_names")

        assert table == "sxd.chunks"
        assert rows[0][0] == "ep1"
        assert "episode_id" in col_names

    def test_upsert_episode(self, manager):
        episode = {"id": "ep1", "status": "UPLOADING", "total_size": 100}
        manager.upsert_episode(episode)

        manager.client.insert.assert_called_once()
        args, kwargs = manager.client.insert.call_args
        assert args[0] == "sxd.episodes"
        assert args[1][0][0] == "ep1"

    def test_get_upload_session(self, manager):
        # Mock named_results for execute_query
        assignments = {"node1": {"files": ["f1"]}}
        # execute_query calls named_results()
        manager.client.query.return_value.named_results.return_value = [
            {
                "session_id": "ep1",
                "customer_id": "cust1",
                "node_assignments": json.dumps(assignments),
            }
        ]

        session = manager.get_upload_session("ep1")

        assert session["session_id"] == "ep1"
        assert session["node_assignments"] == assignments

    def test_insert_telemetry(self, manager):
        from datetime import datetime

        now = datetime.now()
        data = [[now, "metric", 1.0, {"tag": "v"}]]

        manager.insert_telemetry(data)

        manager.client.insert.assert_called_once()
        assert manager.client.insert.call_args[0][0] == "sxd.telemetry"

    def test_list_episodes(self, manager):
        # execute_query uses named_results
        manager.client.query.return_value.named_results.return_value = [
            {"id": "ep1", "status": "COMPLETED"}
        ]

        eps = manager.list_episodes(limit=1)

        assert len(eps) == 1
        assert eps[0]["id"] == "ep1"
        query = manager.client.query.call_args[0][0]
        assert "argMax" in query
        assert "LIMIT 1" in query
