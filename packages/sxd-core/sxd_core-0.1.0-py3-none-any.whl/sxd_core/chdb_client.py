"""
ChDBClient: A chdb-backed client that implements the clickhouse_connect client interface.

This allows ClickHouseManager to work with an embedded chdb session for testing,
enabling simulation tests to exercise real production query logic instead of
duplicating queries in test mocks.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

import chdb.session


class ChDBQueryResult:
    """Wraps chdb query results to match clickhouse_connect's result interface."""

    def __init__(self, data: List[Dict[str, Any]]):
        self._data = data

    def named_results(self):
        """Return results as an iterable of dicts (matching clickhouse_connect)."""
        return iter(self._data)


class ChDBClient:
    """
    A chdb-backed client that implements the subset of clickhouse_connect's
    client interface used by ClickHouseManager.

    This enables testing ClickHouseManager with an embedded ClickHouse engine
    without needing a real ClickHouse server.

    Args:
        session: Optional existing chdb session. If None, creates a new one.
        path: Optional path for persistent session storage.
    """

    def __init__(
        self,
        session: Optional[chdb.session.Session] = None,
        path: Optional[str] = None,
    ):
        if session is not None:
            self._session = session
        else:
            # Create a new session (in-memory if no path)
            self._session = (
                chdb.session.Session(path) if path else chdb.session.Session()
            )

    @property
    def session(self) -> chdb.session.Session:
        """Access the underlying chdb session."""
        return self._session

    def _check_failure(self):
        """Check if ClickHouse is simulated as failing in the current runtime."""
        from sxd_core.simulation import get_runtime, in_simulation

        if in_simulation():
            rt = get_runtime()
            if rt and "clickhouse" in rt.service_failures:
                raise Exception("ClickHouse simulated error: Connection refused")

    def command(self, sql: str) -> None:
        """Execute a DDL/DML command without returning results."""
        self._check_failure()
        self._session.query(sql)

    def query(self, sql: str) -> ChDBQueryResult:
        """Execute a SELECT query and return results."""
        self._check_failure()
        result = self._session.query(sql, "JSON")
        try:
            data = json.loads(result.bytes())
            rows = data.get("data", [])
        except Exception:
            rows = []
        return ChDBQueryResult(rows)

    def insert(
        self,
        table: str,
        data: List[List[Any]],
        column_names: Optional[List[str]] = None,
    ) -> None:
        """
        Insert rows into a table.

        Args:
            table: Full table name (e.g., "sxd.chunks")
            data: List of rows, each row is a list of values
            column_names: Column names corresponding to the values
        """
        if not data or not column_names:
            return

        self._check_failure()

        # Build INSERT statement
        cols = ", ".join(column_names)
        values_list = []

        for row in data:
            formatted_values = []
            for val in row:
                formatted_values.append(self._format_value(val))
            values_list.append(f"({', '.join(formatted_values)})")

        sql = f"INSERT INTO {table} ({cols}) VALUES {', '.join(values_list)}"
        self._session.query(sql)

    def _format_value(self, val: Any) -> str:
        """Format a Python value for SQL insertion."""
        if val is None:
            return "NULL"
        elif isinstance(val, bool):
            return "1" if val else "0"
        elif isinstance(val, (int, float)):
            return str(val)
        elif isinstance(val, datetime):
            # chdb expects ISO format for DateTime64
            return f"'{val.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}'"
        elif isinstance(val, str):
            # Escape single quotes
            escaped = val.replace("'", "''")
            return f"'{escaped}'"
        else:
            # For other types, convert to string
            escaped = str(val).replace("'", "''")
            return f"'{escaped}'"

    def close(self) -> None:
        """Close the client (no-op for chdb sessions)."""
        pass
