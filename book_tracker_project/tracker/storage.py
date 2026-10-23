from .models import Book
import json
from pathlib import Path 


# Path(__file__) is this file. .parent goes up one folder.
# This builds paths that work on Windows, Mac, and Linux.
PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
BOOKS_FILE = DATA_DIR / "books.json"
REPORT_FILE = DATA_DIR / "reading_report.csv"
LOG_FILE = DATA_DIR / "activity.log"


def load_books(path=BOOKS_FILE):
  """Read books.json and return a list of Book objects."""
  try:
    with open(path, "r", encoding="utf-8") as file:
      data = json.load(file)
  except FileNotFoundError:
    print(f"No saved books found at {path.name}.")
    return []
  except json.JSONDecodeError:
    print(f"{path.name} is damaged or empty.")
    return []
  return [Book.from_dict(item) for item in data]