from sxd_core.arrow import get_frame_schema, dicts_to_table, query_table
from sxd_core.data_layer import DataManager


def test_arrow_utilities():
    schema = get_frame_schema(embedding_dim=4)
    data = [
        {
            "frame_index": 0,
            "timestamp": 0.0,
            "embedding": [0.1, 0.2, 0.3, 0.4],
            "blur_score": 100.0,
            "video_id": "v1",
            "customer_id": "c1",
        },
        {
            "frame_index": 1,
            "timestamp": 1.0,
            "embedding": [0.5, 0.6, 0.7, 0.8],
            "blur_score": 150.0,
            "video_id": "v1",
            "customer_id": "c1",
        },
    ]

    table = dicts_to_table(data, schema=schema)
    assert table.num_rows == 2
    assert "embedding" in table.column_names

    # Test query
    result = query_table(table, "SELECT * FROM table WHERE blur_score > 120")
    assert result.num_rows == 1
    assert result.to_pylist()[0]["frame_index"] == 1


def test_data_manager_arrow():
    video_data = [
        {"video_name": "vid1.mp4", "video_path": "/path/to/vid1.mp4"},
        {"video_name": "vid2.mp4", "video_path": "/path/to/vid2.mp4"},
    ]
    table = DataManager.get_video_table(video_data)
    assert table.num_rows == 2
    assert "url" in table.column_names
    assert "timestamp" in table.column_names


def test_arrow_io(tmp_path):
    """Test Arrow IO utilities (parquet read/write)."""
    from sxd_core.arrow import (
        dicts_to_table,
        write_table_as_parquet,
        read_parquet_as_table,
        get_arrow_buffer,
        read_arrow_buffer,
    )

    data = [{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}]
    table = dicts_to_table(data)

    # Test Parquet I/O
    path = str(tmp_path / "test.parquet")
    write_table_as_parquet(table, path)

    loaded = read_parquet_as_table(path)
    assert loaded.num_rows == 2
    assert loaded.schema.names == ["col1", "col2"]
    assert loaded.to_pylist() == data

    # Test Buffer I/O
    buf = get_arrow_buffer(table)
    assert len(buf) > 0

    from_buf = read_arrow_buffer(buf)
    assert from_buf.num_rows == 2
    assert from_buf.to_pylist() == data
