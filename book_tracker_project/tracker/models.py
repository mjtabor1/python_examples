from datetime import date

class Book:
  VALID_STATUSES = ("to-read", "reading", "finished")

  def __init__(self, title, author, pages, genre="Unknown", status="to-read", rating=None, date_added=None):
    self.title = title.strip()
    self.author = author.strip().title()
    self.pages = int(pages)
    self.genre = genre.strip().title()
    self.status = status if status in Book.VALID_STATUSES else "to-read"
    self.rating = rating
    self.date_added = date_added or date.today().isoformat()
  
  def to_dict(self):
    """Return a dictionary representation of the Book instance."""
    return {
      "title": self.title,
      "author": self.author,
      "pages": self.pages,
      "genre": self.genre,
      "status": self.status,
      "rating": self.rating,
      "date_added": self.date_added
    }
  
  @classmethod
  def from_dict(cls, data):
    """Build a Book from a dictionary
    
    'cls' is the class itself (Book). '**data' unpacks the dictionary into keyword arguments
    like so: title=..., author=..., pages=..., etc. This allows us to create a Book instance from a dictionary representation.
    """
    return cls(**data)
