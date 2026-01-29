"""
Tests for sxd_core.ops modules.

Covers config, infra, remote, submit, temporal, metrics, and storage operations.
"""

import subprocess
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# =============================================================================
# Config Module Tests
# =============================================================================


class TestConfigManager:
    """Tests for ConfigManager class."""

    def test_singleton_pattern(self):
        """ConfigManager should be a singleton."""
        from sxd_core.config import ConfigManager

        # Reset singleton for test
        ConfigManager._instance = None
        ConfigManager._config = None

        mgr1 = ConfigManager()
        mgr2 = ConfigManager()
        assert mgr1 is mgr2

    def test_get_temporal_config_defaults(self, monkeypatch):
        """Returns default temporal config when not configured."""
        from sxd_core.config import ConfigManager

        monkeypatch.delenv("SXD_TEMPORAL_HOST", raising=False)
        monkeypatch.delenv("SXD_TEMPORAL_PORT", raising=False)

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        config = mgr.get_temporal_config()
        assert config["host"] == "localhost"
        assert config["port"] == 7233
        assert config["namespace"] == "default"
        assert config["task_queue"] == "video-processing"

    def test_get_temporal_config_from_env(self, monkeypatch):
        """Environment variables override config file."""
        from sxd_core.config import ConfigManager

        monkeypatch.setenv("SXD_TEMPORAL_HOST", "env-host.local")
        monkeypatch.setenv("SXD_TEMPORAL_PORT", "9999")

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {"temporal": {"host": "config-host.local", "port": 7233}}

        config = mgr.get_temporal_config()
        assert config["host"] == "env-host.local"
        assert config["port"] == 9999

    def test_get_storage_config_defaults(self):
        """Returns default storage config."""
        from sxd_core.config import ConfigManager

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        config = mgr.get_storage_config()
        assert config["backend"] == "local"
        assert config["endpoint"] == "http://localhost:8333"

    def test_get_clickhouse_config_defaults(self):
        """Returns default ClickHouse config."""
        from sxd_core.config import ConfigManager

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        config = mgr.get_clickhouse_config()
        assert config["host"] == "localhost"
        assert config["port"] == 8123
        assert config["database"] == "sxd"

    def test_get_remote_config(self, monkeypatch):
        """Returns remote config with env override."""
        from sxd_core.config import ConfigManager

        monkeypatch.setenv("SXD_REMOTE_HOST", "remote.example.com")

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        config = mgr.get_remote_config()
        assert config["host"] == "remote.example.com"

    def test_get_docker_config(self, monkeypatch):
        """Returns Docker config with env override."""
        from sxd_core.config import ConfigManager

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test-project")

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        config = mgr.get_docker_config()
        assert config["project_name"] == "test-project"

    def test_is_master_node(self, monkeypatch):
        """Correctly identifies master node."""
        from sxd_core.config import ConfigManager

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        monkeypatch.setenv("SXD_NODE_TYPE", "master")
        assert mgr.is_master_node() is True
        assert mgr.is_worker_node() is False

    def test_is_worker_node(self, monkeypatch):
        """Correctly identifies worker node."""
        from sxd_core.config import ConfigManager

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        monkeypatch.setenv("SXD_NODE_TYPE", "worker")
        assert mgr.is_worker_node() is True
        assert mgr.is_master_node() is False

    def test_is_local_client(self, monkeypatch):
        """Correctly identifies local client."""
        from sxd_core.config import ConfigManager

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        monkeypatch.delenv("SXD_NODE_TYPE", raising=False)
        assert mgr.is_local_client() is True

    def test_get_backup_config(self):
        """Returns backup config with defaults."""
        from sxd_core.config import ConfigManager

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        config = mgr.get_backup_config()
        assert config["retention_days"] == 7
        assert config["scratch_max_age_hours"] == 24

    def test_reload_config(self, tmp_path):
        """Reload refreshes config from disk."""
        from sxd_core.config import ConfigManager

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {"old": "value"}

        # Mock _load_config to return new value
        with patch.object(mgr, "_load_config", return_value={"new": "value"}):
            mgr.reload()
            assert mgr._config == {"new": "value"}


# =============================================================================
# Infra Module Tests
# =============================================================================


class TestInfraModule:
    """Tests for infrastructure management operations."""

    def test_docker_compose_builds_command(self, monkeypatch):
        """docker_compose builds correct command."""
        from sxd_core.ops.infra import docker_compose

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")
        monkeypatch.delenv("SXD_COMPOSE_PROFILE", raising=False)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            docker_compose("ps")

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "docker" in cmd
        assert "compose" in cmd
        assert "-p" in cmd
        assert "test" in cmd
        assert "ps" in cmd

    def test_docker_compose_with_profile(self, monkeypatch):
        """docker_compose includes profile when set."""
        from sxd_core.ops.infra import docker_compose

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")
        monkeypatch.setenv("SXD_COMPOSE_PROFILE", "dev")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            docker_compose("up", ["-d"])

        cmd = mock_run.call_args[0][0]
        assert "--profile" in cmd
        assert "dev" in cmd

    def test_wait_for_container_success(self):
        """wait_for_container returns True when container is running."""
        from sxd_core.ops.infra import wait_for_container

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="true\n")
            result = wait_for_container("test-container", max_wait=2)

        assert result is True

    def test_wait_for_container_timeout(self):
        """wait_for_container returns False on timeout."""
        from sxd_core.ops.infra import wait_for_container

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="")
            result = wait_for_container("test-container", max_wait=1)

        assert result is False

    def test_stop_services(self, monkeypatch):
        """stop_services calls docker compose down."""
        from sxd_core.ops.infra import stop_services

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")

        with patch("sxd_core.ops.infra.docker_compose") as mock_compose:
            stop_services()

        mock_compose.assert_called_once_with("down")


# =============================================================================
# Remote Module Tests
# =============================================================================


