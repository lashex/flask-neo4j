import flask
import flask.ext.neo4j
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
        self.app.config['GRAPH_DATABASE'] = 'http://localhost:7474/db/data/'
        n4j = flask.ext.neo4j.Neo4j(self.app)
        assert n4j.gdb.neo4j_version is not None

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FlaskRequestTest))
    suite.addTest(unittest.makeSuite(FlaskNeo4jConfigTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
