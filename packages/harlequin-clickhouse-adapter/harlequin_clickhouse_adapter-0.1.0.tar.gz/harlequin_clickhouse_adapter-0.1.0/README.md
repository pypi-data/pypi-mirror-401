# harlequin-clickhouse-adapter

A ClickHouse adapter for [Harlequin](https://harlequin.sh) built on `clickhouse-driver`.

## Installation

Using `uv`:

```bash
uv pip install harlequin-clickhouse-adapter
```

From source:

```bash
uv sync
uv pip install -e .
```

## Usage

Connect with a URL:

```bash
harlequin clickhouse clickhouse://user:password@localhost:9000/default
```

Connect with explicit options:

```bash
harlequin clickhouse \
  --host localhost \
  --port 9000 \
  --user default \
  --database default
```

Or via positional connection tokens (host, port, database, user, password):

```bash
harlequin clickhouse localhost 9000 default default secret
```

### TLS and compression

```bash
harlequin clickhouse \
  --host ch.example.com \
  --port 9440 \
  --secure \
  --ca-cert /path/to/ca.pem \
  --compression
```

### ClickHouse settings

Repeat `--setting` for query-level settings:

```bash
harlequin clickhouse \
  --host localhost \
  --setting max_threads=8 \
  --setting max_memory_usage=10000000000
```
