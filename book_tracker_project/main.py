from tracker.utils import print_header, get_choice, print_books
from tracker.storage import load_books
from tracker import Library, Book

def view_all_books(library):
  '''
  View all books in the library.
  '''
  print_header("All Books")
  field = get_choice("Sort by: ", ("title", "author", "pages", "rating"))
  print_books(library.sorted_by(field))
   


# ---------- The menu ----------
# A dictionary that maps what the user types -> (label, function).
# Functions are objects in Python, so we can store them in a dict!
 
MENU_OPTIONS = {
    "1": ("View all books", view_all_books),
    # "2": ("View books by status", view_by_status),
    # "3": ("Search books", search_books),
    # "4": ("Add a book", add_book),
    # "5": ("Update reading progress", update_progress),
    # "6": ("Remove a book", remove_book),
    # "7": ("Reading stats", show_stats),
    # "8": ("Export report to CSV", export_report),
    # "9": ("View recent activity", show_activity),
}
 
 
def print_menu(library):
    # print_header(f"Book Tracker ({len(library)} books)")
    for key, (label, _function) in MENU_OPTIONS.items():
        print(f"  {key}. {label}")
    print("  0. Quit")

def main():

  library = Library(load_books())  # Create an instance of the Library class

  while True:
    print_menu(library)
    choice = input("\nChoose an option: ").strip()

    option = MENU_OPTIONS.get(choice)
    if option is None:
      print("Invalid choice - please pick a number from the menu.")
      continue
    
    label, action = option
    action(library)

if __name__ == "__main__":
    main()