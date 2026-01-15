from __future__ import annotations

from harlequin.options import FlagOption, ListOption, TextOption


def _validate_port(raw: str) -> tuple[bool, str | None]:
    if raw.isdigit() and 0 < int(raw) < 65536:
        return True, None
    return False, "Port must be an integer between 1 and 65535."


HOST = TextOption(
    name="host",
    description="ClickHouse server host.",
    short_decls=["-H"],
)

PORT = TextOption(
    name="port",
    description="ClickHouse native TCP port.",
    short_decls=["-p"],
    validator=_validate_port,
)

USER = TextOption(
    name="user",
    description="ClickHouse user name.",
    short_decls=["-u"],
)

PASSWORD = TextOption(
    name="password",
    description="ClickHouse password.",
    short_decls=["-W"],
)

DATABASE = TextOption(
    name="database",
    description="Default database to use after connecting.",
    short_decls=["-d"],
)

SECURE = FlagOption(
    name="secure",
    description="Use TLS for the native ClickHouse protocol.",
)

NO_VERIFY = FlagOption(
    name="no-verify",
    description="Disable TLS certificate verification.",
)

CA_CERT = TextOption(
    name="ca-cert",
    description="Path to a CA bundle for TLS verification.",
)

COMPRESSION = FlagOption(
    name="compression",
    description="Enable LZ4 compression for ClickHouse traffic.",
)

CLIENT_NAME = TextOption(
    name="client-name",
    description="Client name reported to ClickHouse in system.processes.",
)

SETTING = ListOption(
    name="setting",
    description="ClickHouse settings as key=value pairs (repeatable).",
    short_decls=["-s"],
)

CLICKHOUSE_OPTIONS = [
    HOST,
    PORT,
    USER,
    PASSWORD,
    DATABASE,
    SECURE,
    NO_VERIFY,
    CA_CERT,
    COMPRESSION,
    CLIENT_NAME,
    SETTING,
]
