from flask import Blueprint

movie_bp = Blueprint("movie_bp", __name__)

# @movie_bp.route("", methods=["POST"])