from flask import Blueprint

auth_router = Blueprint("auth_router", __name__)


@auth_router.route("/login")
def login():
    return "<p1>login</p1>"


@auth_router.route("/register")
def register():
    return "<p1>register</p1>"
