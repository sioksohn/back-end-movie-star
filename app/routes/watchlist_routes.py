from flask import Blueprint

watchlists_bp = Blueprint("watchlists_bp", __name__, url_prefix="/watchlists")

@watchlists_bp.route("", methods=["POST"])
def create_watchlist():
    request_body = validate_request_body(Watchlist, request.get_json())
    new_watchlist = Watchlist.from_dict(request_body)

    db.session.add(new_watchlist)
    db.session.commit() 

    return make_response(jsonify(new_watchlist.to_dict()), 201)

@watchlists_bp.route("", methods=["GET"])
def get_all_watchlists():
    watchlist_query = Watchlist.query
    watchlists = watchlist_query.all()
    watchlist_response = []
    for watchlist in watchlists:
        watchlist_response.append(watchlist.to_dict())
    
    return jsonify(watchlist_response)