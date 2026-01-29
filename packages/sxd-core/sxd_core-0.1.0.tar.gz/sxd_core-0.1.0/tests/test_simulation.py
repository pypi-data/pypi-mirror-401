"""
Tests for the Deterministic Simulation Framework

These tests demonstrate:
1. Basic simulation components work correctly
2. Determinism is preserved (same seed = same results)
3. Fault injection works as expected
4. Invariants catch violations
5. State machines validate transitions

Run with: pytest tests/test_simulation.py -v
"""

import pytest
from typing import Any


# =============================================================================
# Clock Tests
# =============================================================================


class TestSimClock:
    """Tests for SimClock."""

    def test_initial_state(self):
        """Clock starts at time 0."""
        from sxd_core.simulation.clock import SimClock

        clock = SimClock()
        assert clock.now_ns() == 0
        assert clock.monotonic() == 0.0

    def test_advance(self):
        """Clock advances by specified amount."""
        from sxd_core.simulation.clock import SimClock

        clock = SimClock()
        clock.advance(1_000_000_000)  # 1 second
        assert clock.now_ns() == 1_000_000_000
        assert clock.monotonic() == 1.0

    def test_advance_multiple(self):
        """Multiple advances accumulate."""
        from sxd_core.simulation.clock import SimClock

        clock = SimClock()
        clock.advance(100)
        clock.advance(200)
        clock.advance(300)
        assert clock.now_ns() == 600

    def test_advance_to(self):
        """Can advance to specific time."""
        from sxd_core.simulation.clock import SimClock

        clock = SimClock()
        clock.advance_to(5_000_000_000)
        assert clock.now_ns() == 5_000_000_000

    def test_no_backwards_advance(self):
        """Cannot advance backwards."""
        from sxd_core.simulation.clock import SimClock

        clock = SimClock()
        clock.advance(1000)
        with pytest.raises(ValueError):
            clock.advance(-100)

    def test_datetime_conversion(self):
        """Datetime conversion works."""
        from sxd_core.simulation.clock import SimClock
        from datetime import timezone

        clock = SimClock()
        dt = clock.now_datetime()
        assert dt.tzinfo == timezone.utc

    def test_callback_on_advance(self):
        """Callbacks are called when time advances."""
        from sxd_core.simulation.clock import SimClock

        clock = SimClock()
        calls = []
        clock.on_advance(lambda old, new: calls.append((old, new)))

        clock.advance(100)
        clock.advance(200)

        assert calls == [(0, 100), (100, 300)]


# =============================================================================
# RNG Tests
# =============================================================================


class TestSimRng:
    """Tests for SimRng."""

    def test_deterministic(self):
        """Same seed produces same sequence."""
        from sxd_core.simulation.rng import SimRng

        rng1 = SimRng(seed=12345)
        rng2 = SimRng(seed=12345)

        for _ in range(100):
            assert rng1.random() == rng2.random()

    def test_different_seeds(self):
        """Different seeds produce different sequences."""
        from sxd_core.simulation.rng import SimRng

        rng1 = SimRng(seed=12345)
        rng2 = SimRng(seed=54321)

        # Very unlikely to be equal
        assert rng1.random() != rng2.random()

    def test_randint_range(self):
        """randint produces values in range."""
        from sxd_core.simulation.rng import SimRng

        rng = SimRng(seed=42)
        for _ in range(100):
            value = rng.randint(10, 20)
            assert 10 <= value <= 20

    def test_uuid_format(self):
        """UUID has correct format."""
        from sxd_core.simulation.rng import SimRng

        rng = SimRng(seed=42)
        uuid = rng.uuid4()
        assert len(uuid) == 36
        assert uuid.count("-") == 4

    def test_fork_deterministic(self):
        """Forked RNG is deterministic."""
        from sxd_core.simulation.rng import SimRng

        rng1 = SimRng(seed=12345)
        rng2 = SimRng(seed=12345)

        fork1 = rng1.fork("test")
        fork2 = rng2.fork("test")

        for _ in range(100):
            assert fork1.random() == fork2.random()

    def test_fork_independent(self):
        """Different fork names produce different sequences."""
        from sxd_core.simulation.rng import SimRng

        rng = SimRng(seed=12345)
        fork1 = rng.fork("node-1")
        fork2 = rng.fork("node-2")

        assert fork1.random() != fork2.random()

    def test_choice(self):
        """Choice selects from sequence."""
        from sxd_core.simulation.rng import SimRng

        rng = SimRng(seed=42)
        options = ["a", "b", "c"]
        for _ in range(100):
            assert rng.choice(options) in options

    def test_shuffle(self):
        """Shuffle modifies list in place."""
        from sxd_core.simulation.rng import SimRng

        rng = SimRng(seed=42)
        original = [1, 2, 3, 4, 5]
        lst = original.copy()
        rng.shuffle(lst)
        assert set(lst) == set(original)
        # Extremely unlikely to be in same order after shuffle
        # (though technically possible)


