"""
Tests for the DataManager class in data_layer.py.

These tests verify the actual business logic of data fetching,
caching, and extraction.
"""

import hashlib
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestDataManagerLocalFiles:
    """Tests for local file handling."""

    def test_download_local_file_copies_to_scratch(self, tmp_path, monkeypatch):
        """Local file is copied to scratch directory."""
        # Create a source video file
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        source_video = source_dir / "video.mp4"
        source_video.write_bytes(b"video content")

        # Set up scratch path
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        with patch("sxd_core.data_layer.log_audit_event"):
            result = DataManager.download_video(str(source_video), "job-123")

        assert Path(result).exists()
        assert Path(result).read_bytes() == b"video content"
        assert "job-123" in result

    def test_download_nonexistent_file_raises(self, tmp_path, monkeypatch):
        """Non-existent local file raises ValueError."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        with pytest.raises(ValueError, match="Invalid input"):
            DataManager.download_video("/nonexistent/video.mp4", "job-123")

    def test_handle_local_file_no_copy_if_same(self, tmp_path, monkeypatch):
        """Doesn't copy if source and dest are the same path."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        job_dir = scratch_dir / "job-123"
        job_dir.mkdir()

        # Create file already in scratch location
        source_video = job_dir / "source.mp4"
        source_video.write_bytes(b"original content")

        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        result = DataManager._handle_local_file(str(source_video), "job-123")

        # Should return the same path without error
        assert Path(result).read_bytes() == b"original content"


class TestDataManagerCaching:
    """Tests for caching behavior."""

    def test_cached_video_returns_immediately(self, tmp_path, monkeypatch):
        """Already downloaded video returns without re-downloading."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        job_dir = scratch_dir / "job-456"
        job_dir.mkdir()

        # Pre-populate cache
        cached_video = job_dir / "source.mp4"
        cached_video.write_bytes(b"cached video")

        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        # Should not make any HTTP calls
        with patch("sxd_core.data_layer.requests.get") as mock_get:
            result = DataManager.download_video(
                "https://example.com/video.mp4", "job-456"
            )

        mock_get.assert_not_called()
        assert result == str(cached_video)

    def test_shared_cache_path_uses_key(self, tmp_path, monkeypatch):
        """Shared cache path is based on the provided key."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        cache_path = DataManager.get_shared_cache_path("my-cache-key")

        assert "shared_cache" in str(cache_path)
        assert "my-cache-key" in str(cache_path)


class TestDataManagerHTTP:
    """Tests for HTTP download logic."""

    def test_download_http_success(self, tmp_path, monkeypatch):
        """HTTP download writes content to scratch."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_response.raise_for_status = MagicMock()

        with patch("sxd_core.data_layer.requests.get", return_value=mock_response):
            with patch("sxd_core.data_layer.log_audit_event"):
                with patch.object(DataManager, "_validate_url"):
                    result = DataManager.download_video(
                        "https://example.com/video.mp4", "job-http"
                    )

        assert Path(result).exists()
        assert Path(result).read_bytes() == b"chunk1chunk2"

    def test_download_http_error_raises(self, tmp_path, monkeypatch):
        """HTTP error raises exception."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        import requests
        from sxd_core.data_layer import DataManager

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

        with patch("sxd_core.data_layer.requests.get", return_value=mock_response):
            with patch.object(DataManager, "_validate_url"):
                with pytest.raises(requests.HTTPError):
                    DataManager.download_video(
                        "https://example.com/video.mp4", "job-err"
                    )


