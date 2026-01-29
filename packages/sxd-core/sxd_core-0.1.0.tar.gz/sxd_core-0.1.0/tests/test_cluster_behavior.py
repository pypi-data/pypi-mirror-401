"""
Behavioral tests for cluster operations.

These tests verify the observable behavior of cluster discovery,
node management, and service health checking - not implementation details.
Focus areas:
- Node discovery from inventory
- Service connectivity checks
- Cluster health aggregation
"""

import socket
from unittest.mock import MagicMock, patch

from sxd_core.ops.cluster import (
    ClusterInfo,
    NodeInfo,
    ServiceStatus,
    check_port_connectivity,
    get_cluster_info,
    get_docker_service_status,
    get_node_status,
    load_inventory_nodes,
)

# =============================================================================
# Node Discovery - Behavioral Tests
# =============================================================================


class TestNodeDiscovery:
    """Test that node discovery correctly parses inventory files."""

    def test_loads_master_and_worker_nodes(self, tmp_path, monkeypatch):
        """Both master and worker nodes are discovered from inventory."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text(
            """
all:
  vars:
    ansible_user: admin
    ansible_port: 22
  children:
    master:
      hosts:
        sxd-master:
          ansible_host: 10.0.0.1
          run_infra: true
    workers:
      hosts:
        sxd-worker-1:
          ansible_host: 10.0.0.2
          run_worker: true
        sxd-worker-2:
          ansible_host: 10.0.0.3
          run_worker: true
"""
        )

        monkeypatch.chdir(tmp_path)

        nodes = load_inventory_nodes()

        assert len(nodes) == 3
        master_nodes = [n for n in nodes if n.node_type == "master"]
        worker_nodes = [n for n in nodes if n.node_type == "worker"]
        assert len(master_nodes) == 1
        assert len(worker_nodes) == 2

    def test_uses_default_ssh_settings(self, tmp_path, monkeypatch):
        """Default SSH user and port are applied when not specified per-host."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text(
            """
all:
  vars:
    ansible_user: defaultuser
    ansible_port: 3671
  children:
    master:
      hosts:
        sxd-master:
          ansible_host: 10.0.0.1
"""
        )

        monkeypatch.chdir(tmp_path)

        nodes = load_inventory_nodes()

        assert len(nodes) == 1
        assert nodes[0].user == "defaultuser"
        assert nodes[0].port == "3671"

    def test_per_host_settings_override_defaults(self, tmp_path, monkeypatch):
        """Per-host SSH settings override global defaults."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text(
            """
all:
  vars:
    ansible_user: defaultuser
    ansible_port: 22
  children:
    workers:
      hosts:
        custom-worker:
          ansible_host: 10.0.0.5
          ansible_user: customuser
          ansible_port: 2222
