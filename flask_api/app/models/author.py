from app.extensions import db


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)

    # ONE-TO-MANY: one author has many books.
    # back_populates links this to Book.author, so both sides stay in sync.
    # cascade="all, delete-orphan" means deleting an author deletes their books too.
    books = db.relationship("Book", back_populates="author", cascade="all, delete-orphan")

    def to_dict(self, include_books=False):
        """Turn the model into a plain dict that jsonify() can send."""
        data = {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "book_count": len(self.books),
        }
        if include_books:
            data["books"] = [
                {"id": book.id, "title": book.title, "published_year": book.published_year}
                for book in self.books
            ]
        return data

    def __repr__(self):
        return f"<Author {self.id} {self.name!r}>"