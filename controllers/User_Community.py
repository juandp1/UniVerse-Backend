from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.community import CommunityModel
from models.user import UserModel
from models.administrator import AdministratorModel
from models.user_belongs_to_community import UserBelongsToCommunityModel
from models.administrator_manage_community import AdministratorManageCommunityModel


class UserEnterCommunity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id", type=int, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "user_id", type=int, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self):
        data = UserEnterCommunity.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if user_id != data["user_id"]:
            return {"message": "User not found"}, 404

        if not CommunityModel.find_by_id(data["community_id"]):
            return {"message": "Community not found"}, 404

        if not UserModel.find_by_id(data["user_id"]):
            return {"message": "User not found"}, 404

        if UserBelongsToCommunityModel.find_by_user_id_and_community_id(
            data["user_id"], data["community_id"]
        ):
            return {"message": "User already in community"}, 400

        user_belongs_to_community = UserBelongsToCommunityModel(
            data["user_id"], data["community_id"]
        )
        try:
            user_belongs_to_community.save_to_db()
            return user_belongs_to_community.json(), 201
        except:
            return {"message": "An error occurred creating the user."}, 500


class UserLeaveCommunity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id", type=int, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "user_id", type=int, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def delete(self):
        data = UserEnterCommunity.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if user_id != data["user_id"]:
            return {"message": "User not found"}, 404

        if not CommunityModel.find_by_id(data["community_id"]):
            return {"message": "Community not found"}, 404

        if not UserModel.find_by_id(data["user_id"]):
            return {"message": "User not found"}, 404

        user_belongs_to_community = (
            UserBelongsToCommunityModel.find_by_user_id_and_community_id(
                data["user_id"], data["community_id"]
            )
        )
        if not user_belongs_to_community:
            return {"message": "User not in community"}, 400

        try:
            user_belongs_to_community.delete_from_db()
            return {"message": "User left community"}, 200
        except:
            return {"message": "An error occurred leaving the community."}, 500


class UserIsAdmin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id", type=int, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "user_id", type=int, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self):
        data = UserIsAdmin.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if user_id != data["user_id"]:
            return {"message": "User not found"}, 404

        if not CommunityModel.find_by_id(data["community_id"]):
            return {"message": "Community not found"}, 404

        if not UserModel.find_by_id(data["user_id"]):
            return {"message": "User not found"}, 404

        if not AdministratorModel.find_by_user_id(data["user_id"]):
            return {"message": "User is not admin"}, 400

        user_belongs_to_community = (
            UserBelongsToCommunityModel.find_by_user_id_and_community_id(
                data["user_id"], data["community_id"]
            )
        )
        if user_belongs_to_community is None:
            return {"message": "User not in community"}, 400

        user_is_admin_of_community = (
            AdministratorManageCommunityModel.user_is_admin_of_community(
                data["user_id"], data["community_id"]
            )
        )
        if not user_is_admin_of_community:
            return {"message": "User is not admin"}, 400

        return user_is_admin_of_community, 200


class UserIsMember(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "community_id", type=int, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "user_id", type=int, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self):
        data = UserIsMember.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if user_id != data["user_id"]:
            return {"message": "User not found"}, 404

        if not CommunityModel.find_by_id(data["community_id"]):
            return {"message": "Community not found"}, 404

        if not UserModel.find_by_id(data["user_id"]):
            return {"message": "User not found"}, 404

        user_belongs_to_community = (
            UserBelongsToCommunityModel.find_by_user_id_and_community_id(
                data["user_id"], data["community_id"]
            )
        )
        if user_belongs_to_community is None:
            return {"message": "User not in community"}, 400

        return (user_belongs_to_community is not None), 200
