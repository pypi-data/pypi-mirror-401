import sys

import pytest
from harlequin.adapter import HarlequinAdapter, HarlequinConnection, HarlequinCursor
from harlequin.catalog import Catalog, CatalogItem
from harlequin.exception import HarlequinConnectionError, HarlequinQueryError
from harlequin_clickhouse.adapter import ClickHouseAdapter, ClickHouseConnection
from textual_fastdatatable.backend import create_backend

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points


class DummyClient:
    last_query_id = None
    last_settings = None
    killed_query_ids = []

    @classmethod
    def reset(cls):
        cls.last_query_id = None
        cls.last_settings = None
        cls.killed_query_ids = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def execute(
        self,
        query,
        params=None,
        with_column_types=False,
        external_tables=None,
        query_id=None,
        settings=None,
        types_check=False,
        columnar=False,
    ):
        normalized = " ".join(query.strip().lower().split())
        if query_id is not None:
            DummyClient.last_query_id = query_id
        DummyClient.last_settings = settings

        limit_value = None
        if settings and "max_result_rows" in settings:
            limit_value = int(settings["max_result_rows"])

        if normalized.startswith("kill query"):
            if params and "query_id" in params:
                DummyClient.killed_query_ids.append(params["query_id"])
            return []

        if normalized == "select 1":
            return [(1,)]

        if "from system.databases" in normalized:
            return [("default",), ("system",)]

        if "from system.tables" in normalized:
            return [
                ("default", "numbers", "MergeTree"),
                ("default", "my_view", "View"),
            ]

        if "from system.columns" in normalized:
            return [
                ("default", "numbers", "number", "UInt64"),
                ("default", "my_view", "value", "String"),
            ]

        if normalized == "select 1 as a":
            if with_column_types:
                rows = [(1,)]
                if limit_value is not None:
                    rows = rows[:limit_value]
                return rows, [("a", "Int32")]
            rows = [(1,)]
            if limit_value is not None:
                rows = rows[:limit_value]
            return rows

        if normalized == "select 1 as a, 2 as a, 3 as a":
            if with_column_types:
                rows = [(1, 2, 3)]
                if limit_value is not None:
                    rows = rows[:limit_value]
                return rows, [("a", "Int32"), ("a", "Int32"), ("a", "Int32")]
            rows = [(1, 2, 3)]
            if limit_value is not None:
                rows = rows[:limit_value]
            return rows

        if normalized == "select 1 as a union all select 2 union all select 3":
            if with_column_types:
                rows = [(1,), (2,), (3,)]
                if limit_value is not None:
                    rows = rows[:limit_value]
                return rows, [("a", "Int32")]
            rows = [(1,), (2,), (3,)]
            if limit_value is not None:
                rows = rows[:limit_value]
            return rows

        if normalized.startswith("create table"):
            if with_column_types:
                return [], []
            return []

        if normalized == "selec;":
            raise RuntimeError("syntax error")

        if with_column_types:
            return [], []
        return []

    def disconnect(self):
        return None


@pytest.fixture
def connection(monkeypatch) -> ClickHouseConnection:
    DummyClient.reset()
    monkeypatch.setattr(
        "harlequin_clickhouse.adapter.Client",
        DummyClient,
    )
    return ClickHouseAdapter(conn_str=tuple()).connect()


def test_plugin_discovery() -> None:
    plugin_name = "clickhouse"
    eps = entry_points(group="harlequin.adapter")
    ep = next((ep for ep in eps if ep.name == plugin_name), None)
    assert ep is not None
    adapter_cls = ep.load()
    assert issubclass(adapter_cls, HarlequinAdapter)
    assert adapter_cls == ClickHouseAdapter


def test_connect(monkeypatch) -> None:
    DummyClient.reset()
    monkeypatch.setattr(
        "harlequin_clickhouse.adapter.Client",
        DummyClient,
    )
    conn = ClickHouseAdapter(conn_str=tuple()).connect()
    assert isinstance(conn, HarlequinConnection)


def test_init_extra_kwargs(monkeypatch) -> None:
    DummyClient.reset()
    monkeypatch.setattr(
        "harlequin_clickhouse.adapter.Client",
        DummyClient,
    )
    assert ClickHouseAdapter(conn_str=tuple(), secure=True, compression=True).connect()


def test_connect_raises_connection_error(monkeypatch) -> None:
    def raising_client(**kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(
        "harlequin_clickhouse.adapter.Client",
        raising_client,
    )
    with pytest.raises(HarlequinConnectionError):
        _ = ClickHouseAdapter(conn_str=("bad-host",)).connect()


def test_get_catalog(connection: ClickHouseConnection) -> None:
    catalog = connection.get_catalog()
    assert isinstance(catalog, Catalog)
    assert catalog.items
    assert isinstance(catalog.items[0], CatalogItem)


def test_execute_ddl(connection: ClickHouseConnection) -> None:
    cur = connection.execute("create table foo (a int)")
    assert cur is None


def test_execute_select(connection: ClickHouseConnection) -> None:
    cur = connection.execute("select 1 as a")
    assert isinstance(cur, HarlequinCursor)
    data = cur.fetchall()
    assert DummyClient.last_query_id is not None
    assert DummyClient.last_settings["max_result_rows"] == 500
    assert DummyClient.last_settings["result_overflow_mode"] == "break"
    assert cur.columns() == [("a", "##")]
    backend = create_backend(data)
    assert backend.column_count == 1
    assert backend.row_count == 1


def test_execute_select_dupe_cols(connection: ClickHouseConnection) -> None:
    cur = connection.execute("select 1 as a, 2 as a, 3 as a")
    assert isinstance(cur, HarlequinCursor)
    data = cur.fetchall()
    assert DummyClient.last_settings["max_result_rows"] == 500
    assert len(cur.columns()) == 3
    backend = create_backend(data)
    assert backend.column_count == 3
    assert backend.row_count == 1


def test_set_limit(connection: ClickHouseConnection) -> None:
    cur = connection.execute("select 1 as a union all select 2 union all select 3")
    assert isinstance(cur, HarlequinCursor)
    cur = cur.set_limit(2)
    assert isinstance(cur, HarlequinCursor)
    data = cur.fetchall()
    assert DummyClient.last_settings["max_result_rows"] == 2
    backend = create_backend(data)
    assert backend.column_count == 1
    assert backend.row_count == 2


def test_execute_raises_query_error(connection: ClickHouseConnection) -> None:
    with pytest.raises(HarlequinQueryError):
        _ = connection.execute("selec;")


def test_cancel_sends_kill_query(connection: ClickHouseConnection) -> None:
    with connection._query_lock:
        connection._current_query_id = "query-123"
    connection.cancel()
    assert "query-123" in DummyClient.killed_query_ids
