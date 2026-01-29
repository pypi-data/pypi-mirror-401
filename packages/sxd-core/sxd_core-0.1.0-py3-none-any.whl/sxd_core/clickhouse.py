import logging
import os
import threading
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

from sxd_core import io

import clickhouse_connect

from sxd_core.exceptions import ClickHouseConnectionError

# Use standard logging for internal ClickHouse errors to avoid recursion
# with the StructuredLogger which uses ClickHouse for ingestion.
internal_log = logging.getLogger("sxd.clickhouse.internal")


class ClickHousePool:
    """
    Connection pool for ClickHouse clients.

    Manages a pool of ClickHouse connections for efficient reuse.
    Thread-safe for concurrent access.

    Args:
        min_size: Minimum pool size (connections to keep alive).
        max_size: Maximum pool size.
        max_idle_time: Max seconds a connection can be idle before closing.
        connection_timeout: Timeout for acquiring a connection.

    Example:
        pool = ClickHousePool(min_size=2, max_size=10)
        with pool.acquire() as client:
            result = client.query("SELECT 1")
    """

    _instance: Optional["ClickHousePool"] = None
    _lock = threading.Lock()

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str = "sxd",
        min_size: int = 2,
        max_size: int = 10,
        max_idle_time: float = 300.0,
        connection_timeout: float = 30.0,
    ):
        self.host = (
            host
            or os.getenv("SXD_CLICKHOUSE_HOST")
            or os.getenv("CLICKHOUSE_HOST", "127.0.0.1")
        )
        port_val = (
            port
            or os.getenv("SXD_CLICKHOUSE_PORT")
            or os.getenv("CLICKHOUSE_PORT", "8123")
        )
        self.port = int(port_val) if port_val else 8123
        self.user = (
            user
            or os.getenv("SXD_CLICKHOUSE_USER")
            or os.getenv("CLICKHOUSE_USER", "default")
        )
        self.password = (
            password
            if password is not None
            else (
                os.getenv("SXD_CLICKHOUSE_PASSWORD")
                or os.getenv("CLICKHOUSE_PASSWORD", "")
            )
        )
        self.database = database
        self.min_size = min_size
        self.max_size = max_size
        self.max_idle_time = max_idle_time
        self.connection_timeout = connection_timeout

        self._pool: List[tuple] = []  # List of (client, last_used_time)
        self._pool_lock = threading.Lock()
        self._size = 0

        self._stats = {
            "connections_created": 0,
            "connections_reused": 0,
            "connections_closed": 0,
            "acquire_timeouts": 0,
        }

    @classmethod
    def get_pool(cls, **kwargs) -> "ClickHousePool":
        """Get the global pool instance (singleton)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(**kwargs)
        return cls._instance

    @classmethod
    def reset_pool(cls):
        """Reset the global pool (for testing)."""
        with cls._lock:
            if cls._instance:
                cls._instance.close_all()
            cls._instance = None

    def _create_client(self):
        """Create a new ClickHouse client."""
        try:
            client = clickhouse_connect.get_client(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                database=self.database,
            )
            with self._pool_lock:
                self._stats["connections_created"] += 1
            return client
        except Exception as e:
            raise ClickHouseConnectionError(
                host=self.host,
                port=self.port,
                cause=e,
            )

    def _is_healthy(self, client) -> bool:
        """Check if a connection is still healthy."""
        try:
            client.command("SELECT 1")
            return True
        except Exception:
            return False

    @contextmanager
    def acquire(self):
        """
        Acquire a connection from the pool.

        Usage:
            with pool.acquire() as client:
                result = client.query("SELECT 1")
        """
        client = None
        acquired_from_pool = False

        with self._pool_lock:
            # Try to get pool
            now = io.time()
            while self._pool:
                pooled_client, last_used = self._pool.pop(0)
                # Check if connection is stale
                if now - last_used > self.max_idle_time:
                    self._close_client(pooled_client)
                    continue
                # Check health (outside lock to avoid holding lock during network call)
                if self._is_healthy(pooled_client):
                    client = pooled_client
                    acquired_from_pool = True
                    break
                else:
                    self._close_client(pooled_client)

        # Track reuse outside the earlier loop
        if acquired_from_pool:
            with self._pool_lock:
                self._stats["connections_reused"] += 1

        # Create new if needed
        if client is None:
            with self._pool_lock:
                if self._size >= self.max_size:
                    # Pool exhausted - wait or timeout
                    self._stats["acquire_timeouts"] += 1
                    raise ClickHouseConnectionError(
                        host=self.host,
                        port=self.port,
                        cause=Exception("Connection pool exhausted"),
                    )
                self._size += 1

            try:
                client = self._create_client()
            except Exception:
                with self._pool_lock:
                    self._size -= 1
                raise

        try:
            yield client
        finally:
            # Return to pool
            if client:
                self._return_to_pool(client)

    def _return_to_pool(self, client):
        """Return a client to the pool."""
        with self._pool_lock:
            if len(self._pool) < self.max_size:
                self._pool.append((client, io.time()))
            else:
                self._close_client(client)

    def _close_client(self, client):
        """Close a client connection."""
        try:
            if hasattr(client, "close"):
                client.close()
        except Exception:
            pass
        with self._pool_lock:
            self._size = max(0, self._size - 1)
            self._stats["connections_closed"] += 1

    def close_all(self):
        """Close all connections in the pool."""
        with self._pool_lock:
            for client, _ in self._pool:
                try:
                    if hasattr(client, "close"):
                        client.close()
                except Exception:
                    pass
            self._pool.clear()
            self._size = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics."""
        with self._pool_lock:
            return {
                **self._stats,
                "pool_size": len(self._pool),
                "total_connections": self._size,
                "max_size": self.max_size,
            }


