from unittest.mock import patch, MagicMock
from sxd_core.audit import log_audit_event


@patch("sxd_core.audit.get_clickhouse_manager")
@patch.dict(
    "os.environ",
    {"PYTEST_CURRENT_TEST": "", "SXD_DISABLE_CLICKHOUSE_AUDIT": ""},
    clear=True,
)
def test_log_audit_event_clickhouse(mock_get_ch):
    """Verify log_audit_event calls ClickHouse insert when strict conditions met."""
    mock_ch = MagicMock()
    mock_get_ch.return_value = mock_ch

    log_audit_event(
        actor="user:test",
        action="test.action",
        target="foo",
        status="SUCCESS",
        customer_id="cust1",
        details={"a": 1},
    )

    mock_ch.insert_audit_events.assert_called_once()
    args = mock_ch.insert_audit_events.call_args[0][0]  # List of rows
    row = args[0]
    # Row: [timestamp, actor, action, target, status, env, ip, trace, details_json]
    assert row[1] == "user:test"
    assert row[2] == "test.action"
    assert row[4] == "SUCCESS"
    assert "cust1" in row[8]  # details json
