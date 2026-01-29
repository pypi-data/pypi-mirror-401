"""
Authorization module for SXD platform.

Provides role-based access control (RBAC) with:
- User authentication via API keys
- Role-based permissions
- Customer-scoped access
- Permission checking for CLI commands

Usage:
    from sxd_core.auth import get_auth_manager, require_permission, get_current_user

    # Check permissions programmatically
    user = get_current_user()
    if auth.check_permission(user, "job", "submit", customer_id="acme"):
        submit_job(...)

    # Or use decorator on CLI commands
    @require_permission("job", "submit")
    def run_submit(user: User, ...):
        ...
"""

import base64
import functools
import hashlib
import json
import os
import secrets
import sqlite3
import hmac
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, TypeVar

from sxd_core import io

import yaml

# --- JWT / Token Helpers (Zero Dependency) ---


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _base64url_decode(data: str) -> bytes:
    padding = "=" * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)


def create_jwt(payload: dict, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = _base64url_encode(json.dumps(header).encode())
    encoded_payload = _base64url_encode(json.dumps(payload).encode())

    signature_input = f"{encoded_header}.{encoded_payload}".encode()
    signature = hmac.new(secret.encode(), signature_input, hashlib.sha256).digest()
    encoded_signature = _base64url_encode(signature)

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def verify_jwt(token: str, secret: str) -> Optional[dict]:
    try:
        header_segment, payload_segment, crypto_segment = token.split(".")

        signature_input = f"{header_segment}.{payload_segment}".encode()
        signature = hmac.new(secret.encode(), signature_input, hashlib.sha256).digest()

        if not secrets.compare_digest(_base64url_encode(signature), crypto_segment):
            return None

        payload = json.loads(_base64url_decode(payload_segment).decode())
        if payload.get("exp") and payload["exp"] < io.time():
            return None

        return payload
    except Exception:
        return None


F = TypeVar("F", bound=Callable)


@dataclass
class User:
    """Represents an authenticated user."""

    id: str
    name: str
    email: str
    roles: List[str]
    customers: List[str]  # ["*"] means all customers
    api_key_hash: str
    active: bool = True

    def has_customer_access(self, customer_id: str) -> bool:
        """Check if user has access to a specific customer."""
        if not self.active:
            return False
        return "*" in self.customers or customer_id in self.customers

    def to_actor_string(self) -> str:
        """Return actor string for audit logging."""
        return f"user:{self.id}"


@dataclass
class Permission:
    """Represents a permission as resource:action."""

    resource: str
    action: str

    @classmethod
    def parse(cls, perm_str: str) -> "Permission":
        """Parse a permission string like 'job:submit' or 'infra:*'."""
        if perm_str == "*":
            return cls(resource="*", action="*")
        parts = perm_str.split(":", 1)
        return cls(
            resource=parts[0],
            action=parts[1] if len(parts) > 1 else "*",
        )

    def matches(self, required: "Permission") -> bool:
        """Check if this permission grants access to the required permission."""
        # Wildcard matching
        resource_match = self.resource == "*" or self.resource == required.resource
        action_match = self.action == "*" or self.action == required.action
        return resource_match and action_match

    def __hash__(self):
        return hash((self.resource, self.action))

    def __eq__(self, other):
        if not isinstance(other, Permission):
            return False
        return self.resource == other.resource and self.action == other.action

    def __str__(self):
        return f"{self.resource}:{self.action}"


@dataclass
class Role:
    """Represents a role with a set of permissions."""

    name: str
    description: str
    permissions: List[str]


# Command to permission mapping.
# Security Policy: Commands not in this map require super_admin (*:*) permission.
# This ensures new commands are secure by default until explicitly granted.
# When adding new CLI commands, add them here with appropriate (resource, action) tuples.
COMMAND_PERMISSIONS: Dict[str, tuple] = {
    # Infrastructure (infra_admin only, first-time setup on master)
    "infra up": ("infra", "write"),
    "infra down": ("infra", "write"),
    "infra logs": ("infra", "read"),
    "infra init": ("infra", "write"),
    "infra metrics": ("infra", "read"),
    # Deployment
    "deploy": ("deploy", "write"),
    "provision": ("deploy", "write"),
    # Node operations (infra_admin only)
    "ssh": ("node", "write"),
    "nodes": ("node", "read"),
    "worker": ("worker", "write"),
    "workers": ("worker", "read"),
    # Pipeline operations (pipeline_operator)
    "submit": ("job", "submit"),
    "status": ("job", "status"),
    "upload": ("job", "submit"),
    # Data access (pipeline_operator, viewer)
    "ls": ("data", "list"),
    "query": ("data", "read"),
    "cat": ("data", "read"),
    # Workflows
    "workflows": ("pipeline", "status"),
    "run": ("pipeline", "run"),
    # Info/status (generally allowed)
    "info": ("cluster", "read"),
    "version": ("cluster", "read"),
    # Auth commands (unified namespace)
    "auth": ("auth", "read"),  # Default for bare 'auth' command (whoami)
    "auth login": ("auth", "login"),
    "auth logout": ("auth", "login"),
    "auth whoami": ("auth", "read"),
    "auth unlock": ("secrets", "read"),
    # User management (admin only)
    "auth users": ("admin", "read"),
    "auth create-user": ("admin", "write"),
    "auth update-user": ("admin", "write"),
    "auth enable-user": ("admin", "write"),
    "auth disable-user": ("admin", "write"),
    "auth rotate-key": ("auth", "write"),  # Can rotate own key
    # Role management
    "auth roles": ("auth", "read"),
    "auth role": ("auth", "read"),
    # Maintenance (infra_admin)
    "cleanup": ("infra", "write"),
    "backup": ("infra", "write"),
    "restore": ("infra", "write"),
    # Development (generally allowed for developers)
    "scaffold": ("pipeline", "write"),
    "scaffold pipeline": ("pipeline", "write"),
    "publish": ("pipeline", "write"),
    "test": ("dev", "run"),
    "tidy": ("dev", "run"),
    "clean": ("dev", "run"),
    "explore": ("data", "read"),
    "stats": ("cluster", "read"),
}


class AuthManager:
    """Manages user authentication and authorization."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or self._find_config_dir()
        self.db_path = self.config_dir / "auth.db"
        self._roles: Dict[str, Role] = {}

        # Ensure config dir exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self._init_db()
        self._load_roles()
        self._migrate_yaml_users()  # One-time migration

    def _init_db(self):
        """Initialize the SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    roles TEXT, -- JSON list
                    customers TEXT, -- JSON list
                    api_key_hash TEXT,
                    active BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()

    def _migrate_yaml_users(self):
        """Migrate users from users.yaml if DB is empty."""
        users_yaml = self.config_dir / "users.yaml"
        if not users_yaml.exists():
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT count(*) FROM users")
            if cursor.fetchone()[0] > 0:
                return  # Already populated

            print("Migrating users from users.yaml to auth.db...")
            try:
                with io.open_file(users_yaml) as f:
                    data = yaml.safe_load(f) or {}
                    for user_id, user_def in data.get("users", {}).items():
                        conn.execute(
                            "INSERT INTO users (id, name, email, roles, customers, api_key_hash, active) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (
                                user_id,
                                user_def.get("name", user_id),
                                user_def.get("email", ""),
                                json.dumps(user_def.get("roles", [])),
                                json.dumps(user_def.get("customers", ["*"])),
                                user_def.get("api_key_hash", ""),
                                user_def.get("active", True),
                            ),
                        )
                conn.commit()
                print(f"Migrated {len(data.get('users', {}))} users to auth.db")
                # Note: users.yaml is kept as backup; auth.db is now source of truth
            except Exception as e:
                print(f"Migration failed: {e}")

    def _get_jwt_secret(self) -> str:
        """Get JWT secret from environment with environment-aware fallback."""
        secret = os.getenv("SXD_JWT_SECRET")
        if not secret:
            env = os.getenv("SXD_ENV", "development")
            if env == "production":
                raise ValueError(
                    "SXD_JWT_SECRET must be set in production. "
                    "Set via Infisical or environment variable."
                )
            # Development fallback with warning
            if os.getenv("SXD_NODE_TYPE") == "master":
                print("WARNING: SXD_JWT_SECRET not set, using unsafe default (dev only)!")
            return "unsafe-default-secret-change-me"
        return secret

    def create_upload_token(
        self, session_id: str, customer_id: str, ttl: int = 3600
    ) -> str:
        """Create a signed upload token for worker verification."""
        payload = {
            "sub": "upload",
            "sid": session_id,
            "cid": customer_id,
            "exp": int(io.time()) + ttl,
        }
        return create_jwt(payload, self._get_jwt_secret())

    def verify_upload_token(self, token: str) -> Optional[dict]:
        """Verify an upload token."""
        return verify_jwt(token, self._get_jwt_secret())

    def _find_config_dir(self) -> Path:
        """Find the config directory."""
        # Start from this file and search upward
        current = Path(__file__).resolve()
        for _ in range(5):
            current = current.parent
            config_path = current / "config"
            if config_path.exists():
                return config_path
        # Fallback
        return Path(__file__).parent.parent.parent.parent / "config"

    def _load_config(self):
        """Load configuration."""
        self._load_roles()
        # Users are loaded on demand from DB now

    def _load_roles(self):
        """Load role definitions."""
        roles_path = self.config_dir / "roles.yaml"
        if roles_path.exists():
            with io.open_file(roles_path) as f:
                data = yaml.safe_load(f) or {}
                for role_name, role_def in data.get("roles", {}).items():
                    self._roles[role_name] = Role(
                        name=role_name,
                        description=role_def.get("description", ""),
                        permissions=role_def.get("permissions", []),
                    )
        else:
            # Default roles if config doesn't exist
            self._roles = self._get_default_roles()

    # _load_users removed (replaced by DB)

    def _get_default_roles(self) -> Dict[str, Role]:
        """Return default role definitions."""
        return {
            "super_admin": Role(
                name="super_admin",
                description="Full system access",
                permissions=["*"],
            ),
            "infra_admin": Role(
                name="infra_admin",
                description="Infrastructure management",
                permissions=[
                    "infra:*",
                    "node:*",
                    "secrets:read",
                    "deploy:*",
                    "worker:*",
                    "cluster:read",
                ],
            ),
            "pipeline_operator": Role(
                name="pipeline_operator",
                description="Pipeline operations",
                permissions=[
                    "job:submit",
                    "job:status",
                    "job:cancel",
                    "data:read",
                    "data:list",
                    "pipeline:run",
                    "pipeline:status",
                    "cluster:read",
                    "auth:read",
                    "auth:login",
                ],
            ),
            "viewer": Role(
                name="viewer",
                description="Read-only access",
                permissions=[
                    "job:status",
                    "data:read",
                    "data:list",
                    "pipeline:status",
                    "cluster:read",
                    "auth:read",
                    "auth:login",
                ],
            ),
        }

    def reload(self):
        """Reload configuration (roles only)."""
        self._roles.clear()
        self._load_config()

    # --- Authentication ---

    def authenticate(self, api_key: str) -> Optional[User]:
        """Authenticate user by API key."""
        if not api_key:
            return None

        # Hash the provided key
        key_hash = f"sha256:{hashlib.sha256(api_key.encode()).hexdigest()}"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM users WHERE api_key_hash = ? AND active = 1", (key_hash,)
            )
            row = cursor.fetchone()

            if row:
                return User(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    roles=json.loads(row["roles"]),
                    customers=json.loads(row["customers"]),
                    api_key_hash=row["api_key_hash"],
                    active=bool(row["active"]),
                )
        return None

    def hash_api_key(self, api_key: str) -> str:
        """Hash an API key for storage."""
        return f"sha256:{hashlib.sha256(api_key.encode()).hexdigest()}"

    @staticmethod
    def generate_api_key(prefix: str = "sxd_live") -> str:
        """Generate a new API key."""
        token = secrets.token_urlsafe(32)
        return f"{prefix}_{token}"

    # --- Authorization ---

    def get_user_permissions(self, user: User) -> Set[Permission]:
        """Get all permissions for a user based on their roles."""
        perms: Set[Permission] = set()
        for role_name in user.roles:
            role = self._roles.get(role_name)
            if role:
                for perm_str in role.permissions:
                    perms.add(Permission.parse(perm_str))
        return perms

    def check_permission(
        self,
        user: User,
        resource: str,
        action: str,
        customer_id: Optional[str] = None,
    ) -> bool:
        """
        Check if user has permission for an action.

        Args:
            user: The authenticated user.
            resource: Resource type (job, data, infra, etc.).
            action: Action type (read, write, submit, etc.).
            customer_id: Optional customer ID for scoped resources.

        Returns:
            True if permission is granted, False otherwise.
        """
        if not user.active:
            return False

        required = Permission(resource=resource, action=action)
        user_perms = self.get_user_permissions(user)

        # Check if any permission matches
        has_perm = any(p.matches(required) for p in user_perms)
        if not has_perm:
            return False

        # Check customer scope for customer-scoped resources
        if customer_id and resource in ("job", "data", "pipeline"):
            return user.has_customer_access(customer_id)

        return True

    def check_command_permission(
        self,
        user: User,
        command: str,
        customer_id: Optional[str] = None,
    ) -> bool:
        """
        Check if user has permission to run a CLI command.

        Args:
            user: The authenticated user.
            command: Command string (e.g., "submit", "infra up").
            customer_id: Optional customer ID for scoped commands.

        Returns:
            True if permission is granted, False otherwise.
        """
        perm = COMMAND_PERMISSIONS.get(command)
        if perm is None:
            # Security: Unknown commands require super_admin (*:*) permission.
            # This ensures new/unlisted commands are secure by default.
            has_super = self.check_permission(user, "*", "*")
            if not has_super:
                # Log denied attempts for security auditing
                from sxd_core.audit import log_access_denied
                log_access_denied(
                    user_id=user.id,
                    action=command,
                    resource="cli",
                    required_permission="*:*"
                )
            return has_super

        resource, action = perm
        return self.check_permission(user, resource, action, customer_id)

    # --- User Management ---

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            if row:
                return User(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    roles=json.loads(row["roles"]),
                    customers=json.loads(row["customers"]),
                    api_key_hash=row["api_key_hash"],
                    active=bool(row["active"]),
                )
        return None

    def list_users(self) -> List[User]:
        """List all users."""
        users = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            for row in conn.execute("SELECT * FROM users"):
                users.append(
                    User(
                        id=row["id"],
                        name=row["name"],
                        email=row["email"],
                        roles=json.loads(row["roles"]),
                        customers=json.loads(row["customers"]),
                        api_key_hash=row["api_key_hash"],
                        active=bool(row["active"]),
                    )
                )
        return users

    def get_role(self, role_name: str) -> Optional[Role]:
        """Get a role by name."""
        return self._roles.get(role_name)

    def list_roles(self) -> List[Role]:
        """List all roles."""
        return list(self._roles.values())

    def create_user(
        self,
        user_id: str,
        name: str,
        email: str,
        roles: List[str],
        customers: Optional[List[str]] = None,
    ) -> tuple[User, str]:
        """
        Create a new user and return the user object with their API key.

        Returns:
            Tuple of (User, api_key) - api_key is only shown once.
        """
        api_key = self.generate_api_key()
        api_key_hash = self.hash_api_key(api_key)

        user = User(
            id=user_id,
            name=name,
            email=email,
            roles=roles,
            customers=customers or ["*"],
            api_key_hash=api_key_hash,
            active=True,
        )

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO users (id, name, email, roles, customers, api_key_hash, active) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    user.id,
                    user.name,
                    user.email,
                    json.dumps(user.roles),
                    json.dumps(user.customers),
                    user.api_key_hash,
                    user.active,
                ),
            )
            conn.commit()

        return user, api_key

    def rotate_api_key(self, user_id: str) -> Optional[str]:
        """
        Rotate a user's API key.

        Returns:
            New API key, or None if user not found.
        """
        user = self.get_user(user_id)
        if not user:
            return None

        api_key = self.generate_api_key()
        api_key_hash = self.hash_api_key(api_key)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE users SET api_key_hash = ? WHERE id = ?",
                (api_key_hash, user_id),
            )
            if cursor.rowcount == 0:
                return None
            conn.commit()

        return api_key

    def deactivate_user(self, user_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE users SET active = 0 WHERE id = ?", (user_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def enable_user(self, user_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE users SET active = 1 WHERE id = ?", (user_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def update_user(
        self,
        user_id: str,
        name: Optional[str] = None,
        roles: Optional[List[str]] = None,
        customers: Optional[List[str]] = None,
    ) -> Optional[User]:
        """
        Update user details.

        Args:
            user_id: ID of user to update
            name: New display name (optional)
            roles: New list of roles (optional)
            customers: New list of customers (optional)

        Returns:
            Updated User object or None if user not found.
        """
        user = self.get_user(user_id)
        if not user:
            return None

        # Build query dynamically
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if roles is not None:
            updates.append("roles = ?")
            params.append(json.dumps(roles))
        if customers is not None:
            updates.append("customers = ?")
            params.append(json.dumps(customers))

        if not updates:
            return user

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, tuple(params))
            conn.commit()

        return self.get_user(user_id)

    # _save_users removed (replaced by DB)


# --- Global Instance ---

_auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """Get the global AuthManager instance."""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager


def reset_auth_manager():
    """Reset the global AuthManager instance (for testing)."""
    global _auth_manager
    _auth_manager = None


# --- Current User ---


def get_stored_api_key() -> Optional[str]:
    """
    Retrieve API key from environment variable or credentials file.
    """
    api_key = os.environ.get("SXD_API_KEY")

    if not api_key:
        # Try reading from ~/.sxd/credentials
        creds_path = Path.home() / ".sxd" / "credentials"
        if creds_path.exists():
            try:
                with io.open_file(creds_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("api_key"):
                            # Parse: api_key = sxd_live_xxx
                            _, _, value = line.partition("=")
                            api_key = value.strip().strip('"').strip("'")
                            break
            except Exception:
                pass
    return api_key


def get_current_user() -> Optional[User]:
    """
    Get the currently authenticated user from environment or config.

    Checks:
    1. SXD_API_KEY environment variable
    2. ~/.sxd/credentials file

    Returns:
        User if authenticated, None otherwise.
    """
    api_key = get_stored_api_key()

    if not api_key:
        return None

    return get_auth_manager().authenticate(api_key)


# --- Decorator ---


def require_permission(
    resource: str,
    action: str,
    customer_id_param: Optional[str] = None,
) -> Callable[[F], F]:
    """
    Decorator to require permission for a function.

    The decorated function will receive `user` as a keyword argument
    containing the authenticated User object.

    Args:
        resource: Resource type (job, data, infra, etc.).
        action: Action type (read, write, submit, etc.).
        customer_id_param: Name of parameter containing customer_id for scoping.

    Example:
        @require_permission("job", "submit", customer_id_param="customer_id")
        def run_submit(url: str, customer_id: str, user: User):
            ...
    """

    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            from sxd_core.audit import log_audit_event

            user = get_current_user()

            if user is None:
                print(
                    "Error: Not authenticated. "
                    "Set SXD_API_KEY environment variable or run 'sxd auth login'"
                )
                sys.exit(1)

            # Get customer_id from kwargs if specified
            customer_id = None
            if customer_id_param:
                customer_id = kwargs.get(customer_id_param)

            auth = get_auth_manager()
            if not auth.check_permission(user, resource, action, customer_id):
                print(f"Error: Permission denied. Required: {resource}:{action}")
                if customer_id:
                    print(f"       Customer: {customer_id}")

                log_audit_event(
                    actor=user.to_actor_string(),
                    action=f"{resource}.{action}",
                    target=customer_id or "system",
                    status="DENIED",
                    details={"required_permission": f"{resource}:{action}"},
                )
                sys.exit(1)

            # Inject user into kwargs
            kwargs["user"] = user
            return fn(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


def require_auth(fn: F) -> F:
    """
    Simple decorator that just requires authentication (any valid user).

    Example:
        @require_auth
        def run_status(user: User):
            ...
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()

        if user is None:
            print(
                "Error: Not authenticated. "
                "Set SXD_API_KEY environment variable or run 'sxd auth login'"
            )
            sys.exit(1)

        kwargs["user"] = user
        return fn(*args, **kwargs)

    return wrapper  # type: ignore


# --- Exports ---

__all__ = [
    "User",
    "Permission",
    "Role",
    "AuthManager",
    "get_auth_manager",
    "reset_auth_manager",
    "get_current_user",
    "require_permission",
    "require_auth",
    "COMMAND_PERMISSIONS",
    "get_stored_api_key",
]
