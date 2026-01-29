import pytest
from sxd_core.testing.mocks import (
    MockStorage,
    MockClickHouse,
    MockHTTP,
    MockMetrics,
    MockActivityContext,
)


class TestMockStorage:
    def test_basic_io(self):
        s = MockStorage()
        s.write("test.txt", b"content")
        assert s.exists("test.txt")
        assert s.read("test.txt") == b"content"
        assert s.read_text("test.txt") == "content"
        assert s.size("test.txt") == 7

        # Test delete
        assert s.delete("test.txt")
        assert not s.exists("test.txt")
        assert not s.delete("missing.txt")

        # Test missing read
        with pytest.raises(FileNotFoundError):
            s.read("missing.txt")

        with pytest.raises(FileNotFoundError):
            s.size("missing.txt")

    def test_open_modes(self):
        s = MockStorage()

        # Write binary
        with s.open("bin.dat", "wb") as f:
            f.write(b"binary")
        assert s.read("bin.dat") == b"binary"

        # Write text (MockStorage 'w' mode implies binary buffer in implementation details usually,
        # but let's check the code: if "b" in mode: binary=True)
        # s.open("text.txt", "w") -> mode="w", so binary=False (impl: binary="b" in mode)
        # Code: buffer = _MockWriteBuffer(self, path, binary="b" in mode)
        # _MockWriteBuffer is BytesIO subclass.
        # Actually standard python open("w") returns TextIOWrapper.
        # The mock returns _MockWriteBuffer which inherits BytesIO.
        # Use simple write for now.

        # Read binary
        with s.open("bin.dat", "rb") as f:
            assert f.read() == b"binary"

        # Read text
        with s.open("bin.dat", "r") as f:
            assert f.read() == "binary"

        # Unsupported mode
        with pytest.raises(ValueError):
            s.open("x", "x")

    def test_list_and_glob(self):
        s = MockStorage()
        s.write("data/a.txt", b"")
        s.write("data/b.txt", b"")
        s.write("other/c.txt", b"")

        # Test list with absolute prefix because MockStorage normalizes
        # s.list("data/") -> normalized to /mock/data/
        assert len(s.list("data/")) == 2

        # Glob matches against KEYS (absolute paths like /mock/data/a.txt)
        # So we need patterns that match absolute paths
        # "*/data/*.txt" matches ".../data/..."
        files = s.glob("*/data/*.txt")
        assert len(files) == 2

    def test_path_objects(self):
        s = MockStorage()
        s.write("foo/bar.txt", b"content")

        p = s / "foo" / "bar.txt"
        # MockStoragePath string is relative if constructed relatively
        assert str(p) == "foo/bar.txt"
        assert p.name == "bar.txt"
        assert p.parent.name == "foo"
        assert p.exists()  # Checks /mock/foo/bar.txt

        # Write via path
        p2 = s / "new.txt"
        p2.write_bytes(b"new")
        assert s.read("new.txt") == b"new"

        # Iterdir
        d = s / "foo"
        children = list(d.iterdir())
        assert len(children) == 1
        assert children[0].name == "bar.txt"

        # mkdir (pass)
        d.mkdir()


class TestMockClickHouse:
    def test_queries(self):
        ch = MockClickHouse()
        ch.set_query_result("SELECT 1", [{"a": 1}])
        res = ch.execute_query("SELECT 1")
        assert res == [{"a": 1}]
        assert len(ch.queries) == 1

        # Default empty
        assert ch.query("SELECT 2") == []

    def test_inserts(self):
        ch = MockClickHouse()
        ch.insert("table", {"a": 1})
        ch.insert_many("table", [{"a": 2}])

        assert len(ch.inserts) == 2
        assert len(ch.get_table_data("table")) == 2

        # Helpers
        ch.upsert_episode({})
        ch.upsert_chunk({})
        ch.upsert_video({})
        ch.log_event({})

        assert "episodes" in ch._tables
        assert "chunks" in ch._tables
        assert "videos" in ch._tables
        assert "logs" in ch._tables


class TestMockHTTP:
    def test_requests(self):
        h = MockHTTP()
        h.add_response("http://ex.com", json_data={"foo": "bar"})

        r = h.get("http://ex.com")
        assert r.status_code == 200
        assert r.json() == {"foo": "bar"}
        assert (
            r.text == '{"foo": "bar"}'
        )  # implicity json.dumps? No, mock impl: content/json logic
        # Mock impl: if json_data is set, json() returns it. text returns .content.decode().
        # If we didn't set content, text is empty.

        h.post("http://ex.com")
        h.head("http://ex.com")

        assert len(h.requests) == 3


class TestMockMetrics:
    def test_metrics(self):
        m = MockMetrics()
        m.increment("c")
        m.increment("c")
        m.decrement("c")
        assert m.get_counter("c") == 1.0

        m.gauge("g", 42)
        assert m.get_gauge("g") == 42

        m.timing("t", 100)
        assert m.get_timings("t") == [100]

        m.histogram("h", 10)
        assert m.get_histograms("h") == [10]

        m.flush()
        m.clear()
        assert m.get_counter("c") == 0


class TestMockActivityContext:
    def test_context(self):
        ctx = MockActivityContext()
        assert ctx.clickhouse
        assert ctx.log

        ctx.log.info("test")
        assert len(ctx.log.messages) == 1

        # Cache
        ctx.cache.set("k", "v")
        assert ctx.cache.get("k") == "v"
        assert ctx.cache.exists("k")
        ctx.cache.delete("k")
        assert not ctx.cache.exists("k")

        # Progress
        ctx.progress.start()
        ctx.progress.update(50)
        ctx.progress.complete()
        ctx.progress.fail()
        assert len(ctx.progress.updates) == 4

        # Checkpoints
        assert not ctx.checkpoints.has_checkpoint("a")
        with ctx.checkpoints.checkpoint("a"):
            pass

        ctx.flush_metrics()
