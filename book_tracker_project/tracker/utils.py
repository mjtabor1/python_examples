

def print_header(text):
  print()
  print("=" * 50)
  print(text.upper().center(50))
  print("=" * 50)


def get_number(prompt, min_value=None, max_value=None):
  """Keep asking until the user types a valid whole number in range."""
  while True:
    raw = input(prompt).strip()
    try:
      number = int(raw)
    except ValueError:
      print("  That's not a whole number. Try again.")
      continue                        # jump back to the top of the loop

    if min_value is not None and number < min_value:
      print(f"  Must be at least {min_value}.")
    elif max_value is not None and number > max_value:
      print(f"  Must be at most {max_value}.")
    else:
      return number   


def get_choice(prompt, options):
  """Ask the user to pick one item from a list or tuple of options."""
  for number, option in enumerate(options, start=1):
    print(f"  {number}. {option}")
  index = get_number(prompt, 1, len(options))
  return options[index - 1]


def print_books(books):
  if not books:
    print("  No books to show.")
    return
  for number, book in enumerate(books, start=1):
    print(f"\n {number:>2}. {book.title} by {book.author}")

