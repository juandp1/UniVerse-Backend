from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.question import QuestionModel
from models.community import CommunityModel
from models.administrator_manage_community import AdministratorManageCommunityModel


class QuestionsPerCommunity(Resource):
    @jwt_required()
    def get(self):
        return {
            "questions": [
                question.json()
                for question in QuestionModel.num_of_question_per_community()
            ]
        }
class NumberOfUsersPerCommunity(Resource):
    @jwt_required()
    def get(self):
        communities =  [
                community.json()
                for community in CommunityModel.query.filter_by(is_active=True).all()
            ]
        num_users_per_community = {}
        for each in communities:
            id_com = each["id"]
            name_com = each["name"]
            num_users_per_community[name_com] = CommunityModel.number_of_users(id_com)
        return num_users_per_community
