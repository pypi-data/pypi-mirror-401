from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import parse_qs, unquote, urlparse
from uuid import uuid4

from clickhouse_driver import Client
from harlequin import HarlequinAdapter, HarlequinConnection, HarlequinCursor
from harlequin.autocomplete.completion import HarlequinCompletion
from harlequin.catalog import Catalog, CatalogItem
from harlequin.exception import HarlequinConnectionError, HarlequinQueryError
from textual_fastdatatable.backend import AutoBackendType

from harlequin_clickhouse.cli_options import CLICKHOUSE_OPTIONS

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9000
DEFAULT_SECURE_PORT = 9440
DEFAULT_USER = "default"
DEFAULT_CLIENT_NAME = "harlequin-clickhouse"
DEFAULT_QUERY_LIMIT = 500

INT_TYPES = {
    "Int8",
    "Int16",
    "Int32",
    "Int64",
    "Int128",
    "Int256",
    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",
    "UInt128",
    "UInt256",
}
FLOAT_TYPES = {
    "Float32",
    "Float64",
    "Decimal",
    "Decimal32",
    "Decimal64",
    "Decimal128",
    "Decimal256",
}
DATE_TYPES = {"Date", "Date32", "DateTime", "DateTime64"}
BOOL_TYPES = {"Bool", "Boolean"}
STRING_TYPES = {"String", "FixedString", "UUID", "IPv4", "IPv6"}
COMPLEX_PREFIXES = ("Array(", "Map(", "Tuple(", "Nested(")
ROW_RETURNING_KEYWORDS = {"select", "with", "show", "describe", "desc", "explain"}


@dataclass(frozen=True)
class ClickHouseConfig:
    host: str
    port: int
    user: str
    password: str | None
    database: str | None
    secure: bool
    verify: bool
    compression: bool
    settings: dict[str, Any]
    client_name: str
    ca_certs: str | None


def _get_option(options: Mapping[str, Any], *names: str) -> Any | None:
    for name in names:
        if name in options:
            return options[name]
    return None


def _parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return None


def _parse_port(value: str | int | None) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if value.isdigit():
        return int(value)
    raise ValueError("Port must be an integer.")


def _coerce_setting_value(value: str) -> Any:
    normalized = value.strip()
    lower = normalized.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    try:
        return int(normalized)
    except ValueError:
        pass
    try:
        return float(normalized)
    except ValueError:
        return normalized


def _parse_settings(values: Iterable[str]) -> dict[str, Any]:
    settings: dict[str, Any] = {}
    for raw in values:
        if not raw:
            continue
        if "=" not in raw:
            raise ValueError(f"Invalid setting '{raw}'. Expected key=value.")
        key, value = raw.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid setting '{raw}'. Expected key=value.")
        settings[key] = _coerce_setting_value(value)
    return settings


def _parse_url(conn_url: str) -> dict[str, Any]:
    parsed = urlparse(conn_url)
    data: dict[str, Any] = {}
    if parsed.hostname:
        data["host"] = parsed.hostname
    if parsed.port:
        data["port"] = parsed.port
    if parsed.username:
        data["user"] = unquote(parsed.username)
    if parsed.password:
        data["password"] = unquote(parsed.password)
    if parsed.path and parsed.path != "/":
        data["database"] = parsed.path.lstrip("/")

    query = parse_qs(parsed.query)
    secure = _parse_bool(query.get("secure", [None])[0])
    verify = _parse_bool(query.get("verify", [None])[0])
    compression = _parse_bool(query.get("compression", [None])[0])

    if parsed.scheme in {"https", "clickhouse+https"}:
        secure = True

    if secure is not None:
        data["secure"] = secure
    if verify is not None:
        data["verify"] = verify
    if compression is not None:
        data["compression"] = compression

    client_name = query.get("client_name") or query.get("client-name")
    if client_name:
        data["client_name"] = client_name[0]

    ca_certs = query.get("ca_certs") or query.get("ca-cert")
    if ca_certs:
        data["ca_certs"] = ca_certs[0]

    setting_values = query.get("setting", [])
    if setting_values:
        data["settings"] = _parse_settings(setting_values)

    return data


