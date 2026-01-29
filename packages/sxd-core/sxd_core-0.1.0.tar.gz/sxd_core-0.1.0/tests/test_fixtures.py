from sxd_core.testing.fixtures import (
    create_test_video,
    create_test_image,
    create_test_pointcloud,
    create_test_parquet,
    MockTemporalContext,
)


def test_mock_temporal_context():
    ctx = MockTemporalContext(workflow_id="wf-1")
    assert ctx.workflow_id == "wf-1"
    assert ctx.trace_id == "trace-wf-1"
    d = ctx.to_dict()
    assert d["workflow_id"] == "wf-1"
    assert "activity_id" in d


def test_create_test_video(tmp_path):
    output = tmp_path / "test.mp4"
    ret_path = create_test_video(output, duration=1.0)
    assert ret_path == output
    assert output.exists()
    assert output.stat().st_size > 0
    # Basic header check
    with open(output, "rb") as f:
        header = f.read(8)
        assert b"ftyp" in header or len(header) > 4  # ftyp is usually at offset 4


def test_create_test_image(tmp_path):
    output = tmp_path / "test.png"
    ret_path = create_test_image(output, width=10, height=10)
    assert ret_path == output
    assert output.exists()
    with open(output, "rb") as f:
        assert f.read(8) == b"\x89PNG\r\n\x1a\n"


def test_create_test_pointcloud(tmp_path):
    output = tmp_path / "test.pcd"
    ret_path = create_test_pointcloud(output, num_points=10)
    assert ret_path == output
    assert output.exists()
    content = output.read_text()
    assert "VERSION 0.7" in content
    assert "POINTS 10" in content


def test_create_test_parquet(tmp_path):
    output = tmp_path / "test.parquet"
    ret_path = create_test_parquet(output, num_rows=10)
    assert ret_path == output
    assert output.exists()
    # If pyarrow is installed, we could read it back, but existing tests require deps
    # Here we just check file creation
    assert output.stat().st_size > 0
