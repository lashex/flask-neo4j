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

    You can use this extension by providing the Flask app on instantiation or
    by calling the :meth:`init_app` method on an instance object of `Neo4j`. An example
    of providing the application on instantiation: ::

        app = Flask(__name__)
        n4j = Neo4j(app)

    ...and an example calling the :meth:`init_app` method: ::

        n4j = Neo4j()

        def init_app():
            app = Flask(__name__)
            n4j.init_app(app)
            return app
    """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the `app` for use with this :class:`~Neo4j`. This is
        called automatically if `app` is passed to :meth:`~Neo4j.__init__`.

        The app is configured according to the configuration variables
        ``GRAPH_DATABASE``

        :param flask.Flask app: the application configured for use with
           this :class:`~Neo4j`
        """
        app.config.setdefault('GRAPH_DATABASE', neo4j.DEFAULT_URI)
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        gdb = neo4j.GraphDatabaseService.get_instance(
            current_app.config['GRAPH_DATABASE']
        )
        print(gdb.neo4j_version)
        return gdb

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'graph_db'):
            # py2neo does not have an 'open' connection that needs closing
            ctx.graph_db = None

    @property
    def gdb(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'graph_db'):
                ctx.graph_db = self.connect()
            return ctx.graph_db