class TestRemoteModule:
    """Tests for remote/SSH operations."""

    def test_execute_remote_or_local_on_correct_node(self, monkeypatch):
        """Returns True when already on correct node type."""
        from sxd_core.ops.remote import execute_remote_or_local

        monkeypatch.setenv("SXD_NODE_TYPE", "master")

        result = execute_remote_or_local(["test", "cmd"], target_node="master")
        assert result is True

    def test_execute_remote_or_local_master_can_run_worker(self, monkeypatch):
        """Master node can execute worker commands."""
        from sxd_core.ops.remote import execute_remote_or_local

        monkeypatch.setenv("SXD_NODE_TYPE", "master")

        result = execute_remote_or_local(["worker", "start"], target_node="worker")
        assert result is True

    def test_execute_remote_or_local_wrong_node_exits(self, monkeypatch):
        """Exits with error when on wrong node type."""
        from sxd_core.ops.remote import execute_remote_or_local

        monkeypatch.setenv("SXD_NODE_TYPE", "worker")

        with pytest.raises(SystemExit) as exc_info:
            execute_remote_or_local(["infra", "up"], target_node="master")

        assert exc_info.value.code == 1

    def test_ssh_connect_builds_command(self, monkeypatch):
        """ssh_connect builds correct SSH command."""
        from sxd_core.config import ConfigManager
        from sxd_core.ops.remote import ssh_connect

        # Mock config
        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        with patch("sxd_core.ops.remote.get_config", return_value=mgr):
            with patch("subprocess.run") as mock_run:
                ssh_connect("test-host", "echo hello", ssh_key_path="/path/to/key")

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "ssh" in cmd
        assert "-i" in cmd
        assert "/path/to/key" in cmd
        # Host is now in user@host format
        assert any("test-host" in arg for arg in cmd)
        assert "echo hello" in cmd


# =============================================================================
# Submit Module Tests
# =============================================================================


class TestSubmitModule:
    """Tests for job submission operations."""

    @pytest.mark.asyncio
    async def test_submit_video_job_detects_tar(self):
        """submit_video_job redirects TAR files to batch submission."""
        from sxd_core.ops.submit import submit_video_job

        with patch(
            "sxd_core.ops.submit.submit_batch_job", new_callable=AsyncMock
        ) as mock_batch:
            mock_batch.return_value = {"workflow_id": "batch-123", "status": "started"}

            result = await submit_video_job(
                "http://example.com/videos.tar",
                customer_id="test",
                video_id="auto",
            )

        mock_batch.assert_called_once()
        assert result["workflow_id"] == "batch-123"

    @pytest.mark.asyncio
    async def test_submit_video_job_generates_video_id(self):
        """submit_video_job generates ID when set to auto."""
        from sxd_core.ops.submit import submit_video_job

        with patch(
            "sxd_core.ops.submit.submit_generic_workflow", new_callable=AsyncMock
        ) as mock_submit:
            mock_submit.return_value = {"workflow_id": "video-123", "status": "started"}

            await submit_video_job(
                "http://example.com/video.mp4",
                customer_id="test",
                video_id="auto",
            )

        # Check that video_id was generated
        call_args = mock_submit.call_args
        input_data = (
            call_args[1]["input_data"]
            if "input_data" in call_args[1]
            else call_args[0][1]
        )
        assert input_data["video_id"].startswith("video-")

    @pytest.mark.asyncio
    async def test_submit_batch_job_generates_batch_id(self):
        """submit_batch_job generates batch ID when not provided."""
        from sxd_core.ops.submit import submit_batch_job

        with patch(
            "sxd_core.ops.submit.submit_generic_workflow", new_callable=AsyncMock
        ) as mock_submit:
            mock_submit.return_value = {"workflow_id": "batch-123", "status": "started"}

            await submit_batch_job(
                "http://example.com/videos.tar",
                customer_id="test",
                batch_id=None,
            )

        call_args = mock_submit.call_args
        (
            call_args[1]["input_data"]
            if "input_data" in call_args[1]
            else call_args[0][1]
        )

    @pytest.mark.asyncio
    async def test_submit_generic_workflow_unknown_workflow(self):
        """submit_generic_workflow raises for unknown workflow."""
        from sxd_core.ops.submit import submit_generic_workflow

        with patch("sxd_core.ops.submit.get_workflow", return_value=None):
            with patch("sxd_core.ops.submit.list_workflows", return_value={}):
                with pytest.raises(ValueError) as exc_info:
                    await submit_generic_workflow("unknown-workflow", {})

        assert "Unknown workflow" in str(exc_info.value)


# =============================================================================
# Temporal Module Tests
# =============================================================================


class TestTemporalModule:
    """Tests for Temporal operations."""

    def test_poller_info_dataclass(self):
        """PollerInfo dataclass works correctly."""
        from sxd_core.ops.temporal import PollerInfo

        now = datetime.now()
        poller = PollerInfo(identity="worker-1@host", last_access_time=now)

        assert poller.identity == "worker-1@host"
        assert poller.last_access_time == now

    def test_worker_info_dataclass(self):
        """WorkerInfo dataclass works correctly."""
        from sxd_core.ops.temporal import PollerInfo, WorkerInfo

        worker = WorkerInfo(
            task_queue="test-queue",
            workflow_pollers=[PollerInfo("w1")],
            activity_pollers=[PollerInfo("a1"), PollerInfo("a2")],
        )

        assert worker.task_queue == "test-queue"
        assert len(worker.workflow_pollers) == 1
        assert len(worker.activity_pollers) == 2

    def test_workflow_status_dataclass(self):
        """WorkflowStatus dataclass works correctly."""
        from sxd_core.ops.temporal import WorkflowStatus

        status = WorkflowStatus(
            workflow_id="wf-123",
            run_id="run-456",
            status="COMPLETED",
            result={"key": "value"},
        )

        assert status.workflow_id == "wf-123"
        assert status.status == "COMPLETED"
        assert status.result == {"key": "value"}


# =============================================================================
# Metrics Module Tests
# =============================================================================


