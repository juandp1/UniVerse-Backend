from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.question import QuestionModel
from models.community import CommunityModel
from models.administrator_manage_community import AdministratorManageCommunityModel
from models.label_has_community import LabelHasCommunityModel
from models.label import LabelModel


class QuestionsPerCommunity(Resource):
    @jwt_required()
    def get(self):
        return {
            "questions": [
                question.json()
                for question in QuestionModel.num_of_question_per_community()
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
                "communities" : LabelHasCommunityModel.num_of_communities_per_label(label.id)
            }
        return {"message": "That label doesn't exist"}, 400