from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from config.server_variables import *

# Importing the database object and models
from config.database_conf import db
from models.user import UserModel
from models.administrator import AdministratorModel
from models.label import LabelModel
from models.user_follows_label import User_FollowsLabelModel

# Configuring the Flask app
app = Flask(__name__)

app.secret_key = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Configuring the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

# Start the Flask-JWT-Extended and the Flask-ReSTful extension
jwt = JWTManager(app)
api = Api(app)

# Create the database tables
with app.app_context():
    db.init_app(app)
    db.create_all()


def run_server():
    is_dev_env = False if SERVER_ENV == "production" else True
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=is_dev_env)
