"""
Integration Tests: Activities with Simulation Framework

These tests demonstrate how to use the simulation framework to test
activities with deterministic I/O and fault injection.

Key patterns:
1. Use simulation_context() to route all I/O through simulation
2. Use hypothesis for property-based testing with different seeds
3. Inject faults (crashes, corruption) to test recovery
"""

import pytest
from hypothesis import given, settings, strategies as st

from sxd_core import io
from sxd_core.simulation import (
    SimulatorCore,
    simulation_context,
)


class TestChecksumActivity:
    """Tests for calculate_checksum activity under simulation."""

    def test_checksum_deterministic_same_seed(self):
        """Same seed produces same checksum results."""
        from sxd_core.ingest.activities import calculate_checksum

        # Run twice with same seed
        results = []
        for _ in range(2):
            sim = SimulatorCore(seed=12345)
            runtime = sim.create_runtime("worker")

            # Set up test file
            test_data = b"hello world" * 1000
            runtime.disk.write("/data/test.bin", test_data)
            runtime.disk.fsync("/data/test.bin")

            with simulation_context(runtime):
                # Calculate checksum - uses io.* which routes through simulation
                checksum = calculate_checksum("/data/test.bin")
                results.append(checksum)

        assert results[0] == results[1], "Same seed should produce same checksum"

    def test_checksum_different_data(self):
        """Different file contents produce different checksums."""
        from sxd_core.ingest.activities import calculate_checksum

        sim = SimulatorCore(seed=42)
        runtime = sim.create_runtime("worker")

        # Write two different files
        runtime.disk.write("/data/file1.bin", b"content A")
        runtime.disk.write("/data/file2.bin", b"content B")
        runtime.disk.fsync("/data/file1.bin")
        runtime.disk.fsync("/data/file2.bin")

        with simulation_context(runtime):
            checksum1 = calculate_checksum("/data/file1.bin")
            checksum2 = calculate_checksum("/data/file2.bin")

        assert checksum1 != checksum2

    @given(st.binary(min_size=1, max_size=10000))
    @settings(max_examples=10)
    def test_checksum_property_consistent(self, data: bytes):
        """Property: checksum of same data is always the same."""
        from sxd_core.ingest.activities import calculate_checksum

        sim = SimulatorCore(seed=42)
        runtime = sim.create_runtime("worker")

        runtime.disk.write("/data/test.bin", data)
        runtime.disk.fsync("/data/test.bin")

        with simulation_context(runtime):
            checksum1 = calculate_checksum("/data/test.bin")
            checksum2 = calculate_checksum("/data/test.bin")

        assert checksum1 == checksum2


class TestIOWrappers:
    """Tests for the io.* wrapper functions."""

    def test_io_time_deterministic(self):
        """io.time() is deterministic in simulation."""
        sim = SimulatorCore(seed=123)
        runtime = sim.create_runtime("worker")

        with simulation_context(runtime):
            t1 = io.time()
            # Advance simulated time
            runtime.clock.advance(1_000_000_000)  # 1 second
            t2 = io.time()

        assert t2 - t1 == 1.0

    def test_io_uuid_deterministic(self):
        """io.uuid4() is deterministic in simulation."""
        uuids1 = []
        uuids2 = []

        for uuids in [uuids1, uuids2]:
            sim = SimulatorCore(seed=42)
            runtime = sim.create_runtime("worker")
            with simulation_context(runtime):
                for _ in range(5):
                    uuids.append(io.uuid4())

        assert uuids1 == uuids2

    def test_io_file_operations(self):
        """io file operations work in simulation."""
        sim = SimulatorCore(seed=42)
        runtime = sim.create_runtime("worker")

        with simulation_context(runtime):
            # Write
            io.write_bytes("/test/file.txt", b"hello", fsync=True)

            # Read
            data = io.read_bytes("/test/file.txt")
            assert data == b"hello"

            # Exists
            assert io.exists("/test/file.txt")
            assert not io.exists("/nonexistent")

            # Size
            assert io.getsize("/test/file.txt") == 5

    def test_io_crash_loses_unfsynced(self):
        """Crash loses unfsynced data in simulation."""
        sim = SimulatorCore(seed=42)
        runtime = sim.create_runtime("worker")

        with simulation_context(runtime):
            # Write without fsync
            io.write_bytes("/test/file.txt", b"hello", fsync=False)

            # Crash
            runtime.disk.crash()

            # Data should be lost
            assert not io.exists("/test/file.txt")

    def test_io_crash_preserves_fsynced(self):
        """Crash preserves fsynced data in simulation."""
        sim = SimulatorCore(seed=42)
        runtime = sim.create_runtime("worker")

        with simulation_context(runtime):
            # Write with fsync
            io.write_bytes("/test/file.txt", b"hello", fsync=True)

            # Crash
            runtime.disk.crash()

            # Data should survive
            assert io.exists("/test/file.txt")
            assert io.read_bytes("/test/file.txt") == b"hello"


