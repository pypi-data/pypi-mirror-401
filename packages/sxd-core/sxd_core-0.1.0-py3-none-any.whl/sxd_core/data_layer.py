"""
Data Management Layer.

This module encapsulates all data fetching, caching, and extraction logic,
keeping the main activities.py clean and focused on business logic.
"""

import hashlib
import ipaddress
import os
import socket
from pathlib import Path
from urllib.parse import urlparse

from sxd_core import io

import pyarrow as pa
import requests
from huggingface_hub import hf_hub_download, list_repo_files

from sxd_core.audit import log_audit_event
from sxd_core.logging import get_logger
from sxd_core.storage import get_scratch_path

log = get_logger(__name__)

# Enable hf_transfer for faster downloads
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"


class DataManager:
    """Handles intelligent data retrieval with caching."""

    @staticmethod
    def get_shared_cache_path(key: str) -> Path:
        """Get path to the shared cache directory."""
        # Shared cache sits alongside scratch jobs
        return Path(str(get_scratch_path().parent / "shared_cache" / key))

    @classmethod
    def download_video(cls, url: str, job_id: str) -> str:
        """
        Smart download function for videos.
        Handles: Local files, HF URLs, HTTP URLs, and caching.
        """
        # 1. Check if it's already a local file (e.g. from batch extraction)
        # We explicitly check for existence OR if it looks like a path and not a URL
        is_url = (
            url.startswith("http://")
            or url.startswith("https://")
            or url.startswith("hf://")
        )

        if not is_url:
            # Assume it's a local file path
            if Path(url).exists():
                return cls._handle_local_file(url, job_id)
            else:
                # It looks like a file path but doesn't exist?
                # It might be a relative path that needs resolving
                resolved_path = Path(url).resolve()
                if resolved_path.exists():
                    return cls._handle_local_file(str(resolved_path), job_id)

        # 2. Setup job scratch space
        scratch_dir = get_scratch_path() / job_id
        scratch_dir.mkdir(parents=True, exist_ok=True)
        dest_path = scratch_dir / "source.mp4"

        # 3. Check for job-level cache
        if dest_path.exists() and io.getsize(str(dest_path)) > 0:
            return str(dest_path)

        # 4. Download based on protocol
        if url.startswith("hf://"):
            res = cls._download_from_hf(
                url, Path(str(dest_path)), Path(str(scratch_dir))
            )
        elif url.startswith("http://") or url.startswith("https://"):
            cls._validate_url(url)
            res = cls._download_from_http(url, Path(str(dest_path)))
        else:
            # If we got here, it's not a known URL scheme AND it didn't exist as a file
            raise ValueError(
                f"Invalid input: '{url}'. Not a valid URL (http/hf) and file not found locally."
            )

        log_audit_event(
            actor=f"system:worker:{job_id}",
            action="data.download",
            target=url,
            status="SUCCESS",
            details={"dest": str(dest_path)},
        )
        return res

    @classmethod
    def list_tar_contents(cls, tar_url: str) -> list[dict]:
        """
        Smart tar extractor.
        Handles: Shared Caching (so we don't re-download/re-extract), parallel extraction.
        """
        if not tar_url.startswith("hf://"):
            raise ValueError("Only HuggingFace tar URLs supported currently.")

        # Parse HF URL to create a stable cache key
        repo_id, file_path = cls._parse_hf_url(tar_url)
        cache_key = hashlib.md5(f"{repo_id}:{file_path}".encode()).hexdigest()

        # Define shared cache location
        shared_cache_dir = cls.get_shared_cache_path(cache_key)
        extract_dir = shared_cache_dir / "extracted"
        completion_marker = extract_dir / ".complete"

        # Check Shared Cache
        if completion_marker.exists():
            log.info("using cached extraction", cache_dir=str(shared_cache_dir))
        else:
            # Not cached, perform download and extraction
            shared_cache_dir.mkdir(parents=True, exist_ok=True)
            extract_dir.mkdir(parents=True, exist_ok=True)

            # Download
            tar_path = hf_hub_download(
                repo_id=repo_id,
                filename=file_path,
                repo_type="dataset",
                cache_dir=str(shared_cache_dir / "hf_cache"),
            )

            # Atomic Extract with file locking
            lock_file = shared_cache_dir / ".lock"
            import fcntl

            with io.open_file(lock_file, "w") as f:
                try:
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    if not completion_marker.exists():
                        cls._extract_tar(Path(str(tar_path)), Path(str(extract_dir)))
                        completion_marker.touch()
                except BlockingIOError:
                    # Someone else is extracting, wait for them
                    fcntl.flock(f, fcntl.LOCK_EX)
                    # Once we get the lock, the marker should exist

            log_audit_event(
                actor="system:data_layer",
                action="data.batch_extract",
                target=tar_url,
                status="SUCCESS",
                details={
                    "cache_key": cache_key,
                    "count": len(cls._collect_videos(extract_dir)),
                },
            )

        # Gather results
        return cls._collect_videos(extract_dir)

    @classmethod
    def get_video_table(cls, video_data_list: list[dict]) -> "pa.Table":
        """Convert collected video metadata to an Arrow Table."""
        from datetime import datetime

        from sxd_core.arrow import VIDEO_METADATA_SCHEMA, dicts_to_table

        # Prepare for schema compliance
        rows = []
        for item in video_data_list:
            rows.append(
                {
                    "video_id": item.get("video_id", item.get("video_name", "unknown")),
                    "customer_id": item.get("customer_id", "default"),
                    "url": item.get("video_path", ""),
                    "status": "DETECTED",
                    "timestamp": datetime.now(),
                }
            )

        return dicts_to_table(rows, schema=VIDEO_METADATA_SCHEMA)

    # --- Internal Helpers ---

    @staticmethod
    def _handle_local_file(path: str, job_id: str) -> str:
        scratch_dir = get_scratch_path() / job_id
        scratch_dir.mkdir(parents=True, exist_ok=True)
        dest_path = scratch_dir / "source.mp4"

        # Don't copy if it's the exact same file
        if Path(path).resolve() != dest_path.resolve():
            io.copy2(path, str(dest_path))

        return str(dest_path)

    @staticmethod
    def _download_from_hf(url: str, dest_path: Path, cache_dir: Path) -> str:
        repo_id, file_path = DataManager._parse_hf_url(url)

        if not file_path:
            # Auto-detect first video
            files = list_repo_files(repo_id, repo_type="dataset")
            video_files = [f for f in files if f.endswith((".mp4", ".avi", ".mov"))]
            if not video_files:
                raise ValueError(f"No videos found in {repo_id}")
            file_path = video_files[0]

        downloaded = hf_hub_download(
            repo_id=repo_id,
            filename=file_path,
            repo_type="dataset",
            cache_dir=str(cache_dir / "hf_cache"),
        )

        if file_path.endswith(".tar"):
            # If user submitted a tar to the single-video workflow, extract first video
            return DataManager._handle_single_tar_fallback(
                Path(str(downloaded)), Path(str(dest_path))
            )

        io.copy2(str(downloaded), str(dest_path))
        return str(dest_path)

    @staticmethod
    def _download_from_http(url: str, dest_path: Path) -> str:
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()

        # Use .open() on the Path object to handle UPath/S3Path correctly
        with io.open_file(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return str(dest_path)

    @staticmethod
    def _parse_hf_url(url: str):
        parts = url[5:].split("/")
        if len(parts) < 2:
            raise ValueError(f"Invalid HF URL: {url}")
        repo_id = f"{parts[0]}/{parts[1]}"
        file_path = "/".join(parts[2:]) if len(parts) > 2 else None
        return repo_id, file_path

    @staticmethod
    def _extract_tar(tar_path: Path, output_dir: Path):
        """Extract tar using best available method (pigz > tar)."""
        try:
            io.run(["pigz", "--version"], capture_output=True, check=True)
            io.run(
                ["tar", "-I", "pigz", "-xf", str(tar_path), "-C", str(output_dir)],
                check=True,
                capture_output=True,
            )
        except (io.CalledProcessError, FileNotFoundError):
            io.run(
                ["tar", "-xf", str(tar_path), "-C", str(output_dir)],
                check=True,
                capture_output=True,
            )

    @staticmethod
    def _collect_videos(extract_dir: Path) -> list[dict]:
        video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".webm")
        video_files: list[Path] = []
        for ext in video_extensions:
            video_files.extend(extract_dir.rglob(f"*{ext}"))

        return [
            {"video_path": str(f), "video_name": f.name, "index": idx}
            for idx, f in enumerate(sorted(video_files))
        ]

    @staticmethod
    def _handle_single_tar_fallback(tar_path: Path, dest_path: Path) -> str:
        # Emergency fallback logic for legacy behavior
        extract_dir = dest_path.parent / "extracted_fallback"
        extract_dir.mkdir(exist_ok=True)
        DataManager._extract_tar(tar_path, extract_dir)
        videos = DataManager._collect_videos(extract_dir)
        if not videos:
            raise ValueError("No videos in tar")
        io.copy2(videos[0]["video_path"], dest_path)
        return str(dest_path)

    @staticmethod
    def _validate_url(url: str):
        """SSRF Protection: Block non-public IP ranges."""
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            raise ValueError(f"Invalid URL: {url}")

        try:
            ip = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip)

            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                raise ValueError(
                    f"Security Error: Access to internal IP {ip} is blocked."
                )
        except socket.gaierror:
            # If we can't resolve it, we don't block it yet (might be a valid DNS failure)
            pass
        except Exception as e:
            raise ValueError(f"Security validation failed: {str(e)}")
