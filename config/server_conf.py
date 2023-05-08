from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config.server_variables import *

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

# Configuring the Flask-SQLAlchemy
db = SQLAlchemy()

with app.app_context():
    db.init_app(app)
    db.create_all()


def run_server():
    is_dev_env = False if SERVER_ENV == "production" else True
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=is_dev_env)
