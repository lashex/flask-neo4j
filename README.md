# Flask-Neo4j

[![CI](https://github.com/lashex/flask-neo4j/actions/workflows/ci.yml/badge.svg)](https://github.com/lashex/flask-neo4j/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Flask extension that provides simple integration with the
[Neo4j](https://neo4j.com/) graph database using the official
[neo4j Python driver](https://neo4j.com/docs/python-manual/current/).

## Installation

```bash
uv add Flask-Neo4j
```

Or with pip:

```bash
pip install Flask-Neo4j
```

## Quick Start

```python
from flask import Flask
from flask_neo4j import Neo4j

app = Flask(__name__)
app.config["NEO4J_URI"] = "bolt://localhost:7687"
app.config["NEO4J_AUTH"] = ("neo4j", "your-password")

n4j = Neo4j(app)

# Execute a simple query
records = n4j.execute("MATCH (n) RETURN n LIMIT 10")

# Or use a session for more control
with n4j.session() as session:
    result = session.run("CREATE (p:Person {name: $name}) RETURN p", name="Alice")
    print(result.single())
```

### Creating Nodes and Relationships

```python
from flask import Flask
from flask_neo4j import Neo4j

# Configuration
app = Flask(__name__)
app.config["NEO4J_URI"] = "bolt://localhost:7687"
app.config["NEO4J_AUTH"] = ("neo4j", "admin")

n4j = Neo4j(app)

with n4j.session() as session:
    result = session.run(
        """
        CREATE (s:Species {full_name: 'Dracula nosferatu', species_name: 'nosferatu'})
        CREATE (g:Genus {name: 'Dracula'})
        CREATE (s)-[:MEMBER_OF]->(g)
        RETURN s, g
        """,
    )
    print(result.single())

# which all results in a graph that looks like:
#   (Species)-[:MEMBER_OF]->(Genus)
```

### Application Factory Pattern

```python
from flask import Flask
from flask_neo4j import Neo4j

n4j = Neo4j()

def create_app():
    app = Flask(__name__)
    app.config["NEO4J_URI"] = "bolt://localhost:7687"
    app.config["NEO4J_AUTH"] = ("neo4j", "your-password")
    n4j.init_app(app)
    return app
```

## Configuration

| Key | Default | Description |
|-----|---------|-------------|
| `NEO4J_URI` | `"bolt://localhost:7687"` | Bolt URI for the Neo4j server |
| `NEO4J_AUTH` | `("neo4j", "neo4j")` | Authentication tuple `(username, password)` |
| `NEO4J_DATABASE` | `"neo4j"` | Default database name |
| `NEO4J_MAX_CONNECTION_POOL_SIZE` | `100` | Maximum connection pool size |
| `NEO4J_CONNECTION_TIMEOUT` | `30.0` | Connection timeout in seconds |
| `NEO4J_CONNECTION_RETRY` | `False` | Retry on connection failure |
| `NEO4J_RETRY_INTERVAL` | `5` | Seconds between retries |
| `NEO4J_RETRY_COUNT` | `3` | Number of connection retries |
| `NEO4J_DRIVER_CONFIG` | `{}` | Additional kwargs passed to the Neo4j driver |

## Migration from 0.5.x

Flask-Neo4j 0.7.0 is a major rewrite that replaces the `py2neo` dependency with
the official `neo4j` Python driver. Key changes:

### Configuration keys renamed

| Old (0.5.x) | New (0.7.0) |
|---|---|
| `GRAPH_DATABASE` | `NEO4J_URI` |
| `GRAPH_USER` / `GRAPH_PASSWORD` | `NEO4J_AUTH` (tuple) |
| `CONNECTION_RETRY` | `NEO4J_CONNECTION_RETRY` |
| `RETRY_INTERVAL` | `NEO4J_RETRY_INTERVAL` |

### API changes

| Old (0.5.x) | New (0.7.0) |
|---|---|
| `n4j.gdb` (py2neo Graph) | `n4j.driver` (neo4j Driver) |
| `n4j.store` (py2neo OGM) | Removed — use `n4j.session()` |
| `n4j.index` | Removed — use Cypher indexes |
| `n4j.delete_index()` | Removed — use Cypher `DROP INDEX` |

### New features

- `n4j.session()` — opens a Neo4j session with the configured database
- `n4j.execute(query, parameters)` — convenience method for simple queries
- `n4j.close()` — cleanly shuts down the connection pool
- Full type annotations and PEP 561 `py.typed` marker
- Connection retry with configurable count and interval

## License

MIT License. See [LICENSE](LICENSE) for details.