class TestMetricsModule:
    """Tests for metrics operations."""

    def test_stats_24h_dataclass(self):
        """Stats24h dataclass works correctly."""
        from sxd_core.ops.metrics import Stats24h

        stats = Stats24h(
            videos_processed=100,
            videos_successful=95,
            videos_failed=5,
            success_rate=95.0,
            batches_completed=10,
            batches_in_progress=2,
            uploads_completed=50,
            avg_quality_score=0.85,
            total_size_bytes=1024 * 1024 * 1024,
            total_duration_hours=5.5,
            error_count=5,
        )

        assert stats.videos_processed == 100
        assert stats.videos_failed == 5
        assert stats.success_rate == 95.0

    def test_error_summary_dataclass(self):
        """ErrorSummary dataclass works correctly."""
        from sxd_core.ops.metrics import ErrorSummary

        error = ErrorSummary(
            activity="download_video",
            error_count=10,
            last_error_time=datetime.now(),
            sample_message="Connection timed out",
        )

        assert error.activity == "download_video"
        assert error.error_count == 10

    def test_storage_stats_dataclass(self):
        """StorageStats dataclass works correctly."""
        from sxd_core.ops.metrics import StorageStats

        stats = StorageStats(
            table="videos",
            size_bytes=1024 * 1024 * 500,
            size_readable="500.0 MB",
            row_count=10000,
        )

        assert stats.table == "videos"
        assert stats.size_readable == "500.0 MB"


# =============================================================================
# Storage Module Tests
# =============================================================================


class TestStorageModule:
    """Tests for storage operations."""

    def test_video_info_dataclass(self):
        """VideoInfo dataclass works correctly."""
        from sxd_core.ops.storage import VideoInfo

        video = VideoInfo(
            id="id-123",
            video_id="vid-123",
            customer_id="cust-1",
            batch_id="batch-1",
            source_url="http://example.com/video.mp4",
            status="COMPLETED",
            node="worker-1",
            size_bytes=1024000,
            quality_score=0.95,
            blur_mean=0.1,
            frame_count=300,
        )

        assert video.video_id == "vid-123"
        assert video.status == "COMPLETED"

    def test_batch_info_dataclass(self):
        """BatchInfo dataclass works correctly."""
        from sxd_core.ops.storage import BatchInfo

        batch = BatchInfo(
            id="batch-123",
            customer_id="cust-1",
            tar_url="http://example.com/videos.tar",
            status="COMPLETED",
            total_videos=10,
            successful_videos=9,
            failed_videos=1,
        )

        assert batch.total_videos == 10
        assert batch.successful_videos == 9

    def test_episode_info_dataclass(self):
        """EpisodeInfo dataclass works correctly."""
        from sxd_core.ops.storage import EpisodeInfo

        episode = EpisodeInfo(
            id="ep-123",
            customer_id="cust-1",
            source_path="/data/videos",
            total_size=1024 * 1024 * 100,
            chunk_count=5,
            status="COMPLETED",
            target_node="worker-1",
        )

        assert episode.chunk_count == 5
        assert episode.status == "COMPLETED"


# =============================================================================
# Cluster Module Tests
# =============================================================================


class TestInfraModuleExtended:
    """Extended tests for infrastructure management operations."""

    def test_docker_compose_with_extra_args(self, monkeypatch):
        """docker_compose passes extra args correctly."""
        from sxd_core.ops.infra import docker_compose

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")
        monkeypatch.delenv("SXD_COMPOSE_PROFILE", raising=False)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            docker_compose("up", ["-d", "--build"])

        cmd = mock_run.call_args[0][0]
        assert "-d" in cmd
        assert "--build" in cmd
        assert "up" in cmd

    def test_show_logs_with_service(self, monkeypatch):
        """show_logs passes service name."""
        from sxd_core.ops.infra import show_logs

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")
        monkeypatch.delenv("SXD_COMPOSE_PROFILE", raising=False)

        with patch("sxd_core.ops.infra.docker_compose") as mock_compose:
            show_logs(service="temporal", follow=False)

        mock_compose.assert_called_once_with("logs", ["temporal"])

    def test_show_logs_follow(self, monkeypatch):
        """show_logs includes -f when follow=True."""
        from sxd_core.ops.infra import show_logs

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")
        monkeypatch.delenv("SXD_COMPOSE_PROFILE", raising=False)

        with patch("sxd_core.ops.infra.docker_compose") as mock_compose:
            show_logs(follow=True)

        mock_compose.assert_called_once_with("logs", ["-f"])

    def test_start_services_creates_htpasswd(self, monkeypatch, tmp_path):
        """start_services creates .htpasswd file."""
        from sxd_core.config import ConfigManager
        from sxd_core.ops.infra import start_services

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")
        monkeypatch.delenv("SXD_COMPOSE_PROFILE", raising=False)
        monkeypatch.setenv("SXD_ADMIN_PASSWORD", "testpassword")

        htpasswd_path = tmp_path / ".htpasswd"

        mgr = ConfigManager.__new__(ConfigManager)
        mgr._config = {}

        with patch("sxd_core.ops.infra.get_config") as mock_config:
            mock_config.return_value.get_gateway_config.return_value = {
                "admin_username": "admin",
                "admin_password": "testpassword",
                "htpasswd_path": htpasswd_path,
            }
            mock_config.return_value.get_docker_config.return_value = {
                "project_name": "test",
                "compose_file": "deploy/docker-compose.yml",
                "profile": "",
            }
            with patch("subprocess.run") as mock_run:
                # Mock openssl passwd command
                mock_run.return_value = MagicMock(
                    returncode=0, stdout="$apr1$hash$value\n"
                )
                with patch("sxd_core.ops.infra.docker_compose"):
                    start_services()

        assert htpasswd_path.exists()
        content = htpasswd_path.read_text()
        assert "admin:" in content

    def test_wait_for_container_eventual_success(self):
        """wait_for_container succeeds after retries."""
        from sxd_core.ops.infra import wait_for_container

        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] < 3:
                return MagicMock(returncode=1, stdout="")
            return MagicMock(returncode=0, stdout="true\n")

        with patch("subprocess.run", side_effect=side_effect):
            with patch("time.sleep"):  # Skip actual sleeping
                result = wait_for_container("test-container", max_wait=5)

        assert result is True
        assert call_count[0] >= 3

    def test_initialize_databases_waits_for_containers(self, monkeypatch):
        """initialize_databases waits for containers before executing."""
        from sxd_core.ops.infra import initialize_databases

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")

        with patch("sxd_core.ops.infra.get_config") as mock_config:
            mock_config.return_value.get_docker_config.return_value = {
                "project_name": "test",
            }
            mock_config.return_value.get_clickhouse_config.return_value = {
                "database": "sxd",
            }
            with patch("sxd_core.ops.infra.wait_for_container", return_value=True):
                with patch("subprocess.run") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0)
                    initialize_databases()

        # Should have called run for both clickhouse and postgres
        assert mock_run.call_count >= 2

    def test_initialize_databases_clickhouse_not_ready(self, monkeypatch, capsys):
        """initialize_databases warns when ClickHouse not ready."""
        from sxd_core.ops.infra import initialize_databases

        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")

        with patch("sxd_core.ops.infra.get_config") as mock_config:
            mock_config.return_value.get_docker_config.return_value = {
                "project_name": "test",
            }
            mock_config.return_value.get_clickhouse_config.return_value = {
                "database": "sxd",
            }
            with patch("sxd_core.ops.infra.wait_for_container", return_value=False):
                initialize_databases()

        captured = capsys.readouterr()
        assert "ClickHouse container not ready" in captured.out


