from __future__ import print_function

import flask
import flask.ext.neo4j
from py2neo import neo4j
import unittest


class FlaskRequestTest(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask('test')
        self.context = self.app.test_request_context('/')
        self.context.push()

    def tearDown(self):
        self.context.pop()


class FlaskNeo4jConfigTestCase(FlaskRequestTest):
    def test_graph_db_config(self):
        self.app.config['CONNECTION_RETRY'] = True
        self.app.config['RETRY_INTERVAL'] = 2
        flask4j = flask.ext.neo4j.Neo4j(self.app)
        print ('gdb: ', flask4j.gdb)
        assert flask4j.gdb is not None
        assert flask4j.gdb.neo4j_version is not None


class FlaskNeo4jIndexTestCase(FlaskRequestTest):
    def test_index_crud(self):
        self.app.config['GRAPH_DATABASE'] = 'http://localhost:7474/db/data/'
        test_indexes = {'Foo': neo4j.Node, 'BarRel': neo4j.Relationship}
        flask4j = flask.ext.neo4j.Neo4j(self.app, indexes=test_indexes)
        print ('gdb + index:', flask4j.gdb)
        assert flask4j.index['Foo'] is not None
        assert flask4j.index['BarRel'] is not None
        flask4j.delete_index('Foo')
        flask4j.delete_index('BarRel')

class FlaskNeo4jOGMTestCase(FlaskRequestTest):
    def test_ogm_crud(self):
        self.app.config['GRAPH_DATABASE'] = 'http://localhost:7474/db/data/'
        n4j = flask.ext.neo4j.Neo4j(self.app)


if __name__ == '__main__':
    unittest.main()
