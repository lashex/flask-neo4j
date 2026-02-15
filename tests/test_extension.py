"""Unit tests for the Flask-Neo4j extension (mocked driver)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import neo4j.exceptions
import pytest
from flask import Flask

from flask_neo4j import Neo4j


@pytest.fixture()
def mock_driver():
    """Return a mock Neo4j driver that passes verify_connectivity."""
    with patch("flask_neo4j.extension.neo4j.GraphDatabase") as mock_gdb:
        driver = MagicMock()
        driver.verify_connectivity.return_value = None
        mock_gdb.driver.return_value = driver
        yield driver


class TestConstructor:
    def test_direct_init(self, app: Flask, mock_driver: MagicMock) -> None:
        """Neo4j(app) should initialize immediately."""
        n4j = Neo4j(app)
        assert n4j.driver is mock_driver
        assert "neo4j" in app.extensions

    def test_factory_pattern(self, app: Flask, mock_driver: MagicMock) -> None:
        """Neo4j() then init_app(app) should work."""
        n4j = Neo4j()
        with pytest.raises(RuntimeError, match="not initialized"):
            _ = n4j.driver
        n4j.init_app(app)
        assert n4j.driver is mock_driver

    def test_driver_before_init_raises(self) -> None:
        """Accessing driver before init should raise RuntimeError."""
        n4j = Neo4j()
        with pytest.raises(RuntimeError, match="not initialized"):
            _ = n4j.driver


class TestConfigDefaults:
    def test_defaults_are_set(self, mock_driver: MagicMock) -> None:
        """init_app should populate default config values."""
        app = Flask(__name__)
        Neo4j(app)
        assert app.config["NEO4J_URI"] == "bolt://localhost:7687"
        assert app.config["NEO4J_AUTH"] == ("neo4j", "neo4j")
        assert app.config["NEO4J_DATABASE"] == "neo4j"
        assert app.config["NEO4J_MAX_CONNECTION_POOL_SIZE"] == 100
        assert app.config["NEO4J_CONNECTION_TIMEOUT"] == 30.0
        assert app.config["NEO4J_CONNECTION_RETRY"] is False
        assert app.config["NEO4J_RETRY_INTERVAL"] == 5
        assert app.config["NEO4J_RETRY_COUNT"] == 3
        assert app.config["NEO4J_DRIVER_CONFIG"] == {}

    def test_custom_config_preserved(self, mock_driver: MagicMock) -> None:
        """User-provided config should not be overwritten by defaults."""
        app = Flask(__name__)
        app.config["NEO4J_URI"] = "bolt://custom:7687"
        app.config["NEO4J_DATABASE"] = "mydb"
        Neo4j(app)
        assert app.config["NEO4J_URI"] == "bolt://custom:7687"
        assert app.config["NEO4J_DATABASE"] == "mydb"


class TestSession:
    def test_session_uses_default_database(
        self, app: Flask, mock_driver: MagicMock
    ) -> None:
        """session() should pass the configured database."""
        n4j = Neo4j(app)
        n4j.session()
        mock_driver.session.assert_called_once_with(database="neo4j")

    def test_session_allows_override(self, app: Flask, mock_driver: MagicMock) -> None:
        """session(database=...) should override the default."""
        n4j = Neo4j(app)
        n4j.session(database="other")
        mock_driver.session.assert_called_once_with(database="other")


class TestExecute:
    def test_execute_returns_records(self, app: Flask, mock_driver: MagicMock) -> None:
        """execute() should return a list of records."""
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_records = [MagicMock(), MagicMock()]
        mock_result.__iter__ = lambda self: iter(mock_records)
        mock_session.run.return_value = mock_result
        mock_session.__enter__ = lambda self: self
        mock_session.__exit__ = MagicMock(return_value=False)
        mock_driver.session.return_value = mock_session

        n4j = Neo4j(app)
        records = n4j.execute("MATCH (n) RETURN n", {"limit": 10})
        mock_session.run.assert_called_once_with("MATCH (n) RETURN n", {"limit": 10})
        assert records == mock_records


class TestRetry:
    def test_retry_on_service_unavailable(self, app: Flask) -> None:
        """Driver creation should retry on ServiceUnavailable."""
        app.config["NEO4J_CONNECTION_RETRY"] = True
        app.config["NEO4J_RETRY_COUNT"] = 2
        app.config["NEO4J_RETRY_INTERVAL"] = 0  # no delay in tests

        with patch("flask_neo4j.extension.neo4j.GraphDatabase") as mock_gdb:
            driver = MagicMock()
            mock_gdb.driver.return_value = driver
            driver.verify_connectivity.side_effect = [
                neo4j.exceptions.ServiceUnavailable("down"),
                None,  # succeeds on second attempt
            ]
            with patch("flask_neo4j.extension.time.sleep"):
                n4j = Neo4j(app)
            assert n4j.driver is driver
            assert driver.verify_connectivity.call_count == 2

    def test_retry_exhausted_raises(self, app: Flask) -> None:
        """Should raise after all retries are exhausted."""
        app.config["NEO4J_CONNECTION_RETRY"] = True
        app.config["NEO4J_RETRY_COUNT"] = 1
        app.config["NEO4J_RETRY_INTERVAL"] = 0

        with patch("flask_neo4j.extension.neo4j.GraphDatabase") as mock_gdb:
            driver = MagicMock()
            mock_gdb.driver.return_value = driver
            driver.verify_connectivity.side_effect = (
                neo4j.exceptions.ServiceUnavailable("down")
            )
            with (
                patch("flask_neo4j.extension.time.sleep"),
                pytest.raises(neo4j.exceptions.ServiceUnavailable),
            ):
                Neo4j(app)


class TestClose:
    def test_close_shuts_down_driver(self, app: Flask, mock_driver: MagicMock) -> None:
        """close() should call driver.close() and set driver to None."""
        n4j = Neo4j(app)
        n4j.close()
        mock_driver.close.assert_called_once()
        with pytest.raises(RuntimeError):
            _ = n4j.driver

    def test_close_when_no_driver(self) -> None:
        """close() should be safe to call without a driver."""
        n4j = Neo4j()
        n4j.close()  # should not raise
