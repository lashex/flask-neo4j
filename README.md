Flask-Neo4j
===========

Flask extension that provides integration with the Neo4j graph database using
the py2neo library. Under initial development.

Installation
------------
Using pip::

      pip install flask-neo4j

Usage
-------
Typical usage looks like this::

    #!/usr/bin/env python

    from flask import Flask
    from flask.ext.neo4j import Neo4j
    from py2neo import neo4j

    app = Flask(__name__)
    graph_indexes = {'Species': neo4j.Node}
    n4j = Neo4j(app, graph_indexes)
    print n4j.gdb.neo4j_version
    species_index = n4j.index['Species']
    species, = species_index.get_or_create('species_id', 1234,
            {   'full_name': 'Dracula nosferatu',
                'species_name': 'nosferatu',
                'type': 'species'
            }
    )

    ref_node = n4j.gdb.get_reference_node()
    full_path = ref_node.get_or_create_path(
            'ROOT', species,
            'MEMBER_OF', { 'name': 'Dracula', 'type': 'genus' },
    )

    # which all results in a graph that looks like:
    #  (ref_node)-[:ROOT]->(species)-[:MEMBER_OF]->(genus)

Links
`````

* `documentation <http://blah/Flask-Neo4j>`_