import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from pathlib import Path

from sxd_core.worker_upload import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_auth():
    with patch("sxd_core.worker_upload.get_auth_manager") as mock:
        yield mock


@pytest.fixture
def mock_ch():
    with patch("sxd_core.worker_upload.ClickHouseManager") as mock:
        yield mock


@pytest.fixture
def mock_background():
    with patch(
        "sxd_core.worker_upload._trigger_local_workflow", new_callable=AsyncMock
    ) as mock:
        yield mock


def test_upload_file_success(client, mock_auth, mock_ch, tmp_path):
    # Setup Mocks
    mock_auth.return_value.verify_upload_token.return_value = {"sid": "sess-123"}

    mock_ch_instance = mock_ch.return_value
    mock_ch_instance.get_upload_session.return_value = {"status": "ACTIVE"}

    # Configure DATA_DIR to tmp_path
    with patch("sxd_core.worker_upload.DATA_DIR", tmp_path):
        response = client.put(
            "/upload/sess-123/video.mp4",
            content=b"test-content",
            headers={"X-Upload-Token": "valid-token"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["file"] == "video.mp4"
    assert data["size"] == 12

    # Verify file written
    assert (tmp_path / "sess-123" / "video.mp4").read_bytes() == b"test-content"

    # Verify CH update
    mock_ch_instance.increment_upload_session.assert_called_with(
        "sess-123", files_delta=1, bytes_delta=12
    )


def test_upload_file_invalid_token(client, mock_auth):
    mock_auth.return_value.verify_upload_token.return_value = None

    response = client.put(
        "/upload/sess-123/video.mp4",
        content=b"data",
        headers={"X-Upload-Token": "bad-token"},
    )
    assert response.status_code == 401


def test_upload_file_session_mismatch(client, mock_auth):
    mock_auth.return_value.verify_upload_token.return_value = {"sid": "other-sess"}

    response = client.put(
        "/upload/sess-123/video.mp4",
        content=b"data",
        headers={"X-Upload-Token": "valid-token"},
    )
    assert response.status_code == 403


def test_upload_session_not_found(client, mock_auth, mock_ch):
    mock_auth.return_value.verify_upload_token.return_value = {"sid": "sess-123"}
    mock_ch.return_value.get_upload_session.return_value = None

    with patch("sxd_core.worker_upload.DATA_DIR"):
        response = client.put(
            "/upload/sess-123/video.mp4",
            content=b"data",
            headers={"X-Upload-Token": "valid-token"},
        )
    assert response.status_code == 404


def test_complete_session_success(client, mock_ch, mock_background):
    mock_ch_instance = mock_ch.return_value
    mock_ch_instance.get_upload_session.return_value = {
        "status": "ACTIVE",
        "customer_id": "cust-1",
        "files_received": 5,
        "bytes_received": 1000,
    }

    with patch("sxd_core.worker_upload.DATA_DIR", Path("/tmp/sxd-test")):
        response = client.post("/upload/sess-123/complete")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PROCESSING"
    assert data["episode_id"] == "ep-123"

    # Verify CH update
    mock_ch_instance.update_upload_session.assert_called_with(
        "sess-123", status="PROCESSING", episode_id="ep-123"
    )


def test_get_status_success(client, mock_ch, tmp_path):
    mock_ch_instance = mock_ch.return_value
    mock_ch_instance.get_upload_session.return_value = {
        "status": "ACTIVE",
        "files_received": 2,
        "bytes_received": 500,
        "episode_id": None,
    }

    # Create some local files
    sess_dir = tmp_path / "sess-123"
    sess_dir.mkdir()
    (sess_dir / "f1").write_bytes(b"123")

    with patch("sxd_core.worker_upload.DATA_DIR", tmp_path):
        response = client.get("/upload/sess-123/status")

    assert response.status_code == 200
    data = response.json()
    assert data["local_files"] == 1
    assert data["local_bytes"] == 3


def test_health_check(client, mock_ch, tmp_path):
    mock_ch.return_value.execute_query.return_value = []

    with patch("sxd_core.worker_upload.DATA_DIR", tmp_path):
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