class TestDataManagerSSRF:
    """Tests for SSRF protection."""

    def test_blocks_private_ip(self, tmp_path, monkeypatch):
        """Private IP addresses are blocked."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        # Mock DNS resolution to return private IP
        with patch(
            "sxd_core.data_layer.socket.gethostbyname", return_value="192.168.1.1"
        ):
            with pytest.raises(ValueError, match="Security Error"):
                DataManager._validate_url("https://evil.com/video.mp4")

    def test_blocks_loopback(self, tmp_path, monkeypatch):
        """Loopback addresses are blocked."""
        from sxd_core.data_layer import DataManager

        with patch(
            "sxd_core.data_layer.socket.gethostbyname", return_value="127.0.0.1"
        ):
            with pytest.raises(ValueError, match="Security Error"):
                DataManager._validate_url("https://localhost/video.mp4")

    def test_blocks_link_local(self, tmp_path, monkeypatch):
        """Link-local addresses are blocked."""
        from sxd_core.data_layer import DataManager

        with patch(
            "sxd_core.data_layer.socket.gethostbyname", return_value="169.254.1.1"
        ):
            with pytest.raises(ValueError, match="Security Error"):
                DataManager._validate_url("https://metadata.internal/video.mp4")

    def test_allows_public_ip(self, tmp_path, monkeypatch):
        """Public IP addresses are allowed."""
        from sxd_core.data_layer import DataManager

        with patch("sxd_core.data_layer.socket.gethostbyname", return_value="8.8.8.8"):
            # Should not raise
            DataManager._validate_url("https://google.com/video.mp4")

    def test_invalid_url_raises(self, tmp_path, monkeypatch):
        """Invalid URL raises ValueError."""
        from sxd_core.data_layer import DataManager

        with pytest.raises(ValueError, match="Invalid URL"):
            DataManager._validate_url("not-a-url")


class TestDataManagerHF:
    """Tests for HuggingFace URL handling."""

    def test_parse_hf_url_with_file(self):
        """Parses HF URL with file path correctly."""
        from sxd_core.data_layer import DataManager

        repo_id, file_path = DataManager._parse_hf_url(
            "hf://user/dataset/videos/video.mp4"
        )

        assert repo_id == "user/dataset"
        assert file_path == "videos/video.mp4"

    def test_parse_hf_url_without_file(self):
        """Parses HF URL without file path."""
        from sxd_core.data_layer import DataManager

        repo_id, file_path = DataManager._parse_hf_url("hf://user/dataset")

        assert repo_id == "user/dataset"
        assert file_path is None

    def test_parse_hf_url_invalid(self):
        """Invalid HF URL raises ValueError."""
        from sxd_core.data_layer import DataManager

        with pytest.raises(ValueError, match="Invalid HF URL"):
            DataManager._parse_hf_url("hf://invalid")

    def test_download_hf_auto_detects_video(self, tmp_path, monkeypatch):
        """Auto-detects first video file when no path specified."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        # Create a fake downloaded file
        fake_video = tmp_path / "fake_video.mp4"
        fake_video.write_bytes(b"hf video content")

        with patch(
            "sxd_core.data_layer.list_repo_files",
            return_value=["readme.md", "video1.mp4", "video2.avi"],
        ):
            with patch(
                "sxd_core.data_layer.hf_hub_download", return_value=str(fake_video)
            ):
                dest_path = scratch_dir / "job-hf" / "source.mp4"
                dest_path.parent.mkdir(parents=True)

                result = DataManager._download_from_hf(
                    "hf://user/dataset", dest_path, scratch_dir
                )

        assert Path(result).read_bytes() == b"hf video content"

    def test_download_hf_no_videos_raises(self, tmp_path, monkeypatch):
        """Raises error when no videos found in HF repo."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()

        from sxd_core.data_layer import DataManager

        with patch(
            "sxd_core.data_layer.list_repo_files",
            return_value=["readme.md", "data.csv"],
        ):
            dest_path = scratch_dir / "job-hf" / "source.mp4"
            dest_path.parent.mkdir(parents=True)

            with pytest.raises(ValueError, match="No videos found"):
                DataManager._download_from_hf(
                    "hf://user/dataset", dest_path, scratch_dir
                )


class TestDataManagerTar:
    """Tests for tar extraction logic."""

    def test_extract_tar_uses_pigz_if_available(self, tmp_path):
        """Uses pigz for faster extraction when available."""
        from sxd_core.data_layer import DataManager

        tar_path = tmp_path / "archive.tar"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch("sxd_core.data_layer.io.run") as mock_run:
            # First call checks pigz version, second extracts
            mock_run.return_value = MagicMock(returncode=0)

            DataManager._extract_tar(tar_path, output_dir)

        # Should have called subprocess twice (pigz check + tar with pigz)
        assert mock_run.call_count == 2
        # Second call should use pigz
        second_call_args = mock_run.call_args_list[1][0][0]
        assert "-I" in second_call_args
        assert "pigz" in second_call_args

    def test_extract_tar_fallback_to_tar(self, tmp_path):
        """Falls back to regular tar if pigz not available."""
        from sxd_core.data_layer import DataManager

        tar_path = tmp_path / "archive.tar"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        def mock_run_side_effect(cmd, **kwargs):
            if "pigz" in cmd:
                raise FileNotFoundError("pigz not found")
            return MagicMock(returncode=0)

        with patch("sxd_core.data_layer.io.run", side_effect=mock_run_side_effect):
            DataManager._extract_tar(tar_path, output_dir)

        # Should complete without error (using fallback)

    def test_collect_videos_finds_all_extensions(self, tmp_path):
        """Collects videos with various extensions."""
        from sxd_core.data_layer import DataManager

        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()

        # Create videos with different extensions
        (extract_dir / "video1.mp4").write_bytes(b"mp4")
        (extract_dir / "video2.avi").write_bytes(b"avi")
        (extract_dir / "video3.mov").write_bytes(b"mov")
        (extract_dir / "video4.mkv").write_bytes(b"mkv")
        (extract_dir / "video5.webm").write_bytes(b"webm")
        (extract_dir / "readme.txt").write_bytes(b"not a video")

        result = DataManager._collect_videos(extract_dir)

        assert len(result) == 5
        video_names = [v["video_name"] for v in result]
        assert "video1.mp4" in video_names
        assert "video2.avi" in video_names
        assert "readme.txt" not in video_names

    def test_collect_videos_nested_directories(self, tmp_path):
        """Collects videos from nested directories."""
        from sxd_core.data_layer import DataManager

        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()

        # Create nested structure
        (extract_dir / "subdir1").mkdir()
        (extract_dir / "subdir1" / "video1.mp4").write_bytes(b"mp4")
        (extract_dir / "subdir2" / "deep").mkdir(parents=True)
        (extract_dir / "subdir2" / "deep" / "video2.mp4").write_bytes(b"mp4")

        result = DataManager._collect_videos(extract_dir)

        assert len(result) == 2

    def test_collect_videos_returns_sorted_with_index(self, tmp_path):
        """Videos are sorted and have correct indices."""
        from sxd_core.data_layer import DataManager

        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()

        (extract_dir / "c_video.mp4").write_bytes(b"c")
        (extract_dir / "a_video.mp4").write_bytes(b"a")
        (extract_dir / "b_video.mp4").write_bytes(b"b")

        result = DataManager._collect_videos(extract_dir)

        # Should be sorted alphabetically
        assert result[0]["video_name"] == "a_video.mp4"
        assert result[0]["index"] == 0
        assert result[1]["video_name"] == "b_video.mp4"
        assert result[1]["index"] == 1
        assert result[2]["video_name"] == "c_video.mp4"
        assert result[2]["index"] == 2


class TestDataManagerArrowTable:
    """Tests for Arrow table conversion."""

    def test_get_video_table_creates_table(self):
        """Converts video list to Arrow table."""
        from sxd_core.data_layer import DataManager

        video_list = [
            {"video_id": "vid1", "customer_id": "cust1", "video_path": "/path/1.mp4"},
            {"video_id": "vid2", "customer_id": "cust2", "video_path": "/path/2.mp4"},
        ]

        with patch("sxd_core.arrow.dicts_to_table") as mock_dicts_to_table:
            mock_table = MagicMock()
            mock_dicts_to_table.return_value = mock_table

            DataManager.get_video_table(video_list)

        mock_dicts_to_table.assert_called_once()
        call_args = mock_dicts_to_table.call_args[0][0]
        assert len(call_args) == 2
        assert call_args[0]["video_id"] == "vid1"
        assert call_args[0]["status"] == "DETECTED"

    def test_get_video_table_uses_video_name_fallback(self):
        """Uses video_name as fallback for video_id."""
        from sxd_core.data_layer import DataManager

        video_list = [
            {"video_name": "fallback_name.mp4", "video_path": "/path/1.mp4"},
        ]

        with patch("sxd_core.arrow.dicts_to_table") as mock_dicts_to_table:
            mock_table = MagicMock()
            mock_dicts_to_table.return_value = mock_table

            DataManager.get_video_table(video_list)

        call_args = mock_dicts_to_table.call_args[0][0]
        assert call_args[0]["video_id"] == "fallback_name.mp4"

    def test_get_video_table_default_customer_id(self):
        """Uses 'default' as customer_id when not provided."""
        from sxd_core.data_layer import DataManager

        video_list = [
            {"video_id": "vid1", "video_path": "/path/1.mp4"},
        ]

        with patch("sxd_core.arrow.dicts_to_table") as mock_dicts_to_table:
            mock_table = MagicMock()
            mock_dicts_to_table.return_value = mock_table

            DataManager.get_video_table(video_list)

        call_args = mock_dicts_to_table.call_args[0][0]
        assert call_args[0]["customer_id"] == "default"


class TestListTarContents:
    """Tests for list_tar_contents method."""

    def test_rejects_non_hf_urls(self):
        """Only HuggingFace URLs are supported."""
        from sxd_core.data_layer import DataManager

        with pytest.raises(ValueError, match="Only HuggingFace"):
            DataManager.list_tar_contents("https://example.com/archive.tar")

    def test_uses_cache_when_available(self, tmp_path, monkeypatch):
        """Uses cached extraction when completion marker exists."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        # Create cache structure with completion marker
        cache_key = hashlib.md5(b"user/dataset:archive.tar").hexdigest()
        cache_dir = scratch_dir.parent / "shared_cache" / cache_key
        extract_dir = cache_dir / "extracted"
        extract_dir.mkdir(parents=True)
        (extract_dir / ".complete").touch()
        (extract_dir / "video.mp4").write_bytes(b"cached video")

        with patch("sxd_core.data_layer.hf_hub_download") as mock_download:
            result = DataManager.list_tar_contents("hf://user/dataset/archive.tar")

        # Should not download
        mock_download.assert_not_called()
        assert len(result) == 1
        assert result[0]["video_name"] == "video.mp4"


