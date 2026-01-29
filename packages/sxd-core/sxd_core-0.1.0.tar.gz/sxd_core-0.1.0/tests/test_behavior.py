from unittest.mock import patch

import pytest
from sxd_core.audit import get_trace_id, log_audit_event, set_trace_id
from sxd_core.data_layer import DataManager


# 1. Behavioral: SSRF Protection
def test_ssrf_blocklist():
    """Verify that DataManager blocks internal/private IP ranges."""
    dm = DataManager()

    # Test cases: (hostname, mock_resolved_ip, expected_to_block)
    test_hosts = [
        ("metadata.internal", "169.254.169.254", True),
        ("localhost", "127.0.0.1", True),
        ("internal.lan", "192.168.1.1", True),
        ("google.com", "8.8.8.8", False),
    ]

    for host, resolved_ip, should_block in test_hosts:
        with patch("socket.gethostbyname", return_value=resolved_ip):
            url = f"http://{host}/data"
            if should_block:
                with pytest.raises(ValueError, match="Security Error"):
                    dm._validate_url(url)
            else:
                # Should not raise
                dm._validate_url(url)


# 2. Behavioral: ClickHouse Metadata Upsert
# Note: Full integration test requires ClickHouse running.
# This test is a placeholder for the migration to ClickHouse-based metadata.
def test_clickhouse_metadata_schema():
    """Verify ClickHouseManager has the expected metadata methods."""
    # Reload to avoid any mock patching from other tests
    import importlib

    import sxd_core.clickhouse as ch_module

    importlib.reload(ch_module)

    ClickHouseManager = ch_module.ClickHouseManager

    # Verify methods exist on the class itself (not instance, to avoid connection)
    assert hasattr(ClickHouseManager, "upsert_video_metadata")
    assert hasattr(ClickHouseManager, "upsert_batch_metadata")

    # Also verify on instance (connection is lazy, so this is safe)
    ch = ClickHouseManager()
    assert callable(ch.upsert_video_metadata)
    assert callable(ch.upsert_batch_metadata)


# 3. Behavioral: Audit Trail Correlation
def test_audit_trace_id_propagation():
    """Verify that trace_id is correctly set and captured in audit logs."""
    from sxd_core.audit import _trace_id_ctx

    test_trace = "workflow_id_123"
    set_trace_id(test_trace)

    assert get_trace_id() == test_trace

    with patch("sxd_core.audit.audit_logger._log") as mock_log:
        log_audit_event("user", "test_action", "target", "SUCCESS")

        # Check the captured structured data
        _, kwargs = mock_log.call_args
        assert kwargs["event_type"] == "audit"
        assert kwargs["trace_id"] == test_trace

    # Cleanup
    _trace_id_ctx.set(None)


# 4. Behavioral: ClickHouse connection is lazy
def test_lazy_clickhouse_connection():
    """Verify ClickHouseManager doesn't connect on init."""
    from sxd_core.clickhouse import ClickHouseManager

    # We pass invalid host but it shouldn't raise on init
    ch = ClickHouseManager(host="invalid-host-12345")
    assert ch.host == "invalid-host-12345"
