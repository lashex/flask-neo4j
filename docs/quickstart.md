# Quick Start

## Installation

```bash
uv add Flask-Neo4j
```

Or with pip:

```bash
pip install Flask-Neo4j
```

## Basic Usage

```python
from flask import Flask
from flask_neo4j import Neo4j

app = Flask(__name__)
app.config["NEO4J_URI"] = "bolt://localhost:7687"
app.config["NEO4J_AUTH"] = ("neo4j", "your-password")

n4j = Neo4j(app)
```

### Executing Queries

The simplest way to run a Cypher query:

```python
records = n4j.execute("MATCH (p:Person) RETURN p.name AS name LIMIT 10")
for record in records:
    print(record["name"])
```

### Using Sessions

For more control, use a session directly:

```python
with n4j.session() as session:
    result = session.run(
        "CREATE (p:Person {name: $name}) RETURN p",
        name="Alice",
    )
    node = result.single()["p"]
    print(node["name"])
```

## Application Factory Pattern

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

## Connection Retry

Enable automatic retry for environments where Neo4j may not be immediately
available (e.g., Docker Compose startup ordering):

```python
app.config["NEO4J_CONNECTION_RETRY"] = True
app.config["NEO4J_RETRY_COUNT"] = 5
app.config["NEO4J_RETRY_INTERVAL"] = 3  # seconds
```
