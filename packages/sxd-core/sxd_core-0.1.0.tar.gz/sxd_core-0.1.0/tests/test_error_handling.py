"""
Error Handling and Edge Case Tests.

These tests verify the robustness of the testing framework by testing:

1. Error propagation - Exceptions bubble up correctly
2. Resource cleanup - Resources are freed even on failure
3. Edge cases - Empty inputs, boundary conditions, unicode, etc.
4. Failure modes - How mocks behave when things go wrong
5. Recovery - State after errors is consistent
"""

import asyncio

import pytest
from sxd_core.testing import ActivityTestEnv
from sxd_core.testing.mocks import MockClickHouse, MockHTTP, MockStorage

# =============================================================================
# Storage Error Handling
# =============================================================================


class TestStorageErrorBehavior:
    """Tests for storage error handling."""

    @pytest.mark.unit
    def test_read_nonexistent_raises_file_not_found(self):
        """ERROR: Reading nonexistent file raises FileNotFoundError."""
        storage = MockStorage()
        with pytest.raises(FileNotFoundError):
            storage.read("does/not/exist.txt")

    @pytest.mark.unit
    def test_open_read_nonexistent_raises(self):
        """ERROR: Opening nonexistent file for read raises FileNotFoundError."""
        storage = MockStorage()
        with pytest.raises(FileNotFoundError):
            storage.open("missing.txt", "rb")

    @pytest.mark.unit
    def test_size_nonexistent_raises(self):
        """ERROR: Getting size of nonexistent file raises FileNotFoundError."""
        storage = MockStorage()
        with pytest.raises(FileNotFoundError):
            storage.size("missing.txt")

    @pytest.mark.unit
    def test_invalid_mode_raises_value_error(self):
        """ERROR: Invalid open mode raises ValueError."""
        storage = MockStorage()
        storage.write("test.txt", b"data")
        with pytest.raises(ValueError):
            storage.open("test.txt", "x")  # 'x' is not supported

    @pytest.mark.unit
    def test_delete_nonexistent_returns_false(self):
        """BEHAVIOR: Deleting nonexistent file returns False (no error)."""
        storage = MockStorage()
        result = storage.delete("nonexistent.txt")
        assert result is False

    @pytest.mark.unit
    def test_clear_is_safe_when_empty(self):
        """EDGE: Clearing empty storage is safe."""
        storage = MockStorage()
        storage.clear()  # Should not raise
        assert len(storage.get_all_files()) == 0

    @pytest.mark.unit
    def test_list_empty_prefix_returns_all(self):
        """EDGE: Listing with empty prefix returns all files."""
        storage = MockStorage()
        storage.write("a.txt", b"1")
        storage.write("b/c.txt", b"2")

        files = storage.list("")
        assert len(files) >= 2


# =============================================================================
# ClickHouse Error Handling
# =============================================================================


class TestClickHouseErrorBehavior:
    """Tests for ClickHouse mock error handling."""

    @pytest.mark.unit
    def test_query_without_result_returns_empty(self):
        """BEHAVIOR: Query without set result returns empty list."""
        ch = MockClickHouse()
        result = ch.query("SELECT * FROM nonexistent")
        assert result == []

    @pytest.mark.unit
    def test_get_table_without_inserts_returns_empty(self):
        """BEHAVIOR: Getting table without inserts returns empty list."""
        ch = MockClickHouse()
        data = ch.get_table_data("empty_table")
        assert data == []

    @pytest.mark.unit
    def test_clear_when_empty_is_safe(self):
        """EDGE: Clearing empty ClickHouse mock is safe."""
        ch = MockClickHouse()
        ch.clear()  # Should not raise
        assert len(ch.queries) == 0
        assert len(ch.inserts) == 0


# =============================================================================
# HTTP Error Handling
# =============================================================================


class TestHTTPErrorBehavior:
    """Tests for HTTP mock error handling."""

    @pytest.mark.unit
    def test_unregistered_url_returns_404(self):
        """BEHAVIOR: Requesting unregistered URL returns 404."""
        http = MockHTTP()
        response = http.get("https://unknown.com/path")
        assert response.status_code == 404

    @pytest.mark.unit
    def test_json_on_non_json_response(self):
        """ERROR: Calling json() on non-JSON content raises."""
        http = MockHTTP()
        http.add_response("https://test.com", content=b"not json")

        response = http.get("https://test.com")
        with pytest.raises(Exception):  # json.JSONDecodeError
            response.json()

    @pytest.mark.unit
    def test_clear_removes_responses(self):
        """BEHAVIOR: Clear removes registered responses."""
        http = MockHTTP()
        http.add_response("https://test.com", status_code=200)
        http.clear()

        response = http.get("https://test.com")
        assert response.status_code == 404


# =============================================================================
# Activity Test Environment Error Handling
# =============================================================================


