from app.extensions import db

book_genres = db.Table(
  "book_genres",
  db.Column("book_id", db.Integer, db.ForeignKey("books.id"), primary_key=True),
  db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True)
)

class Book(db.Model):
  __tablename__ = "books"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  published_year = db.Column(db.Integer)

  author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

  author = db.relationship("Author", back_populates="books") # many-to-one
  genres = db.relationship("Genre", secondary=book_genres, back_populates="books") # many-to-many
  reviews = db.relationship("Review", back_populates="book", cascade="all, delete-orphan", order_by="Review.id.desc()")


  @property
  def average_rating(self):
    if not self.reviews:
      return None
    return round(sum(r.rating for r in self.reviews) / len(self.reviews), 2)

  def to_dict(self, include_reviews=False):
    data = {
      "id": self.id,
      "title": self.title,
      "published_year": self.published_year,
      "author": {"id": self.author.id, "name": self.author.name},
      "genres": [genre.name for genre in self.genres],
      "average_rating": self.average_rating,
      "review_count": len(self.reviews)
    }
    if include_reviews:
      data["reviews"] = [review.to_dict() for review in self.reviews]
    return data