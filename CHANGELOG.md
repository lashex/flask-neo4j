# Changelog

## 0.7.0

Major modernization release replacing `py2neo` with the official `neo4j` Python driver.

### Breaking Changes

- **Replaced `py2neo` with the official `neo4j` driver** — all `py2neo` APIs are removed
- **Removed OGM support** — the `store` property is gone; use sessions and Cypher directly
- **Removed legacy index management** — `index` property and `delete_index()` removed; use Cypher index commands
- **Renamed configuration keys** — `GRAPH_DATABASE` -> `NEO4J_URI`, `GRAPH_USER`/`GRAPH_PASSWORD` -> `NEO4J_AUTH`, etc.
- **Dropped Python 2.7 and Python < 3.9 support**
- **Requires Flask >= 2.0**

### Added

- `Neo4j.driver` property — returns the `neo4j.Driver` instance
- `Neo4j.session()` method — opens a session with the configured default database
- `Neo4j.execute()` method — convenience for simple Cypher queries
- `Neo4j.close()` method — cleanly shuts down the driver
- Full type annotations with PEP 561 `py.typed` marker
- Configurable connection retry with `NEO4J_RETRY_COUNT` and `NEO4J_RETRY_INTERVAL`
- `NEO4J_DRIVER_CONFIG` for pass-through driver configuration
- GitHub Actions CI with Python 3.9–3.13 test matrix
- Integration tests with Neo4j 5 service container
- Sphinx documentation with furo theme and MyST Markdown

### Removed

- `py2neo` dependency
- `future` dependency
- Python 2 compatibility code
- Travis CI configuration
- `setup.py` / `setup.cfg` (replaced by `pyproject.toml` with hatchling)

## 0.5.1

- Fixed `setup.py` to require `future`

## 0.5.0

- Added Python 3 support
- Added Neo4j authentication

## 0.4.1

- Broadened range of DBs tested against

## 0.4.0

- Upgraded dependency for py2neo to 2.0.1
- Added license attribution
- Code changes to reflect new py2neo API

## 0.3.1

- Added support for Travis CI
- Configured Sphinx documentation
- Added `delete_index()` method