def _parse_conn_tokens(conn_str: Sequence[str]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    if not conn_str:
        return data

    if len(conn_str) == 1 and ":" in conn_str[0] and "//" not in conn_str[0]:
        host, port = conn_str[0].rsplit(":", 1)
        if host:
            data["host"] = host
        if port:
            data["port"] = _parse_port(port)
        return data

    if len(conn_str) >= 1:
        data["host"] = conn_str[0]
    if len(conn_str) >= 2:
        data["port"] = _parse_port(conn_str[1])
    if len(conn_str) >= 3:
        data["database"] = conn_str[2]
    if len(conn_str) >= 4:
        data["user"] = conn_str[3]
    if len(conn_str) >= 5:
        data["password"] = conn_str[4]
    return data


def _build_config(conn_str: Sequence[str], options: Mapping[str, Any]) -> ClickHouseConfig:
    parsed: dict[str, Any] = {}
    if conn_str:
        if len(conn_str) == 1 and "://" in conn_str[0]:
            parsed = _parse_url(conn_str[0])
        else:
            parsed = _parse_conn_tokens(conn_str)

    host = (
        _get_option(options, "host")
        or parsed.get("host")
        or DEFAULT_HOST
    )

    port_option = _get_option(options, "port")
    port = _parse_port(port_option) if port_option else parsed.get("port")
    port_specified = port_option is not None or "port" in parsed

    user = (
        _get_option(options, "user")
        or parsed.get("user")
        or DEFAULT_USER
    )

    password = _get_option(options, "password") or parsed.get("password")
    database = _get_option(options, "database") or parsed.get("database")

    secure = bool(parsed.get("secure")) or bool(_get_option(options, "secure"))

    verify = parsed.get("verify")
    if verify is None:
        verify = True
    if _get_option(options, "no-verify", "no_verify"):
        verify = False

    compression = bool(parsed.get("compression")) or bool(
        _get_option(options, "compression")
    )

    settings = {}
    settings.update(parsed.get("settings", {}))
    setting_values = _get_option(options, "setting") or tuple()
    settings.update(_parse_settings(setting_values))

    client_name = (
        _get_option(options, "client-name", "client_name")
        or parsed.get("client_name")
        or DEFAULT_CLIENT_NAME
    )

    ca_certs = _get_option(options, "ca-cert", "ca_certs") or parsed.get("ca_certs")

    if secure and not port_specified:
        port = DEFAULT_SECURE_PORT
    if port is None:
        port = DEFAULT_PORT

    return ClickHouseConfig(
        host=str(host),
        port=port,
        user=str(user),
        password=str(password) if password is not None else None,
        database=str(database) if database is not None else None,
        secure=secure,
        verify=verify,
        compression=compression,
        settings=settings,
        client_name=str(client_name),
        ca_certs=str(ca_certs) if ca_certs is not None else None,
    )


def _quote_identifier(identifier: str) -> str:
    escaped = identifier.replace("`", "``")
    return f"`{escaped}`"


def _table_type_label(engine: str) -> str:
    normalized = engine.lower()
    if "materializedview" in normalized:
        return "mv"
    if normalized.endswith("view"):
        return "v"
    if "dictionary" in normalized:
        return "d"
    return "t"


def _short_type(type_str: str) -> str:
    if not type_str:
        return "?"

    raw = type_str.strip()
    for wrapper in ("Nullable(", "LowCardinality("):
        while raw.startswith(wrapper) and raw.endswith(")"):
            raw = raw[len(wrapper) : -1]

    if raw.startswith(COMPLEX_PREFIXES):
        return "arr"

    base = raw.split("(", 1)[0]

    if base in INT_TYPES:
        return "##"
    if base in FLOAT_TYPES:
        return "#.#"
    if base in DATE_TYPES:
        return "dt"
    if base in BOOL_TYPES:
        return "b"
    if base in STRING_TYPES:
        return "s"
    return "s"


def _leading_keyword(query: str) -> str:
    stripped = query.lstrip()
    if not stripped:
        return ""
    return stripped.split(None, 1)[0].lower()


class ClickHouseCursor(HarlequinCursor):
    def __init__(
        self,
        connection: ClickHouseConnection,
        query: str,
        default_limit: int | None,
    ) -> None:
        self._connection = connection
        self._query = query
        self._limit = default_limit
        self._rows: Sequence[Sequence[Any]] | None = None
        self._columns: Sequence[tuple[str, str]] | None = None

    def columns(self) -> list[tuple[str, str]]:
        if self._columns is None:
            return []
        return [(name, _short_type(type_str)) for name, type_str in self._columns]

    def set_limit(self, limit: int) -> ClickHouseCursor:
        if limit <= 0:
            self._limit = None
        else:
            self._limit = limit
        return self

    def fetchall(self) -> AutoBackendType:
        try:
            if self._rows is None or self._columns is None:
                rows, columns = self._connection._execute_query(
                    self._query, self._limit
                )
                self._rows = rows
                self._columns = columns

            if not self._rows:
                return None
            return self._rows
        except Exception as e:
            raise HarlequinQueryError(
                msg=str(e),
                title="Harlequin encountered an error while fetching your results.",
            ) from e


class ClickHouseConnection(HarlequinConnection):
    def __init__(
        self,
        conn_str: Sequence[str],
        options: Mapping[str, Any],
        init_message: str = "",
    ) -> None:
        self.init_message = init_message
        self._lock = Lock()
        self._query_lock = Lock()
        self._current_query_id: str | None = None
        try:
            config = _build_config(conn_str, options)
            self._client_kwargs: dict[str, Any] = {
                "host": config.host,
                "port": config.port,
                "user": config.user,
                "password": config.password or "",
                "database": config.database or "default",
                "secure": config.secure,
                "compression": config.compression,
                "settings": config.settings or None,
                "client_name": config.client_name,
            }
            if config.secure:
                self._client_kwargs["verify"] = config.verify
                if config.ca_certs is not None:
                    self._client_kwargs["ca_certs"] = config.ca_certs
            self._client = Client(**self._client_kwargs)
            self._client.execute("SELECT 1")
        except Exception as e:
            raise HarlequinConnectionError(
                msg=str(e),
                title="Harlequin could not connect to ClickHouse.",
            ) from e

    def close(self) -> None:
        disconnect = getattr(self._client, "disconnect", None)
        if callable(disconnect):
            disconnect()

    def execute(self, query: str) -> HarlequinCursor | None:
        keyword = _leading_keyword(query)
        if keyword not in ROW_RETURNING_KEYWORDS:
            self._execute_ddl(query)
            return None

        return ClickHouseCursor(self, query, DEFAULT_QUERY_LIMIT)

    def get_catalog(self) -> Catalog:
        try:
            with self._lock:
                databases = self._client.execute(
                    "SELECT name FROM system.databases ORDER BY name"
                )
                tables = self._client.execute(
                    "SELECT database, name, engine "
                    "FROM system.tables WHERE is_temporary = 0"
                )
                columns = self._client.execute(
                    "SELECT database, table, name, type "
                    "FROM system.columns ORDER BY database, table, position"
                )
        except Exception as e:
            raise HarlequinQueryError(
                msg=str(e),
                title="Harlequin could not load the ClickHouse catalog.",
            ) from e

        tables_by_db: dict[str, dict[str, dict[str, Any]]] = {}
        for database, table, engine in tables:
            tables_by_db.setdefault(database, {})[table] = {
                "engine": engine,
                "columns": [],
            }

        for database, table, column, col_type in columns:
            db_tables = tables_by_db.setdefault(database, {})
            table_entry = db_tables.setdefault(
                table, {"engine": "", "columns": []}
            )
            table_entry["columns"].append((column, col_type))

        items: list[CatalogItem] = []
        for (database,) in databases:
            table_items: list[CatalogItem] = []
            for table, meta in sorted(tables_by_db.get(database, {}).items()):
                column_items = [
                    CatalogItem(
                        qualified_identifier=(
                            f"{_quote_identifier(database)}."
                            f"{_quote_identifier(table)}."
                            f"{_quote_identifier(column)}"
                        ),
                        query_name=_quote_identifier(column),
                        label=column,
                        type_label=_short_type(col_type),
                    )
                    for column, col_type in meta["columns"]
                ]
                table_items.append(
                    CatalogItem(
                        qualified_identifier=(
                            f"{_quote_identifier(database)}."
                            f"{_quote_identifier(table)}"
                        ),
                        query_name=(
                            f"{_quote_identifier(database)}."
                            f"{_quote_identifier(table)}"
                        ),
                        label=table,
                        type_label=_table_type_label(str(meta["engine"])),
                        children=column_items,
                    )
                )
            items.append(
                CatalogItem(
                    qualified_identifier=_quote_identifier(database),
                    query_name=_quote_identifier(database),
                    label=database,
                    type_label="db",
                    children=table_items,
                )
            )

        return Catalog(items=items)

    def get_completions(self) -> list[HarlequinCompletion]:
        extra_keywords = [
            "PREWHERE",
            "SAMPLE",
            "FINAL",
            "LIMIT BY",
            "FORMAT",
            "ARRAY JOIN",
            "SETTINGS",
            "TTL",
            "MATERIALIZED",
            "ALIAS",
            "ENGINE",
            "ON CLUSTER",
        ]
        return [
            HarlequinCompletion(
                label=item,
                type_label="kw",
                value=item,
                priority=1000,
                context=None,
            )
            for item in extra_keywords
        ]

    def _execute_ddl(self, query: str) -> None:
        query_id = uuid4().hex
        with self._query_lock:
            self._current_query_id = query_id
        try:
            with self._lock:
                self._client.execute(query, query_id=query_id)
        except Exception as e:
            raise HarlequinQueryError(
                msg=str(e),
                title="Harlequin encountered an error while executing your query.",
            ) from e
        finally:
            with self._query_lock:
                self._current_query_id = None

    def _execute_query(
        self, query: str, limit: int | None
    ) -> tuple[Sequence[Sequence[Any]], Sequence[tuple[str, str]]]:
        query_id = uuid4().hex
        with self._query_lock:
            self._current_query_id = query_id
        settings = None
        if limit is not None:
            settings = {"max_result_rows": limit, "result_overflow_mode": "break"}
        try:
            with self._lock:
                data, columns = self._client.execute(
                    query,
                    with_column_types=True,
                    query_id=query_id,
                    settings=settings,
                )
        except Exception as e:
            raise HarlequinQueryError(
                msg=str(e),
                title="Harlequin encountered an error while executing your query.",
            ) from e
        finally:
            with self._query_lock:
                self._current_query_id = None
        return data, columns

    def cancel(self) -> None:
        with self._query_lock:
            query_id = self._current_query_id

        if not query_id:
            return

        cancel_client: Client | None = None
        try:
            cancel_client = Client(**self._client_kwargs)
            cancel_client.execute(
                "KILL QUERY WHERE query_id = %(query_id)s",
                params={"query_id": query_id},
            )
        except Exception:
            pass
        finally:
            if cancel_client is not None:
                try:
                    cancel_client.disconnect()
                except Exception:
                    pass


class ClickHouseAdapter(HarlequinAdapter):
    ADAPTER_OPTIONS = CLICKHOUSE_OPTIONS
    IMPLEMENTS_CANCEL = True

    def __init__(self, conn_str: Sequence[str], **options: Any) -> None:
        self.conn_str = conn_str
        self.options = options

    def connect(self) -> ClickHouseConnection:
        return ClickHouseConnection(self.conn_str, self.options)
