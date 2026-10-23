

class Library:
  """
  Library class to manage a collection of books.
  """
  def __init__(self, books=None):
    self.books = books if books is not None else []
  
  def add_book(self, book):
    self.books.append(book)

  def find_by_title(self, title):
    """Return the matching Book, or None if it isn't found."""
    for book in self.books:
      if book.title.lower() == title.strip().lower():
        return book
  
  def remove_book(self, title):
    """Remove a book by title."""
    book = self.find_by_title(title)
    if book:
      self.books.remove(book)
    return book
  
  def sorted_by(self, field):
    """Return a list of books sorted by the given field."""
    sort_keys = {
      "title": lambda book: book.title.lower(),
      "author": lambda book: book.author.lower(),
      "pages": lambda book: book.pages,
      "rating": lambda book: book.rating or 0,
    }

    key_func = sort_keys.get(field, sort_keys["title"])  # Default to sorting by title if field is invalid
    return sorted(self.books, key=key_func, reverse=(field == "rating"))