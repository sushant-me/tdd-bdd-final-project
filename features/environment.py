"""
Behave environment hooks.

Behave is an end-to-end acceptance suite, so the scenarios must talk to a
*running* service rather than to an in-process test client.  `before_all`
starts the real Flask application on a background thread (using the same WSGI
app `wsgi.py` serves in production) and `after_all` shuts it down again.

The database URI comes from `DATABASE_URI`; CI sets it to a throwaway SQLite
file so the job needs no database service.
"""
import os
import threading
from urllib.parse import urlparse

from werkzeug.serving import make_server

from service import app
from service.models import Product

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")

_parsed = urlparse(BASE_URL)
SERVER_HOST = _parsed.hostname or "localhost"
SERVER_PORT = _parsed.port or 80

_server = None
_thread = None


def before_all(context):
    """Create the schema and start the service the scenarios talk to."""
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    Product.init_db(app)

    global _server, _thread
    _server = make_server(SERVER_HOST, SERVER_PORT, app, threaded=True)
    _thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _thread.start()

    # Values consumed by the step definitions
    context.base_url = BASE_URL
    context.wait_seconds = int(os.getenv("WAIT_SECONDS", "10"))


def after_all(context):
    """Stop the background service."""
    global _server, _thread
    if _server is not None:
        _server.shutdown()
        _server = None
    if _thread is not None:
        _thread.join(timeout=5)
        _thread = None
