from flask import Blueprint, jsonify

from app.extensions import db
from app.helpers import get_json_body
from app.models import Author

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")


@authors_bp.get("")
def list_authors():
    # SELECT * FROM authors ORDER BY name
    query = db.select(Author).order_by(Author.name)
    authors = db.session.execute(query).scalars().all()
    return jsonify([author.to_dict() for author in authors])


@authors_bp.post("")
def create_author():
    data = get_json_body("name")
    author = Author(name=data["name"], bio=data.get("bio"))

    db.session.add(author)  # stage the change...
    db.session.commit()     # ...then save it for real
    return jsonify(author.to_dict()), 201


@authors_bp.get("/<int:author_id>")
def get_author(author_id):
    # get_or_404: look up by primary key, or stop with a 404 error
    author = db.get_or_404(Author, author_id, description=f"Author {author_id} not found.")
    return jsonify(author.to_dict(include_books=True))


@authors_bp.patch("/<int:author_id>")
def update_author(author_id):
    author = db.get_or_404(Author, author_id, description=f"Author {author_id} not found.")
    data = get_json_body()

    # PATCH = only change the fields that were sent
    if "name" in data:
        author.name = data["name"]
    if "bio" in data:
        author.bio = data["bio"]

    db.session.commit()  # SQLAlchemy noticed the changes; no add() needed
    return jsonify(author.to_dict())


@authors_bp.delete("/<int:author_id>")
def delete_author(author_id):
    author = db.get_or_404(Author, author_id, description=f"Author {author_id} not found.")
    db.session.delete(author)  # cascade also deletes their books (and those books' reviews)
    db.session.commit()
    return "", 204