# =============================================================================
# Additional Behavioral Edge Case Tests
# =============================================================================


class TestDataManagerURLSchemeHandling:
    """Test URL scheme detection and routing."""

    def test_relative_path_treated_as_local(self, tmp_path, monkeypatch):
        """Relative path without URL scheme is treated as local file."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        # Create file at relative path
        video_file = tmp_path / "video.mp4"
        video_file.write_bytes(b"relative video")

        # Change to tmp_path so relative path works
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            from sxd_core.data_layer import DataManager

            with patch("sxd_core.data_layer.log_audit_event"):
                result = DataManager.download_video("video.mp4", "job-relative")

            assert Path(result).read_bytes() == b"relative video"
        finally:
            os.chdir(original_cwd)

    def test_absolute_path_treated_as_local(self, tmp_path, monkeypatch):
        """Absolute path is treated as local file."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        video_file = tmp_path / "absolute_video.mp4"
        video_file.write_bytes(b"absolute video")

        from sxd_core.data_layer import DataManager

        with patch("sxd_core.data_layer.log_audit_event"):
            result = DataManager.download_video(str(video_file), "job-absolute")

        assert Path(result).read_bytes() == b"absolute video"


class TestDataManagerSSRFEdgeCases:
    """Additional SSRF protection edge cases."""

    def test_blocks_class_a_private_range(self):
        """Blocks 10.x.x.x (Class A private range)."""
        from sxd_core.data_layer import DataManager

        with patch("sxd_core.data_layer.socket.gethostbyname", return_value="10.0.0.1"):
            with pytest.raises(ValueError, match="Security Error"):
                DataManager._validate_url("https://internal.corp/data")

    def test_blocks_class_b_private_range(self):
        """Blocks 172.16.x.x - 172.31.x.x (Class B private range)."""
        from sxd_core.data_layer import DataManager

        with patch(
            "sxd_core.data_layer.socket.gethostbyname", return_value="172.16.0.1"
        ):
            with pytest.raises(ValueError, match="Security Error"):
                DataManager._validate_url("https://internal.corp/data")

    def test_allows_dns_resolution_failure(self):
        """DNS resolution failure does not block the request."""
        import socket

        from sxd_core.data_layer import DataManager

        with patch(
            "sxd_core.data_layer.socket.gethostbyname",
            side_effect=socket.gaierror("DNS resolution failed"),
        ):
            # Should not raise - DNS failures are passed through
            DataManager._validate_url("https://example.com/video.mp4")

    def test_url_without_hostname_rejected(self):
        """URL without hostname is rejected."""
        from sxd_core.data_layer import DataManager

        with pytest.raises(ValueError, match="Invalid URL"):
            DataManager._validate_url("file:///etc/passwd")


