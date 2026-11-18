"""
The application factory.

LESSON: Instead of one global `app = Flask(__name__)`, we write a function
that BUILDS an app. That lets us make a development app, a testing app
(with a throwaway database), or a production app from the same code.
`flask run` finds this function through FLASK_APP in .flaskenv.
"""

import os

from flask import Flask

from app.config import config_by_name
from app.extensions import db, migrate


def create_app(config_name=None):
    config_name = config_name or os.environ.get("APP_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # 1. Connect the extensions to this app
    db.init_app(app)
    # render_as_batch lets migrations ALTER tables on SQLite (which has limited ALTER support)
    migrate.init_app(app, db, render_as_batch=True)

    # 2. Import the models so SQLAlchemy (and Flask-Migrate) know they exist
    from app import models  # noqa: F401

    # 3. Register the routes, error handlers and CLI commands
    from app.errors import register_error_handlers
    from app.routes import register_blueprints
    from app.seed import register_commands

    register_blueprints(app)
    register_error_handlers(app)
    register_commands(app)

    return app