"""Flask extension for Neo4j graph database integration."""

from __future__ import annotations

import logging
import time
from typing import Any

import neo4j
from flask import Flask

log = logging.getLogger("flask.neo4j")


class Neo4j:
    """Flask extension that provides integration with the Neo4j graph database
    using the official ``neo4j`` Python driver.

    Supports both direct initialization and the application factory pattern::

        # Direct initialization
        app = Flask(__name__)
        n4j = Neo4j(app)

        # Factory pattern
        n4j = Neo4j()

        def create_app():
            app = Flask(__name__)
            n4j.init_app(app)
            return app

    Configuration keys (set on ``app.config``):

    - ``NEO4J_URI`` — Bolt URI (default ``"bolt://localhost:7687"``)
    - ``NEO4J_AUTH`` — Auth tuple (default ``("neo4j", "neo4j")``)
    - ``NEO4J_DATABASE`` — Database name (default ``"neo4j"``)
    - ``NEO4J_MAX_CONNECTION_POOL_SIZE`` — Max pool size (default ``100``)
    - ``NEO4J_CONNECTION_TIMEOUT`` — Connection timeout in seconds (default ``30.0``)
    - ``NEO4J_CONNECTION_RETRY`` — Enable retry on failure (default ``False``)
    - ``NEO4J_RETRY_INTERVAL`` — Seconds between retries (default ``5``)
    - ``NEO4J_RETRY_COUNT`` — Number of retries (default ``3``)
    - ``NEO4J_DRIVER_CONFIG`` — Additional kwargs passed to the driver (default ``{}``)
    """

    def __init__(self, app: Flask | None = None) -> None:
        self._app = app
        self._driver: neo4j.Driver | None = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize the extension with a Flask application.

        Sets configuration defaults, creates the Neo4j driver, and registers
        a teardown handler to close the driver when the app context ends.

        :param app: The Flask application instance.
        """
        self._app = app

        app.config.setdefault("NEO4J_URI", "bolt://localhost:7687")
        app.config.setdefault("NEO4J_AUTH", ("neo4j", "neo4j"))
        app.config.setdefault("NEO4J_DATABASE", "neo4j")
        app.config.setdefault("NEO4J_MAX_CONNECTION_POOL_SIZE", 100)
        app.config.setdefault("NEO4J_CONNECTION_TIMEOUT", 30.0)
        app.config.setdefault("NEO4J_CONNECTION_RETRY", False)
        app.config.setdefault("NEO4J_RETRY_INTERVAL", 5)
        app.config.setdefault("NEO4J_RETRY_COUNT", 3)
        app.config.setdefault("NEO4J_DRIVER_CONFIG", {})

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["neo4j"] = self

        self._driver = self._create_driver(app)
        app.teardown_appcontext(self._teardown)

    def _create_driver(self, app: Flask) -> neo4j.Driver:
        """Create a Neo4j driver with retry logic.

        :param app: The Flask application instance.
        :returns: A connected Neo4j driver.
        :raises neo4j.exceptions.ServiceUnavailable: If connection fails after
            all retry attempts.
        """
        uri = app.config["NEO4J_URI"]
        auth = app.config["NEO4J_AUTH"]
        extra_config: dict[str, Any] = dict(app.config["NEO4J_DRIVER_CONFIG"])
        extra_config.setdefault(
            "max_connection_pool_size", app.config["NEO4J_MAX_CONNECTION_POOL_SIZE"]
        )
        extra_config.setdefault(
            "connection_timeout", app.config["NEO4J_CONNECTION_TIMEOUT"]
        )

        retry = app.config["NEO4J_CONNECTION_RETRY"]
        retry_interval = app.config["NEO4J_RETRY_INTERVAL"]
        retry_count = app.config["NEO4J_RETRY_COUNT"]

        last_exc: Exception | None = None
        attempts = 1 if not retry else retry_count + 1

        for attempt in range(attempts):
            try:
                driver = neo4j.GraphDatabase.driver(uri, auth=auth, **extra_config)
                driver.verify_connectivity()
                log.info("Connected to Neo4j at %s", uri)
                return driver
            except neo4j.exceptions.ServiceUnavailable as exc:
                last_exc = exc
                if attempt < attempts - 1:
                    log.warning(
                        "Neo4j connection attempt %d failed, retrying in %ds...",
                        attempt + 1,
                        retry_interval,
                    )
                    time.sleep(retry_interval)
                else:
                    log.error("Neo4j connection failed after %d attempts", attempts)

        raise last_exc  # type: ignore[misc]

    def _teardown(self, exception: BaseException | None) -> None:
        """Teardown handler registered with Flask."""

    @property
    def driver(self) -> neo4j.Driver:
        """Return the Neo4j driver instance.

        :raises RuntimeError: If the extension has not been initialized.
        """
        if self._driver is None:
            raise RuntimeError(
                "Neo4j extension is not initialized. "
                "Call init_app() or pass a Flask app to the constructor."
            )
        return self._driver

    def session(self, **kwargs: Any) -> neo4j.Session:
        """Open a new Neo4j session.

        If ``database`` is not specified in *kwargs*, the configured
        ``NEO4J_DATABASE`` value is used.

        :param kwargs: Additional keyword arguments passed to
            ``neo4j.Driver.session()``.
        :returns: A new Neo4j session.
        """
        if self._app is not None and "database" not in kwargs:
            kwargs["database"] = self._app.config["NEO4J_DATABASE"]
        return self.driver.session(**kwargs)

    def execute(
        self, query: str, parameters: dict[str, Any] | None = None
    ) -> list[neo4j.Record]:
        """Execute a Cypher query and return all result records.

        This is a convenience method that opens a session, runs the query,
        consumes all records, and closes the session.

        :param query: The Cypher query string.
        :param parameters: Optional query parameters.
        :returns: A list of :class:`neo4j.Record` objects.
        """
        with self.session() as session:
            result = session.run(query, parameters)
            return list(result)

    def close(self) -> None:
        """Close the Neo4j driver and release all resources."""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            log.info("Neo4j driver closed")
