from app import db
from app.models.user import User
from app.models.content import Content
from app.models.watchlist import Watchlist
# from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

users_bp = Blueprint("users_bp", __name__, url_prefix="/users")

@users_bp.route("", methods=["POST"])
def create_user():
    request_body = validate_request_body(User, request.get_json())
    new_user = User.from_dict(request_body)

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify(new_user.to_dict()), 201)

@users_bp.route("", methods=["GET"])
def get_users():
    users = User.query.all()
    user_response = []
    for user in users:
        user_response.append(user.to_dict())

    return jsonify(user_response)

@users_bp.route("/<user_id>", methods=["GET"])
def get_one_user(user_id):
    user = validate_model(User, user_id)
    return jsonify(user.to_dict())

@users_bp.route("/<user_id>",methods=["PUT"])
def update_one_user(user_id):
    user_info = validate_model(User, user_id)
    request_body = validate_request_body(User, request.get_json())

    user_info.name = request_body["name"]
    user_info.email = request_body["email"]
    # user_info.password = request_body["password"]

    db.session.commit()

    return make_response(jsonify(user_info.to_dict()), 200)

@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_one_user(user_id):
    user = validate_model(User, user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return make_response(jsonify(user.to_dict()), 200)

@users_bp.route("/<user_id>/watchlist", methods=["GET"])
def get_current_watchlists(user_id):
    user = validate_model(User, user_id)

    watchlists_response = []
    for content in users.watchLists:
        watchlists_response.append(content.to_dict())
        
    return jsonify(watchlists_response)