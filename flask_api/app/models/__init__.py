"""
Importing every model here means `from app.models import Book` works
everywhere, and one `import app.models` registers ALL tables with
SQLAlchemy (which Flask-Migrate needs to autogenerate migrations).

When you add a new model file, import it here too.
"""

from app.models.author import Author
from app.models.book import Book, book_genres
from app.models.genre import Genre
from app.models.review import Review

__all__ = ["Author", "Book", "book_genres", "Genre", "Review"]