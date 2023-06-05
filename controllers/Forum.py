from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.community import CommunityModel
from models.question import QuestionModel
from models.topic import TopicModel
from models.user_belongs_to_community import UserBelongsToCommunityModel
from models.user import UserModel


class Questions(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "title", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "description", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "topic_id", type=int, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "community_id", type=int, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def get(self):
        questions = QuestionModel.find_all()
        return {"questions": [question.json() for question in questions]}, 200

    @jwt_required()
    def post(self):
        data = Questions.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if not TopicModel.find_by_id(data["topic_id"]):
            return {"message": "Topic not found"}, 404

        if not CommunityModel.find_by_id(data["community_id"]):
            return {"message": "Community not found"}, 404

        question = QuestionModel(**data, user_id=user_id)

        try:
            question.save_to_db()
            return question.json(), 201
        except:
            return {"message": "An error occurred creating the question."}, 500


class QuestionId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "title", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "description", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "topic_id", type=int, required=False, help="This field cannot be blank."
    )

    @jwt_required()
    def put(self, id_question):
        data = QuestionId.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        question = QuestionModel.find_by_id(id_question)

        if question is None:
            return {"message": "Question not found"}, 404

        if question.user_id != user_id:
            return {"message": "Question not found"}, 404

        if data["title"]:
            question.title = data["title"]
        if data["description"]:
            question.description = data["description"]
        if data["topic_id"]:
            question.topic_id = data["topic_id"]

        try:
            question.save_to_db()
            return question.json(), 200
        except:
            return {"message": "An error occurred updating the question."}, 500

    @jwt_required()
    def delete(self, id_question):
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        question = QuestionModel.find_by_id(id_question)

        if question is None:
            return {"message": "Question not found"}, 404

        if question.user_id != user_id:
            return {"message": "Question not found"}, 404

        try:
            question.delete_from_db()
            return {"message": "Question deleted"}, 200
        except:
            return {"message": "An error occurred deleting the question."}, 500


class QuestionsByCommunityAndTopic(Resource):
    @jwt_required()
    def get(self, community_id, topic_id):
        if not TopicModel.find_by_id(topic_id):
            return {"message": "Topic not found"}, 404

        if not CommunityModel.find_by_id(community_id):
            return {"message": "Community not found"}, 404

        questions = QuestionModel.find_by_community_and_topic(community_id, topic_id)

        if questions is None:
            return {"message": "Questions not found"}, 404

        return {"questions": [question.json() for question in questions]}, 200


class QuestionListByCommunity(Resource):
    @jwt_required()
    def get(self, community_id):
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if not CommunityModel.find_by_id(community_id):
            return {"message": "Community not found"}, 404
        if not UserBelongsToCommunityModel.find_by_user_id_and_community_id(
            user_id, community_id
        ):
            return {"message": "User not found in community"}, 404

        questions = QuestionModel.find_by_community(community_id)
        if questions is None:
            return {"message": "Questions not found"}, 404

        return {"questions": [question.json() for question in questions]}, 200


class QuestionListByTopic(Resource):
    @jwt_required()
    def get(self, topic_id):
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if not TopicModel.find_by_id(topic_id):
            return {"message": "Topic not found"}, 404
        if not UserModel.find_by_id(user_id):
            return {"message": "User not found"}, 404

        questions = QuestionModel.find_by_topic(topic_id)
        if questions is None:
            return {"message": "Questions not found"}, 404

        return {"questions": [question.json() for question in questions]}, 200


class MostRecentQuestion(Resource):
    @jwt_required()
    def get(self):
        question = QuestionModel.find_more_recent()
        if question is None:
            return {"message": "Question not found"}, 404

        return question.json(), 200