"""
        )

        monkeypatch.chdir(tmp_path)

        nodes = load_inventory_nodes()

        assert len(nodes) == 1
        assert nodes[0].user == "customuser"
        assert nodes[0].port == "2222"

    def test_missing_inventory_returns_empty_list(self, tmp_path, monkeypatch):
        """Missing inventory file returns empty node list."""
        monkeypatch.chdir(tmp_path)

        nodes = load_inventory_nodes()

        assert nodes == []

    def test_malformed_inventory_returns_empty_list(self, tmp_path, monkeypatch):
        """Malformed YAML returns empty node list."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text("not: valid: yaml: content: [[[")

        monkeypatch.chdir(tmp_path)

        nodes = load_inventory_nodes()

        assert nodes == []

    def test_node_info_captures_role_flags(self, tmp_path, monkeypatch):
        """Node roles (run_worker, run_infra) are captured."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text(
            """
all:
  children:
    master:
      hosts:
        infra-node:
          ansible_host: 10.0.0.1
          run_infra: true
          run_worker: false
    workers:
      hosts:
        compute-node:
          ansible_host: 10.0.0.2
          run_worker: true
          run_infra: false
"""
        )

        monkeypatch.chdir(tmp_path)

        nodes = load_inventory_nodes()

        infra_node = next(n for n in nodes if n.name == "infra-node")
        compute_node = next(n for n in nodes if n.name == "compute-node")

        assert infra_node.run_infra is True
        assert infra_node.run_worker is False
        assert compute_node.run_worker is True
        assert compute_node.run_infra is False


# =============================================================================
# Port Connectivity - Behavioral Tests
# =============================================================================


class TestPortConnectivity:
    """Test port connectivity checking behavior."""

    def test_reachable_port_returns_true(self):
        """Reachable port returns True."""
        with patch("socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_instance.connect_ex.return_value = 0
            mock_socket.return_value = mock_instance

            result = check_port_connectivity("localhost", 8080)

        assert result is True

    def test_unreachable_port_returns_false(self):
        """Unreachable port returns False."""
        with patch("socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_instance.connect_ex.return_value = 111  # Connection refused
            mock_socket.return_value = mock_instance

            result = check_port_connectivity("localhost", 9999)

        assert result is False

    def test_connection_timeout_returns_false(self):
        """Socket timeout returns False."""
        with patch("socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_instance.connect_ex.side_effect = socket.timeout("timed out")
            mock_socket.return_value = mock_instance

            result = check_port_connectivity("unreachable.host", 80)

        assert result is False

    def test_dns_failure_returns_false(self):
        """DNS resolution failure returns False."""
        with patch("socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_instance.connect_ex.side_effect = socket.gaierror(
                "Name resolution failed"
            )
            mock_socket.return_value = mock_instance

            result = check_port_connectivity("nonexistent.domain.invalid", 80)

        assert result is False

    def test_respects_timeout_parameter(self):
        """Timeout parameter is passed to socket."""
        with patch("socket.socket") as mock_socket:
            mock_instance = MagicMock()
            mock_instance.connect_ex.return_value = 0
            mock_socket.return_value = mock_instance

            check_port_connectivity("localhost", 80, timeout=5.0)

        mock_instance.settimeout.assert_called_with(5.0)


# =============================================================================
# Docker Service Status - Behavioral Tests
# =============================================================================


class TestDockerServiceStatus:
    """Test Docker container status detection."""

    def test_running_container_detected(self):
        """Running container is detected with correct status."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="running\n")

            result = get_docker_service_status("my-container", "My Service", "8080")

        assert result.status == "running"
        assert result.display_name == "My Service"
        assert result.port == "8080"

    def test_stopped_container_detected(self):
        """Stopped container is detected."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="exited\n")

            result = get_docker_service_status("stopped-container", "Stopped", "80")

        assert result.status == "exited"

    def test_nonexistent_container_detected(self):
        """Non-existent container returns not_found status."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="")

            result = get_docker_service_status("missing-container", "Missing", "80")

        assert result.status == "not_found"

    def test_container_health_status_captured(self):
        """Container health status is captured when available."""
        with patch("subprocess.run") as mock_run:
            # First call: container status, Second call: health status
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="running\n"),
                MagicMock(returncode=0, stdout="healthy\n"),
            ]

            result = get_docker_service_status("healthy-container", "Healthy", "80")

        assert result.status == "running"
        assert result.health == "healthy"

    def test_docker_command_timeout_returns_unknown(self):
        """Docker command timeout returns unknown status."""
        import subprocess

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("docker", 5)

            result = get_docker_service_status("slow-container", "Slow", "80")

        assert result.status == "unknown"


# =============================================================================
# Node Status - Behavioral Tests
# =============================================================================


class TestNodeStatus:
    """Test node status aggregation."""

    def test_returns_status_for_all_nodes(self, tmp_path, monkeypatch):
        """Status is returned for all discovered nodes."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text(
            """
all:
  children:
    master:
      hosts:
        master-1:
          ansible_host: 10.0.0.1
    workers:
      hosts:
        worker-1:
          ansible_host: 10.0.0.2
        worker-2:
          ansible_host: 10.0.0.3
"""
        )

        monkeypatch.chdir(tmp_path)

        # No vault file, should return unknown status
        result = get_node_status()

        assert len(result) == 3
        node_names = {n["name"] for n in result}
        assert "master-1" in node_names
        assert "worker-1" in node_names
        assert "worker-2" in node_names

    def test_returns_unknown_without_vault_file(self, tmp_path, monkeypatch):
        """Returns unknown status when vault password file is missing."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text(
            """
all:
  children:
    master:
      hosts:
        node-1:
          ansible_host: 10.0.0.1
"""
        )

        monkeypatch.chdir(tmp_path)

        result = get_node_status()

        assert len(result) == 1
        assert result[0]["worker_status"] == "unknown"

    def test_parses_systemd_status_from_ansible(self, tmp_path, monkeypatch):
        """Parses systemd service status from Ansible output."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text(
            """
all:
  children:
    workers:
      hosts:
        worker-1:
          ansible_host: 10.0.0.1
          run_worker: true
