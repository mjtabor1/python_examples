from app.extensions import db

class Genre(db.Model):
  __tablename__ = "genres"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  # This is the other side of the many-to-many. "book_genres" is the join table's name. 
  books = db.relationship("Book", secondary="book_genres", back_populates="genres")


  def to_dict(self, include_books=False):
    data = {"id": self.id, "name": self.name, "book_count": len(self.books)}
    if include_books:
      data["books"] = [{ "id": book.id, "title": book.title} for book in self.books]
    return data