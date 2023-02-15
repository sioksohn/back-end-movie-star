from app import db
from app.models.content import Content
from app.models.customer import Customer
from app.models.rental import Rental
# from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request


contents_bp = Blueprint("contents_bp", __name__, url_prefix="/contents")

@contents_bp.route("", methods=["POST"])
def create_content():
    request_body = validate_request_body(Content, request.get_json())
    new_content = Content.from_dict(request_body)

    db.session.add(new_content)
    db.session.commit() 

    return make_response(jsonify(new_content.to_dict()), 201)

@contents_bp.route("", methods=["GET"])
def get_all_contents():
    content_query = Content.query
    contents = content_query.all()
    content_response = []
    for content in contents:
        content_response.append(content.to_dict())
    
    return jsonify(content_response)

@contents_bp.route("/<content_id>", methods=["GET"])
def get_one_content(content_id):
    content = validate_model(Content, content_id)
    return jsonify(content.to_dict())

@contents_bp.route("/<content_id>",methods=["PUT"])
def update_one_content(content_id):
    content_info = validate_model(Content, content_id)
    request_body = validate_request_body(Content, request.get_json())

    content_info.title = request_body["title"]
    content_info.release_date = request_body["release_date"]
    content_info.total_inventory = request_body["total_inventory"]

    db.session.commit()

    return make_response(jsonify(content_info.to_dict()), 200)

@contents_bp.route("/<content_id>",methods=["DELETE"])
def delete_one_content(content_id):
    content_info = validate_model(Content, content_id)
    
    db.session.delete(content_info)
    db.session.commit()
    
    return make_response(jsonify(content_info.to_dict()), 200)

@contents_bp.route("/<content_id>/rentals", methods=["GET"])
def get_current_rentals(content_id):
    validate_model(Content, content_id)
    customer_query = Customer.query.join(Rental, Rental.customer_id==Customer.id).filter(Rental.content_id==content_id)

    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "name":
            customer_query = customer_query.order_by(Customer.name.asc())
        elif sort_query == "postal_code":
            customer_query = customer_query.order_by(Customer.postal_code.asc())
        elif sort_query == "invalid":
            customer_query = customer_query.order_by(Customer.id.asc())
    else:
        customer_query = customer_query.order_by(Customer.id.asc())

    count_query = request.args.get("count")
    if count_query:
        if count_query == "invalid":
            customer_query = customer_query
        else:
            customer_query = customer_query.limit(count_query)
    
    page_num_query = request.args.get("page_num")
    if page_num_query:
        if page_num_query == "invalid":
            customer_query = customer_query
        else:
            offset_query = str(int(count_query) * (int(page_num_query) - 1))
            customer_query = customer_query.offset(offset_query)
    
    rentals_response = []
    customers = customer_query.all()
    for customer in customers:
            rentals_response.append(customer.to_dict())

    return jsonify(rentals_response)