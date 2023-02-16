from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from app.models.content import Content

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    # Setup DB
    db.init_app(app)
    migrate.init_app(app, db)

    # import models for Alembic Setup
    from app.models.viewer import Viewer
    from app.models.watchlist import Watchlist    


    from .routes.viewer_routes import viewers_bp
    app.register_blueprint(viewers_bp)

    from .routes.content_routes import contents_bp
    app.register_blueprint(contents_bp)

    from .routes.watchlist_routes import watchlist_bp
    app.register_blueprint(watchlist_bp)

    return app