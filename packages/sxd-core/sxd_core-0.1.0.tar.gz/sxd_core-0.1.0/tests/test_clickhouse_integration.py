import pytest
import json
from sxd_core.clickhouse import ClickHouseManager
import chdb.dbapi as dbapi  # type: ignore


class ChdbClientWrapper:
    """Wraps chdb to look like clickhouse_connect client."""

    def __init__(self):
        self.conn = dbapi.connect()
        self.cursor = self.conn.cursor()

    def command(self, sql):
        # chdb doesn't support DateTime64(6, 'UTC') fully in DDL sometimes?
        # But let's try.
        # clickhouse_connect command just runs it.
        try:
            self.cursor.execute(sql)
        except Exception as e:
            # Re-raise to fail test if DDL is bad
            raise e

    def insert(self, table, data, column_names=None):
        # Simple naive insert implementation for testing
        if not data:
            return

        cols = ", ".join(column_names) if column_names else ""

        # Convert values to SQL string representations
        values_list = []
        for row in data:
            row_vals = []
            for v in row:
                if isinstance(v, str):
                    v_esc = v.replace("'", "\\'")
                    row_vals.append(f"'{v_esc}'")
                elif v is None:
                    row_vals.append("NULL")
                elif isinstance(v, (dict, list)):
                    val = json.dumps(v).replace("'", "\\'")
                    row_vals.append(f"'{val}'")
                elif hasattr(v, "strftime"):  # datetime
                    # format as string
                    row_vals.append(f"'{v.strftime('%Y-%m-%d %H:%M:%S.%f')}'")
                else:
                    row_vals.append(str(v))
            values_list.append(f"({', '.join(row_vals)})")

        values_str = ", ".join(values_list)
        sql = f"INSERT INTO {table} ({cols}) VALUES {values_str}"
        self.cursor.execute(sql)

    def query(self, sql):
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        # clickhouse_connect returns an object with result_rows
        class QResult:
            def __init__(self, r):
                self.result_rows = r

        return QResult(rows)

    def close(self):
        self.conn.close()


@pytest.fixture
def chdb_manager():
    client = ChdbClientWrapper()
    mgr = ClickHouseManager(client_override=client, database="sxd")
    return mgr


def test_init_db_valid_sql(chdb_manager):
    """Verify that init_db executes valid SQL against chdb."""
    # This checks ddl syntax
    chdb_manager.init_db()

    # Check tables exist
    client = chdb_manager.client
    client.cursor.execute("SHOW TABLES FROM sxd")
    tables = [r[0] for r in client.cursor.fetchall()]
    assert "logs" in tables
    assert "audit_events" in tables
    assert "videos" in tables
    assert "episodes" in tables


def test_insert_and_query_logs(chdb_manager):
    chdb_manager.init_db()

    # Test insert
    rows = [
        [
            "2023-01-01 10:00:00.000",
            "INFO",
            "test_logger",
            "hello world",
            "tid1",
            "jid1",
            "act1",
            "{}",
        ]
    ]
    chdb_manager.insert_logs(rows)

    # Verify insert via raw query
    client = chdb_manager.client
    client.cursor.execute("SELECT message FROM sxd.logs")
    res = client.cursor.fetchall()
    assert len(res) == 1
    assert res[0][0] == "hello world"


def test_upsert_video(chdb_manager):
    chdb_manager.init_db()

    data = {"id": "v1", "state": "PROCESSING", "size_bytes": 1024}
    chdb_manager.upsert_video_metadata(data)

    client = chdb_manager.client
    client.cursor.execute("SELECT id, size_bytes FROM sxd.videos WHERE id='v1'")
    res = client.cursor.fetchall()
    assert len(res) == 1
    assert res[0][0] == "v1"
    assert res[0][1] == 1024
