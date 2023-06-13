from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.question import QuestionModel
from models.community import CommunityModel
from models.label import LabelModel
from models.label_has_community import LabelHasCommunityModel
from models.user_belongs_to_community import UserBelongsToCommunityModel


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
        communities = [
            community.json()
            for community in CommunityModel.query.filter_by(is_active=True).all()
        ]
        num_users_per_community = {}
        for each in communities:
            id_com = each["id"]
            name_com = each["name"]
            num_users_per_community[name_com] = CommunityModel.number_of_users(id_com)
        return num_users_per_community


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
        return {
            "users_belongs_to_community": [
                user_belongs_to_community.json()
                for user_belongs_to_community in UserBelongsToCommunityModel.num_of_users_per_community()
            ]
        }


class TopicsPerCommunity(Resource):
    @jwt_required
    def get(self):
        return {
            "topics_per_community": [
                topics_per_community.json()
                for topics_per_community in QuestionModel.num_of_topics_per_community()
            ]
        }


class CommunitiesPerLabel(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "label", type=str, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def get(self):
        data = CommunitiesPerLabel.parser.parse_args()
        label = LabelModel.find_by_name(data["label"])
        if label:
            return {
                "communities": LabelHasCommunityModel.num_of_communities_per_label(
                    label.id
                )
            }
        return {"message": "That label doesn't exist"}, 400
