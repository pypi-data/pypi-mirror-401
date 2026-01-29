"""
Storage abstraction layer using universal_pathlib.

Phase 0-1: Uses local filesystem
Phase 2+: Switches to S3-compatible storage (e.g. Cloudflare R2)

The beauty of UPath is that Phase transition is just changing the base URI:
- Phase 0-1: "./data"  or "/opt/sxd/data"
- Phase 2+:  "s3://staging"

Usage:
    from src.storage import get_storage

    # Get a path
    storage = get_storage()
    video_path = storage / "customer-1" / "video.mp4"

    # Write
    video_path.parent.mkdir(parents=True, exist_ok=True)
    video_path.write_bytes(b"video data")

    # Read
    data = video_path.read_bytes()

    # Check existence
    if video_path.exists():
        print("File exists")

    # List files
    for file in video_path.parent.iterdir():
        print(file.name)
"""

from pathlib import Path

import yaml
from upath import UPath

from sxd_core import io
from sxd_core.audit import get_trace_id, log_audit_event


def get_storage() -> UPath:
    """
    Get the configured storage path.

    Returns UPath that works with both local filesystem and S3.
    Phase migration is just changing config, not code.
    """
    # Read configuration
    config_env = io.getenv("SXD_CONFIG_PATH")
    if config_env:
        config_path = Path(config_env)
    else:
        config_path = (
            Path(__file__).parent.parent.parent.parent / "config" / "settings.yaml"
        )

    if config_path.exists():
        with io.open_file(config_path) as f:
            config = yaml.safe_load(f)

        storage_config = config.get("storage", {})
        # Prioritize environment variable, fallback to config, then default
        backend = io.getenv("SXD_STORAGE_BACKEND") or storage_config.get(
            "backend", "local"
        )

        if backend == "r2":
            # Cloudflare R2
            endpoint = io.getenv("SXD_R2_ENDPOINT")
            bucket = io.getenv("SXD_R2_BUCKET", "sxd-backup")
            access_key = io.getenv("SXD_R2_ACCESS_KEY")
            secret_key = io.getenv("SXD_R2_SECRET_KEY")

            if not all([endpoint, access_key, secret_key]):
                raise ValueError(
                    "R2 backend requires SXD_R2_ENDPOINT, SXD_R2_ACCESS_KEY, and SXD_R2_SECRET_KEY"
                )

            return UPath(
                f"s3://{bucket}",
                endpoint_url=endpoint,
                key=access_key,
                secret=secret_key,
                client_kwargs={"region_name": "auto"},
            )

        elif backend == "s3":
            # S3 storage (Cloudflare R2 or AWS)
            endpoint = io.getenv("SXD_STORAGE_ENDPOINT") or storage_config.get(
                "endpoint"
            )
            bucket = io.getenv("SXD_STORAGE_BUCKET") or storage_config.get(
                "bucket", "staging"
            )
            access_key = io.getenv("SXD_STORAGE_ACCESS_KEY", "")
            secret_key = io.getenv("SXD_STORAGE_SECRET_KEY", "")

            # S3 backends with -iam=false or public buckets might need anonymous requests
            return UPath(
                f"s3://{bucket}",
                endpoint_url=endpoint,
                key=access_key if access_key else None,
                secret=secret_key if secret_key else None,
                anon=not (access_key and secret_key),  # Anonymous if no creds
                client_kwargs={"region_name": "us-east-1"},
            )
        else:
            # Phase 0-1: Local filesystem
            base_path = storage_config.get("base_path", ".")
            return UPath(base_path)
    else:
        # Default to current directory
        return UPath(".")


def get_staging_path() -> UPath:
    """Get staging directory path."""
    config_path = (
        Path(__file__).parent.parent.parent.parent / "config" / "settings.yaml"
    )

    if config_path.exists():
        with io.open_file(config_path) as f:
            config = yaml.safe_load(f)
        staging_dir = config.get("storage", {}).get("staging_dir", "data")
    else:
        staging_dir = "data"

    return get_storage() / staging_dir


def get_scratch_path() -> UPath:
    """
    Get scratch directory path.
    ALWAYS local, even if staging is S3, because processing tools (FFmpeg) need local files.
    """
    config_env = io.getenv("SXD_CONFIG_PATH")
    if config_env:
        config_path = Path(config_env)
    else:
        config_path = (
            Path(__file__).parent.parent.parent.parent / "config" / "settings.yaml"
        )

    if config_path.exists():
        with io.open_file(config_path) as f:
            config = yaml.safe_load(f)
        storage_config = config.get("storage", {})
        scratch_dir = storage_config.get("scratch_dir", "scratch")
        # Use base_path from local config or default to current dir
        base_path = storage_config.get("base_path", ".")
        return UPath(base_path) / scratch_dir
    else:
        return UPath("scratch")


def upload_artifact(source_path: str, dest_rel_path: str) -> str:
    """
    Upload an artifact to the configured storage backend.

    This is the primary interface for activities to save data.
    It handles backend selection (S3 vs Local) and path structure transparently.

    Args:
        source_path: Local path to the file to upload.
        dest_rel_path: Relative path (e.g., 'job-123/video.mp4').
                       Will be prefixed with staging/data automatically.
    """
    # Standard UPath Abstraction (S3 or Local)
    staging_base = get_staging_path()
    dest_path = staging_base / dest_rel_path

    # Ensure parent exists (mainly for local filesystem or emulators)
    try:
        if not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        # S3 sometimes errors on checking parent existence or mkdir, which is fine
        pass

    with io.open_file(source_path, "rb") as src:
        dest_path.write_bytes(src.read())

    # Audit logging
    log_audit_event(
        actor="system:storage",
        action="data.upload",
        target=str(dest_path),
        status="SUCCESS",
        trace_id=get_trace_id(),
        details={"source": source_path, "rel_path": dest_rel_path},
    )

    # Return string representation of the path
    # For S3 this might be s3://..., for local it's /path/to...
    # For consumer consistency, we might want a URL, but path is standard for now.
    return str(dest_path)
