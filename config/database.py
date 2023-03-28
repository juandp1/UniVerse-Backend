import os
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db_controller = Blueprint("db_controller", __name__)

database_uri = (
    "mysql+pymysql://"
    + os.getenv("MYSQL_USER")
    + ":"
    + os.getenv("MYSQL_PASSWORD")
    + "@"
    + os.getenv("HOST")
    + "/"
    + os.getenv("MYSQL_DB_NAME")
)
db_controller.config["SQL_ALCHEMY_DATABASE_URI"] = database_uri
db_controller.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(db_controller)
marshmallow = Marshmallow(db_controller)
