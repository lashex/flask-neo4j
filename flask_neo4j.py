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
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('GRAPH_DATABASE', neo4j.DEFAULT_URI)
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        graph_db = neo4j.GraphDatabaseService.get_instance(
            current_app.config['GRAPH_DATABASE']
        )
        print(graph_db.neo4j_version)
        return graph_db

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'graph_db'):
            # py2neo does not have an 'open' connection that needs closing
            ctx.graph_db = None

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'graph_db'):
                ctx.graph_db = self.connect()
            return ctx.graph_db
