from flask import Flask
from routes.auth import auth_router
from config.database import db_controller

from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.register_blueprint(auth_router)
app.register_blueprint(db_controller)
