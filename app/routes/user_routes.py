from app import db
from app.models.user import User
from app.models.content import Content
from app.models.watchlist import Watchlist
# from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request


users_bp = Blueprint("users_bp", __name__, url_prefix="/users")

@users_bp.route("", methods=["POST"])
def create_user():

    user_data = validate_request_body(User, request.get_json())
    user_data["contents_checked_out_count"] = 0
    new_user = User.from_dict(user_data)

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify(new_user.to_dict()), 201)

@users_bp.route("", methods=["GET"])
def get_users():
    user_query = User.query

    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "name":
            user_query = user_query.order_by(User.name.asc())
        elif sort_query == "postal_code":
            user_query = user_query.order_by(User.postal_code.asc())
        elif sort_query == "invalid":
            user_query = user_query.order_by(User.id.asc())
    else:
        user_query = user_query.order_by(User.id.asc())
    
    count_query = request.args.get("count")
    if count_query:
        if count_query == "invalid":
            user_query = user_query
        else:
            user_query = user_query.limit(count_query)
    
    page_num_query = request.args.get("page_num")
    if page_num_query:
        if page_num_query == "invalid":
            user_query = user_query
        else:
            offset_query = str(int(count_query) * (int(page_num_query) - 1))
            user_query = user_query.offset(offset_query)

    users = user_query.all()
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
    user_info.postal_code = request_body["postal_code"]
    user_info.phone = request_body["phone"]

    db.session.commit()

    return make_response(jsonify(user_info.to_dict()), 200)

@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_one_user(user_id):
    user = validate_model(User, user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return make_response(jsonify(user.to_dict()), 200)

@users_bp.route("/<user_id>/watchlists", methods=["GET"])
def get_current_watchlists(user_id):
    validate_model(User, user_id)
    content_query = Content.query.join(Watchlist, Watchlist.content_id==Content.id).filter(Watchlist.user_id==user_id)
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "title":
            content_query = content_query.order_by(Content.title.asc())
        elif sort_query == "invalid":
            content_query = content_query.order_by(Content.id.asc())
    else:
        content_query = content_query.order_by(Content.id.asc())
    
    count_query = request.args.get("count")
    if count_query:
        if count_query == "invalid":
            content_query = content_query
        else:
            content_query = content_query.limit(count_query)
    
    page_num_query = request.args.get("page_num")
    if page_num_query:
        if page_num_query == "invalid":
            content_query = content_query
        else:
            offset_query = str(int(count_query) * (int(page_num_query) - 1))
            content_query = content_query.offset(offset_query)
    contents = content_query.all()

    watchlists_response = []
    for content in contents:
        watchlists_response.append(content.to_dict())
        
    return jsonify(watchlists_response)