# =============================================================================
# Disk Tests
# =============================================================================


class TestSimDisk:
    """Tests for SimDisk."""

    def test_write_read(self):
        """Basic write and read works."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.disk import SimDisk
        from sxd_core.simulation.runtime import DiskResult

        clock = SimClock()
        rng = SimRng(seed=42)
        disk = SimDisk(clock=clock, rng=rng)

        result = disk.write("/test.txt", b"hello")
        assert result == DiskResult.OK

        data, result = disk.read("/test.txt")
        assert result == DiskResult.OK
        assert data == b"hello"

    def test_unfsynced_lost_on_crash(self):
        """Unfsynced data is lost on crash."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.disk import SimDisk
        from sxd_core.simulation.runtime import DiskResult

        clock = SimClock()
        rng = SimRng(seed=42)
        disk = SimDisk(clock=clock, rng=rng)

        # Write without fsync
        disk.write("/test.txt", b"hello")

        # Crash
        disk.crash()

        # Data should be lost
        data, result = disk.read("/test.txt")
        assert result == DiskResult.NOT_FOUND

    def test_fsynced_survives_crash(self):
        """Fsynced data survives crash."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.disk import SimDisk
        from sxd_core.simulation.runtime import DiskResult

        clock = SimClock()
        rng = SimRng(seed=42)
        disk = SimDisk(clock=clock, rng=rng)

        # Write and fsync
        disk.write("/test.txt", b"hello")
        disk.fsync("/test.txt")

        # Crash
        disk.crash()

        # Data should survive
        data, result = disk.read("/test.txt")
        assert result == DiskResult.OK
        assert data == b"hello"

    def test_directory_operations(self):
        """Directory operations work."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.disk import SimDisk
        from sxd_core.simulation.runtime import DiskResult

        clock = SimClock()
        rng = SimRng(seed=42)
        disk = SimDisk(clock=clock, rng=rng)

        # Create directory
        result = disk.mkdir("/data", parents=True)
        assert result == DiskResult.OK
        assert disk.is_dir("/data")

        # Create file in directory
        disk.write("/data/file.txt", b"content")
        disk.fsync("/data/file.txt")

        # List directory
        entries = disk.list_dir("/data")
        assert "file.txt" in entries

    def test_corruption_injection(self):
        """Corruption injection works."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.disk import SimDisk
        from sxd_core.simulation.runtime import DiskResult

        clock = SimClock()
        rng = SimRng(seed=42)
        disk = SimDisk(clock=clock, rng=rng)

        # Write and fsync
        original = b"hello world"
        disk.write("/test.txt", original)
        disk.fsync("/test.txt")

        # Enable 100% corruption rate
        disk.set_corruption_rate(1.0)

        # Read should be corrupted
        data, result = disk.read("/test.txt")
        assert result == DiskResult.CORRUPTION
        assert data != original

    def test_glob(self):
        """Glob pattern matching works."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.disk import SimDisk

        clock = SimClock()
        rng = SimRng(seed=42)
        disk = SimDisk(clock=clock, rng=rng)

        disk.write("/data/file1.txt", b"a")
        disk.write("/data/file2.txt", b"b")
        disk.write("/data/file.csv", b"c")
        disk.fsync("/data/file1.txt")
        disk.fsync("/data/file2.txt")
        disk.fsync("/data/file.csv")

        matches = disk.glob("/data/*.txt")
        assert len(matches) == 2
        assert all(".txt" in m for m in matches)


