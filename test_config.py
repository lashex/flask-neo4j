import flask
import flask.ext.neo4j
import unittest
from py2neo import neo4j


class FlaskRequestTest(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask('test')
        self.context = self.app.test_request_context('/')
        self.context.push()

    def tearDown(self):
        self.context.pop()


class FlaskNeo4jConfigTestCase(FlaskRequestTest):
    def test_something(self):
        self.app.config['GRAPH_DATABASE'] = neo4j.DEFAULT_URI
        n4j = flask.ext.neo4j.Neo4j(self.app)
        assert n4j.gdb.neo4j_version is not None


if __name__ == '__main__':
    unittest.main()
