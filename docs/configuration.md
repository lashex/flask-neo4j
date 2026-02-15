# Configuration

All configuration is done through Flask's `app.config`.

## Configuration Reference

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `NEO4J_URI` | `str` | `"bolt://localhost:7687"` | Bolt URI for the Neo4j server |
| `NEO4J_AUTH` | `tuple` | `("neo4j", "neo4j")` | Authentication credentials `(username, password)` |
| `NEO4J_DATABASE` | `str` | `"neo4j"` | Default database name |
| `NEO4J_MAX_CONNECTION_POOL_SIZE` | `int` | `100` | Maximum number of connections in the pool |
| `NEO4J_CONNECTION_TIMEOUT` | `float` | `30.0` | Timeout in seconds for establishing a connection |
| `NEO4J_CONNECTION_RETRY` | `bool` | `False` | Enable connection retry on startup failure |
| `NEO4J_RETRY_INTERVAL` | `int` | `5` | Seconds to wait between retry attempts |
| `NEO4J_RETRY_COUNT` | `int` | `3` | Maximum number of retry attempts |
| `NEO4J_DRIVER_CONFIG` | `dict` | `{}` | Additional keyword arguments passed directly to `neo4j.GraphDatabase.driver()` |

## Example Configuration

```python
app.config.update(
    NEO4J_URI="bolt://db.example.com:7687",
    NEO4J_AUTH=("neo4j", "secret"),
    NEO4J_DATABASE="myapp",
    NEO4J_MAX_CONNECTION_POOL_SIZE=50,
    NEO4J_CONNECTION_RETRY=True,
    NEO4J_RETRY_COUNT=5,
    NEO4J_DRIVER_CONFIG={
        "encrypted": True,
    },
)
```

## Driver Pass-Through Configuration

The `NEO4J_DRIVER_CONFIG` dictionary is unpacked as keyword arguments to
`neo4j.GraphDatabase.driver()`. This allows you to configure any driver option
supported by the official Neo4j Python driver, such as `encrypted`,
`trusted_certificates`, `keep_alive`, etc.