class TestDataManagerCacheIntegrity:
    """Test cache integrity and edge cases."""

    def test_empty_cached_file_triggers_redownload(self, tmp_path, monkeypatch):
        """Empty cached file (0 bytes) triggers re-download."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        job_dir = scratch_dir / "job-empty"
        job_dir.mkdir()

        # Create empty cached file
        empty_cache = job_dir / "source.mp4"
        empty_cache.touch()  # 0 bytes

        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"fresh content"]
        mock_response.raise_for_status = MagicMock()

        with patch("sxd_core.data_layer.requests.get", return_value=mock_response):
            with patch("sxd_core.data_layer.log_audit_event"):
                with patch.object(DataManager, "_validate_url"):
                    result = DataManager.download_video(
                        "https://example.com/video.mp4", "job-empty"
                    )

        # Should have downloaded fresh content
        assert Path(result).read_bytes() == b"fresh content"

    def test_job_scratch_directory_created_if_missing(self, tmp_path, monkeypatch):
        """Job scratch directory is created if it doesn't exist."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        # Note: job directory does NOT exist yet

        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"content"]
        mock_response.raise_for_status = MagicMock()

        with patch("sxd_core.data_layer.requests.get", return_value=mock_response):
            with patch("sxd_core.data_layer.log_audit_event"):
                with patch.object(DataManager, "_validate_url"):
                    result = DataManager.download_video(
                        "https://example.com/video.mp4", "new-job"
                    )

        # Directory should have been created
        assert (scratch_dir / "new-job").exists()
        assert Path(result).exists()