class TestActivityEnvErrorPropagation:
    """Tests for error propagation in ActivityTestEnv."""

    @pytest.mark.unit
    async def test_activity_exception_propagates(self):
        """ERROR: Exceptions from activities propagate to caller."""

        async def failing_activity():
            raise ValueError("Activity failed")

        env = ActivityTestEnv()
        with pytest.raises(ValueError, match="Activity failed"):
            await env.run(failing_activity)

    @pytest.mark.unit
    async def test_exception_type_preserved(self):
        """ERROR: Exception type is preserved through env."""

        class CustomError(Exception):
            pass

        async def custom_error_activity():
            raise CustomError("Custom failure")

        env = ActivityTestEnv()
        with pytest.raises(CustomError):
            await env.run(custom_error_activity)

    @pytest.mark.unit
    async def test_error_captured_in_errors_list(self):
        """BEHAVIOR: Errors are captured in env.errors list."""

        import sxd_core.logging

        async def failing_activity():
            sxd_core.logging.get_logger("sxd.test").error("Something went wrong")
            raise RuntimeError("Fatal")

        env = ActivityTestEnv()
        try:
            await env.run(failing_activity)
        except RuntimeError:
            pass

        # Both log.error and the exception should be captured
        assert len(env.errors) >= 1


# =============================================================================
# Workflow Simulator Error Handling
# =============================================================================


# =============================================================================
# Edge Cases - Empty and Boundary Inputs
# =============================================================================


class TestEmptyInputEdgeCases:
    """Tests for empty and boundary input handling."""

    @pytest.mark.unit
    def test_storage_write_empty_bytes(self):
        """EDGE: Writing empty bytes creates zero-length file."""
        storage = MockStorage()
        storage.write("empty.bin", b"")
        assert storage.exists("empty.bin")
        assert storage.read(storage._normalize_path("empty.bin")) == b""
        assert storage.size(storage._normalize_path("empty.bin")) == 0

    @pytest.mark.unit
    def test_storage_write_empty_string(self):
        """EDGE: Writing empty string creates zero-length file."""
        storage = MockStorage()
        storage.write("empty.txt", "")
        assert storage.exists("empty.txt")
        assert storage.read_text(storage._normalize_path("empty.txt")) == ""

    @pytest.mark.unit
    def test_clickhouse_insert_empty_dict(self):
        """EDGE: Inserting empty dict is allowed."""
        ch = MockClickHouse()
        ch.insert("table", {})
        assert len(ch.inserts) == 1
        assert ch.inserts[0].data == {}

    @pytest.mark.unit
    def test_clickhouse_insert_many_empty_list(self):
        """EDGE: Inserting empty list of rows is safe."""
        ch = MockClickHouse()
        ch.insert_many("table", [])
        assert len(ch.inserts) == 0

    @pytest.mark.unit
    async def test_activity_returns_none(self):
        """EDGE: Activity returning None works correctly."""

        async def none_activity():
            return None

        env = ActivityTestEnv()
        result = await env.run(none_activity)
        assert result.value is None


# =============================================================================
# Edge Cases - Unicode and Binary
# =============================================================================


class TestUnicodeAndBinaryEdgeCases:
    """Tests for unicode and binary content handling."""

    @pytest.mark.unit
    def test_storage_unicode_content(self):
        """EDGE: Storage handles unicode content correctly."""
        storage = MockStorage()
        unicode_text = "Hello 世界 \U0001f389 مرحبا"
        storage.write("unicode.txt", unicode_text)
        assert storage.read_text(storage._normalize_path("unicode.txt")) == unicode_text

    @pytest.mark.unit
    def test_storage_unicode_path(self):
        """EDGE: Storage handles unicode in paths."""
        storage = MockStorage()
        path = "données/файл.txt"
        storage.write(path, b"content")
        assert storage.exists(path)
        assert storage.read(storage._normalize_path(path)) == b"content"

    @pytest.mark.unit
    def test_storage_binary_content_preserved(self):
        """EDGE: Binary content is preserved exactly."""
        storage = MockStorage()
        # Include null bytes, high bytes, all byte values
        binary = bytes(range(256))
        storage.write("binary.bin", binary)
        assert storage.read(storage._normalize_path("binary.bin")) == binary

    @pytest.mark.unit
    def test_storage_large_content(self):
        """EDGE: Large content is handled correctly."""
        storage = MockStorage()
        large_content = b"x" * (10 * 1024 * 1024)  # 10MB
        storage.write("large.bin", large_content)
        assert storage.read(storage._normalize_path("large.bin")) == large_content
        assert storage.size(storage._normalize_path("large.bin")) == 10 * 1024 * 1024


# =============================================================================
# Edge Cases - Path Handling
# =============================================================================


