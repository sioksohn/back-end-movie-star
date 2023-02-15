from app import db
from app.models.viewer import Viewer
from app.models.content import Content
from app.models.watchlist import Watchlist
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

watchlist_bp = Blueprint("watchlist_bp", __name__, url_prefix="/watchlist")

@watchlist_bp.route("", methods=["POST"])
def create_watchlist():
    request_body = validate_request_body(Watchlist, request.get_json())
    viewer = validate_model(Viewer, request_body["Viewer_id"])
    content = validate_model(Content, request_body["content_id"])
    new_watchlist = Watchlist.from_dict(request_body)

    db.session.add(new_watchlist)
    db.session.commit()

    return make_response(jsonify(f"Watchlist {new_watchlist.id} successfully created"), 201)

@watchlist_bp.route("", methods=["GET"])
def read_all_watchlists():
    watchlist_query = Watchlist.query
    watchlist_response = []
    for watchlist in watchlist_query:
        watchlist_response.append(watchlist.to_dict())
    return jsonify(watchlist_response)

@watchlist_bp.route("/add", methods=["POST"])
def add_to_watchlist():
    request_body = validate_request_body(Watchlist, request.get_json())
    viewer = validate_model(Viewer, request_body["viewer_id"])
    content = validate_model(Content, request_body["content_id"])
    # Create new watchlist
    new_watchlist = Watchlist(
        viewer_id=viewer.id,
        content_id=content.id,
        )
    db.session.add(new_watchlist)
    db.session.commit()
    
    return make_response(jsonify({
        "viewer_id": viewer.id,
        "content_id": content.id,
        }), 200)

@watchlist_bp.route("/remove", methods=["DELETE"])
def remove_from_watchlist():
    request_body = validate_request_body(watchlist, request.get_json())
    viewer = validate_model(Viewer, request_body["viewer_id"])
    content = validate_model(Content, request_body["content_id"])
    
    watchlist_query = Watchlist.query.all()
    existing_watchlists = []

    if watchlist_query:
        watchlist_query = Watchlist.query.filter_by(viewer_id=viewer.id).filter_by(content_id=content.id)
        for watchlist in watchlist_query:
            existing_watchlists.append(watchlist)

    if not existing_watchlists:
        abort(make_response({"message": f"No outstanding watchlists for viewer {viewer.id} and content {content.id}"}, 400))

    watchlist_to_remove = existing_watchlists[0]
    
    db.session.delete(watchlist_to_remove)
    db.session.commit()


    return make_response(jsonify({
        "viewer_id": viewer.id,
        "content_id": content.id
        }), 200)