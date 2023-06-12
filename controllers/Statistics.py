from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.question import QuestionModel
from models.community import CommunityModel
from models.user_belongs_to_community import UserBelongsToCommunityModel
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

class UsersPerCommunity(Resource):
    @jwt_required()
    def get(self):
        return{
            "users_belongs_to_community": [
                user_belongs_to_community.json()
                for user_belongs_to_community in UserBelongsToCommunityModel.num_of_users_per_community()
            ]
        }
    
class TopicsPerCommunity(Resource):
    @jwt_required
    def get(self):
        return{
            "topics_per_community": [
                topics_per_community.json()
                for topics_per_community in QuestionModel.num_of_topics_per_community()
            ]
        }