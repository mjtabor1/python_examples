from app.extensions import db
from datetime import datetime, timezone


def utc_now():
  return datetime.now(timezone.utc)


class Review(db.Model):
  __tablename__ = "reviews"

  # A CHECK constraint: the database itself rejects ratings outside 1-5.
  __table_args__ = (db.CheckConstraint("rating BETWEEN 1 AND 5", name="rating_range"))

  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer, nullable=False)
  body = db.Column(db.Text)
  reviewer_name = db.Column(db.String(100), nullable=False, default="anonymous")
  created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

  book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
  book = db.relationship("Book", back_populates="reviews")


  def to_dict(self):
    return {
      "id": self.id,
      "book_id": self.book_id,
      "rating": self.rating,
      "body": self.body,
      "reviewer_name": self.reviewer_name,
      "created_at": self.created_at.isoformat()
    }