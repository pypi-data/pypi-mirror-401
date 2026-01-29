from unittest.mock import patch
from sxd_core.ops.secrets import (
    get_secret,
    check_infisical,
    get_infisical_path,
    pull_secrets_from_infisical,
)


def test_get_infisical_path_found():
    with patch("sxd_core.io.which", return_value="/usr/bin/infisical"):
        assert get_infisical_path() == "/usr/bin/infisical"


def test_get_infisical_path_brew():
    with (
        patch("sxd_core.io.which", return_value=None),
        patch("sxd_core.io.exists", return_value=True),
    ):
        path = get_infisical_path()
        assert path is not None
        assert "homebrew" in path


def test_check_infisical():
    with patch(
        "sxd_core.ops.secrets.get_infisical_path", return_value="/bin/infisical"
    ):
        assert check_infisical() is True


def test_get_secret_env():
    with patch("sxd_core.io.getenv", return_value="secret_val"):
        assert get_secret("MY_SEC") == "secret_val"


def test_get_secret_infisical():
    with (
        patch("sxd_core.io.getenv", return_value=None),
        patch("sxd_core.ops.secrets.get_infisical_path", return_value="/bin/infisical"),
        patch("sxd_core.io.run") as mock_run,
    ):

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "secret_val\n"

        assert get_secret("MY_SEC") == "secret_val"
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "secrets" in cmd and "get" in cmd


def test_pull_secrets_success(tmp_path):
    env_file = tmp_path / ".env"

    with (
        patch("sxd_core.ops.secrets.get_infisical_path", return_value="/bin/infisical"),
        patch("sxd_core.io.run") as mock_run,
    ):

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "FOO=bar\nSSH_PRIVATE_KEY=key"

        res = pull_secrets_from_infisical(env_file)
        assert res is True
        assert env_file.read_text().startswith("FOO=bar")
