"""
Configuration classes.

LESSON: Each environment (development, testing, production) gets its own
class. They inherit from a shared base `Config`, so we only write the
differences. `create_app()` picks one by name.
"""

import os


class Config:
    # Where the database lives. A relative SQLite path like this one is
    # created inside the project's `instance/` folder by Flask-SQLAlchemy.
    # Set DATABASE_URL to use Postgres/MySQL later without touching code.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///bookshelf.db")

    # Set to True to print every SQL statement SQLAlchemy runs (great for learning!)
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(Config):
    # Run with `SQL_ECHO=1 flask run` to watch the SQL in your terminal
    SQLALCHEMY_ECHO = os.environ.get("SQL_ECHO") == "1"


class TestingConfig(Config):
    TESTING = True
    # An in-memory database: fast, and thrown away after each test run
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    pass


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}