"""
        )

        (tmp_path / ".temp").mkdir()
        (tmp_path / ".temp" / ".vault_pass").write_text("secret")

        monkeypatch.chdir(tmp_path)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout="worker-1 | SUCCESS | rc=0 | (stdout) active\n"
            )

            result = get_node_status()

        assert len(result) == 1
        assert result[0]["worker_status"] == "active"


# =============================================================================
# Cluster Info Aggregation - Behavioral Tests
# =============================================================================


class TestClusterInfoAggregation:
    """Test overall cluster information gathering."""

    def test_aggregates_nodes_and_services(self, tmp_path, monkeypatch):
        """Cluster info includes both nodes and service status."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text(
            """
all:
  children:
    master:
      hosts:
        master-node:
          ansible_host: 192.168.1.1
"""
        )

        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("SXD_COMPOSE_PROJECT_NAME", "test")

        with patch("sxd_core.ops.cluster.get_config") as mock_config:
            mock_config.return_value.get_temporal_config.return_value = {
                "host": "192.168.1.1",
                "port": 7233,
                "namespace": "default",
            }
            mock_config.return_value.get_clickhouse_config.return_value = {
                "host": "192.168.1.1",
                "port": 8123,
            }
            mock_config.return_value.is_local_client.return_value = False

            with patch("sxd_core.ops.cluster.get_service_status") as mock_services:
                mock_services.return_value = [
                    ServiceStatus("temporal", "Temporal", "7233", "running"),
                ]

                with patch("sxd_core.ops.cluster.check_port_connectivity") as mock_conn:
                    mock_conn.return_value = True

                    info = get_cluster_info()

        assert len(info.nodes) == 1
        assert len(info.services) == 1
        assert info.temporal_connected is True

    def test_connectivity_checks_use_correct_hosts(self, tmp_path, monkeypatch):
        """Connectivity checks target the correct service hosts."""
        inventory = tmp_path / "deploy" / "ansible" / "inventory.yml"
        inventory.parent.mkdir(parents=True)
        inventory.write_text("all:\n  children: {}")

        monkeypatch.chdir(tmp_path)

        connectivity_checks = []

        def track_connectivity(host, port, **kwargs):
            connectivity_checks.append((host, port))
            return True

        with patch("sxd_core.ops.cluster.get_config") as mock_config:
            mock_config.return_value.get_temporal_config.return_value = {
                "host": "temporal.example.com",
                "port": 7233,
                "namespace": "default",
            }
            mock_config.return_value.get_clickhouse_config.return_value = {
                "host": "clickhouse.example.com",
                "port": 8123,
            }
            mock_config.return_value.is_local_client.return_value = False

            with patch("sxd_core.ops.cluster.get_service_status", return_value=[]):
                with patch(
                    "sxd_core.ops.cluster.check_port_connectivity",
                    side_effect=track_connectivity,
                ):
                    get_cluster_info()

        # Should have checked both Temporal and ClickHouse
        hosts_checked = {h for h, _ in connectivity_checks}
        assert "temporal.example.com" in hosts_checked
        assert "clickhouse.example.com" in hosts_checked


# =============================================================================
# Data Classes - Contract Tests
# =============================================================================


class TestDataClassContracts:
    """Test that data classes have expected fields and behavior."""

    def test_node_info_has_all_required_fields(self):
        """NodeInfo contains all required fields."""
        node = NodeInfo(
            name="test-node",
            host="10.0.0.1",
            port="22",
            user="admin",
            node_type="worker",
            run_worker=True,
            run_infra=False,
        )

        assert node.name == "test-node"
        assert node.host == "10.0.0.1"
        assert node.port == "22"
        assert node.user == "admin"
        assert node.node_type == "worker"
        assert node.run_worker is True
        assert node.run_infra is False

    def test_service_status_has_all_required_fields(self):
        """ServiceStatus contains all required fields."""
        status = ServiceStatus(
            name="container-name",
            display_name="Display Name",
            port="8080",
            status="running",
            health="healthy",
        )

        assert status.name == "container-name"
        assert status.display_name == "Display Name"
        assert status.port == "8080"
        assert status.status == "running"
        assert status.health == "healthy"

    def test_cluster_info_has_all_required_fields(self):
        """ClusterInfo contains all required fields."""
        info = ClusterInfo(
            master_host="10.0.0.1",
            master_port="22",
            nodes=[],
            services=[],
            temporal_connected=True,
            clickhouse_connected=False,
        )

        assert info.master_host == "10.0.0.1"
        assert info.master_port == "22"
        assert info.nodes == []
        assert info.services == []
        assert info.temporal_connected is True
        assert info.clickhouse_connected is False
