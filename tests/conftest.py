"""Shared pytest fixtures for Flask-Neo4j tests."""

from __future__ import annotations

import pytest
from flask import Flask


@pytest.fixture()
def app() -> Flask:
    """Create a minimal Flask app with test configuration."""
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        NEO4J_URI="bolt://localhost:7687",
        NEO4J_AUTH=("neo4j", "testpassword"),
        NEO4J_DATABASE="neo4j",
    )
    return app
