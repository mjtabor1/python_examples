"""
LESSON: A Blueprint is a group of related routes. Each resource (authors,
books, genres) gets its own file and blueprint, and they're all plugged
into the app here. Adding a new resource = new file + one line below.
"""

from app.routes.authors import authors_bp
from app.routes.books import books_bp
from app.routes.genres import genres_bp
from app.routes.main import main_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(genres_bp)