"""
Tests for sxd_core.ops.auth_ops module.
"""

from unittest.mock import patch
import pytest

from sxd_core.auth import User, Permission, Role
from sxd_core.ops import auth_ops


@pytest.fixture
def mock_auth_manager():
    with patch("sxd_core.ops.auth_ops.get_auth_manager") as mock:
        yield mock.return_value


@pytest.fixture
def mock_get_current_user():
    with patch("sxd_core.ops.auth_ops.get_current_user") as mock:
        yield mock


@pytest.fixture
def mock_credentials_path(tmp_path):
    creds_path = tmp_path / "credentials"
    with patch("sxd_core.ops.auth_ops.get_credentials_path", return_value=creds_path):
        yield creds_path


class TestAuthOps:
    """Tests for authentication CLI operations."""

    def test_run_auth_login_interactive(self, mock_auth_manager, mock_credentials_path):
        """Should prompt for key, validate, and save credentials."""
        user = User(
            id="test-user",
            name="Test",
            email="test@ex.com",
            roles=[],
            customers=[],
            api_key_hash="hash",
        )
        mock_auth_manager.authenticate.return_value = user

        # Mock getpass
        with patch("getpass.getpass", return_value="sxd_live_key"):
            with patch("sxd_core.io.chmod") as mock_chmod:
                auth_ops.run_auth_login(api_key=None)

        # Verify authentication
        mock_auth_manager.authenticate.assert_called_with("sxd_live_key")

        # Verify file written
        assert mock_credentials_path.exists()
        content = mock_credentials_path.read_text()
        assert "api_key = sxd_live_key" in content

        # Verify permissions set
        mock_chmod.assert_called_with(mock_credentials_path, 0o600)

    def test_run_auth_login_argument(self, mock_auth_manager, mock_credentials_path):
        """Should use provided key argument."""
        user = User(
            id="test-user",
            name="Test",
            email="test@ex.com",
            roles=[],
            customers=[],
            api_key_hash="hash",
        )
        mock_auth_manager.authenticate.return_value = user

        with patch("sxd_core.io.chmod"):
            auth_ops.run_auth_login(api_key="arg_key")

        mock_auth_manager.authenticate.assert_called_with("arg_key")

    def test_run_auth_login_invalid_key(self, mock_auth_manager):
        """Should exit on invalid key."""
        mock_auth_manager.authenticate.return_value = None

        with pytest.raises(SystemExit) as exc:
            auth_ops.run_auth_login(api_key="bad_key")
        assert exc.value.code == 1

    def test_run_auth_logout(self, mock_credentials_path):
        """Should remove credentials file."""
        # Create dummy credentials
        mock_credentials_path.write_text("api_key=foo")

        auth_ops.run_auth_logout()

        assert not mock_credentials_path.exists()

    def test_run_auth_whoami(self, mock_get_current_user, mock_auth_manager, capsys):
        """Should print user details."""
        user = User(
            id="whoami-user",
            name="Who Am I",
            email="who@ex.com",
            roles=["viewer"],
            customers=["*"],
            api_key_hash="hash",
            active=True,
        )
        mock_get_current_user.return_value = user
        mock_auth_manager.get_user_permissions.return_value = {
            Permission("data", "read")
        }

        auth_ops.run_auth_whoami()

        captured = capsys.readouterr()
        assert "User ID:    whoami-user" in captured.out
        assert "Name:       Who Am I" in captured.out
        assert "data:read" in captured.out

    def test_run_auth_whoami_unauthenticated(self, mock_get_current_user):
        """Should exit if not authenticated."""
        mock_get_current_user.return_value = None

        with pytest.raises(SystemExit) as exc:
            auth_ops.run_auth_whoami()
        assert exc.value.code == 1

    def test_run_auth_create_user(self, mock_get_current_user, mock_auth_manager):
        """Should create user if permission granted."""
        admin = User(
            id="admin",
            name="Admin",
            email="admin@ex.com",
            roles=["super_admin"],
            customers=[],
            api_key_hash="hash",
        )
        mock_get_current_user.return_value = admin

        # Permission granted
        mock_auth_manager.check_permission.return_value = True

        # Valid role
        mock_auth_manager.get_role.return_value = Role("viewer", "desc", [])

        # User not exists
        mock_auth_manager.get_user.return_value = None

        # Mock creation
        new_user = User(
            id="new-user",
            name="New",
            email="new@ex.com",
            roles=["viewer"],
            customers=[],
            api_key_hash="hash",
        )
        mock_auth_manager.create_user.return_value = (new_user, "sxd_live_newkey")

        auth_ops.run_auth_create_user(
            user_id="new-user", name="New", email="new@ex.com", roles=["viewer"]
        )

        mock_auth_manager.create_user.assert_called_once()

    def test_run_auth_create_user_permission_denied(
        self, mock_get_current_user, mock_auth_manager
    ):
        """Should fail if permission denied."""
        viewer = User(
            id="viewer",
            name="Viewer",
            email="view@ex.com",
            roles=["viewer"],
            customers=[],
            api_key_hash="hash",
        )
        mock_get_current_user.return_value = viewer

        mock_auth_manager.check_permission.return_value = False

        with pytest.raises(SystemExit) as exc:
            auth_ops.run_auth_create_user("new", "New", "n@e.c", ["viewer"])
        assert exc.value.code == 1

    def test_run_auth_rotate_key_own(
        self, mock_get_current_user, mock_auth_manager, mock_credentials_path
    ):
        """Should allow rotating own key and update credentials."""
        user = User(
            id="me",
            name="Me",
            email="me@ex.com",
            roles=[],
            customers=[],
            api_key_hash="hash",
        )
        mock_get_current_user.return_value = user
        mock_auth_manager.get_user.return_value = user
        mock_auth_manager.rotate_api_key.return_value = "new_key"

        # Mock creds path exists
        mock_credentials_path.touch()

        with patch("sxd_core.io.chmod"):
            auth_ops.run_auth_rotate_key(user_id=None)  # Rotate own

        mock_auth_manager.rotate_api_key.assert_called_with("me")

        # Check creds updated
        assert "new_key" in mock_credentials_path.read_text()

    def test_run_auth_rotate_key_other_denied(
        self, mock_get_current_user, mock_auth_manager
    ):
        """Should deny rotating other's key without permission."""
        user = User(
            id="me",
            name="Me",
            email="me@ex.com",
            roles=["viewer"],
            customers=[],
            api_key_hash="hash",
        )
        mock_get_current_user.return_value = user

        # Admin check fails
        mock_auth_manager.check_permission.return_value = False

        with pytest.raises(SystemExit) as exc:
            auth_ops.run_auth_rotate_key(user_id="other")
        assert exc.value.code == 1

    def test_run_auth_list_users(
        self, mock_get_current_user, mock_auth_manager, capsys
    ):
        """Should list users."""
        admin = User(
            id="admin",
            name="Admin",
            email="a@e.c",
            roles=["admin"],
            customers=[],
            api_key_hash="h",
        )
        mock_get_current_user.return_value = admin
        mock_auth_manager.check_permission.return_value = True

        mock_auth_manager.list_users.return_value = [
            User(
                id="u1",
                name="User 1",
                email="u1@e.c",
                roles=["r1"],
                customers=["active"],
                api_key_hash="h",
                active=True,
            ),
            User(
                id="u2",
                name="User 2",
                email="u2@e.c",
                roles=["r2"],
                customers=["*"],
                api_key_hash="h",
                active=False,
            ),
        ]

        auth_ops.run_auth_list_users()

        captured = capsys.readouterr()
        assert "u1" in captured.out
        assert "u2" in captured.out
        assert "Yes" in captured.out  # active
        assert "No" in captured.out  # inactive

    def test_run_auth_deactivate_user(self, mock_get_current_user, mock_auth_manager):
        """Should deactivate user."""
        admin = User(
            id="admin",
            name="Admin",
            email="a",
            roles=["admin"],
            customers=[],
            api_key_hash="h",
        )
        mock_get_current_user.return_value = admin
        mock_auth_manager.check_permission.return_value = True

        target = User(
            id="target", name="T", email="t", roles=[], customers=[], api_key_hash="h"
        )
        mock_auth_manager.get_user.return_value = target

        auth_ops.run_auth_deactivate_user("target")

        mock_auth_manager.deactivate_user.assert_called_with("target")

    def test_run_auth_deactivate_self_fails(
        self, mock_get_current_user, mock_auth_manager
    ):
        """Should prevent deactivating self."""
        admin = User(
            id="admin",
            name="Admin",
            email="a",
            roles=["admin"],
            customers=[],
            api_key_hash="h",
        )
        mock_get_current_user.return_value = admin
        mock_auth_manager.check_permission.return_value = True

        with pytest.raises(SystemExit):
            auth_ops.run_auth_deactivate_user("admin")

    def test_run_user_enable(self, mock_get_current_user, mock_auth_manager):
        """Should enable user."""
        admin = User(
            id="admin",
            name="Admin",
            email="a",
            roles=["admin"],
            customers=[],
            api_key_hash="h",
        )
        mock_get_current_user.return_value = admin
        mock_auth_manager.check_permission.return_value = True

        target = User(
            id="target", name="T", email="t", roles=[], customers=[], api_key_hash="h"
        )
        mock_auth_manager.get_user.return_value = target

        auth_ops.run_user_enable("target")

        mock_auth_manager.enable_user.assert_called_with("target")

    def test_run_user_update(self, mock_get_current_user, mock_auth_manager):
        """Should update user."""
        admin = User(
            id="admin",
            name="Admin",
            email="a",
            roles=["admin"],
            customers=[],
            api_key_hash="h",
        )
        mock_get_current_user.return_value = admin
        mock_auth_manager.check_permission.return_value = True

        target = User(
            id="target", name="T", email="t", roles=[], customers=[], api_key_hash="h"
        )
        mock_auth_manager.update_user.return_value = target

        auth_ops.run_user_update("target", name="New Name")

        mock_auth_manager.update_user.assert_called_with(
            "target", name="New Name", roles=None, customers=None
        )

    def test_run_auth_list_roles(self, mock_auth_manager, capsys):
        """Should list roles."""
        mock_auth_manager.list_roles.return_value = [
            Role("r1", "desc1", []),
            Role("r2", "desc2", [Permission("p1", "a1")]),
        ]

        auth_ops.run_auth_list_roles()

        captured = capsys.readouterr()
        assert "r1" in captured.out
        assert "desc1" in captured.out
        assert "r2" in captured.out
        assert "p1" in captured.out

    def test_run_role_show(self, mock_auth_manager, capsys):
        """Should show role details."""
        mock_auth_manager.get_role.return_value = Role(
            "r1", "desc1", [Permission("p1", "a1")]
        )

        auth_ops.run_role_show("r1")

        captured = capsys.readouterr()
        assert "Role: r1" in captured.out
        assert "p1" in captured.out
