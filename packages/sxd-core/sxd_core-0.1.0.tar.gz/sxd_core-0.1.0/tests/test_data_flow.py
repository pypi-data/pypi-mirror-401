"""
Data Flow and State Transition Tests.

These tests verify the correct flow of data through the testing framework:

1. Activity data flow - Input/output data integrity through activities
2. Workflow state transitions - State changes during workflow execution
3. Storage data lifecycle - Data written, read, modified, deleted correctly
4. Logging data flow - Structured data flows to log capture
5. Mock data consistency - Mocks maintain consistent state
6. End-to-end data journeys - Complete data paths through system
"""

import pytest
from sxd_core.testing import ActivityTestEnv
from sxd_core.testing.mocks import MockClickHouse, MockStorage

# =============================================================================
# Activity Data Flow Tests
# =============================================================================


class TestActivityDataFlow:
    """Tests for data flow through activities."""

    @pytest.mark.unit
    async def test_input_data_reaches_activity(self):
        """FLOW: Input arguments reach activity function."""
        received = {}

        async def capture_activity(arg1, arg2, kwarg1=None):
            received["arg1"] = arg1
            received["arg2"] = arg2
            received["kwarg1"] = kwarg1
            return "captured"

        env = ActivityTestEnv()
        await env.run(capture_activity, "first", "second", kwarg1="keyword")

        assert received["arg1"] == "first"
        assert received["arg2"] == "second"
        assert received["kwarg1"] == "keyword"

    @pytest.mark.unit
    async def test_output_data_returned_correctly(self):
        """FLOW: Activity return value is captured correctly."""

        async def producer_activity():
            return {
                "string": "hello",
                "number": 42,
                "nested": {"key": "value"},
                "list": [1, 2, 3],
            }

        env = ActivityTestEnv()
        result = await env.run(producer_activity)

        assert result.value["string"] == "hello"
        assert result.value["number"] == 42
        assert result.value["nested"]["key"] == "value"
        assert result.value["list"] == [1, 2, 3]

    @pytest.mark.unit
    async def test_storage_data_roundtrip(self):
        """FLOW: Data written to storage can be read back."""

        import sxd_core.storage

        async def storage_writer(data):
            sxd_core.storage.get_storage().write("output.json", data.encode())
            return "written"

        async def storage_reader():
            storage = sxd_core.storage.get_storage()
            return storage.read_text(storage._normalize_path("output.json"))

        env = ActivityTestEnv()

        await env.run(storage_writer, '{"key": "value"}')
        result = await env.run(storage_reader)

        assert result.value == '{"key": "value"}'

    @pytest.mark.unit
    async def test_complex_data_structures_preserved(self):
        """FLOW: Complex nested data structures are preserved."""

        async def complex_activity(data):
            # Transform data and return
            return {
                "original": data,
                "transformed": {k: v * 2 for k, v in data.items()},
            }

        env = ActivityTestEnv()
        input_data = {"a": 1, "b": 2, "c": 3}
        result = await env.run(complex_activity, input_data)

        assert result.value["original"] == input_data
        assert result.value["transformed"] == {"a": 2, "b": 4, "c": 6}


# =============================================================================
# Workflow State Transition Tests
# =============================================================================


# =============================================================================
# Storage Data Lifecycle Tests
# =============================================================================


