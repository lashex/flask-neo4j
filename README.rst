Flask-Neo4j
===========
.. image:: https://secure.travis-ci.org/lashex/flask-neo4j.png?branch=master
   :target: http://travis-ci.org/lashex/flask-neo4j
.. image:: https://pypip.in/d/Flask-Neo4j/badge.png?period=month
    :target: https://pypi.python.org/pypi/Flask-Neo4j/
    :alt: Downloads
.. image:: https://pypip.in/license/Flask-Neo4j/badge.png
    :target: https://pypi.python.org/pypi/Flask-Neo4j/
    :alt: License

A Flask extension that provides simple interaction with the Neo4j graph
database.

These capabilities are made possible by the fine library: `py2neo <http://book.py2neo.org>`_


Installation
------------
Using pip::

    pip install flask-neo4j

Usage
-----
Typical usage looks like this::

    from flask import Flask
    from flask.ext.neo4j import Neo4j
    from py2neo import neo4j

    app = Flask(__name__)
    graph_indexes = {'Species': neo4j.Node}
    flask4j = Neo4j(app, graph_indexes)
    print flask4j.gdb.neo4j_version
    nosferatu = flask4j.index['Species'].get_or_create('species_id', 1234,
        {   'full_name': 'Dracula nosferatu',
            'species_name': 'nosferatu',
            'type': 'species'
        }
    )

    full_path = nosferatu.get_or_create_path(
        'MEMBER_OF', { 'name': 'Dracula', 'type': 'genus' },
    )

    # which all results in a graph that looks like:
    #  (species)-[:MEMBER_OF]->(genus)


Links
-----

* `documentation <http://blah/Flask-Neo4j>`_