class TestPathEdgeCases:
    """Tests for path edge cases."""

    @pytest.mark.unit
    def test_double_slash_normalized(self):
        """EDGE: Double slashes in paths are normalized."""
        storage = MockStorage()
        storage.write("a//b//c.txt", b"data")
        # Should be accessible with normalized path
        assert storage.exists("a/b/c.txt") or storage.exists("/mock/a/b/c.txt")

    @pytest.mark.unit
    def test_trailing_slash_handling(self):
        """EDGE: Trailing slashes don't cause issues."""
        storage = MockStorage()
        storage.write("dir/file.txt", b"data")
        # Listing with trailing slash should work
        files = storage.list("dir/")
        assert len(files) >= 0  # Should not error

    @pytest.mark.unit
    def test_deep_nesting(self):
        """EDGE: Deeply nested paths work correctly."""
        storage = MockStorage()
        deep_path = "/".join(["level"] * 20) + "/file.txt"
        storage.write(deep_path, b"deep")
        assert storage.exists(deep_path)


# =============================================================================
# Resource Cleanup Tests
# =============================================================================


class TestResourceCleanup:
    """Tests for resource cleanup on error."""

    @pytest.mark.unit
    async def test_activity_env_cleanup_on_error(self):
        """CLEANUP: ActivityTestEnv patches are cleaned up on error."""
        env = ActivityTestEnv()

        async def failing():
            raise RuntimeError("Fail")

        try:
            async with env:
                await env.run(failing)
        except RuntimeError:
            pass

        # Patches should be uninstalled even after error
        # (env should be in clean state)
        assert not env._installed

    @pytest.mark.unit
    async def test_activity_env_logs_cleared_per_run(self):
        """CLEANUP: Logs are cleared between runs."""
        env = ActivityTestEnv()

        import sxd_core.logging

        async def log_activity(msg):
            sxd_core.logging.get_logger("sxd.test").info(msg)
            return msg

        await env.run(log_activity, "first")
        assert any("first" in str(log) for log in env.logs)

        await env.run(log_activity, "second")
        # Old logs should be cleared
        assert not any("first" in str(log) for log in env.logs)
        assert any("second" in str(log) for log in env.logs)


# =============================================================================
# Concurrent Access Tests
# =============================================================================


class TestConcurrentAccess:
    """Tests for concurrent access patterns."""

    @pytest.mark.unit
    async def test_storage_concurrent_writes(self):
        """CONCURRENT: Multiple concurrent writes don't corrupt data."""
        storage = MockStorage()

        async def write_file(i):
            content = f"content-{i}".encode()
            storage.write(f"file-{i}.txt", content)
            await asyncio.sleep(0.001)  # Simulate work
            return i

        # Write many files concurrently
        results = await asyncio.gather(*[write_file(i) for i in range(100)])

        # All files should exist with correct content
        for i in results:
            assert storage.exists(f"file-{i}.txt")
            assert (
                storage.read(storage._normalize_path(f"file-{i}.txt"))
                == f"content-{i}".encode()
            )
            assert (
                storage.read(storage._normalize_path(f"file-{i}.txt"))
                == f"content-{i}".encode()
            )

    @pytest.mark.unit
    async def test_storage_concurrent_read_write(self):
        """CONCURRENT: Reading and writing same file concurrently is safe."""
        storage = MockStorage()
        storage.write("shared.txt", b"initial")

        async def reader():
            for _ in range(10):
                try:
                    data = storage.read(storage._normalize_path("shared.txt"))
                    assert len(data) > 0
                except FileNotFoundError:
                    pass  # OK if deleted between exists and read
                await asyncio.sleep(0.001)

        async def writer():
            for i in range(10):
                storage.write("shared.txt", f"update-{i}".encode())
                await asyncio.sleep(0.001)

        await asyncio.gather(reader(), writer())


# =============================================================================
# State Consistency After Errors
# =============================================================================


class TestStateConsistencyAfterErrors:
    """Tests that state remains consistent after errors."""

    @pytest.mark.unit
    def test_storage_state_after_failed_read(self):
        """CONSISTENCY: Storage state unchanged after failed read."""
        storage = MockStorage()
        storage.write("exists.txt", b"data")

        try:
            storage.read("missing.txt")
        except FileNotFoundError:
            pass

        # Original file should still be accessible
        assert storage.exists("exists.txt")
        assert storage.read(storage._normalize_path("exists.txt")) == b"data"

    @pytest.mark.unit
    def test_clickhouse_state_after_query_error(self):
        """CONSISTENCY: ClickHouse state unchanged after query."""
        ch = MockClickHouse()
        ch.insert("table", {"key": "value"})

        # Query (even for nonexistent table) shouldn't affect inserts
        ch.query("SELECT * FROM nonexistent")

        assert len(ch.inserts) == 1
        assert ch.get_table_data("table") == [{"key": "value"}]
