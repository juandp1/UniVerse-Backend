from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import JWTManager
from config.database_conf import db
from config.server_variables import *
from config.routes_conf import start_routes

# Import models
from config.load_models import *

# Configuring the Flask app
app = Flask(__name__)
cors = CORS(app)

app.secret_key = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Configuring the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Start the Flask-JWT-Extended and the Flask-ReSTful extension
jwt = JWTManager(app)
api = Api(app)

with app.app_context():
    db.init_app(app)
    db.create_all()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlockListModel.query.filter_by(jti=jti).one_or_none()

    return token is not None


# Start the routes
start_routes(api)


def run_server():
    is_dev_env = False if SERVER_ENV == "production" else True
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=is_dev_env)
