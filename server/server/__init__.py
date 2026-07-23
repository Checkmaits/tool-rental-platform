import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_talisman import Talisman

from server.extensions.db_extension import db
from server.routes.admin_auth_route import admin_auth_bp
from server.routes.customer_route import customer_bp
from server.routes.user_route import user_bp


def get_mysql_uri():
    username = os.getenv("MYSQL_USERNAME")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")
    database = os.getenv("MYSQL_DATABASE")

    return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SESSION_SECRET")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_mysql_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    CORS(app)
    Talisman(app)
    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(admin_auth_bp, url_prefix="/adminauth")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(user_bp, url_prefix="/users")

    return app
