from models.user import UserModel
from datetime import datetime, timezone
from flask_restful import Resource, reqparse
import utils.encryption as encryption
import bcrypt
from models.token_blocklist import TokenBlockListModel
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    create_refresh_token,
    get_jwt,
)


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def get(self, id):
        user = UserModel.find_by_id(id)

        if user is not None and user.is_active:
            return user.json(), 200
        return {"message": "User not found"}, 404

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        if current_user["id"] != id:
            return {"message": "Not found"}, 404

        data = User.parser.parse_args()
        hashed_email = encryption.hash_data(data["email"])
        hashed_name = encryption.hash_data(data["name"])

        existing_user = UserModel.query.filter_by(
            email_hash=hashed_email, is_active=True
        ).one_or_none()
        if (
            existing_user is not None
            and existing_user.id != id
            and UserModel.is_valid_email(data["email"])
        ):
            return {"message": "A user with that email already exists"}, 400
        existing_user = UserModel.query.filter_by(
            name_hash=hashed_name, is_active=True
        ).one_or_none()
        if existing_user is not None and existing_user.id != id:
            return {"message": "A user with that name already exists"}, 400

        if data["password"] == "" or len(data["password"]) < 8:
            return {"message": "Password must be at least 8 characters"}, 400
        if data["name"] == "" or data["email"] == "":
            return {"message": "Name and email cannot be empty"}, 400

        user = UserModel.find_by_id(id)
        if user is None:
            user = UserModel(**data)
        else:
            user.name = data["name"]
            user.email = data["email"]
            user.password = encryption.hash_password(data["password"], user.salt)

        try:
            user.save_to_db()
            return user.json(), 200
        except:
            return {"message": "An error occurred updating the user."}, 500

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user["id"] != id:
            return {"message": "Not found"}, 404

        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()

        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)

        token = TokenBlockListModel(
            jti,
            type=ttype,
            created_at=now,
            user_id=get_jwt_identity()["id"] if ttype == "access" else None,
        )

        try:
            token.save_to_db()
            return {"message": "User deleted"}, 200
        except:
            return {"message": "An error occurred deleting the user."}, 500


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        hashed_email = encryption.hash_data(data["email"])
        hashed_name = encryption.hash_data(data["name"])

        existing_user = UserModel.query.filter_by(
            email_hash=hashed_email, is_active=True
        ).one_or_none()
        if (
            existing_user is not None
            and existing_user.id != id
            and UserModel.is_valid_email(data["email"])
        ):
            return {"message": "A user with that email already exists"}, 400
        existing_user = UserModel.query.filter_by(
            name_hash=hashed_name, is_active=True
        ).one_or_none()
        if existing_user is not None and existing_user.id != id:
            return {"message": "A user with that name already exists"}, 400

        if not UserModel.is_valid_email(data["email"]):
            return {"message": "Invalid email format"}, 400

        existing_user = UserModel.query.filter_by(
            email_hash=hashed_email, is_active=False
        ).one_or_none()
        if existing_user is not None:
            user = UserModel.query.filter_by(
                email_hash=hashed_email, is_active=False
            ).one_or_none()
            user.recover_user()
            return user.json(), 201

        user = UserModel(**data)        
        user.salt = bcrypt.gensalt().decode("utf-8")
        user.password = encryption.hash_password(data["password"], user.salt)
        try:
            user.save_to_db()
            access_token = create_access_token(identity=user.json())
            refresh_token = create_refresh_token(identity=user.json())
            return {
                "user": user.json(),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        except:
            return {"message": "An error occurred creating the user."}, 500


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "email", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "token", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = UserLogin.parser.parse_args()
        email = data["email"]
        hashed_email = encryption.hash_data(data["email"])
        name = data["name"]
        hashed_name = encryption.hash_data(data["name"])
        password = data["password"]
        token = data["token"]

        if not email and not name:
            return {"message": "Invalid credentials"}, 401

        user_email = UserModel.query.filter_by(
            email_hash=hashed_email, is_active=True
        ).one_or_none()
        user_name = UserModel.query.filter_by(
            name_hash=hashed_name, is_active=True
        ).one_or_none()

        if user_email is None and user_name is None:
            return {"message": "Invalid credentials"}, 401

        user = user_email if user_email is not None else user_name
        if not user or not user.check_password(password) or not user.verify_totp(token):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user.json())
        refresh_token = create_refresh_token(identity=user.json())
        return {
            "user": user.jsonP(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 200


class UserLogout(Resource):
    @jwt_required(verify_type=False)
    def delete(self):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)

        token = TokenBlockListModel(
            jti,
            type=ttype,
            created_at=now,
            user_id=get_jwt_identity()["id"] if ttype == "access" else None,
        )

        try:
            token.save_to_db()
            return {"message": "Successfully logged out"}, 200
        except:
            return {"message": "An error occurred logging out"}, 500


class User2FA(Resource):
    @jwt_required(verify_type=False)
    def get(self):
        user = UserModel.find_by_id(get_jwt_identity()["id"])
        if user is None:
            return {"message": "User not found"}, 404

        return {"uri": user.get_totp_uri()}, 200