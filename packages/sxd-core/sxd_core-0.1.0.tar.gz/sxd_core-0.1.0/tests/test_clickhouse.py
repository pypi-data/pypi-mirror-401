from unittest.mock import MagicMock, patch
from sxd_core.clickhouse import ClickHouseManager


def test_clickhouse_manager_init():
    mgr = ClickHouseManager(host="localhost", port=8123, database="test_db")
    assert mgr.host == "localhost"
    assert mgr.port == 8123
    assert mgr.database == "test_db"


@patch("clickhouse_connect.get_client")
def test_clickhouse_init_db(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mgr = ClickHouseManager()
    mgr.init_db()

    # Verify database and tables were created
    calls = mock_client.command.call_args_list
    assert any("CREATE DATABASE IF NOT EXISTS" in call.args[0] for call in calls)
    assert any("CREATE TABLE IF NOT EXISTS sxd.logs" in call.args[0] for call in calls)
    assert any(
        "CREATE TABLE IF NOT EXISTS sxd.audit_events" in call.args[0] for call in calls
    )
    assert any(
        "CREATE TABLE IF NOT EXISTS sxd.telemetry" in call.args[0] for call in calls
    )


@patch("clickhouse_connect.get_client")
def test_clickhouse_insert(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mgr = ClickHouseManager()
    # Mock property
    with patch.object(ClickHouseManager, "client", mock_client):
        mgr.insert_logs([["2023-01-01", "INFO", "test", "msg", "t1", "j1", "a1", "{}"]])
        mock_client.insert.assert_called_once()
        assert "logs" in mock_client.insert.call_args[0][0]
