from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.question import QuestionModel
from models.community import CommunityModel
from models.administrator_manage_community import AdministratorManageCommunityModel


class QuestionsPerCommunity(Resource):
    @jwt_required()
    def get(self, community_id):
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if CommunityModel.find_by_id(community_id) is None:
            return {"message": "Community not found"}, 404
        if not AdministratorManageCommunityModel.user_is_admin_of_community(
            user_id, community_id=community_id
        ):
            return {"message": "You are not an admin of this community"}, 401

        return {
            "num_questions": QuestionModel.num_of_question_per_community(
                community_id=community_id
            )
        }