class TestStorageDataLifecycle:
    """Tests for complete data lifecycle in storage."""

    @pytest.mark.unit
    def test_create_read_update_delete_lifecycle(self):
        """LIFECYCLE: Full CRUD lifecycle works correctly."""
        storage = MockStorage()

        # Create
        storage.write("data.txt", b"version1")
        assert storage.exists("data.txt")
        assert storage.read(storage._normalize_path("data.txt")) == b"version1"

        # Update
        storage.write("data.txt", b"version2")
        assert storage.read(storage._normalize_path("data.txt")) == b"version2"

        # Delete
        deleted = storage.delete("data.txt")
        assert deleted is True
        assert not storage.exists("data.txt")

    @pytest.mark.unit
    def test_multiple_files_independent_lifecycle(self):
        """LIFECYCLE: Multiple files have independent lifecycles."""
        storage = MockStorage()

        # Create multiple files
        storage.write("file1.txt", b"content1")
        storage.write("file2.txt", b"content2")
        storage.write("file3.txt", b"content3")

        # Delete one
        storage.delete("file2.txt")

        # Others should be unaffected
        assert storage.exists("file1.txt")
        assert not storage.exists("file2.txt")
        assert storage.exists("file3.txt")
        assert storage.read(storage._normalize_path("file1.txt")) == b"content1"
        assert storage.read(storage._normalize_path("file3.txt")) == b"content3"

    @pytest.mark.unit
    def test_directory_like_structure(self):
        """LIFECYCLE: Directory-like paths work correctly."""
        storage = MockStorage()

        # Create files in "directories"
        storage.write("project/src/main.py", b"code")
        storage.write("project/src/utils.py", b"utils")
        storage.write("project/tests/test_main.py", b"tests")
        storage.write("project/README.md", b"readme")

        # List by prefix
        src_files = storage.list("/mock/project/src")
        assert len(src_files) >= 2

        # Delete a "directory" worth of files
        for f in src_files:
            storage.delete(f)

        # Only tests and readme should remain
        remaining = storage.list("/mock/project")
        # The src files should be gone - check they're not in remaining list
        assert not any("src/main.py" in f for f in remaining)
        assert not any("src/utils.py" in f for f in remaining)

    @pytest.mark.unit
    async def test_activity_storage_lifecycle(self):
        """LIFECYCLE: Storage lifecycle through activity execution."""

        import sxd_core.storage

        async def lifecycle_activity(filename, content):
            storage = sxd_core.storage.get_storage()
            # Create
            storage.write(filename, content.encode())

            # Read
            read_content = storage.read_text(storage._normalize_path(filename))

            # Update
            storage.write(filename, (content + "_updated").encode())

            # Read updated
            updated_content = storage.read_text(storage._normalize_path(filename))

            # Delete
            storage.delete(filename)

            return {
                "created": read_content,
                "updated": updated_content,
                "exists_after_delete": storage.exists(filename),
            }

        env = ActivityTestEnv()
        result = await env.run(lifecycle_activity, "test.txt", "original")

        assert result.value["created"] == "original"
        assert result.value["updated"] == "original_updated"
        assert result.value["exists_after_delete"] is False


# =============================================================================
# Logging Data Flow Tests
# =============================================================================


class TestLoggingDataFlow:
    """Tests for structured logging data flow."""

    @pytest.mark.unit
    async def test_log_messages_captured(self):
        """FLOW: Log messages are captured in env.logs."""

        import sxd_core.logging

        async def logging_activity():
            log = sxd_core.logging.get_logger("sxd.test")
            log.info("Starting process")
            log.debug("Debug details")
            log.warning("Something to note")
            return "done"

        env = ActivityTestEnv()
        await env.run(logging_activity)

        assert len(env.logs) == 3
        assert env.logs[0]["level"] == "INFO"
        assert env.logs[1]["level"] == "DEBUG"
        assert env.logs[2]["level"] == "WARNING"

    @pytest.mark.unit
    async def test_structured_log_data_preserved(self):
        """FLOW: Structured log kwargs are preserved."""

        import sxd_core.logging

        async def structured_log_activity():
            sxd_core.logging.get_logger("sxd.test").info(
                "Processing file",
                filename="video.mp4",
                size_bytes=1024000,
                format="mp4",
            )
            return "done"

        env = ActivityTestEnv()
        await env.run(structured_log_activity)

        log = env.logs[0]
        assert log["filename"] == "video.mp4"
        assert log["size_bytes"] == 1024000
        assert log["format"] == "mp4"

    @pytest.mark.unit
    async def test_error_logs_separate_from_info(self):
        """FLOW: Error logs go to errors list, not logs."""

        import sxd_core.logging

        async def mixed_log_activity():
            log = sxd_core.logging.get_logger("sxd.test")
            log.info("Info message")
            log.error("Error occurred", code=500)
            log.info("Continuing...")
            return "done"

        env = ActivityTestEnv()
        await env.run(mixed_log_activity)

        # Info/debug/warning go to logs
        assert len(env.logs) == 2
        assert all(log["level"] != "ERROR" for log in env.logs)

        # Errors go to errors
        assert len(env.errors) == 1
        assert env.errors[0]["level"] == "ERROR"
        assert env.errors[0]["code"] == 500


# =============================================================================
# Mock Data Consistency Tests
# =============================================================================


