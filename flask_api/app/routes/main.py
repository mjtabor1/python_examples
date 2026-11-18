from flask import Blueprint, current_app, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    """List every endpoint the app knows about (handy while exploring)."""
    endpoints = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue
        methods = sorted(rule.methods - {"HEAD", "OPTIONS"})
        endpoints.append({"path": rule.rule, "methods": methods})

    endpoints.sort(key=lambda e: e["path"])
    return jsonify({"name": "Bookshelf API", "endpoints": endpoints})