# =============================================================================
# Remote Module Extended Tests
# =============================================================================


class TestRemoteModuleExtended:
    """Extended tests for remote/SSH operations."""

    def test_execute_remote_or_local_no_remote_host(self, monkeypatch):
        """execute_remote_or_local exits when no remote host configured."""
        from sxd_core.ops.remote import execute_remote_or_local

        monkeypatch.delenv("SXD_NODE_TYPE", raising=False)
        monkeypatch.delenv("SXD_REMOTE_HOST", raising=False)

        with patch("sxd_core.ops.remote.get_config") as mock_config:
            mock_config.return_value.get_node_type.return_value = None
            mock_config.return_value.get_remote_config.return_value = {"host": ""}
            with pytest.raises(SystemExit) as exc_info:
                execute_remote_or_local(["test"], target_node="master")

        assert exc_info.value.code == 1

    def test_execute_remote_or_local_proxies_to_ssh(self, monkeypatch):
        """execute_remote_or_local proxies command via SSH."""
        from sxd_core.ops.remote import execute_remote_or_local

        monkeypatch.delenv("SXD_NODE_TYPE", raising=False)

        with patch("sxd_core.ops.remote.get_config") as mock_config:
            mock_config.return_value.get_node_type.return_value = None
            mock_config.return_value.get_remote_config.return_value = {
                "host": "remote.example.com"
            }
            with patch("sxd_core.ops.remote.ssh_connect") as mock_ssh:
                with pytest.raises(SystemExit) as exc_info:
                    execute_remote_or_local(["infra", "up"], target_node="master")

        mock_ssh.assert_called_once()
        assert exc_info.value.code == 0

    def test_execute_remote_or_local_ssh_failure(self, monkeypatch):
        """execute_remote_or_local handles SSH failures."""
        from sxd_core.ops.remote import execute_remote_or_local

        monkeypatch.delenv("SXD_NODE_TYPE", raising=False)

        with patch("sxd_core.ops.remote.get_config") as mock_config:
            mock_config.return_value.get_node_type.return_value = None
            mock_config.return_value.get_remote_config.return_value = {
                "host": "remote.example.com"
            }
            with patch("sxd_core.ops.remote.ssh_connect") as mock_ssh:
                mock_ssh.side_effect = subprocess.CalledProcessError(1, "ssh")
                with pytest.raises(SystemExit) as exc_info:
                    execute_remote_or_local(["test"], target_node="master")

        assert exc_info.value.code == 1

    def test_run_ansible_playbook_builds_command(self, tmp_path, monkeypatch):
        """run_ansible_playbook builds correct ansible command."""
        from sxd_core.ops.remote import run_ansible_playbook

        monkeypatch.chdir(tmp_path)

        # Create .temp directory for vars file
        (tmp_path / ".temp").mkdir(exist_ok=True)
        (tmp_path / ".temp" / "ansible_vars.yaml").write_text("secret: value")

        with patch("sxd_core.ops.remote.get_config") as mock_config:
            mock_config.return_value.get_remote_config.return_value = {
                "inventory_path": "deploy/inventory.yml"
            }
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                run_ansible_playbook(
                    "deploy/ansible/site.yml",
                    limit="master",
                    tags=["deploy", "restart"],
                    extra_vars={"version": "1.0.0"},
                )

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        # Command now starts with uv run if infisical not found, or infisical run -- uv run
        assert "ansible-playbook" in cmd
        assert "--limit" in cmd
        assert "master" in cmd
        assert "--tags" in cmd
        assert "deploy,restart" in cmd
        assert "-e" in cmd
        assert "version=1.0.0" in cmd

    def test_select_node_interactive_no_nodes(self, capsys):
        """select_node_interactive returns None when no nodes."""
        from sxd_core.ops.remote import select_node_interactive

        with patch("sxd_core.ops.remote.load_inventory_nodes", return_value=[]):
            result = select_node_interactive()

        assert result is None
        captured = capsys.readouterr()
        assert "No nodes found" in captured.out

    def test_select_node_interactive_cancel(self):
        """select_node_interactive returns None on cancel."""
        from sxd_core.ops.cluster import NodeInfo
        from sxd_core.ops.remote import select_node_interactive

        nodes = [NodeInfo("node1", "10.0.0.1", "22", "admin", "master", True, True)]

        with patch("sxd_core.ops.remote.load_inventory_nodes", return_value=nodes):
            with patch("builtins.input", return_value="0"):
                result = select_node_interactive()

        assert result is None

    def test_select_node_interactive_all(self):
        """select_node_interactive returns 'all' for all selection."""
        from sxd_core.ops.cluster import NodeInfo
        from sxd_core.ops.remote import select_node_interactive

        nodes = [NodeInfo("node1", "10.0.0.1", "22", "admin", "master", True, True)]

        with patch("sxd_core.ops.remote.load_inventory_nodes", return_value=nodes):
            with patch("builtins.input", return_value="a"):
                result = select_node_interactive()

        assert result == "all"

    def test_select_node_interactive_specific_node(self):
        """select_node_interactive returns node name for valid selection."""
        from sxd_core.ops.cluster import NodeInfo
        from sxd_core.ops.remote import select_node_interactive

        nodes = [
            NodeInfo("master", "10.0.0.1", "22", "admin", "master", True, True),
            NodeInfo("worker1", "10.0.0.2", "22", "admin", "worker", True, False),
        ]

        with patch("sxd_core.ops.remote.load_inventory_nodes", return_value=nodes):
            with patch("builtins.input", return_value="2"):
                result = select_node_interactive()

        assert result == "worker1"

    def test_get_cluster_node_status_success(self, tmp_path, monkeypatch):
        """get_cluster_node_status parses ansible output."""
        from sxd_core.ops.remote import get_cluster_node_status

        monkeypatch.chdir(tmp_path)
        (tmp_path / ".temp").mkdir()
        # Optional vars file
        (tmp_path / ".temp" / "ansible_vars.yaml").write_text("secret: value")

        (tmp_path / "deploy" / "ansible").mkdir(parents=True)
        (tmp_path / "deploy" / "ansible" / "inventory.yml").write_text("---")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="node1 | SUCCESS => active\nnode2 | SUCCESS => active",
            )
            result = get_cluster_node_status()

        assert "nodes" in result
        assert "node1" in result["nodes"]

    def test_get_cluster_node_status_timeout(self, tmp_path, monkeypatch):
        """get_cluster_node_status handles timeout."""
        from sxd_core.ops.remote import get_cluster_node_status

        monkeypatch.chdir(tmp_path)
        (tmp_path / ".temp").mkdir()
        (tmp_path / ".temp" / ".vault_pass").write_text("secret")

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("cmd", 30)
            result = get_cluster_node_status()

        assert "error" in result
        assert "timed out" in result["error"]

    def test_provision_nodes_cancelled(self):
        """provision_nodes handles cancellation."""
        from sxd_core.ops.remote import provision_nodes

        with patch("sxd_core.ops.remote.select_node_interactive", return_value=None):
            provision_nodes()  # Should not raise

    def test_deploy_code_cancelled(self):
        """deploy_code handles cancellation."""
        from sxd_core.ops.remote import deploy_code

        with patch("sxd_core.ops.remote.select_node_interactive", return_value=None):
            deploy_code()  # Should not raise


