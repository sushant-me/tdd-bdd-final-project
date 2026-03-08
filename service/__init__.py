import os
import logging
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

# Create the Flask app
app = Flask(__name__)

# ##################################################################
# Security Headers using Flask-Talisman
# ##################################################################
# This adds headers like Content-Security-Policy and X-Frame-Options
talisman = Talisman(app)

# ##################################################################
# CORS Policies
# ##################################################################
# This allows the API to be accessed from different domains
CORS(app)

# Import the routes and models so they are registered with the app
from service import routes, models
from service.common import log_handlers

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info("Service initialized!")
