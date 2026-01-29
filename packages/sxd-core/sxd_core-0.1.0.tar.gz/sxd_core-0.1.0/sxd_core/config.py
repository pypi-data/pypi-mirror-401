"""
Centralized configuration management for SXD platform.

This module provides a single source of truth for all configuration,
eliminating duplication across sxd.py, sxdt.py, and ops modules.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ConfigManager:
    """Singleton configuration manager for SXD platform."""

    _instance: Optional["ConfigManager"] = None
    _config: Optional[Dict[str, Any]] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize configuration manager."""
        if self._config is None:
            self._config = self._load_config()

    @property
    def config_dir_path(self) -> Path:
        """Get the directory containing configuration files."""
        return self._find_config_path().parent

    def _find_config_path(self) -> Path:
        """Find the settings.yaml file in the repository."""
        # Start from this file and search upward for config/settings.yaml
        current = Path(__file__).resolve()

        # Search up to 5 levels
        for _ in range(5):
            current = current.parent
            config_path = current / "config" / "settings.yaml"
            if config_path.exists():
                return config_path

        # Fallback: assume we're in a standard location
        return Path(__file__).parent.parent.parent.parent / "config" / "settings.yaml"

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from settings.yaml."""
        config_path = self._find_config_path()

        if not config_path.exists():
            # Return minimal defaults if config doesn't exist
            return {
                "temporal": {
                    "host": "localhost",
                    "port": 7233,
                    "namespace": "default",
                    "task_queue": "video-processing",
                },
                "storage": {
                    "backend": "local",
                    "endpoint": "http://localhost:8333",
                    "base_path": "/data",
                },
                "clickhouse": {
                    "host": "localhost",
                    "port": 8123,
                    "database": "sxd",
                },
            }

        from sxd_core import io

        with io.open_file(config_path) as f:
            return yaml.safe_load(f) or {}

    def reload(self) -> None:
        """Reload configuration from disk."""
        self._config = self._load_config()

    @property
    def config(self) -> Dict[str, Any]:
        """Get the full configuration dictionary."""
        return self._config or {}

    # --- Temporal Configuration ---

    def get_temporal_config(self) -> Dict[str, Any]:
        """Get Temporal connection configuration."""
        temporal_config = self.config.get("temporal", {})

        # Check for environment overrides
        host = os.getenv("SXD_TEMPORAL_HOST") or temporal_config.get(
            "host", "localhost"
        )
        port = int(os.getenv("SXD_TEMPORAL_PORT", temporal_config.get("port", 7233)))

        return {
            "host": host,
            "port": port,
            "namespace": temporal_config.get("namespace", "default"),
            "task_queue": temporal_config.get("task_queue", "video-processing"),
        }

    def get_temporal_url(self) -> str:
        """Get Temporal URL in host:port format."""
        tc = self.get_temporal_config()
        return f"{tc['host']}:{tc['port']}"

    # --- Storage Configuration ---

    def get_storage_config(self) -> Dict[str, Any]:
        """Get storage backend configuration."""
        storage_config = self.config.get("storage", {})

        return {
            "backend": storage_config.get("backend", "local"),
            "endpoint": storage_config.get("endpoint", "http://localhost:8333"),
            "base_path": storage_config.get("base_path", "/data"),
            "scratch_path": storage_config.get("scratch_path", "/scratch"),
        }

    def get_storage_endpoint(self) -> str:
        """Get storage endpoint URL."""
        return self.get_storage_config()["endpoint"]

    # --- ClickHouse Configuration ---

    def get_clickhouse_config(self) -> Dict[str, Any]:
        """Get ClickHouse connection configuration."""
        ch_config = self.config.get("clickhouse", {})

        return {
            "host": ch_config.get("host", "localhost"),
            "port": ch_config.get("port", 8123),
            "database": ch_config.get("database", "sxd"),
            "username": ch_config.get("username", "default"),
            "password": ch_config.get("password", ""),
        }

    # --- Remote/SSH Configuration ---

    def get_remote_config(self) -> Dict[str, Any]:
        """Get remote host configuration."""
        remote_config = self.config.get("remote", {})

        return {
            "host": os.getenv("SXD_REMOTE_HOST")
            or remote_config.get("host")
            or remote_config.get("master_ip", ""),
            "user": os.getenv("SXD_REMOTE_USER")
            or remote_config.get("user", os.getenv("USER", "root")),
            "ssh_port": os.getenv("SXD_SSH_PORT")
            or remote_config.get("ssh_port", "22"),
            "ssh_key_path": os.getenv("SXD_SSH_KEY_PATH")
            or remote_config.get("ssh_key_path")
            or (
                str(Path(".temp/private_key"))
                if Path(".temp/private_key").exists()
                else None
            )
            or str(Path.home() / ".ssh" / "id_ed25519"),
            "inventory_path": remote_config.get(
                "inventory_path", "deploy/inventory.yml"
            ),
        }

    def get_ssh_key_path(self) -> str:
        """Get SSH key path for remote operations."""
        return self.get_remote_config()["ssh_key_path"]

    # --- Node Configuration ---

    def get_node_type(self) -> Optional[str]:
        """Get current node type from environment."""
        return os.getenv("SXD_NODE_TYPE")

    def is_master_node(self) -> bool:
        """Check if running on master node."""
        return self.get_node_type() == "master"

    def is_worker_node(self) -> bool:
        """Check if running on worker node."""
        return self.get_node_type() == "worker"

    def is_local_client(self) -> bool:
        """Check if running as local client (not on a node)."""
        return self.get_node_type() is None

    # --- Docker Configuration ---

    def get_execution_mode(self) -> str:
        """Get execution mode (cluster or local)."""
        return os.getenv("SXD_MODE", "cluster")

    def get_docker_config(self) -> Dict[str, Any]:
        """Get Docker Compose configuration."""
        docker_config = self.config.get("docker", {})

        return {
            "project_name": os.getenv("SXD_COMPOSE_PROJECT_NAME", "sxd"),
            "compose_file": docker_config.get(
                "compose_file", "deploy/docker-compose.yml"
            ),
            "profile": os.getenv(
                "SXD_COMPOSE_PROFILE", docker_config.get("profile", "")
            ),
        }

    # --- Gateway/Auth Configuration ---

    def get_gateway_config(self) -> Dict[str, Any]:
        """Get gateway authentication configuration."""
        gateway_config = self.config.get("gateway", {})

        return {
            "admin_username": os.getenv(
                "SXD_ADMIN_USERNAME", gateway_config.get("admin_username", "admin")
            ),
            "admin_password": os.getenv(
                "SXD_ADMIN_PASSWORD", gateway_config.get("admin_password", "")
            ),
            "htpasswd_path": Path(".temp/.htpasswd"),
        }

    # --- Backup Configuration ---

    def get_backup_config(self) -> Dict[str, Any]:
        """Get backup/maintenance configuration."""
        backup_config = self.config.get("backup", {})

        return {
            "backup_dir": Path(backup_config.get("backup_dir", "/data/backups")),
            "retention_days": backup_config.get("retention_days", 7),
            "scratch_max_age_hours": backup_config.get("scratch_max_age_hours", 24),
        }

    # --- Node Configuration ---

    def get_nodes_config(self) -> Dict[str, Dict[str, Any]]:
        """Get configuration for all cluster nodes.

        Returns:
            Dict mapping hostname to node config (cpu_cores, port, user).
        """
        return self.config.get("nodes", {})

    def get_available_nodes(self) -> list:
        """Get list of available node hostnames."""
        return list(self.get_nodes_config().keys())

    # --- Load Balancer Configuration ---

    def get_load_balancer_config(self) -> Dict[str, Any]:
        """Get load balancer configuration.

        Returns:
            Dict with weights and refresh settings.
        """
        lb_config = self.config.get("load_balancer", {})

        return {
            "weights": lb_config.get(
                "weights",
                {
                    "disk": 0.35,
                    "queue": 0.30,
                    "cpu": 0.20,
                    "balance": 0.15,
                },
            ),
            "metrics_refresh_seconds": lb_config.get("metrics_refresh_seconds", 60),
        }


# Global singleton instance
_config_manager: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get the global ConfigManager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


# Convenience functions for backward compatibility
def load_config() -> Dict[str, Any]:
    """Load configuration (legacy function for compatibility)."""
    return get_config().config


def get_temporal_config() -> Dict[str, Any]:
    """Get Temporal configuration (legacy function for compatibility)."""
    return get_config().get_temporal_config()


def get_storage_endpoint() -> str:
    """Get storage endpoint (legacy function for compatibility)."""
    return get_config().get_storage_endpoint()


def get_clickhouse_config() -> Dict[str, Any]:
    """Get ClickHouse configuration."""
    return get_config().get_clickhouse_config()


def get_execution_mode() -> str:
    """Get execution mode (cluster or local)."""
    return get_config().get_execution_mode()