# =============================================================================
# Temporal Module Extended Tests
# =============================================================================


class TestTemporalModuleExtended:
    """Extended tests for Temporal operations."""

    @pytest.mark.asyncio
    async def test_get_workers_async_parses_pollers(self):
        """_get_workers_async parses poller information."""
        from sxd_core.ops.temporal import _get_workers_async

        mock_client = AsyncMock()

        # Mock workflow pollers response
        workflow_poller = MagicMock()
        workflow_poller.identity = "worker-1@host"
        workflow_poller.last_access_time = None

        activity_poller = MagicMock()
        activity_poller.identity = "worker-1@host"
        activity_poller.last_access_time = None

        workflow_desc = MagicMock()
        workflow_desc.pollers = [workflow_poller]

        activity_desc = MagicMock()
        activity_desc.pollers = [activity_poller]

        mock_client.workflow_service.describe_task_queue = AsyncMock(
            side_effect=[workflow_desc, activity_desc]
        )

        with patch("sxd_core.ops.temporal.get_config") as mock_config:
            mock_config.return_value.get_temporal_config.return_value = {
                "host": "localhost",
                "port": 7233,
                "namespace": "default",
                "task_queue": "test-queue",
            }
            with patch("temporalio.client.Client.connect", return_value=mock_client):
                result = await _get_workers_async("test-queue")

        assert result.task_queue == "test-queue"
        assert len(result.workflow_pollers) == 1
        assert result.workflow_pollers[0].identity == "worker-1@host"

    @pytest.mark.asyncio
    async def test_get_workflow_status_async_completed(self):
        """_get_workflow_status_async returns completed workflow."""
        from sxd_core.ops.temporal import _get_workflow_status_async

        mock_client = MagicMock()
        mock_handle = MagicMock()

        mock_desc = MagicMock()
        mock_desc.run_id = "run-123"
        mock_desc.status.name = "COMPLETED"
        mock_desc.start_time = datetime.now()
        mock_desc.close_time = datetime.now()

        # Use AsyncMock for async methods
        mock_handle.describe = AsyncMock(return_value=mock_desc)
        mock_handle.result = AsyncMock(return_value={"key": "value"})
        mock_client.get_workflow_handle.return_value = mock_handle

        with patch("sxd_core.ops.temporal.get_config") as mock_config:
            mock_config.return_value.get_temporal_config.return_value = {
                "host": "localhost",
                "port": 7233,
                "namespace": "default",
            }
            with patch(
                "temporalio.client.Client.connect",
                new_callable=AsyncMock,
                return_value=mock_client,
            ):
                result = await _get_workflow_status_async("wf-123")

        assert result.workflow_id == "wf-123"
        assert result.status == "COMPLETED"
        assert result.result == {"key": "value"}

    @pytest.mark.asyncio
    async def test_get_workflow_status_async_failed(self):
        """_get_workflow_status_async returns failed workflow with error."""
        from sxd_core.ops.temporal import _get_workflow_status_async

        mock_client = MagicMock()
        mock_handle = MagicMock()

        mock_desc = MagicMock()
        mock_desc.run_id = "run-123"
        mock_desc.status.name = "FAILED"
        mock_desc.start_time = datetime.now()
        mock_desc.close_time = datetime.now()

        # Use AsyncMock for async methods
        mock_handle.describe = AsyncMock(return_value=mock_desc)
        mock_handle.result = AsyncMock(
            side_effect=Exception("Workflow failed: timeout")
        )
        mock_client.get_workflow_handle.return_value = mock_handle

        with patch("sxd_core.ops.temporal.get_config") as mock_config:
            mock_config.return_value.get_temporal_config.return_value = {
                "host": "localhost",
                "port": 7233,
                "namespace": "default",
            }
            with patch(
                "temporalio.client.Client.connect",
                new_callable=AsyncMock,
                return_value=mock_client,
            ):
                result = await _get_workflow_status_async("wf-123")

        assert result.status == "FAILED"
        assert "timeout" in result.failure

    @pytest.mark.asyncio
    async def test_get_workflow_status_async_not_found(self):
        """_get_workflow_status_async returns None for missing workflow."""
        from sxd_core.ops.temporal import _get_workflow_status_async

        mock_client = MagicMock()
        mock_handle = MagicMock()
        mock_handle.describe = AsyncMock(
            side_effect=Exception("NotFound: no workflow execution")
        )
        mock_client.get_workflow_handle.return_value = mock_handle

        with patch("sxd_core.ops.temporal.get_config") as mock_config:
            mock_config.return_value.get_temporal_config.return_value = {
                "host": "localhost",
                "port": 7233,
                "namespace": "default",
            }
            with patch(
                "temporalio.client.Client.connect",
                new_callable=AsyncMock,
                return_value=mock_client,
            ):
                result = await _get_workflow_status_async("wf-missing")

        assert result is None


