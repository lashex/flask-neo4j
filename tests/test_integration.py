"""Integration tests requiring a running Neo4j instance.

Run with: pytest -m integration
"""

from __future__ import annotations

import os

import pytest
from flask import Flask

from flask_neo4j import Neo4j

pytestmark = pytest.mark.integration


@pytest.fixture()
def neo4j_app() -> Flask:
    """Flask app configured for a local Neo4j instance."""
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    auth_str = os.environ.get("NEO4J_AUTH", "neo4j/testpassword")
    user, password = auth_str.split("/", 1)
    app = Flask(__name__)
    app.config.update(
        NEO4J_URI=uri,
        NEO4J_AUTH=(user, password),
        NEO4J_DATABASE="neo4j",
    )
    return app


class TestIntegration:
    def test_connect_and_query(self, neo4j_app: Flask) -> None:
        """Should connect to Neo4j and execute a simple query."""
        n4j = Neo4j(neo4j_app)
        try:
            records = n4j.execute("RETURN 1 AS n")
            assert len(records) == 1
            assert records[0]["n"] == 1
        finally:
            n4j.close()

    def test_session_context_manager(self, neo4j_app: Flask) -> None:
        """Should support using session as a context manager."""
        n4j = Neo4j(neo4j_app)
        try:
            with n4j.session() as session:
                result = session.run("RETURN 'hello' AS greeting")
                record = result.single()
                assert record is not None
                assert record["greeting"] == "hello"
        finally:
            n4j.close()

    def test_driver_property(self, neo4j_app: Flask) -> None:
        """Driver property should return a functional driver."""
        n4j = Neo4j(neo4j_app)
        try:
            info = n4j.driver.get_server_info()
            assert info is not None
        finally:
            n4j.close()
