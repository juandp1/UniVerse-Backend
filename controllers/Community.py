from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.community import CommunityModel
from models.administrator_manage_community import AdministratorManageCommunityModel


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

    @jwt_required()
    def post(self):
        data = CommunityName.parser.parse_args()

        existing_community = CommunityModel.find_by_name(data["name"])
        if existing_community:
            return {"message": "A community with that name already exists."}, 400

        existing_community = CommunityModel.query.filter_by(
            name=data["name"], is_active=False
        ).first()
        if existing_community:
            existing_community.description = data["description"]
            existing_community.is_active = True
            try:
                existing_community.save_to_db()

                # Update Admins
                jwt_user = get_jwt_identity()
                user_id = jwt_user["id"]
                AdministratorManageCommunityModel.add_admin_to_community(
                    user_id, existing_community.id
                )

                return existing_community.json(), 200
            except:
                return {"message": "An error occurred creating the community."}, 500

        community = CommunityModel(**data)
        try:
            community.save_to_db()

            # Update Admins
            jwt_user = get_jwt_identity()
            user_id = jwt_user["id"]
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