class ClickHouseManager:
    """
    Manages connections and schema for ClickHouse.
    Consolidates logs, audit events, and telemetry.

    Can operate in two modes:
    - Direct mode (default): Creates its own connection
    - Pool mode: Uses the global connection pool

    Args:
        use_pool: If True, use connection pooling.
    """

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str = "sxd",
        use_pool: bool = False,
        client_override: Any = None,
    ):
        # Dependency Injection: Allow client override for testing (e.g., ChDBClient for in-memory tests).
        # This bypasses connection setup and is the recommended pattern for unit testing.
        if client_override is not None:
            self._client = client_override
            self.database = database
            self.use_pool = False
            self._pool = None
            self.host = None
            self.port = None
            self.user = None
            self.password = None
            return

        # Check for SXD_ prefixed variables first, then fallback to CLICKHOUSE_ for compatibility
        self.host = (
            host
            or os.getenv("SXD_CLICKHOUSE_HOST")
            or os.getenv("CLICKHOUSE_HOST", "127.0.0.1")
        )
        port_val = (
            port
            or os.getenv("SXD_CLICKHOUSE_PORT")
            or os.getenv("CLICKHOUSE_PORT", "8123")
        )
        self.port = int(port_val) if port_val else 8123
        self.user = (
            user
            or os.getenv("SXD_CLICKHOUSE_USER")
            or os.getenv("CLICKHOUSE_USER", "default")
        )
        self.password = (
            password
            if password is not None
            else (
                os.getenv("SXD_CLICKHOUSE_PASSWORD")
                or os.getenv("CLICKHOUSE_PASSWORD", "")
            )
        )
        self.database = database
        self.use_pool = use_pool
        self._client = None
        self._pool = None

        if use_pool:
            self._pool = ClickHousePool.get_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=database,
            )

    @property
    def client(self):
        """Get a ClickHouse client.

        If using pool mode, this returns the pool for use with context manager.
        For direct mode, returns a persistent client connection.
        """
        if self.use_pool and self._pool:
            # For pool mode, caller should use get_client() context manager
            return None

        if self._client is None:
            try:
                self._client = clickhouse_connect.get_client(
                    host=self.host,
                    port=self.port,
                    username=self.user,
                    password=self.password,
                    database=self.database,
                )
            except Exception as e:
                # In dev, we don't want to hard-crash if ClickHouse isn't up yet
                internal_log.warning("Could not connect to ClickHouse: %s", str(e))
                return None
        return self._client

    @contextmanager
    def get_client(self):
        """Get a client from the pool (for pool mode) or return the direct client.

        Usage:
            with manager.get_client() as client:
                result = client.query("SELECT 1")
        """
        if self.use_pool and self._pool:
            with self._pool.acquire() as client:
                yield client
        else:
            yield self.client

    def get_pool_stats(self) -> Optional[Dict[str, Any]]:
        """Get connection pool statistics (if using pool mode)."""
        if self._pool:
            return self._pool.get_stats()
        return None

    def init_db(self):
        """Initialize the SXD database and tables if they don't exist."""
        client = self.client
        if not client:
            return

        client.command(f"CREATE DATABASE IF NOT EXISTS {self.database}")

        # Logs Table
        client.command(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.logs (
                timestamp DateTime64(6, 'UTC'),
                level LowCardinality(String),
                logger LowCardinality(String),
                message String,
                trace_id String,
                job_id String,
                activity String,
                details String
            ) ENGINE = MergeTree()
            PARTITION BY toYYYYMM(timestamp)
            ORDER BY (timestamp, level, logger)
        """
        )

        # Audit Events Table (SOC 2)
        client.command(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.audit_events (
                timestamp DateTime64(6, 'UTC'),
                actor String,
                action LowCardinality(String),
                target String,
                status LowCardinality(String),
                environment LowCardinality(String),
                client_ip String,
                trace_id String,
                details String
            ) ENGINE = MergeTree()
            PARTITION BY toYYYYMM(timestamp)
            ORDER BY (timestamp, action, actor)
        """
        )

        # Telemetry Table (Generic Metrics)
        client.command(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.telemetry (
                timestamp DateTime64(6, 'UTC'),
                metric_name LowCardinality(String),
                value Float64,
                tags Map(String, String)
            ) ENGINE = MergeTree()
            PARTITION BY toYYYYMM(timestamp)
            ORDER BY (metric_name, timestamp)
        """
        )

        # Video Metadata Table (migrated from PostgreSQL)
        client.command(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.videos (
                id String,
                customer_id String,
                video_id String,
                batch_id String,
                source_url String,
                staging_path String,
                parquet_path String,
                lance_path String,
                quality_score Float64,
                blur_mean Float64,
                frame_count Int32,
                status LowCardinality(String),
                node String,
                size_bytes Int64,
                error String,
                meta_json String,
                created_at DateTime64(6, 'UTC'),
                updated_at DateTime64(6, 'UTC')
            ) ENGINE = ReplacingMergeTree(updated_at)
            PARTITION BY toYYYYMM(created_at)
            ORDER BY (customer_id, id)
        """
        )

        # Batch Metadata Table (migrated from PostgreSQL)
        client.command(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.batches (
                id String,
                customer_id String,
                tar_url String,
                status LowCardinality(String),
                total_videos Int32,
                successful_videos Int32,
                failed_videos Int32,
                created_at DateTime64(6, 'UTC'),
                updated_at DateTime64(6, 'UTC')
            ) ENGINE = ReplacingMergeTree(updated_at)
            PARTITION BY toYYYYMM(created_at)
            ORDER BY (customer_id, id)
        """
        )

        # Episodes Table (Upload Sessions / Data Orders)
        # Status lifecycle: UPLOADING -> UPLOADED -> PROCESSING -> COMPLETED -> ARCHIVED
        client.command(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.episodes (
                id String,
                customer_id String,
                source_path String,
                total_size Int64,
                chunk_count Int32,
                file_count Int32,
                total_duration_seconds Float64,
                resolution LowCardinality(String),
                status LowCardinality(String),
                processing_status LowCardinality(String),
                target_node String,
                workflow_id String,
                created_at DateTime64(6, 'UTC'),
                updated_at DateTime64(6, 'UTC')
            ) ENGINE = ReplacingMergeTree(updated_at)
            PARTITION BY toYYYYMM(created_at)
            ORDER BY (customer_id, id)
        """
        )

        # Chunks Table (Individual Parts)
        client.command(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.chunks (
                episode_id String,
                chunk_index Int32,
                file_name String,
                size_bytes Int64,
                checksum String,
                status LowCardinality(String),
                target_node String,
                remote_path String,
                error String,
                started_at DateTime64(6, 'UTC'),
                completed_at DateTime64(6, 'UTC')
            ) ENGINE = ReplacingMergeTree(completed_at)
            PARTITION BY episode_id
            ORDER BY (episode_id, chunk_index)
        """
        )

        # Upload Sessions Table (HTTP Upload Tracking)
        # Tracks HTTP uploads before they become Temporal-managed episodes
        # Status lifecycle: ACTIVE -> RECEIVING -> PROCESSING -> COMPLETED/FAILED
        # node_assignments: JSON mapping node -> {files: [...], total_bytes: N}
        client.command(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.upload_sessions (
                session_id String,
                customer_id String,
                status LowCardinality(String),
                total_files Int32,
                files_received Int32,
                total_bytes Int64,
                bytes_received Int64,
                staging_path String,
                node_assignments String,
                episode_id String,
                error String,
                created_at DateTime64(6, 'UTC'),
                updated_at DateTime64(6, 'UTC'),
                expires_at DateTime64(6, 'UTC')
            ) ENGINE = ReplacingMergeTree(updated_at)
            PARTITION BY toYYYYMM(created_at)
            ORDER BY (customer_id, session_id)
            TTL expires_at + INTERVAL 7 DAY
        """
        )

        # Pipelines Table (Persisted metadata for workflows/apps)
        client.command(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.pipelines (
                name String,
                version String,
                description String,
                base_image String,
                gpu Boolean,
                timeout Int32,
                updated_at DateTime64(6, 'UTC')
            ) ENGINE = ReplacingMergeTree(updated_at)
            ORDER BY (name)
        """
        )

        internal_log.info(
            "ClickHouse database and tables initialized: %s", self.database
        )

    def insert_logs(self, rows: List[List[Any]]):
        """Insert logs into ClickHouse."""
        client = self.client
        if client:
            client.insert(
                f"{self.database}.logs",
                rows,
                column_names=[
                    "timestamp",
                    "level",
                    "logger",
                    "message",
                    "trace_id",
                    "job_id",
                    "activity",
                    "details",
                ],
            )

    def insert_audit_events(self, rows: List[List[Any]]):
        """Insert audit events into ClickHouse."""
        client = self.client
        if client:
            client.insert(
                f"{self.database}.audit_events",
                rows,
                column_names=[
                    "timestamp",
                    "actor",
                    "action",
                    "target",
                    "status",
                    "environment",
                    "client_ip",
                    "trace_id",
                    "details",
                ],
            )

    def insert_telemetry(self, rows: List[List[Any]]):
        """Insert telemetry into ClickHouse."""
        client = self.client
        if client:
            client.insert(
                f"{self.database}.telemetry",
                rows,
                column_names=["timestamp", "metric_name", "value", "tags"],
            )

    def upsert_video_metadata(self, data: Dict[str, Any]) -> str:
        """
        Insert or update video metadata.
        Uses ReplacingMergeTree - inserts new row with updated_at, older rows are merged away.
        """
        import json
        from sxd_core import io

        client = self.client
        if not client:
            internal_log.warning(
                "ClickHouse not available, skipping video metadata upsert"
            )
            return data.get("id", "")

        now = io.now()
        row = [
            [
                str(data.get("id", "")),
                str(data.get("customer_id", "")),
                str(data.get("video_id", "")),
                str(data.get("batch_id", "")),
                str(data.get("source_url", "")),
                str(data.get("staging_path", "")),
                str(data.get("parquet_path", "")),
                str(data.get("lance_path", "")),
                float(data.get("quality_score", 0.0)),
                float(data.get("blur_mean", 0.0)),
                int(data.get("frame_count", 0)),
                str(data.get("status", "PROCESSING")),
                str(data.get("node", os.getenv("SXD_NODE_ID", ""))),
                int(data.get("size_bytes", 0)),
                str(data.get("error", "")),
                (
                    json.dumps(data.get("meta_json", {}))
                    if isinstance(data.get("meta_json"), dict)
                    else str(data.get("meta_json", "{}"))
                ),
                data.get("created_at", now),
                now,  # updated_at
            ]
        ]

        client.insert(
            f"{self.database}.videos",
            row,
            column_names=[
                "id",
                "customer_id",
                "video_id",
                "batch_id",
                "source_url",
                "staging_path",
                "parquet_path",
                "lance_path",
                "quality_score",
                "blur_mean",
                "frame_count",
                "status",
                "node",
                "size_bytes",
                "error",
                "meta_json",
                "created_at",
                "updated_at",
            ],
        )
        return data.get("id", "")

    def upsert_batch_metadata(self, data: Dict[str, Any]) -> str:
        """
        Insert or update batch metadata.
        Uses ReplacingMergeTree - inserts new row with updated_at, older rows are merged away.
        """
        from sxd_core import io

        client = self.client
        if not client:
            internal_log.warning(
                "ClickHouse not available, skipping batch metadata upsert"
            )
            return data.get("id", "")

        now = io.now()
        row = [
            [
                str(data.get("id", "")),
                str(data.get("customer_id", "")),
                str(data.get("tar_url", "")),
                str(data.get("status", "PENDING")),
                int(data.get("total_videos", 0)),
                int(data.get("successful_videos", 0)),
                int(data.get("failed_videos", 0)),
                data.get("created_at", now),
                now,  # updated_at
            ]
        ]

        client.insert(
            f"{self.database}.batches",
            row,
            column_names=[
                "id",
                "customer_id",
                "tar_url",
                "status",
                "total_videos",
                "successful_videos",
                "failed_videos",
                "created_at",
                "updated_at",
            ],
        )
        return data.get("id", "")

    def upsert_episode(self, data: Dict[str, Any]) -> str:
        """
        Insert or update episode metadata.

        Fields:
            - status: Upload state (UPLOADING, UPLOADED, FAILED, CANCELLED)
            - target_node: Node where data is stored
            - workflow_id: Temporal workflow ID
        """
        from sxd_core import io

        client = self.client
        if not client:
            return data.get("id", "")

        now = io.now()
        # Use only core columns that exist in all schema versions
        row = [
            [
                str(data.get("id", "")),
                str(data.get("customer_id", "")),
                str(data.get("source_path", "")),
                int(data.get("total_size", 0)),
                int(data.get("chunk_count", 0)),
                str(data.get("status", "UPLOADING")),
                str(data.get("target_node", "")),
                str(data.get("workflow_id", "")),
                data.get("created_at", now),
                now,  # updated_at
            ]
        ]

        client.insert(
            f"{self.database}.episodes",
            row,
            column_names=[
                "id",
                "customer_id",
                "source_path",
                "total_size",
                "chunk_count",
                "status",
                "target_node",
                "workflow_id",
                "created_at",
                "updated_at",
            ],
        )
        return data.get("id", "")

    def upsert_chunk(self, data: Dict[str, Any]):
        """
        Insert or update chunk metadata.
        """
        from sxd_core import io

        client = self.client
        if not client:
            return

        now = io.now()
        # Handle completed_at being optional
        completed = data.get("completed_at", now)
        if completed is None:
            completed = now  # Check consistency - maybe future? or 0? ReplacingMergeTree needs a value. Use 'start' if clean.

        row = [
            [
                str(data.get("episode_id", "")),
                int(data.get("chunk_index", 0)),
                str(data.get("file_name", "")),
                int(data.get("size_bytes", 0)),
                str(data.get("checksum", "")),
                str(data.get("status", "PENDING")),
                str(data.get("target_node", "")),
                str(data.get("remote_path", "")),
                str(data.get("error", "")),
                data.get("started_at", now),
                completed,
            ]
        ]

        client.insert(
            f"{self.database}.chunks",
            row,
            column_names=[
                "episode_id",
                "chunk_index",
                "file_name",
                "size_bytes",
                "checksum",
                "status",
                "target_node",
                "remote_path",
                "error",
                "started_at",
                "completed_at",
            ],
        )

    def upsert_pipeline(self, data: Dict[str, Any]):
        """
        Insert or update pipeline metadata.
        """
        from sxd_core import io

        client = self.client
        if not client:
            return

        now = io.now()
        row = [
            [
                str(data.get("name", "")),
                str(data.get("version", "0.1.0")),
                str(data.get("description", "")),
                str(data.get("base_image", "sxd-base")),
                bool(data.get("gpu", False)),
                int(data.get("timeout", 3600)),
                now,
            ]
        ]

        client.insert(
            f"{self.database}.pipelines",
            row,
            column_names=[
                "name",
                "version",
                "description",
                "base_image",
                "gpu",
                "timeout",
                "updated_at",
            ],
        )

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a raw SQL query and return results as list of dicts."""
        client = self.client
        if not client:
            return []

        try:
            result = client.query(query)
            # Convert named results to list to ensure it's subscriptable
            return list(result.named_results())
        except Exception as e:
            internal_log.error(f"Query failed: {query}. Error: {e}")
            raise

    def export_table(self, table: str, output_path: str, format: str = "Parquet") -> None:
        """
        Export table content to a file using streaming.
        Useful for backups.
        """
        client = self.client
        if not client:
            raise RuntimeError("ClickHouse client not available")

        query = f"SELECT * FROM {table}"
        try:
            # Use raw_stream to get bytes without loading into memory
            # clickhouse_connect client supports raw_stream(query, fmt)
            with open(output_path, "wb") as f:
                for chunk in client.raw_stream(query=query, fmt=format):
                    f.write(chunk)
        except Exception as e:
            internal_log.error(f"Export failed for {table}. Error: {e}")
            raise

    def list_videos(
        self, limit: int = 50, offset: int = 0, customer_id: str | None = None
    ) -> List[Dict[str, Any]]:
        """List processed videos."""
        where_clause = f"WHERE customer_id = '{customer_id}'" if customer_id else ""
        return self.execute_query(
            f"""
            SELECT * FROM {self.database}.videos
            {where_clause}
            ORDER BY created_at DESC
            LIMIT {limit} OFFSET {offset}
        """
        )

    def list_batches(
        self, limit: int = 20, customer_id: str | None = None
    ) -> List[Dict[str, Any]]:
        """List submitted batches."""
        where_clause = f"WHERE customer_id = '{customer_id}'" if customer_id else ""
        return self.execute_query(
            f"""
            SELECT * FROM {self.database}.batches
            {where_clause}
            ORDER BY created_at DESC
            LIMIT {limit}
        """
        )

    def list_episodes(
        self, limit: int = 20, customer_id: str | None = None
    ) -> List[Dict[str, Any]]:
        """List upload episodes."""
        where_clause = f"WHERE customer_id = '{customer_id}'" if customer_id else ""
        # Use argMax to get only the latest row per episode ID
        # ReplacingMergeTree with FINAL can still show duplicates if merge hasn't run
        # argMax guarantees we get the most recent status for each episode
        return self.execute_query(
            f"""
            SELECT
                id,
                argMax(customer_id, updated_at) as customer_id,
                argMax(source_path, updated_at) as source_path,
                argMax(total_size, updated_at) as total_size,
                argMax(chunk_count, updated_at) as chunk_count,
                argMax(status, updated_at) as status,
                argMax(target_node, updated_at) as target_node,
                argMax(workflow_id, updated_at) as workflow_id,
                argMax(created_at, updated_at) as created_at,
                max(updated_at) as last_updated
            FROM {self.database}.episodes
            {where_clause}
            GROUP BY id
            ORDER BY last_updated DESC
            LIMIT {limit}
        """
        )

    def get_video(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get video details by ID."""
        res = self.execute_query(
            f"""
            SELECT * FROM {self.database}.videos
            WHERE video_id = '{video_id}' OR id = '{video_id}'
            LIMIT 1
        """
        )
        return res[0] if res else None

    # -------------------------------------------------------------------------
    # Upload Session Methods (HTTP Upload Tracking)
    # -------------------------------------------------------------------------

    def create_upload_session(
        self,
        session_id: str,
        customer_id: str,
        total_files: int = 1,
        total_bytes: int = 0,
        staging_path: str = "",
        node_assignments: Optional[Dict[str, Any]] = None,
        expires_hours: int = 24,
    ) -> Dict[str, Any]:
        """
        Create a new upload session for HTTP-based uploads.

        Args:
            session_id: Unique session identifier (e.g., "sess-abc123")
            customer_id: Customer/tenant ID
            total_files: Expected number of files
            total_bytes: Expected total size in bytes
            staging_path: Base staging directory path template
            node_assignments: Dict mapping node -> {url, files, total_bytes}
            expires_hours: Hours until session expires (default 24)

        Returns:
            Created session data
        """
        import json
        from datetime import timedelta

        client = self.client
        if not client:
            raise ClickHouseConnectionError(
                host=self.host or "127.0.0.1",
                port=self.port or 8123,
                cause=Exception("ClickHouse not available"),
            )

        now = io.now()
        expires_at = now + timedelta(hours=expires_hours)
        assignments_json = json.dumps(node_assignments or {})

        row = [
            [
                session_id,
                customer_id,
                "ACTIVE",  # status
                total_files,
                0,  # files_received
                total_bytes,
                0,  # bytes_received
                staging_path,
                assignments_json,  # node_assignments
                "",  # episode_id (set when workflow starts)
                "",  # error
                now,  # created_at
                now,  # updated_at
                expires_at,
            ]
        ]

        client.insert(
            f"{self.database}.upload_sessions",
            row,
            column_names=[
                "session_id",
                "customer_id",
                "status",
                "total_files",
                "files_received",
                "total_bytes",
                "bytes_received",
                "staging_path",
                "node_assignments",
                "episode_id",
                "error",
                "created_at",
                "updated_at",
                "expires_at",
            ],
        )

        return {
            "session_id": session_id,
            "customer_id": customer_id,
            "status": "ACTIVE",
            "total_files": total_files,
            "files_received": 0,
            "total_bytes": total_bytes,
            "bytes_received": 0,
            "staging_path": staging_path,
            "node_assignments": node_assignments or {},
            "episode_id": "",
            "created_at": now,
            "updated_at": now,
            "expires_at": expires_at,
        }

    def get_upload_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get upload session by ID.

        Uses argMax to handle ReplacingMergeTree duplicates.

        Args:
            session_id: Session identifier

        Returns:
            Session data or None if not found (node_assignments parsed as dict)
        """
        import json

        res = self.execute_query(
            f"""
            SELECT
                session_id,
                argMax(customer_id, updated_at) as customer_id,
                argMax(status, updated_at) as status,
                argMax(total_files, updated_at) as total_files,
                argMax(files_received, updated_at) as files_received,
                argMax(total_bytes, updated_at) as total_bytes,
                argMax(bytes_received, updated_at) as bytes_received,
                argMax(staging_path, updated_at) as staging_path,
                argMax(node_assignments, updated_at) as node_assignments,
                argMax(episode_id, updated_at) as episode_id,
                argMax(error, updated_at) as error,
                argMax(created_at, updated_at) as created_at,
                max(updated_at) as updated_at,
                argMax(expires_at, updated_at) as expires_at
            FROM {self.database}.upload_sessions
            WHERE session_id = '{session_id}'
            GROUP BY session_id
        """
        )
        if not res:
            return None

        session = res[0]
        # Parse node_assignments JSON
        if session.get("node_assignments"):
            try:
                session["node_assignments"] = json.loads(session["node_assignments"])
            except (json.JSONDecodeError, TypeError):
                session["node_assignments"] = {}
        else:
            session["node_assignments"] = {}

        return session

    def update_upload_session(self, session_id: str, **updates) -> bool:
        """
        Update upload session fields.

        Inserts a new row with updated values (ReplacingMergeTree semantics).

        Args:
            session_id: Session identifier
            **updates: Fields to update (status, files_received, bytes_received,
                       node_assignments, episode_id, error, etc.)

        Returns:
            True if updated, False if session not found
        """
        import json
        from sxd_core import io

        # Get current session data
        current = self.get_upload_session(session_id)
        if not current:
            return False

        client = self.client
        if not client:
            return False

        now = io.now()

        # Handle node_assignments - serialize to JSON if dict provided
        node_assignments = updates.get(
            "node_assignments", current.get("node_assignments", {})
        )
        if isinstance(node_assignments, dict):
            node_assignments_json = json.dumps(node_assignments)
        else:
            node_assignments_json = node_assignments or "{}"

        # Merge updates with current data
        data = {
            "session_id": session_id,
            "customer_id": current["customer_id"],
            "status": updates.get("status", current["status"]),
            "total_files": updates.get("total_files", current["total_files"]),
            "files_received": updates.get("files_received", current["files_received"]),
            "total_bytes": updates.get("total_bytes", current["total_bytes"]),
            "bytes_received": updates.get("bytes_received", current["bytes_received"]),
            "staging_path": updates.get("staging_path", current["staging_path"]),
            "node_assignments": node_assignments_json,
            "episode_id": updates.get("episode_id", current.get("episode_id", "")),
            "error": updates.get("error", current.get("error", "")),
            "created_at": current["created_at"],
            "updated_at": now,
            "expires_at": current["expires_at"],
        }

        row = [
            [
                data["session_id"],
                data["customer_id"],
                data["status"],
                data["total_files"],
                data["files_received"],
                data["total_bytes"],
                data["bytes_received"],
                data["staging_path"],
                data["node_assignments"],
                data["episode_id"],
                data["error"],
                data["created_at"],
                data["updated_at"],
                data["expires_at"],
            ]
        ]

        client.insert(
            f"{self.database}.upload_sessions",
            row,
            column_names=[
                "session_id",
                "customer_id",
                "status",
                "total_files",
                "files_received",
                "total_bytes",
                "bytes_received",
                "staging_path",
                "node_assignments",
                "episode_id",
                "error",
                "created_at",
                "updated_at",
                "expires_at",
            ],
        )
        return True

    def increment_upload_session(
        self, session_id: str, files_delta: int = 0, bytes_delta: int = 0
    ) -> bool:
        """
        Atomically increment files_received and bytes_received counters.

        More efficient than get + update for high-frequency file uploads.

        Args:
            session_id: Session identifier
            files_delta: Number of files to add (usually 1)
            bytes_delta: Number of bytes to add

        Returns:
            True if updated, False if session not found
        """
        current = self.get_upload_session(session_id)
        if not current:
            return False

        return self.update_upload_session(
            session_id,
            files_received=current["files_received"] + files_delta,
            bytes_received=current["bytes_received"] + bytes_delta,
            status="RECEIVING" if current["status"] == "ACTIVE" else current["status"],
        )

    def list_upload_sessions(
        self,
        limit: int = 20,
        customer_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List upload sessions with optional filters.

        Args:
            limit: Maximum sessions to return
            customer_id: Filter by customer
            status: Filter by status (ACTIVE, RECEIVING, PROCESSING, COMPLETED, FAILED)

        Returns:
            List of session data
        """
        conditions = []
        if customer_id:
            conditions.append(f"customer_id = '{customer_id}'")
        if status:
            conditions.append(f"status = '{status}'")

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        return self.execute_query(
            f"""
            SELECT
                session_id,
                argMax(customer_id, updated_at) as customer_id,
                argMax(status, updated_at) as status,
                argMax(total_files, updated_at) as total_files,
                argMax(files_received, updated_at) as files_received,
                argMax(total_bytes, updated_at) as total_bytes,
                argMax(bytes_received, updated_at) as bytes_received,
                argMax(staging_path, updated_at) as staging_path,
                argMax(episode_id, updated_at) as episode_id,
                argMax(created_at, updated_at) as created_at,
                max(updated_at) as updated_at
            FROM {self.database}.upload_sessions
            {where_clause}
            GROUP BY session_id
            ORDER BY updated_at DESC
            LIMIT {limit}
        """
        )