class TestChunkingSimulation:
    """Property tests for chunking operations."""

    @given(st.integers(min_value=1, max_value=100))
    @settings(max_examples=5)
    def test_file_discovery_finds_all_files(self, num_files: int):
        """discover_local_files finds all files in staging."""
        from sxd_core.ingest.activities import discover_local_files

        sim = SimulatorCore(seed=42)
        runtime = sim.create_runtime("worker")

        # Create test files
        staging_path = "/staging/ep-123"
        runtime.disk.mkdir(staging_path, parents=True)
        expected_files = []

        for i in range(num_files):
            filename = f"file_{i}.bin"
            filepath = f"{staging_path}/{filename}"
            data = f"content_{i}".encode()
            runtime.disk.write(filepath, data)
            runtime.disk.fsync(filepath)
            expected_files.append(filename)

        with simulation_context(runtime):
            files = discover_local_files(staging_path, "ep-123")

        assert len(files) == num_files
        found_names = {f["file_name"] for f in files}
        assert found_names == set(expected_files)

    def test_cleanup_staging_removes_directory(self):
        """cleanup_staging removes the staging directory."""
        from sxd_core.ingest.activities import cleanup_staging

        sim = SimulatorCore(seed=42)
        runtime = sim.create_runtime("worker")

        # Create staging directory with files
        staging_path = ".temp/staging/ep-123"
        runtime.disk.mkdir(staging_path, parents=True)
        runtime.disk.write(f"{staging_path}/file.bin", b"test")
        runtime.disk.fsync(f"{staging_path}/file.bin")
        runtime.disk.fsync_dir(staging_path)

        with simulation_context(runtime):
            assert io.exists(staging_path)
            cleanup_staging("ep-123")
            assert not io.exists(staging_path)


class TestFaultInjection:
    """Tests demonstrating fault injection scenarios."""

    def test_checksum_with_disk_corruption(self):
        """Checksum fails gracefully with disk corruption."""

        sim = SimulatorCore(seed=42)
        runtime = sim.create_runtime("worker")

        # Write file
        runtime.disk.write("/data/test.bin", b"hello world")
        runtime.disk.fsync("/data/test.bin")

        # Enable corruption
        runtime.disk.set_corruption_rate(1.0)

        with simulation_context(runtime):
            # Reading corrupted file should still return data
            # (the checksum will just be wrong)
            with pytest.raises(IOError):
                # Our io.read_bytes raises IOError on corruption
                io.read_bytes("/data/test.bin")

    def test_verify_checksum_after_crash(self):
        """Verify checksum detects data loss after crash."""
        from sxd_core.ingest.activities import calculate_checksum

        sim = SimulatorCore(seed=42)
        runtime = sim.create_runtime("worker")

        # Write file properly (with fsync)
        runtime.disk.write("/data/test.bin", b"original content")
        runtime.disk.fsync("/data/test.bin")

        with simulation_context(runtime):
            original_checksum = calculate_checksum("/data/test.bin")

        # Write new content WITHOUT fsync
        runtime.disk.write("/data/test.bin", b"modified content")

        # Crash - should lose the modification
        runtime.disk.crash()

        with simulation_context(runtime):
            # File should still have original content
            checksum_after_crash = calculate_checksum("/data/test.bin")

        assert original_checksum == checksum_after_crash


class TestDeterministicReplay:
    """Tests demonstrating replay capabilities."""

    @given(st.integers(min_value=0, max_value=2**32 - 1))
    @settings(max_examples=5)
    def test_simulation_replay_same_seed(self, seed: int):
        """Running simulation twice with same seed gives identical results."""
        from sxd_core.ingest.activities import calculate_checksum

        results = []

        for _ in range(2):
            sim = SimulatorCore(seed=seed)
            runtime = sim.create_runtime("worker")

            # Generate "random" file content using simulation RNG
            with simulation_context(runtime):
                content = bytes([io.randint(0, 255) for _ in range(100)])
                io.write_bytes("/data/random.bin", content, fsync=True)
                checksum = calculate_checksum("/data/random.bin")
                results.append((content, checksum))

        # Both runs should produce identical results
        assert results[0] == results[1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
