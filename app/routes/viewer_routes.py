from app import db
from app.models.viewer import Viewer
from app.models.content import Content
from app.models.watchlist import Watchlist
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

viewers_bp = Blueprint("viewers_bp", __name__, url_prefix="/viewers")

@viewers_bp.route("", methods=["POST"])
def create_viewer():
    request_body = validate_request_body(Viewer, request.get_json())
    new_viewer = viewer.from_dict(request_body)

    db.session.add(new_viewer)
    db.session.commit()

    return make_response(jsonify(new_viewer.to_dict()), 201)

@viewers_bp.route("", methods=["GET"])
def get_viewers():
    viewers = Viewer.query.all()
    viewer_response = []
    for viewer in viewers:
        viewer_response.append(viewer.to_dict())

    return jsonify(viewer_response)

@viewers_bp.route("/<viewer_id>", methods=["GET"])
def get_one_viewer(viewer_id):
    viewer = validate_model(Viewer, viewer_id)
    return jsonify(viewer.to_dict())

@viewers_bp.route("/<viewer_id>",methods=["PUT"])
def update_one_viewer(viewer_id):
    viewer_info = validate_model(Viewer, viewer_id)
    request_body = validate_request_body(Viewer, request.get_json())

    viewer_info.name = request_body["name"]
    viewer_info.email = request_body["email"]
    # viewer_info.password = request_body["password"]

    db.session.commit()

    return make_response(jsonify(viewer_info.to_dict()), 200)

@viewers_bp.route("/<viewer_id>", methods=["DELETE"])
def delete_one_viewer(viewer_id):
    viewer = validate_model(Viewer, viewer_id)
    
    db.session.delete(viewer)
    db.session.commit()
    
    return make_response(jsonify(viewer.to_dict()), 200)

@viewers_bp.route("/<viewer_id>/watchlist", methods=["GET"])
def get_current_watchlists(viewer_id):
    viewer = validate_model(Viewer, viewer_id)

    watchlists_response = []
    for content in viewers.watchlists:
        watchlists_response.append(content.to_dict())
        
    return jsonify(watchlists_response)