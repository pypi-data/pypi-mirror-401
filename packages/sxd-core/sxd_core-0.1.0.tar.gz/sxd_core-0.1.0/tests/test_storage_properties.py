import pytest
from unittest.mock import patch, MagicMock, mock_open
from sxd_core.storage import get_storage, get_staging_path, upload_artifact
from sxd_core.testing.mocks import MockStorage, MockStoragePath


@pytest.fixture
def mock_io():
    with patch("sxd_core.storage.io") as m:
        yield m


def test_get_storage_local_default(mock_io):
    mock_io.getenv.return_value = None
    with patch("pathlib.Path.exists", return_value=False):
        storage = get_storage()
        assert str(storage) == "."


def test_get_storage_config_path(mock_io):
    mock_io.getenv.side_effect = lambda k, d=None: (
        "/config/settings.yaml" if k == "SXD_CONFIG_PATH" else None
    )

    yaml_content = "storage:\n  base_path: /data"
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("sxd_core.storage.open", mock_open(read_data=yaml_content)),
        patch("sxd_core.storage.io.open_file", mock_open(read_data=yaml_content)),
    ):

        storage = get_storage()
        assert str(storage) == "/data"


def test_get_storage_s3(mock_io):
    mock_io.getenv.side_effect = lambda k, d=None: (
        "s3"
        if k == "SXD_STORAGE_BACKEND"
        else ("my-bucket" if k == "SXD_STORAGE_BUCKET" else None)
    )

    # Mock config file exists to trigger reading loop
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("sxd_core.storage.io.open_file", mock_open(read_data="{}")),
    ):

        storage = get_storage()
        assert str(storage) == "s3://my-bucket/"


def test_get_staging_path(mock_io):
    with patch("sxd_core.storage.get_storage") as mock_get_storage:
        mock_root = MagicMock()
        mock_get_storage.return_value = mock_root

        # Default config
        with patch("pathlib.Path.exists", return_value=False):
            get_staging_path()
            mock_root.__truediv__.assert_called_with("data")


def test_upload_artifact(mock_io):
    # Mock staging path
    with patch("sxd_core.storage.get_staging_path") as mock_get_staging:
        mock_root = MockStoragePath(MockStorage(), "/staging")
        mock_get_staging.return_value = mock_root

        # Mock source file read
        mock_io.open_file.return_value.__enter__.return_value.read.return_value = (
            b"data"
        )

        res = upload_artifact("source.txt", "dest/file.txt")

        assert res == "/staging/dest/file.txt"
        assert mock_root._storage.read("/staging/dest/file.txt") == b"data"
