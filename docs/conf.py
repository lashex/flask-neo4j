"""Sphinx configuration for Flask-Neo4j documentation."""

project = "Flask-Neo4j"
copyright = "2013-2026, Brett Francis"
author = "Brett Francis"
version = "0.7"
release = "0.7.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "myst_parser",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build"]

html_theme = "furo"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "flask": ("https://flask.palletsprojects.com/en/latest/", None),
    "neo4j": ("https://neo4j.com/docs/api/python-driver/current/", None),
}