# =============================================================================
# Metrics Module Extended Tests
# =============================================================================


class TestMetricsModuleExtended:
    """Extended tests for metrics operations."""

    def test_get_24h_stats_success(self):
        """get_24h_stats returns parsed statistics."""
        from sxd_core.ops.metrics import get_24h_stats

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.side_effect = [
            [
                {
                    "total": 100,
                    "successful": 95,
                    "failed": 5,
                    "avg_quality": 0.85,
                    "total_size": 1024000,
                }
            ],
            [{"completed": 10, "in_progress": 2}],
            [{"completed": 50}],
        ]

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_24h_stats()

        assert result.videos_processed == 100
        assert result.videos_successful == 95
        assert result.success_rate == 95.0
        assert result.batches_completed == 10
        assert result.uploads_completed == 50

    def test_get_24h_stats_empty_results(self):
        """get_24h_stats handles empty results."""
        from sxd_core.ops.metrics import get_24h_stats

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.side_effect = [[], [], []]

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_24h_stats()

        assert result.videos_processed == 0
        assert result.success_rate == 0.0

    def test_get_24h_stats_exception(self):
        """get_24h_stats returns zeros on exception."""
        from sxd_core.ops.metrics import get_24h_stats

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.side_effect = Exception("Connection failed")

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_24h_stats()

        assert result.videos_processed == 0
        assert result.success_rate == 0.0

    def test_get_error_summary_success(self):
        """get_error_summary returns parsed errors."""
        from sxd_core.ops.metrics import get_error_summary

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.return_value = [
            {
                "activity": "download_video",
                "error_count": 10,
                "last_error_time": datetime.now(),
                "sample_message": "Connection timed out",
            },
            {
                "activity": "process_frames",
                "error_count": 5,
                "last_error_time": datetime.now(),
                "sample_message": "Out of memory",
            },
        ]

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_error_summary(limit=10)

        assert len(result) == 2
        assert result[0].activity == "download_video"
        assert result[0].error_count == 10

    def test_get_error_summary_exception(self):
        """get_error_summary returns empty list on exception."""
        from sxd_core.ops.metrics import get_error_summary

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.side_effect = Exception("Query failed")

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_error_summary()

        assert result == []

    def test_get_storage_stats_success(self):
        """get_storage_stats returns parsed stats."""
        from sxd_core.ops.metrics import get_storage_stats

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.return_value = [
            {
                "table": "videos",
                "size_bytes": 500000000,
                "size_readable": "500 MB",
                "row_count": 10000,
            },
            {
                "table": "logs",
                "size_bytes": 100000000,
                "size_readable": "100 MB",
                "row_count": 500000,
            },
        ]

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_storage_stats()

        assert len(result) == 2
        assert result[0].table == "videos"
        assert result[0].size_bytes == 500000000

    def test_get_storage_stats_exception(self):
        """get_storage_stats returns empty list on exception."""
        from sxd_core.ops.metrics import get_storage_stats

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.side_effect = Exception("Query failed")

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_storage_stats()

        assert result == []

    def test_get_log_counts_success(self):
        """get_log_counts returns log level counts."""
        from sxd_core.ops.metrics import get_log_counts

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.return_value = [
            {"level": "INFO", "cnt": 1000},
            {"level": "ERROR", "cnt": 50},
            {"level": "WARNING", "cnt": 100},
        ]

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_log_counts()

        assert result["INFO"] == 1000
        assert result["ERROR"] == 50

    def test_get_log_counts_exception(self):
        """get_log_counts returns empty dict on exception."""
        from sxd_core.ops.metrics import get_log_counts

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.side_effect = Exception("Query failed")

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_log_counts()

        assert result == {}

    def test_get_recent_activity_success(self):
        """get_recent_activity returns audit events."""
        from sxd_core.ops.metrics import get_recent_activity

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.return_value = [
            {
                "timestamp": datetime.now(),
                "actor": "user@example.com",
                "action": "submit_video",
                "target": "video-123",
                "status": "success",
            }
        ]

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_recent_activity(limit=10)

        assert len(result) == 1
        assert result[0]["action"] == "submit_video"

    def test_get_recent_activity_exception(self):
        """get_recent_activity returns empty list on exception."""
        from sxd_core.ops.metrics import get_recent_activity

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.side_effect = Exception("Query failed")

        with patch(
            "sxd_core.ops.metrics._get_clickhouse_manager", return_value=mock_ch
        ):
            result = get_recent_activity()

        assert result == []


# =============================================================================
# ClickHouse Module Tests
# =============================================================================


