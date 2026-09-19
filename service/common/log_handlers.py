"""
Logging Handlers

Configures Python logging for the service.  In production the app runs under
Gunicorn, so application log records are routed to the Gunicorn error logger.
When that logger is not present (``flask run``, tests, local development) an
extra stream handler on stderr is attached so the records are not lost.
"""
import logging
import sys

# Format used for every log record emitted by the service
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s"


def init_logging(app, logger_name="gunicorn.error"):
    """Initialize logging for the Flask application.

    :param app: the Flask application instance
    :param str logger_name: name of the logger that should receive the
                            application's log records (Gunicorn's error
                            logger by default)
    """
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # Avoid duplicate handlers if the app is imported more than once
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        logger.addHandler(handler)

    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

    app.logger.info("Logging initialized for %s", logger_name)
