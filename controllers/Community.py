from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.community import CommunityModel


class CommunityId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "id", type=int, required=True, help="This field cannot be blank."
    )
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
    def post(self):
        data = CommunityId.parser.parse_args()
        community = CommunityModel(**data)

        try:
            community.save_to_db()
            return community.json(), 201
        except:
            return {"message": "An error occurred creating the community."}, 500

    @jwt_required()
    def delete(self, id):
        community = CommunityModel.find_by_id(id)
        if community:
            community.delete_from_db()

        return {"message": "Community deleted"}, 200

    @jwt_required()
    def put(self, id):
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
    def post(self):
        data = CommunityName.parser.parse_args()
        community = CommunityModel(**data)

        try:
            community.save_to_db()
            return community.json(), 201
        except:
            return {"message": "An error occurred creating the community."}, 500

    @jwt_required()
    def delete(self, name):
        community = CommunityModel.find_by_name(name)
        if community:
            community.delete_from_db()

        return {"message": "Community deleted"}, 200

    @jwt_required()
    def put(self, name):
        data = CommunityName.parser.parse_args()
        community = CommunityModel.find_by_name(name)

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


class CommunityList(Resource):
    @jwt_required()
    def get(self):
        return {
            "communities": [
                community.json()
                for community in CommunityModel.query.all().where(is_active=True)
            ]
        }
