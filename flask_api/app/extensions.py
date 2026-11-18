"""
Extension objects live here, created WITHOUT an app.

LESSON: If `db` were created inside `create_app()`, every model file would
need to import the app, and the app would need to import the models: a
circular import. Instead we make the objects here, import them anywhere,
and connect them to the app later with `init_app()`.
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Gives every constraint (foreign keys, unique, etc.) a predictable name.
# Migrations need names to find a constraint later if you change or drop it.
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()