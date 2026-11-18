from flask import Blueprint, abort, jsonify, request

from app.extensions import db
from app.helpers import get_json_body
from app.models import Author, Book, Genre, Review

books_bp = Blueprint("books", __name__, url_prefix="/books")


# ---------- helpers used by the routes below ----------

def find_book(book_id):
    return db.get_or_404(Book, book_id, description=f"Book {book_id} not found.")


def load_author(author_id):
    """Like get_or_404, but a bad id in the BODY is the client's mistake (400), not a missing page (404)."""
    author = db.session.get(Author, author_id)
    if author is None:
        abort(400, description=f"Author {author_id} does not exist.")
    return author


def load_genres(genre_ids):
    """Turn a list of ids like [1, 3] into Genre objects, or 400 if any don't exist."""
    if not isinstance(genre_ids, list):
        abort(400, description="genre_ids must be a list of ids, e.g. [1, 3].")
    query = db.select(Genre).where(Genre.id.in_(genre_ids))  # WHERE id IN (1, 3)
    genres = db.session.execute(query).scalars().all()
    if len(genres) != len(set(genre_ids)):
        abort(400, description="One or more genre_ids do not exist.")
    return genres


# ---------- routes ----------

@books_bp.get("")
def list_books():
    """
    GET /books                     all books, A-Z
    GET /books?search=dune         title contains "dune" (any case)
    GET /books?author_id=1         books by one author
    GET /books?genre=fantasy       books in a genre (uses a JOIN)
    GET /books?sort=newest         sort: title | oldest | newest
    Filters can be combined: /books?genre=science fiction&sort=newest
    """
    # LESSON: we build the query step by step. Nothing runs until execute().
    query = db.select(Book)

    search = request.args.get("search")
    if search:
        query = query.where(Book.title.ilike(f"%{search}%"))

    author_id = request.args.get("author_id", type=int)
    if author_id:
        query = query.where(Book.author_id == author_id)

    genre = request.args.get("genre")
    if genre:
        # JOIN through the book_genres table to reach Genre, then filter on it
        query = query.join(Book.genres).where(Genre.name.ilike(genre))

    sort_options = {
        "title": Book.title,
        "oldest": Book.published_year,
        "newest": Book.published_year.desc(),
    }
    query = query.order_by(sort_options.get(request.args.get("sort"), Book.title))

    books = db.session.execute(query).scalars().all()
    return jsonify([book.to_dict() for book in books])


@books_bp.get("/top-rated")
def top_rated_books():
    """
    GET /books/top-rated?limit=3

    LESSON: an AGGREGATE query. The database groups reviews by book and
    averages the ratings itself, so we don't load every review into Python.
    Roughly:  SELECT books.*, AVG(rating), COUNT(reviews.id)
              FROM books JOIN reviews ON ... GROUP BY books.id
              ORDER BY AVG(rating) DESC LIMIT 3
    """
    limit = request.args.get("limit", default=5, type=int)
    avg_rating = db.func.avg(Review.rating).label("avg_rating")
    review_count = db.func.count(Review.id).label("review_count")

    query = (
        db.select(Book, avg_rating, review_count)
        .join(Book.reviews)
        .group_by(Book.id)
        .order_by(avg_rating.desc(), review_count.desc(), Book.title)  # ties: more reviews, then A-Z
        .limit(limit)
    )
    rows = db.session.execute(query).all()  # each row is (Book, avg, count)

    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author.name,
            "average_rating": round(avg, 2),
            "review_count": count,
        }
        for book, avg, count in rows
    ])


@books_bp.post("")
def create_book():
    data = get_json_body("title", "author_id")

    book = Book(
        title=data["title"],
        published_year=data.get("published_year"),
        author=load_author(data["author_id"]),       # set the relationship, SQLAlchemy fills in author_id
        genres=load_genres(data.get("genre_ids", [])),
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201


@books_bp.get("/<int:book_id>")
def get_book(book_id):
    return jsonify(find_book(book_id).to_dict(include_reviews=True))


@books_bp.patch("/<int:book_id>")
def update_book(book_id):
    book = find_book(book_id)
    data = get_json_body()

    if "title" in data:
        book.title = data["title"]
    if "published_year" in data:
        book.published_year = data["published_year"]
    if "author_id" in data:
        book.author = load_author(data["author_id"])
    if "genre_ids" in data:
        book.genres = load_genres(data["genre_ids"])  # replaces the whole list of genres

    db.session.commit()
    return jsonify(book.to_dict())


@books_bp.delete("/<int:book_id>")
def delete_book(book_id):
    book = find_book(book_id)
    db.session.delete(book)  # its reviews go too (cascade); its book_genres rows are removed automatically
    db.session.commit()
    return "", 204


# ---------- nested resource: a book's reviews ----------

@books_bp.get("/<int:book_id>/reviews")
def list_reviews(book_id):
    book = find_book(book_id)
    return jsonify([review.to_dict() for review in book.reviews])


@books_bp.post("/<int:book_id>/reviews")
def create_review(book_id):
    book = find_book(book_id)
    data = get_json_body("rating")

    rating = data["rating"]
    if not isinstance(rating, int) or not 1 <= rating <= 5:
        abort(400, description="rating must be a whole number from 1 to 5.")

    review = Review(
        book=book,
        rating=rating,
        body=data.get("body"),
        reviewer_name=data.get("reviewer_name") or "anonymous",
    )
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201