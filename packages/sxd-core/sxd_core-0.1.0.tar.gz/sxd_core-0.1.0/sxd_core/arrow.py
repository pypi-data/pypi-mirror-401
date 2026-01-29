from typing import Any, Dict, List, Optional

import chdb  # type: ignore
import pyarrow as pa

# --- Standard Schemas ---

# Video Metadata Schema
# Used for recording high-level video info (url, IDs, etc)
VIDEO_METADATA_SCHEMA = pa.schema(
    [
        ("video_id", pa.string()),
        ("customer_id", pa.string()),
        ("url", pa.string()),
        ("status", pa.string()),
        ("timestamp", pa.timestamp("ms")),
    ]
)


# Frame-level Data Schema
# Used for Parquet/Lance exports
def get_frame_schema(embedding_dim: int) -> pa.schema:
    return pa.schema(
        [
            ("frame_index", pa.int32()),
            ("timestamp", pa.float32()),
            ("embedding", pa.list_(pa.float32(), embedding_dim)),
            ("blur_score", pa.float32()),
            ("video_id", pa.string()),
            ("customer_id", pa.string()),
        ]
    )


# --- Utilities ---


def dicts_to_table(
    data: List[Dict[str, Any]], schema: Optional[pa.Schema] = None
) -> pa.Table:
    """Convert a list of dictionaries to a PyArrow Table."""
    if not data:
        return (
            pa.Table.from_batches([], schema=schema)
            if schema
            else pa.Table.from_arrays([])
        )

    return pa.Table.from_pylist(data, schema=schema)


def table_to_dicts(table: pa.Table) -> List[Dict[str, Any]]:
    """Convert a PyArrow Table to a list of dictionaries."""
    return table.to_pylist()


def query_table(table: pa.Table, query: str) -> pa.Table:
    """Query an Arrow Table using chDB SQL."""
    # Use the chDB Python(table) table function
    # The 'table' argument to chdb.query maps the table object to the 'Python(table)' function in SQL
    formatted_query = query.replace("table", "Python(table)")
    return chdb.query(formatted_query, "ArrowTable")


def read_parquet_as_table(path: str) -> pa.Table:
    """Read a Parquet file as an Arrow Table."""
    import pyarrow.parquet as pq

    return pq.read_table(path)


def write_table_as_parquet(table: pa.Table, path: str, compression: str = "snappy"):
    """Write an Arrow Table to a Parquet file."""
    import pyarrow.parquet as pq

    pq.write_table(table, path, compression=compression)


def get_arrow_buffer(table: pa.Table) -> pa.Buffer:
    """Serialize an Arrow Table to a buffer (RecordBatchStreamWriter)."""
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table)
    return sink.getvalue()


def read_arrow_buffer(buffer: pa.Buffer) -> pa.Table:
    """Deserialize an Arrow Table from a buffer (RecordBatchStreamReader)."""
    with pa.ipc.open_stream(buffer) as reader:
        return reader.read_all()
