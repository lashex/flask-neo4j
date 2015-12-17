from __future__ import print_function

import time
import logging
from py2neo import Graph,Node
from py2neo.ext import ogm
from py2neo.packages.httpstream.http import SocketError

log = logging.getLogger('flask.neo4j')
logging.basicConfig()

# Find the stack on which we want to store the GraphDatabaseService instance.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class Neo4j(object):
    """Automatically connects to Neo4j graph database using parameters defined
    in Flask configuration.

    One can use this extension by providing the Flask app on instantiation or
    by calling the :meth:`init_app` method on an instance object of `Neo4j`. An example
    of providing the application on instantiation: ::

        app = Flask(__name__)
        n4j = Neo4j(app)

    ...and an example calling the :meth:`init_app` method instead: ::

        n4j = Neo4j()

        def init_app():
            app = Flask(__name__)
            n4j.init_app(app)
            return app

    One can also providing a dict of indexes that will be used to automatically
    get or create indexes in the graph database ::
        app = Flask(__name__)
        graph_indexes = {'Species': neo4j.Node}
        n4j = Neo4j(app, graph_indexes)
        print n4j.gdb.neo4j_version
        species_index = n4j.index['Species']
        ...

    """
    def __init__(self, app=None, indexes=None):
        self.app = app
        self._indexes = indexes
        if app is not None:
            self.init_app(app)
            print ("flask.ext.Neo4j init_app called")

    def init_app(self, app):
        """Initialize the `app` for use with this :class:`~Neo4j`. This is
        called automatically if `app` is passed to :meth:`~Neo4j.__init__`.

        The app is configured according to these configuration variables
        ``CONNECTION_RETRY``
        ``RETRY_INTERVAL``

        :param flask.Flask app: the application configured for use with
           this :class:`~Neo4j`
        """
        self.app = app
        app.n4j = self
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['neo4j'] = self

        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        ctx = stack.top # TODO clean up teardown related to graph_db behavior
        if hasattr(ctx, 'graph_db'):
            # py2neo does not have an 'open' connection that needs closing
            ctx.graph_db = None

    @property
    def gdb(self):
        """The graph database service instance as a property, for convenience.

        Note: The property will use these configuration variables
        ``CONNECTION_RETRY``
        ``RETRY_INTERVAL``

        :return: the graph database service as a property
        """
        retry = False
        if 'CONNECTION_RETRY' in self.app.config:
            retry = self.app.config['CONNECTION_RETRY']
        retry_interval = 5
        if 'RETRY_INTERVAL' in self.app.config:
            retry_interval = self.app.config['RETRY_INTERVAL']
        retry_count = 0
        try:
            self.graph_db = Graph(self.app.config['GRAPH_DATABASE'])
        except SocketError as se:
            log.error('SocketError: {0}'.format(se.message))
            if retry:
                while retry_count < 3:
                    log.debug('Waiting {0}secs before Connection Retry to GraphDatabaseService'.format(
                        retry_interval
                    ))
                    time.sleep(retry_interval)
                    #time.sleep(1)
                    retry_count += 1
                    try:
                        self.graph_db = Graph(self.app.config['GRAPH_DATABASE'])
                    except SocketError as sse:
                        log.error('SocketError: {0}'.format(sse.message))

        if not hasattr(self, 'index'):
            self.index = {}
            # add all the indexes as app attributes
            if self._indexes is not None:
                for i, i_type in iter(self._indexes.items()):
                    log.debug('getting or creating graph index:{0} {1}'.format(
                        i, i_type
                    ))
                    self.index[i] = \
                        self.graph_db.legacy.get_or_create_index(i_type, i)

        return self.graph_db

    @property
    def store(self):
        """
        The object graph mapping store available as a property.

        Note: The property will use these configuration variables
        ``CONNECTION_RETRY``
        ``RETRY_INTERVAL``

        :return: the object graph mapping store property
        """
        store = ogm.Store(self.gdb)
        return store

    def delete_index(self, index_name):
        """
        Simple delete index capability that takes only a name.
        Note: uses the index_types as remembered from indexes variable given at
        initialization.

        :param index_name: the name of the index to delete from the database
        """
        i_type = self._indexes[index_name]
        self.graph_db.legacy.delete_index(content_type=i_type, index_name=index_name)

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['GRAPH_DATABASE'] = 'http://localhost:7474/db/data/'
    graph_indexes = {'Species': Node}
    flask4j = Neo4j(app, graph_indexes)
    print (flask4j.gdb.neo4j_version)
    species_index = flask4j.index['Species']
    print ('species index:', species_index)
    flask4j.delete_index('Species')
