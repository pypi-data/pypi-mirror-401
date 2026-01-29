"""
Tests for sxd_core.auth module.
"""

import sqlite3
import pytest

from sxd_core.auth import (
    AuthManager,
    reset_auth_manager,
)


@pytest.fixture
def temp_auth_config(tmp_path):
    """Fixture to provide a temporary auth configuration."""
    # Reset global singleton
    reset_auth_manager()

    # Create config dir
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    # Initialize AuthManager with temp config
    auth = AuthManager(config_dir=config_dir)

    yield auth

    # Cleanup
    reset_auth_manager()


class TestAuthManager:
    """Tests for AuthManager class."""

    def test_init_creates_db(self, temp_auth_config):
        """AuthManager should initialize the database."""
        db_path = temp_auth_config.db_path
        assert db_path.exists()

        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
            )
            assert cursor.fetchone() is not None

    def test_create_user(self, temp_auth_config):
        """Should create a new user and return user object and api key."""
        user, api_key = temp_auth_config.create_user(
            user_id="test-user",
            name="Test User",
            email="test@example.com",
            roles=["viewer"],
            customers=["cust-1"],
        )

        assert user.id == "test-user"
        assert user.name == "Test User"
        assert user.roles == ["viewer"]
        assert user.customers == ["cust-1"]
        assert api_key.startswith("sxd_live_")

        # Verify stored in DB
        stored = temp_auth_config.get_user("test-user")
        assert stored is not None
        assert stored.id == "test-user"
        assert stored.api_key_hash is not None
        assert stored.api_key_hash != api_key  # Should be hashed

    def test_authenticate(self, temp_auth_config):
        """Should authenticate with valid API key."""
        user, api_key = temp_auth_config.create_user(
            user_id="auth-user",
            name="Auth User",
            email="auth@example.com",
            roles=["viewer"],
        )

        # Authenticate with returned key
        auth_user = temp_auth_config.authenticate(api_key)
        assert auth_user is not None
        assert auth_user.id == "auth-user"

        # Authenticate with invalid key
        assert temp_auth_config.authenticate("invalid-key") is None
        assert temp_auth_config.authenticate("") is None

    def test_rbac_permissions(self, temp_auth_config):
        """Should correctly check RBAC permissions."""
        # Create users with different roles
        admin, _ = temp_auth_config.create_user(
            user_id="admin",
            name="Admin",
            email="admin@example.com",
            roles=["infra_admin"],
        )

        viewer, _ = temp_auth_config.create_user(
            user_id="viewer",
            name="Viewer",
            email="viewer@example.com",
            roles=["viewer"],
        )

        # Check admin permissions (infra:*)
        assert temp_auth_config.check_permission(admin, "infra", "up")
        assert temp_auth_config.check_permission(admin, "infra", "down")
        assert temp_auth_config.check_permission(admin, "cluster", "read")

        # Admin should NOT have job:submit (pipeline_operator role)
        # unless infra_admin implies it? Let's check default roles.
        # infra_admin has: infra:*, node:*, secrets:read, deploy:*, worker:*, cluster:read
        assert not temp_auth_config.check_permission(admin, "job", "submit")

        # Check viewer permissions
        assert temp_auth_config.check_permission(viewer, "data", "read")
        assert temp_auth_config.check_permission(viewer, "job", "status")
        assert not temp_auth_config.check_permission(viewer, "infra", "up")
        assert not temp_auth_config.check_permission(viewer, "data", "write")

    def test_customer_scoping(self, temp_auth_config):
        """Should enforce customer access scoping."""
        user, _ = temp_auth_config.create_user(
            user_id="scoped",
            name="Scoped User",
            email="scoped@example.com",
            roles=["pipeline_operator"],
            customers=["cust-A", "cust-B"],
        )

        # Should have access to assigned customers
        assert temp_auth_config.check_permission(
            user, "job", "submit", customer_id="cust-A"
        )
        assert temp_auth_config.check_permission(
            user, "job", "submit", customer_id="cust-B"
        )

        # Should NOT have access to other customers
        assert not temp_auth_config.check_permission(
            user, "job", "submit", customer_id="cust-C"
        )

        # Pipeline operator permissions check (job:submit)
        assert temp_auth_config.check_permission(user, "job", "submit")

    def test_wildcard_customer_access(self, temp_auth_config):
        """Users with '*' customer should access all customers."""
        user, _ = temp_auth_config.create_user(
            user_id="super-user",
            name="Super User",
            email="super@example.com",
            roles=["pipeline_operator"],
            customers=["*"],
        )

        assert temp_auth_config.check_permission(
            user, "job", "submit", customer_id="cust-X"
        )
        assert temp_auth_config.check_permission(
            user, "job", "submit", customer_id="cust-Y"
        )

    def test_deactivate_user(self, temp_auth_config):
        """Deactivated users should not be able to authenticate or act."""
        user, api_key = temp_auth_config.create_user(
            user_id="temp-user",
            name="Temp",
            email="temp@example.com",
            roles=["viewer"],
        )

        # Verify active first
        assert temp_auth_config.authenticate(api_key) is not None
        assert temp_auth_config.check_permission(user, "data", "read")

        # Deactivate
        assert temp_auth_config.deactivate_user("temp-user")

        # Verify inactive
        # Reload user object to get new status
        user = temp_auth_config.get_user("temp-user")
        assert not user.active

        # Authenticate should fail (returns None? Implementation check: logic filters 'active=1')
        assert temp_auth_config.authenticate(api_key) is None

        # Permission check should fail even if we have the user object
        assert not temp_auth_config.check_permission(user, "data", "read")

    def test_rotate_api_key(self, temp_auth_config):
        """Rotating API key should invalidate old key and enable new one."""
        user, old_key = temp_auth_config.create_user(
            user_id="rotate-test",
            name="Rotate Test",
            email="test@example.com",
            roles=["viewer"],
        )

        assert temp_auth_config.authenticate(old_key) is not None

        new_key = temp_auth_config.rotate_api_key("rotate-test")
        assert new_key is not None
        assert new_key != old_key

        assert temp_auth_config.authenticate(old_key) is None
        assert temp_auth_config.authenticate(new_key) is not None

    def test_update_user(self, temp_auth_config):
        """Should update user details."""
        temp_auth_config.create_user(
            user_id="update-me",
            name="Old Name",
            email="old@example.com",
            roles=["viewer"],
        )

        updated = temp_auth_config.update_user(
            user_id="update-me",
            name="New Name",
            roles=["infra_admin"],
            customers=["new-cust"],
        )

        assert updated.name == "New Name"
        assert updated.roles == ["infra_admin"]
        assert updated.customers == ["new-cust"]

        stored = temp_auth_config.get_user("update-me")
        assert stored.name == "New Name"

    def test_token_operations(self, temp_auth_config, monkeypatch):
        """Test JWT creation and verification."""
        # Mock secret
        monkeypatch.setenv("SXD_JWT_SECRET", "test-secret")

        token = temp_auth_config.create_upload_token(
            session_id="sess-1", customer_id="cust-1", ttl=60
        )

        assert token is not None

        payload = temp_auth_config.verify_upload_token(token)
        assert payload is not None
        assert payload["sid"] == "sess-1"
        assert payload["cid"] == "cust-1"
        assert payload["sub"] == "upload"

        # Test invalid signature
        parts = token.split(".")
        bad_token = f"{parts[0]}.{parts[1]}.badsignature"
        assert temp_auth_config.verify_upload_token(bad_token) is None
