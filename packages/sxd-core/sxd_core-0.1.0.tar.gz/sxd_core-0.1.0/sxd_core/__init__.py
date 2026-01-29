"""
SXD Core - Shared infrastructure for SentientX Data Platform
"""

# Authorization
from sxd_core.auth import (
    AuthManager,
    Permission,
    Role,
    User,
    get_auth_manager,
    get_current_user,
    require_auth,
    require_permission,
)

# Configuration
from sxd_core.config import (
    ConfigManager,
    get_clickhouse_config,
    get_config,
    get_storage_endpoint,
    get_temporal_config,
    load_config,
)

# Exceptions
from sxd_core.exceptions import (
    ConfigurationError,
    ServiceUnavailableError,
    StorageAccessError,
    StorageError,
    SXDConnectionError,
    SXDError,
    WorkflowError,
)

# Utilities
from sxd_core.logging import StructuredLogger, get_logger

# Legacy decorators (for backward compatibility)
from sxd_core.registry import (
    get_workflow,
    list_activities,
    list_workflows,
    load_pipelines,
)
from sxd_core.storage import get_scratch_path, get_staging_path, get_storage


__all__ = [
    # Configuration
    "get_config",
    "ConfigManager",
    "load_config",
    "get_temporal_config",
    "get_storage_endpoint",
    "get_clickhouse_config",
    # Legacy API (backward compatible)
    "get_workflow",
    "list_workflows",
    "list_activities",
    "load_pipelines",
    # Utilities
    "get_logger",
    "StructuredLogger",
    "get_storage",
    "get_staging_path",
    "get_scratch_path",
    # Exceptions
    "SXDError",
    "WorkflowError",
    "StorageError",
    "StorageAccessError",
    "ConfigurationError",
    "ServiceUnavailableError",
    "SXDConnectionError",
    # Authorization
    "AuthManager",
    "User",
    "Permission",
    "Role",
    "get_auth_manager",
    "get_current_user",
    "require_permission",
    "require_auth",
]
