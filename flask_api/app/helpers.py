"""Small helpers shared by the route files."""

from flask import abort, request


def get_json_body(*required_fields):
    """
    Return the request's JSON body as a dict, or stop with a 400 error.

        data = get_json_body("title", "author_id")   # both must be present
    """
    data = request.get_json(silent=True)  # silent=True: return None instead of raising
    if not isinstance(data, dict):
        abort(400, description="Request body must be a JSON object.")

    missing = [field for field in required_fields if data.get(field) in (None, "")]
    if missing:
        abort(400, description=f"Missing required field(s): {', '.join(missing)}")

    return data