class TestMockDataConsistency:
    """Tests for mock data consistency."""

    @pytest.mark.unit
    def test_clickhouse_inserts_accumulate(self):
        """CONSISTENCY: ClickHouse inserts accumulate across calls."""
        ch = MockClickHouse()

        ch.insert("events", {"type": "click", "count": 1})
        ch.insert("events", {"type": "view", "count": 5})
        ch.insert("metrics", {"name": "latency", "value": 100})

        assert len(ch.inserts) == 3
        assert len(ch.get_table_data("events")) == 2
        assert len(ch.get_table_data("metrics")) == 1

    @pytest.mark.unit
    def test_clickhouse_query_results_match_pattern(self):
        """CONSISTENCY: Query results match by pattern correctly."""
        ch = MockClickHouse()

        ch.set_query_result("SELECT.*FROM events", [{"id": 1}, {"id": 2}])
        ch.set_query_result("SELECT.*FROM users", [{"name": "alice"}])

        events = ch.query("SELECT * FROM events WHERE date > '2024-01-01'")
        users = ch.query("SELECT name FROM users")

        assert events == [{"id": 1}, {"id": 2}]
        assert users == [{"name": "alice"}]

    @pytest.mark.unit
    def test_storage_state_isolated_per_instance(self):
        """CONSISTENCY: Each storage instance has isolated state."""
        storage1 = MockStorage()
        storage2 = MockStorage()

        storage1.write("shared.txt", b"from storage1")
        storage2.write("shared.txt", b"from storage2")

        assert storage1.read(storage1._normalize_path("shared.txt")) == b"from storage1"
        assert storage2.read(storage2._normalize_path("shared.txt")) == b"from storage2"


# =============================================================================
# End-to-End Data Journey Tests
# =============================================================================


class TestEndToEndDataJourney:
    """Tests for complete data journeys through the system."""

    @pytest.mark.simulation
    @pytest.mark.unit
    async def test_activity_storage_and_logging_journey(self):
        """E2E: Activity uses storage and logging throughout execution."""

        import sxd_core.logging
        import sxd_core.storage

        async def full_journey_activity(input_file):
            log = sxd_core.logging.get_logger("sxd.test")
            storage = sxd_core.storage.get_storage()
            log.info("Starting processing", file=input_file)

            # Read input
            content = storage.read(storage._normalize_path(input_file))
            log.debug("Read input", size=len(content))

            # Process (uppercase in this case)
            processed = content.upper()
            log.info("Processing complete")

            # Write output
            output_file = input_file.replace("input", "output")
            storage.write(output_file, processed)
            log.info("Wrote output", file=output_file)

            return {"output_file": output_file, "bytes_processed": len(content)}

        env = ActivityTestEnv()

        # Setup input
        env.storage.write("input/data.txt", b"hello world")

        # Run activity
        result = await env.run(full_journey_activity, "input/data.txt")

        # Verify result
        assert result.value["bytes_processed"] == 11

        # Verify output exists in storage
        output_path = result.value["output_file"]
        assert env.storage.exists(output_path)
        assert (
            env.storage.read(env.storage._normalize_path(output_path)) == b"HELLO WORLD"
        )

        # Verify logging captured the journey
        assert any("Starting processing" in log["msg"] for log in env.logs)
        assert any("Processing complete" in log["msg"] for log in env.logs)
        assert any("Wrote output" in log["msg"] for log in env.logs)


# =============================================================================
# Data Transformation Tests
# =============================================================================


class TestDataTransformations:
    """Tests for data transformation accuracy."""

    @pytest.mark.unit
    async def test_binary_to_text_transformation(self):
        """TRANSFORM: Binary to text conversion preserves data."""

        import sxd_core.storage

        async def transform_activity():
            storage = sxd_core.storage.get_storage()
            # Write binary
            binary_data = bytes([0x48, 0x65, 0x6C, 0x6C, 0x6F])  # "Hello"
            storage.write("binary.bin", binary_data)

            # Read as text
            text = storage.read_text(storage._normalize_path("binary.bin"))
            return text

        env = ActivityTestEnv()
        result = await env.run(transform_activity)
        assert result.value == "Hello"

    @pytest.mark.unit
    async def test_json_roundtrip(self):
        """TRANSFORM: JSON data survives storage roundtrip."""
        import sxd_core.storage
        import json

        async def json_activity(data):
            storage = sxd_core.storage.get_storage()
            # Serialize and store
            json_str = json.dumps(data)
            storage.write("data.json", json_str.encode())

            # Read and deserialize
            stored = storage.read_text(storage._normalize_path("data.json"))
            return json.loads(stored)

        env = ActivityTestEnv()
        original = {
            "string": "value",
            "number": 42,
            "float": 3.14,
            "bool": True,
            "null": None,
            "array": [1, 2, 3],
            "nested": {"key": "value"},
        }
        result = await env.run(json_activity, original)

        assert result.value == original