class TestDataManagerHFEdgeCases:
    """Additional HuggingFace handling edge cases."""

    def test_hf_url_with_nested_path(self):
        """Parses HF URL with deeply nested file path."""
        from sxd_core.data_layer import DataManager

        repo_id, file_path = DataManager._parse_hf_url(
            "hf://org/dataset/path/to/deep/nested/video.mp4"
        )

        assert repo_id == "org/dataset"
        assert file_path == "path/to/deep/nested/video.mp4"

    def test_hf_downloads_first_video_found(self, tmp_path, monkeypatch):
        """Downloads the first video file found in repository file list."""
        scratch_dir = tmp_path / "scratch"
        scratch_dir.mkdir()
        monkeypatch.setattr("sxd_core.data_layer.get_scratch_path", lambda: scratch_dir)

        from sxd_core.data_layer import DataManager

        fake_video = tmp_path / "fake.mp4"
        fake_video.write_bytes(b"video")

        # The code filters for video extensions and takes the first match
        with patch(
            "sxd_core.data_layer.list_repo_files",
            return_value=[
                "readme.md",
                "data.csv",
                "first_video.mp4",
                "second_video.avi",
            ],
        ):
            with patch(
                "sxd_core.data_layer.hf_hub_download", return_value=str(fake_video)
            ) as mock_download:
                dest_path = scratch_dir / "job-priority" / "source.mp4"
                dest_path.parent.mkdir(parents=True)

                DataManager._download_from_hf(
                    "hf://user/dataset", dest_path, scratch_dir
                )

        # Should download the first video found in the list
        downloaded_file = mock_download.call_args[1]["filename"]
        assert downloaded_file == "first_video.mp4"


class TestDataManagerTarEdgeCases:
    """Additional tar handling edge cases."""

    def test_collect_videos_empty_directory(self, tmp_path):
        """Empty directory returns empty list."""
        from sxd_core.data_layer import DataManager

        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = DataManager._collect_videos(empty_dir)

        assert result == []

    def test_collect_videos_only_non_video_files(self, tmp_path):
        """Directory with no video files returns empty list."""
        from sxd_core.data_layer import DataManager

        dir_with_files = tmp_path / "no_videos"
        dir_with_files.mkdir()
        (dir_with_files / "readme.md").write_text("# Readme")
        (dir_with_files / "data.json").write_text("{}")
        (dir_with_files / "config.yaml").write_text("key: value")

        result = DataManager._collect_videos(dir_with_files)

        assert result == []

    def test_handle_single_tar_fallback_extracts_first_video(self, tmp_path):
        """Single tar fallback extracts and returns first video."""
        from sxd_core.data_layer import DataManager

        # Create a fake tar path (we'll mock extraction)
        tar_path = tmp_path / "archive.tar"
        tar_path.touch()

        dest_path = tmp_path / "dest" / "source.mp4"
        dest_path.parent.mkdir(parents=True)

        # Mock extraction to create videos
        def mock_extract(tar, output_dir):
            (output_dir / "video1.mp4").write_bytes(b"first video")
            (output_dir / "video2.mp4").write_bytes(b"second video")

        with patch.object(DataManager, "_extract_tar", side_effect=mock_extract):
            result = DataManager._handle_single_tar_fallback(tar_path, dest_path)

        # Should have extracted first video
        assert Path(result).read_bytes() == b"first video"

    def test_handle_single_tar_fallback_no_videos_raises(self, tmp_path):
        """Single tar fallback raises if no videos in tar."""
        from sxd_core.data_layer import DataManager

        tar_path = tmp_path / "archive.tar"
        tar_path.touch()

        dest_path = tmp_path / "dest" / "source.mp4"
        dest_path.parent.mkdir(parents=True)

        # Mock extraction that creates no videos
        def mock_extract(tar, output_dir):
            (output_dir / "readme.txt").write_text("no videos here")

        with patch.object(DataManager, "_extract_tar", side_effect=mock_extract):
            with pytest.raises(ValueError, match="No videos in tar"):
                DataManager._handle_single_tar_fallback(tar_path, dest_path)
