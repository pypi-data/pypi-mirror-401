"""
Worker Upload Service - Direct file upload endpoint for data locality.

Runs on each worker node, accepts file uploads directly from operators.
Files land locally where they'll be processed - no data movement needed.

Usage:
    uvicorn sxd_core.worker_upload:app --host 0.0.0.0 --port 8081
"""

import os
from pathlib import Path

import aiofiles
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from pydantic import BaseModel

from sxd_core.clickhouse import ClickHouseManager
from sxd_core.logging import get_logger
from sxd_core.auth import get_auth_manager
from sxd_core import io

log = get_logger(__name__)

app = FastAPI(
    title="SXD Worker Upload",
    description="Direct file upload service for data-local processing",
)

# Configuration
DATA_DIR = Path(os.getenv("SXD_DATA_DIR", "/data/incoming"))
CHUNK_SIZE = 4 * 1024 * 1024  # 4MB streaming chunks


class UploadResponse(BaseModel):
    file: str
    size: int
    session_id: str


class CompleteResponse(BaseModel):
    session_id: str
    episode_id: str
    status: str
    files_received: int
    bytes_received: int


@app.put("/upload/{session_id}/{path:path}")
async def upload_file(session_id: str, path: str, request: Request) -> UploadResponse:
    """
    Stream a file directly to local disk.

    Files are stored in: {DATA_DIR}/{session_id}/{path}
    Uses streaming to handle large files without memory buffering.
    """
    # 1. Verify Token
    token = request.headers.get("X-Upload-Token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing upload token")

    auth = get_auth_manager()
    payload = auth.verify_upload_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired upload token")

    if payload.get("sid") != session_id:
        raise HTTPException(status_code=403, detail="Token mismatch for session")

    # 2. Check Session State
    ch = ClickHouseManager()
    session = ch.get_upload_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["status"] not in ("ACTIVE", "RECEIVING"):
        raise HTTPException(
            status_code=400,
            detail=f"Session not accepting uploads (status: {session['status']})",
        )

    # Create file path
    file_path = DATA_DIR / session_id / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Stream to disk without buffering entire file in memory
    bytes_written = 0
    try:
        async with aiofiles.open(file_path, "wb") as f:
            async for chunk in request.stream():
                await f.write(chunk)
                bytes_written += len(chunk)
    except Exception as e:
        log.error("upload failed", session_id=session_id, path=path, error=str(e))
        # Clean up partial file
        if io.exists(file_path):
            io.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

    # Update session counters in ClickHouse
    ch.increment_upload_session(session_id, files_delta=1, bytes_delta=bytes_written)

    log.info(
        "file uploaded",
        session_id=session_id,
        path=path,
        size_mb=bytes_written / (1024 * 1024),
    )

    return UploadResponse(file=path, size=bytes_written, session_id=session_id)


@app.post("/upload/{session_id}/complete")
async def complete_upload(
    session_id: str, background_tasks: BackgroundTasks
) -> CompleteResponse:
    """
    Finalize upload and trigger local processing workflow.

    Since files are already on this node, processing starts immediately
    with no data transfer required.
    """
    ch = ClickHouseManager()
    session = ch.get_upload_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["status"] == "COMPLETED":
        # Already completed - return existing episode
        return CompleteResponse(
            session_id=session_id,
            episode_id=session.get("episode_id", ""),
            status="COMPLETED",
            files_received=session["files_received"],
            bytes_received=session["bytes_received"],
        )

    if session["status"] not in ("ACTIVE", "RECEIVING"):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete session (status: {session['status']})",
        )

    # Generate episode ID from session ID
    episode_id = f"ep-{session_id[5:]}"  # sess-xxx -> ep-xxx
    staging_path = str(DATA_DIR / session_id)

    # Update session status
    ch.update_upload_session(session_id, status="PROCESSING", episode_id=episode_id)

    log.info(
        "upload complete, triggering workflow",
        session_id=session_id,
        episode_id=episode_id,
        files=session["files_received"],
        bytes=session["bytes_received"],
    )

    # Trigger local processing workflow in background
    background_tasks.add_task(
        _trigger_local_workflow,
        episode_id=episode_id,
        customer_id=session["customer_id"],
        staging_path=staging_path,
        session_id=session_id,
    )

    return CompleteResponse(
        session_id=session_id,
        episode_id=episode_id,
        status="PROCESSING",
        files_received=session["files_received"],
        bytes_received=session["bytes_received"],
    )


@app.get("/upload/{session_id}/status")
async def get_upload_status(session_id: str):
    """Get current upload progress for a session on this worker."""
    ch = ClickHouseManager()
    session = ch.get_upload_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check local files
    session_dir = DATA_DIR / session_id
    local_files = []
    local_bytes = 0
    if io.exists(session_dir):
        for f in io.rglob(session_dir, "*"):
            if io.isfile(f):
                f_path = Path(f)
                local_files.append(str(f_path.relative_to(session_dir)))
                local_bytes += io.getsize(f)

    return {
        "session_id": session_id,
        "status": session["status"],
        "files_received": session["files_received"],
        "bytes_received": session["bytes_received"],
        "local_files": len(local_files),
        "local_bytes": local_bytes,
        "episode_id": session.get("episode_id"),
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    # Check ClickHouse connectivity
    try:
        ch = ClickHouseManager()
        ch.execute_query("SELECT 1")
        ch_status = "connected"
    except Exception as e:
        ch_status = f"error: {e}"

    # Check data directory
    data_dir_ok = io.exists(DATA_DIR) and os.access(DATA_DIR, os.W_OK)

    return {
        "status": "ok" if ch_status == "connected" and data_dir_ok else "degraded",
        "clickhouse": ch_status,
        "data_dir": str(DATA_DIR),
        "data_dir_writable": data_dir_ok,
        "node": os.getenv("SXD_NODE_ID", "unknown"),
    }


async def _trigger_local_workflow(
    episode_id: str,
    customer_id: str,
    staging_path: str,
    session_id: str,
):
    """
    Trigger local processing workflow via Temporal.

    Since files are already on this node, no transfer is needed.
    The workflow just checksums, indexes, and processes locally.
    """
    from sxd_core.config import get_temporal_config

    try:
        from temporalio.client import Client

        tc = get_temporal_config()
        client = await Client.connect(f"{tc['host']}:{tc['port']}")

        # Start local ingest workflow
        # This workflow runs activities on this node since data is local
        await client.start_workflow(
            "local-ingest",
            args=[
                {
                    "episode_id": episode_id,
                    "customer_id": customer_id,
                    "staging_path": staging_path,
                }
            ],
            id=f"local-ingest-{episode_id}",
            task_queue=f"node-{os.getenv('SXD_NODE_ID', 'worker')}",
        )

        log.info("local workflow started", episode_id=episode_id)

        # Update session status
        ch = ClickHouseManager()
        ch.update_upload_session(session_id, status="COMPLETED")

    except Exception as e:
        log.error("failed to start local workflow", episode_id=episode_id, error=str(e))
        ch = ClickHouseManager()
        ch.update_upload_session(session_id, status="FAILED", error=str(e))


def main():
    """Run the worker upload service."""
    import uvicorn

    host = os.getenv("SXD_UPLOAD_HOST", "0.0.0.0")
    port = int(os.getenv("SXD_UPLOAD_PORT", "8081"))

    log.info(
        "starting worker upload service", host=host, port=port, data_dir=str(DATA_DIR)
    )
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