@pytest.fixture
def clean_clickhouse_env(monkeypatch):
    """Clean ClickHouse environment variables and restore real ClickHouseManager."""
    import importlib

    import sxd_core.clickhouse

    # Clean environment variables
    monkeypatch.delenv("SXD_CLICKHOUSE_HOST", raising=False)
    monkeypatch.delenv("CLICKHOUSE_HOST", raising=False)
    monkeypatch.delenv("SXD_CLICKHOUSE_PORT", raising=False)
    monkeypatch.delenv("CLICKHOUSE_PORT", raising=False)
    monkeypatch.delenv("SXD_CLICKHOUSE_USER", raising=False)
    monkeypatch.delenv("CLICKHOUSE_USER", raising=False)
    monkeypatch.delenv("SXD_CLICKHOUSE_PASSWORD", raising=False)
    monkeypatch.delenv("CLICKHOUSE_PASSWORD", raising=False)

    # Reload the module to ensure we have the real ClickHouseManager
    # (in case it was patched by MockRegistry in other tests)
    importlib.reload(sxd_core.clickhouse)


class TestClickHouseManager:
    """Tests for ClickHouseManager class."""

    def test_init_with_defaults(self, clean_clickhouse_env):
        """ClickHouseManager uses defaults when no config."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()

        assert mgr.host == "127.0.0.1"
        assert mgr.port == 8123
        assert mgr.database == "sxd"

    def test_init_with_env_vars(self, clean_clickhouse_env, monkeypatch):
        """ClickHouseManager uses environment variables."""
        monkeypatch.setenv("SXD_CLICKHOUSE_HOST", "ch.example.com")
        monkeypatch.setenv("SXD_CLICKHOUSE_PORT", "9000")
        monkeypatch.setenv("SXD_CLICKHOUSE_USER", "admin")
        monkeypatch.setenv("SXD_CLICKHOUSE_PASSWORD", "secret")

        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()

        assert mgr.host == "ch.example.com"
        assert mgr.port == 9000
        assert mgr.user == "admin"
        assert mgr.password == "secret"

    def test_init_with_explicit_params(self, clean_clickhouse_env, monkeypatch):
        """ClickHouseManager uses explicit parameters over env."""
        monkeypatch.setenv("SXD_CLICKHOUSE_HOST", "env-host")

        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager(
            host="param-host", port=9999, user="paramuser", password="parampass"
        )

        assert mgr.host == "param-host"
        assert mgr.port == 9999
        assert mgr.user == "paramuser"
        assert mgr.password == "parampass"

    def test_client_property_connection_failure(self, clean_clickhouse_env):
        """client property returns None on connection failure."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager(host="nonexistent-host", port=9999)

        with patch("clickhouse_connect.get_client") as mock_get:
            mock_get.side_effect = Exception("Connection refused")
            result = mgr.client

        assert result is None

    def test_client_property_caches_connection(self, clean_clickhouse_env):
        """client property caches the connection."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()

        with patch(
            "clickhouse_connect.get_client", return_value=mock_client
        ) as mock_get:
            client1 = mgr.client
            client2 = mgr.client

        # Should only call get_client once
        mock_get.assert_called_once()
        assert client1 is client2

    def test_insert_logs(self, clean_clickhouse_env):
        """insert_logs inserts rows into logs table."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()
        mgr._client = mock_client

        rows = [[datetime.now(), "INFO", "test", "Test message", "", "", "", "{}"]]
        mgr.insert_logs(rows)

        mock_client.insert.assert_called_once()
        call_args = mock_client.insert.call_args
        assert "logs" in call_args[0][0]

    def test_insert_logs_no_client(self, clean_clickhouse_env):
        """insert_logs does nothing when no client."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mgr._client = None

        # Mock the client property to return None
        with patch.object(
            ClickHouseManager,
            "client",
            new_callable=lambda: property(lambda self: None),
        ):
            mgr.insert_logs([])  # Should not raise

    def test_insert_audit_events(self, clean_clickhouse_env):
        """insert_audit_events inserts rows into audit_events table."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()
        mgr._client = mock_client

        rows = [
            [
                datetime.now(),
                "user",
                "action",
                "target",
                "success",
                "prod",
                "1.2.3.4",
                "",
                "{}",
            ]
        ]
        mgr.insert_audit_events(rows)

        mock_client.insert.assert_called_once()
        call_args = mock_client.insert.call_args
        assert "audit_events" in call_args[0][0]

    def test_insert_telemetry(self, clean_clickhouse_env):
        """insert_telemetry inserts rows into telemetry table."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()
        mgr._client = mock_client

        rows = [[datetime.now(), "metric_name", 1.0, {"tag": "value"}]]
        mgr.insert_telemetry(rows)

        mock_client.insert.assert_called_once()
        call_args = mock_client.insert.call_args
        assert "telemetry" in call_args[0][0]

    def test_upsert_video_metadata(self, clean_clickhouse_env):
        """upsert_video_metadata inserts video data."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()
        mgr._client = mock_client

        data = {
            "id": "video-123",
            "customer_id": "cust-1",
            "video_id": "vid-123",
            "source_url": "http://example.com/video.mp4",
            "status": "COMPLETED",
            "quality_score": 0.95,
        }
        result = mgr.upsert_video_metadata(data)

        assert result == "video-123"
        mock_client.insert.assert_called_once()

    def test_upsert_video_metadata_no_client(self, clean_clickhouse_env):
        """upsert_video_metadata returns id when no client."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mgr._client = None

        # Mock the client property to return None
        with patch.object(
            ClickHouseManager,
            "client",
            new_callable=lambda: property(lambda self: None),
        ):
            result = mgr.upsert_video_metadata({"id": "test-id"})

        assert result == "test-id"

    def test_upsert_batch_metadata(self, clean_clickhouse_env):
        """upsert_batch_metadata inserts batch data."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()
        mgr._client = mock_client

        data = {
            "id": "batch-123",
            "customer_id": "cust-1",
            "tar_url": "http://example.com/videos.tar",
            "status": "COMPLETED",
            "total_videos": 10,
        }
        result = mgr.upsert_batch_metadata(data)

        assert result == "batch-123"
        mock_client.insert.assert_called_once()

    def test_upsert_episode(self, clean_clickhouse_env):
        """upsert_episode inserts episode data."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()
        mgr._client = mock_client

        data = {
            "id": "ep-123",
            "customer_id": "cust-1",
            "source_path": "/data/videos",
            "total_size": 1024000,
            "chunk_count": 5,
        }
        result = mgr.upsert_episode(data)

        assert result == "ep-123"
        mock_client.insert.assert_called_once()

    def test_upsert_chunk(self, clean_clickhouse_env):
        """upsert_chunk inserts chunk data."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()
        mgr._client = mock_client

        data = {
            "episode_id": "ep-123",
            "chunk_index": 0,
            "file_name": "chunk_0.tar",
            "size_bytes": 102400,
            "status": "COMPLETED",
        }
        mgr.upsert_chunk(data)

        mock_client.insert.assert_called_once()

    def test_execute_query_success(self, clean_clickhouse_env):
        """execute_query returns list of dicts."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()
        mock_result = MagicMock()
        mock_result.named_results.return_value = iter(
            [{"col1": "val1"}, {"col1": "val2"}]
        )
        mock_client.query.return_value = mock_result
        mgr._client = mock_client

        result = mgr.execute_query("SELECT * FROM test")

        assert len(result) == 2
        assert result[0]["col1"] == "val1"

    def test_execute_query_no_client(self, clean_clickhouse_env):
        """execute_query returns empty list when no client."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mgr._client = None

        # Mock the client property to return None
        with patch.object(
            ClickHouseManager,
            "client",
            new_callable=lambda: property(lambda self: None),
        ):
            result = mgr.execute_query("SELECT 1")

        assert result == []

    def test_execute_query_error(self, clean_clickhouse_env):
        """execute_query raises on query failure."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        mock_client = MagicMock()
        mock_client.query.side_effect = Exception("Query syntax error")
        mgr._client = mock_client

        with pytest.raises(Exception) as exc_info:
            mgr.execute_query("INVALID QUERY")

        assert "Query syntax error" in str(exc_info.value)

    def test_list_videos(self, clean_clickhouse_env):
        """list_videos calls execute_query with correct SQL."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()

        with patch.object(mgr, "execute_query", return_value=[]) as mock_query:
            mgr.list_videos(limit=10, offset=5)

        mock_query.assert_called_once()
        query = mock_query.call_args[0][0]
        assert "videos" in query
        assert "LIMIT 10" in query
        assert "OFFSET 5" in query

    def test_list_batches(self, clean_clickhouse_env):
        """list_batches calls execute_query with correct SQL."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()

        with patch.object(mgr, "execute_query", return_value=[]) as mock_query:
            mgr.list_batches(limit=20)

        mock_query.assert_called_once()
        query = mock_query.call_args[0][0]
        assert "batches" in query
        assert "LIMIT 20" in query

    def test_list_episodes(self, clean_clickhouse_env):
        """list_episodes calls execute_query with correct SQL."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()

        with patch.object(mgr, "execute_query", return_value=[]) as mock_query:
            mgr.list_episodes(limit=15)

        mock_query.assert_called_once()
        query = mock_query.call_args[0][0]
        assert "episodes" in query
        assert "LIMIT 15" in query

    def test_get_video_found(self, clean_clickhouse_env):
        """get_video returns video when found."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()
        video_data = {"id": "vid-123", "status": "COMPLETED"}

        with patch.object(mgr, "execute_query", return_value=[video_data]):
            result = mgr.get_video("vid-123")

        assert result == video_data

    def test_get_video_not_found(self, clean_clickhouse_env):
        """get_video returns None when not found."""
        from sxd_core.clickhouse import ClickHouseManager

        mgr = ClickHouseManager()

        with patch.object(mgr, "execute_query", return_value=[]):
            result = mgr.get_video("nonexistent")

        assert result is None

    def test_init_db(self, clean_clickhouse_env):
        """init_db creates database and tables."""
        from sxd_core.clickhouse import ClickHouseManager

        mock_client = MagicMock()

        with patch("clickhouse_connect.get_client", return_value=mock_client):
            mgr = ClickHouseManager()
            mgr.init_db()

        # Should have called command multiple times for CREATE statements
        assert mock_client.command.call_count >= 7  # DB + 6 tables


# =============================================================================
# Cluster Module Tests
# =============================================================================


class TestClusterModule:
    """Tests for cluster operations."""

    def test_node_info_dataclass(self):
        """NodeInfo dataclass works correctly."""
        from sxd_core.ops.cluster import NodeInfo

        node = NodeInfo(
            name="sxd-master",
            host="10.0.0.1",
            port="22",
            user="admin",
            node_type="master",
            run_worker=True,
            run_infra=True,
        )

        assert node.name == "sxd-master"
        assert node.node_type == "master"
        assert node.run_infra is True

    def test_service_status_dataclass(self):
        """ServiceStatus dataclass works correctly."""
        from sxd_core.ops.cluster import ServiceStatus

        status = ServiceStatus(
            name="temporal",
            display_name="Temporal",
            port="7233",
            status="running",
            health="healthy",
        )

        assert status.status == "running"
        assert status.health == "healthy"

    def test_cluster_info_dataclass(self):
        """ClusterInfo dataclass works correctly."""
        from sxd_core.ops.cluster import ClusterInfo

        info = ClusterInfo(
            master_host="10.0.0.1",
            master_port="22",
            nodes=[],
            services=[],
            temporal_connected=True,
            clickhouse_connected=True,
        )

        assert info.temporal_connected is True
        assert info.clickhouse_connected is True

    def test_check_port_connectivity_success(self):
        """check_port_connectivity returns True for open port."""
        from sxd_core.ops.cluster import check_port_connectivity

        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_sock.connect_ex.return_value = 0
            mock_socket.return_value = mock_sock

            result = check_port_connectivity("localhost", 8080)

        assert result is True

    def test_check_port_connectivity_failure(self):
        """check_port_connectivity returns False for closed port."""
        from sxd_core.ops.cluster import check_port_connectivity

        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_sock.connect_ex.return_value = 1
            mock_socket.return_value = mock_sock

            result = check_port_connectivity("localhost", 8080)

        assert result is False

    def test_load_inventory_nodes_no_file(self, tmp_path, monkeypatch):
        """load_inventory_nodes returns empty list when file doesn't exist."""
        from sxd_core.ops.cluster import load_inventory_nodes

        monkeypatch.chdir(tmp_path)
        result = load_inventory_nodes()
        assert result == []
