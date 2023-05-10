from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models.user import UserModel


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
        if user:
            return user.json()
        return {"message": "User not found"}, 404

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        if current_user["id"] != id:
            return {"message": "Not found"}, 404

        data = User.parser.parse_args()
        existing_user = UserModel.query.filter_by(email=data["email"]).one_or_none()
        if (
            existing_user
            and existing_user.id != id
            and UserModel.is_valid_email(data["email"])
        ):
            return {"message": "A user with that email already exists"}, 400

        user = UserModel.find_by_id(id)
        if user is None:
            user = UserModel(**data)
        else:
            user.name = data["name"]
            user.email = data["email"]
            user.password = data["password"]

        user.save_to_db()
        return user.json(), 200

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user["id"] != id:
            return {"message": "Not found"}, 404

        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()

        return {"message": "User deleted"}, 200


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
        existing_user = UserModel.query.filter_by(email=data["email"]).one_or_none()
        if existing_user:
            return {"message": "A user with that email already exists"}, 400

        if not UserModel.is_valid_email(data["email"]):
            return {"message": "Invalid email format"}, 400

        user = UserModel(**data)
        try:
            user.save_to_db()
            return user.json(), 201
        except:
            return {"message": "An error occurred creating the user."}, 500


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = UserLogin.parser.parse_args()
        email = data["email"]
        password = data["password"]

        user = UserModel.query.filter_by(email=email).one_or_none()
        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user.json())
        return {"access_token": access_token}, 200
