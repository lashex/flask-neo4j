from py2neo import neo4j
from flask import current_app

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
            print "flask.ext.Neo4j init_app called"

    def init_app(self, app):
        """Initialize the `app` for use with this :class:`~Neo4j`. This is
        called automatically if `app` is passed to :meth:`~Neo4j.__init__`.

        The app is configured according to the configuration variable
        ``GRAPH_DATABASE``

        :param flask.Flask app: the application configured for use with
           this :class:`~Neo4j`
        """
        self.app = app
        app.n4j = self
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['neo4j'] = self

        app.config.setdefault('GRAPH_DATABASE', neo4j.DEFAULT_URI)

        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'graph_db'):
            # py2neo does not have an 'open' connection that needs closing
            ctx.graph_db = None

    @property
    def gdb(self):
        """Initialize the graph database service instance for use as a property.

        The instance with which to connect is configured according to the
        configuration variable
        ``GRAPH_DATABASE``

        :return: the graph database service property
        """
        self.graph_db = neo4j.GraphDatabaseService.get_instance(
            self.app.config['GRAPH_DATABASE']
        )
        print 'Connected to:', self.graph_db.neo4j_version

        if not hasattr(self, 'index'):
            self.index = {}
            # add all the indexes as app attributes
            if self._indexes is not None:
                for i, i_type in self._indexes.iteritems():
                    print 'getting or creating graph index:', i
                    self.index[i] = \
                        self.graph_db.get_or_create_index(i_type, i)

        return self.graph_db

    # def _connect(self):
    #     _gdb = neo4j.GraphDatabaseService.get_instance(
    #         current_app.config['GRAPH_DATABASE']
    #     )
    #     print 'Connected to:', _gdb.neo4j_version
    #     return _gdb
    #
    # @property
    # def gdb(self):
    #     ctx = stack.top
    #     if ctx is not None:
    #         if not hasattr(ctx, 'graph_db'):
    #             ctx.graph_db = self._connect()
    #         print 'past context setting...'
    #         # add all the indexes as app attributes
    #         if self._indexes is not None:
    #             for i, i_type in self._indexes.iteritems():
    #                 print 'getting or creating graph index:', i
    #                 graph_index = ctx.graph_db.get_or_create_index(i_type, i)
    #                 self.index[i] = graph_index
    #                 graph_index = None
    #
    #     return ctx.graph_db