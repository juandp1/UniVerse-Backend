from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.community import CommunityModel
from models.user_belongs_to_community import UserBelongsToCommunityModel
from models.administrator_manage_community import AdministratorManageCommunityModel
from models.label import LabelModel
from models.label_has_community import LabelHasCommunityModel


class CommunityId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "description", type=str, required=False, help="This field cannot be blank."
    )

    @jwt_required()
    def get(self, id):
        community = CommunityModel.find_by_id(id)
        if community:
            return community.json()
        return {"message": "Community not found"}, 404

    @jwt_required()
    def delete(self, id):
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]
        if not AdministratorManageCommunityModel.user_is_admin_of_community(
            user_id, id
        ):
            return {"message": "You are not an admin of this community"}, 401

        community = CommunityModel.find_by_id(id)
        if community:
            community.delete_from_db()

        return {"message": "Community deleted"}, 200

    @jwt_required()
    def put(self, id):
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]
        if not AdministratorManageCommunityModel.user_is_admin_of_community(
            user_id, id
        ):
            return {"message": "You are not an admin of this community"}, 401

        data = CommunityId.parser.parse_args()
        community = CommunityModel.find_by_id(id)

        if community is None:
            community = CommunityModel(**data)
        else:
            community.name = data["name"]
            community.description = data["description"]

        try:
            community.save_to_db()
            return community.json(), 200
        except:
            return {"message": "An error occurred updating the community."}, 500


class CommunityName(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "description", type=str, required=False, help="This field cannot be blank."
    )

    @jwt_required()
    def get(self, name):
        community = CommunityModel.find_by_name(name)
        if community:
            return community.json()
        return {"message": "Community not found"}, 404

    @jwt_required()
    def delete(self, name):
        jwt_user = get_jwt_identity()
        community = CommunityModel.find_by_name(name)

        if community is None:
            return {"message": "Community not found"}, 404

        id = community.id
        user_id = jwt_user["id"]
        if not AdministratorManageCommunityModel.user_is_admin_of_community(
            user_id, id
        ):
            return {"message": "You are not an admin of this community"}, 401

        if community:
            community.delete_from_db()

        return {"message": "Community deleted"}, 200

    @jwt_required()
    def put(self, name):
        jwt_user = get_jwt_identity()
        community = CommunityModel.find_by_name(name)

        if community is None:
            return {"message": "Community not found"}, 404

        id = community.id
        user_id = jwt_user["id"]
        if not AdministratorManageCommunityModel.user_is_admin_of_community(
            user_id, id
        ):
            return {"message": "You are not an admin of this community"}, 401

        data = CommunityName.parser.parse_args()

        community.name = data["name"]
        community.description = data["description"]

        try:
            community.save_to_db()
            return community.json(), 200
        except:
            return {"message": "An error occurred updating the community."}, 500


class CommunitySimilarName(Resource):
    @jwt_required()
    def get(self, name):
        return {
            "communities": [
                community.json()
                for community in CommunityModel.find_by_similar_name(name)
            ]
        }, 200


class CommunityList(Resource):
    @jwt_required()
    def get(self):
        return {
            "communities": [
                community.json()
                for community in CommunityModel.query.filter_by(is_active=True).all()
            ]
        }, 200


class CreateCommunity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "description", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "label", type=str, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self):
        data = CreateCommunity.parser.parse_args()

        if data["name"] == "":
            return {"message": "Name cannot be empty"}, 400
        if data["description"] == "":
            return {"message": "Description cannot be empty"}, 400

        existing_community = CommunityModel.find_by_name(data["name"])
        if existing_community:
            return {"message": "A community with that name already exists."}, 400

        # Create Label
        existing_label = LabelModel.find_by_name(data["label"])
        if not existing_label:
            existing_label = LabelModel(name=data["label"])
            existing_label.save_to_db()

        existing_community = CommunityModel.query.filter_by(
            name=data["name"], is_active=False
        ).first()
        if existing_community:
            return {"message": "This community already exists"}, 400

        community = CommunityModel(name=data["name"], description=data["description"])
        try:
            community.save_to_db()

            # Create Connection Label-Community
            label = LabelHasCommunityModel(
                label_id=existing_label.id, community_id=community.id
            )
            label.save_to_db()

            # Create Connection User-Community
            jwt_user = get_jwt_identity()
            user_id = jwt_user["id"]
            user_comm = UserBelongsToCommunityModel(
                user_id=user_id, community_id=community.id
            )
            user_comm.save_to_db()

            # Update Admins
            AdministratorManageCommunityModel.add_admin_to_community(
                user_id, community.id
            )

            return community.json(), 201
        except:
            return {"message": "An error occurred creating the community."}, 500


class SearchCommunity(Resource):
    @jwt_required()
    def get(self, name):
        community = CommunityModel.find_by_name(name)
        if community is None:
            return {"message": "Community not found"}, 404

        return community.json(), 200
