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
    viewer = validate_model(Viewer, request_body["viewer_id"])
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

@watchlist_bp.route("/<watchlist_id>", methods=["DELETE"])
def delete_one_watchlist(viewer_id):
    watchlist = validate_model(Watchlist, watchlist_id)
    
    db.session.delete(watchlist)
    db.session.commit()
    
    return make_response(jsonify(watchlist.to_dict()), 200)