# =============================================================================
# Network Tests
# =============================================================================


class TestSimNetwork:
    """Tests for SimNetwork."""

    def test_basic_send_recv(self):
        """Basic message delivery works."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.network import SimNetwork

        clock = SimClock()
        rng = SimRng(seed=42)
        network = SimNetwork(clock=clock, rng=rng)

        # Send message
        network.send("node-a", "node-b", b"hello")

        # Advance time past delivery
        clock.advance(100_000_000)  # 100ms

        # Receive message
        msg = network.recv("node-b")
        assert msg is not None
        assert msg.payload == b"hello"
        assert msg.src == "node-a"
        assert msg.dst == "node-b"

    def test_partition_blocks_messages(self):
        """Partitioned nodes cannot communicate."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.network import SimNetwork

        clock = SimClock()
        rng = SimRng(seed=42)
        network = SimNetwork(clock=clock, rng=rng)

        # Create partition
        network.partition("node-a", "node-b")

        # Send message
        network.send("node-a", "node-b", b"hello")

        # Advance time
        clock.advance(1_000_000_000)

        # Message should not be delivered
        msg = network.recv("node-b")
        assert msg is None

    def test_partition_heal(self):
        """Healed partition allows communication."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.network import SimNetwork

        clock = SimClock()
        rng = SimRng(seed=42)
        network = SimNetwork(clock=clock, rng=rng)

        # Create and heal partition
        network.partition("node-a", "node-b")
        network.heal_partition("node-a", "node-b")

        # Send message
        network.send("node-a", "node-b", b"hello")

        # Advance time
        clock.advance(100_000_000)

        # Message should be delivered
        msg = network.recv("node-b")
        assert msg is not None

    def test_drop_rate(self):
        """Drop rate causes message loss."""
        from sxd_core.simulation.clock import SimClock
        from sxd_core.simulation.rng import SimRng
        from sxd_core.simulation.network import SimNetwork

        clock = SimClock()
        rng = SimRng(seed=42)
        network = SimNetwork(clock=clock, rng=rng)

        # Set 100% drop rate
        network.set_drop_rate("node-a", "node-b", 1.0)

        # Send messages
        for _ in range(10):
            network.send("node-a", "node-b", b"hello")

        # Advance time
        clock.advance(1_000_000_000)

        # All messages should be dropped
        messages = network.recv_all("node-b")
        assert len(messages) == 0


# =============================================================================
# State Machine Tests
# =============================================================================


class TestStateMachine:
    """Tests for StateMachine."""

    def test_valid_transition(self):
        """Valid transitions succeed."""
        from sxd_core.simulation.state_machine import (
            EpisodeState,
            EpisodeEvent,
            create_episode_state_machine,
        )

        sm = create_episode_state_machine("test-1")
        assert sm.state == EpisodeState.CREATED

        sm.apply(EpisodeEvent.START_DISCOVERY)
        assert sm.state == EpisodeState.DISCOVERING

    def test_invalid_transition(self):
        """Invalid transitions raise exception."""
        from sxd_core.simulation.state_machine import (
            EpisodeEvent,
            create_episode_state_machine,
            InvalidTransition,
        )

        sm = create_episode_state_machine("test-1")

        # Cannot go directly to UPLOADING from CREATED
        with pytest.raises(InvalidTransition):
            sm.apply(EpisodeEvent.UPLOAD_COMPLETE)

    def test_history_tracking(self):
        """Transition history is tracked."""
        from sxd_core.simulation.state_machine import (
            EpisodeEvent,
            create_episode_state_machine,
        )

        sm = create_episode_state_machine("test-1")
        sm.apply(EpisodeEvent.START_DISCOVERY)
        sm.apply(EpisodeEvent.DISCOVERY_COMPLETE)

        history = sm.history
        assert len(history) == 2
        assert history[0].event == EpisodeEvent.START_DISCOVERY
        assert history[1].event == EpisodeEvent.DISCOVERY_COMPLETE

    def test_can_apply(self):
        """can_apply correctly checks validity."""
        from sxd_core.simulation.state_machine import (
            EpisodeEvent,
            create_episode_state_machine,
        )

        sm = create_episode_state_machine("test-1")

        assert sm.can_apply(EpisodeEvent.START_DISCOVERY)
        assert not sm.can_apply(EpisodeEvent.UPLOAD_COMPLETE)

    def test_get_valid_events(self):
        """get_valid_events returns correct events."""
        from sxd_core.simulation.state_machine import (
            EpisodeEvent,
            create_episode_state_machine,
        )

        sm = create_episode_state_machine("test-1")
        valid = sm.get_valid_events()

        assert EpisodeEvent.START_DISCOVERY in valid
        assert EpisodeEvent.UPLOAD_COMPLETE not in valid


# =============================================================================
# Simulator Core Tests
# =============================================================================


class TestSimulatorCore:
    """Tests for SimulatorCore."""

    def test_creation(self):
        """Simulator can be created."""
        from sxd_core.simulation.simulator import SimulatorCore

        sim = SimulatorCore(seed=12345)
        assert sim.seed == 12345
        assert sim.clock.now_ns() == 0

    def test_deterministic(self):
        """Same seed produces same results."""
        from sxd_core.simulation.simulator import SimulatorCore, EventType
        from sxd_core.simulation.node import WorkerNode

        def run_sim(seed: int) -> list[int]:
            sim = SimulatorCore(seed=seed)
            sim.add_node("worker", WorkerNode("worker"))

            # Schedule some events
            for i in range(10):
                sim.schedule_event(
                    delay_ns=sim.rng.randint(1000, 1000000),
                    event_type=EventType.CUSTOM,
                    node_id="worker",
                    payload=i,
                )

            sim.run_until(max_events=10)
            return [sim.clock.now_ns()]

        result1 = run_sim(12345)
        result2 = run_sim(12345)
        result3 = run_sim(54321)

        assert result1 == result2
        assert result1 != result3

    def test_event_ordering(self):
        """Events are processed in time order."""
        from sxd_core.simulation.simulator import SimulatorCore, EventType
        from sxd_core.simulation.node import Node

        class RecordingNode(Node):
            def __init__(self, node_id: str):
                super().__init__(node_id)
                self.received: list[Any] = []

            def on_custom_event(self, payload: Any) -> None:
                self.received.append(payload)

        sim = SimulatorCore(seed=42)
        node = RecordingNode("test")
        sim.add_node("test", node)
        node.start()  # Node must be started to receive events

        # Schedule events out of order
        sim.schedule_event(300, EventType.CUSTOM, "test", "third")
        sim.schedule_event(100, EventType.CUSTOM, "test", "first")
        sim.schedule_event(200, EventType.CUSTOM, "test", "second")

        sim.run_until(max_events=3)

        assert node.received == ["first", "second", "third"]


# =============================================================================
# Fault Injection Tests
# =============================================================================


class TestFaultInjector:
    """Tests for FaultInjector."""

    def test_node_crash(self):
        """Node crash works."""
        from sxd_core.simulation.simulator import SimulatorCore
        from sxd_core.simulation.node import WorkerNode
        from sxd_core.simulation.faults import FaultInjector

        sim = SimulatorCore(seed=42)
        worker = WorkerNode("worker-0")
        sim.add_node("worker-0", worker)
        worker.start()

        injector = FaultInjector(sim)
        sim.set_fault_injector(injector)

        assert worker.is_alive

        injector.crash_node("worker-0")
        sim.run_until(max_events=1)

        assert not worker.is_alive

    def test_network_partition(self):
        """Network partition works."""
        from sxd_core.simulation.simulator import SimulatorCore
        from sxd_core.simulation.node import WorkerNode
        from sxd_core.simulation.faults import FaultInjector

        sim = SimulatorCore(seed=42)
        sim.add_node("node-a", WorkerNode("node-a"))
        sim.add_node("node-b", WorkerNode("node-b"))

        injector = FaultInjector(sim)
        sim.set_fault_injector(injector)

        injector.partition_nodes("node-a", "node-b")

        assert sim.network.is_partitioned("node-a", "node-b")
        assert sim.network.is_partitioned("node-b", "node-a")


# =============================================================================
# Invariant Tests
# =============================================================================


class TestInvariants:
    """Tests for invariant checking."""

    def test_no_violation_when_correct(self):
        """No violation when system behaves correctly."""
        from sxd_core.simulation.simulator import SimulatorCore
        from sxd_core.simulation.node import WorkerNode
        from sxd_core.simulation.invariants import NoLostWork

        sim = SimulatorCore(seed=42)
        sim.add_node("worker", WorkerNode("worker"))

        invariant = NoLostWork()
        sim.add_invariant(invariant)

        sim.run_until(max_events=10)

        assert not sim.has_violations()


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """Integration tests for the full framework."""

    def test_full_simulation(self):
        """Full simulation runs without errors."""
        from sxd_core.simulation.simulator import SimulatorCore, EventType
        from sxd_core.simulation.node import WorkerNode, MasterNode
        from sxd_core.simulation.faults import FaultInjector
        from sxd_core.simulation.invariants import get_default_invariants
        from sxd_core.simulation.trace import TraceRecorder

        # Create simulator
        sim = SimulatorCore(seed=12345)

        # Add nodes
        sim.add_node("master", MasterNode("master"))
        for i in range(3):
            sim.add_node(f"worker-{i}", WorkerNode(f"worker-{i}"))

        # Start all nodes
        for node in sim.get_nodes().values():
            node.start()

        # Set up fault injection
        injector = FaultInjector(sim)
        sim.set_fault_injector(injector)

        # Set up tracing
        recorder = TraceRecorder(seed=12345)
        sim.set_trace_recorder(recorder)

        # Add invariants
        for inv in get_default_invariants():
            sim.add_invariant(inv)

        # Schedule some work
        sim.schedule_event(
            delay_ns=1_000_000,
            event_type=EventType.WORKFLOW_START,
            node_id="master",
            payload={"job_id": "test-job"},
        )

        # Inject some faults
        from sxd_core.simulation.faults import Fault, FaultType

        injector.schedule(
            delay_ns=10_000_000,
            fault=Fault(
                type=FaultType.NETWORK_DELAY,
                target=("worker-0", "worker-1"),
                duration_ns=5_000_000,
            ),
        )

        # Run simulation
        sim.run_until(max_events=100)

        # Verify
        assert sim.stats.events_processed > 0
        assert recorder.events_recorded > 0

    def test_replay_produces_same_result(self):
        """Replaying a trace produces identical results."""
        from sxd_core.simulation.simulator import SimulatorCore, EventType
        from sxd_core.simulation.node import WorkerNode

        def run_and_get_final_time(seed: int) -> int:
            sim = SimulatorCore(seed=seed)
            sim.add_node("worker", WorkerNode("worker"))

            for i in range(10):
                sim.schedule_event(
                    delay_ns=sim.rng.randint(1000, 100000),
                    event_type=EventType.CUSTOM,
                    node_id="worker",
                    payload=i,
                )

            sim.run_until(max_events=10)
            return sim.clock.now_ns()

        # Run twice with same seed
        time1 = run_and_get_final_time(42)
        time2 = run_and_get_final_time(42)

        assert time1 == time2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
