from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.community import CommunityModel
from models.question import QuestionModel
from models.response import ResponseModel
from models.topic import TopicModel
from models.user_belongs_to_community import UserBelongsToCommunityModel
from models.user import UserModel
from models.response import ResponseModel


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

        questions = [
            question.json()
            for question in QuestionModel.find_by_community_and_topic(
                community_id, topic_id
            )
        ]

        if questions is None:
            return {"message": "Questions not found"}, 404

        QuestionModel.change_user_id_for_user_name(questions)

        return {"questions": questions}, 200


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
        for question in questions:
            QuestionModel.change_user_id_for_user_name(question)
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
    def get(self, community_id):
        question = QuestionModel.find_more_recent(community_id)
        if question is None:
            return {"message": "Question not found"}, 404

        return question.json(), 200


class QuestionVoted(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "vote_type", type=str, required=False, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self, id_question):
        data = QuestionVoted.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        question = QuestionModel.find_by_id(id_question)

        if question is None:
            return {"message": "Question not found"}, 404

        if question.user_id == user_id:
            return {"message": "You cannot vote on your own question"}, 400

        if data["vote_type"] == "1":
            question.update_score(1)
        elif data["vote_type"] == "-1":
            question.update_score(-1)
        else:
            return {"message": "Invalid vote type"}, 400

        try:
            question.save_to_db()
            return question.json(), 200
        except:
            return {"message": "An error occurred while voting on the question"}, 500


class MostVotedQuestion(Resource):
    @jwt_required()
    def get(self, community_id):
        responses = ResponseModel.find_more_voted()
        if responses is None:
            return {"message": "Question not found"}, 404

        for response in responses:
            question = QuestionModel.find_by_id(response.question_id)
            if question.community_id == community_id:
                return response.json(), 200
        return {}, 200


class ResponseVoted(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "vote_type", type=str, required=False, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self, id_response):
        data = ResponseVoted.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        response = ResponseModel.find_by_id(id_response)

        if response is None:
            return {"message": "Response not found"}, 404

        if response.user_id == user_id:
            return {"message": "You cannot vote on your own response"}, 400

        if data["vote_type"] == "1":
            response.update_score(1)
        elif data["vote_type"] == "-1":
            response.update_score(-1)
        else:
            return {"message": "Invalid vote type"}, 400

        try:
            response.save_to_db()
            return response.json(), 200
        except:
            return {"message": "An error occurred while voting on the response"}, 500


class MostVotedResponse(Resource):
    @jwt_required()
    def get(self):
        response = ResponseModel.find_more_voted()
        if response is None:
            return {"message": "Response not found"}, 404

        return response.json(), 200


class Responses(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "description", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "question_id", type=int, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def get(self):
        responses = ResponseModel.find_all()
        return {"responses": [response.json() for response in responses]}, 200

    @jwt_required()
    def post(self):
        data = Responses.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if not QuestionModel.find_by_id(data["question_id"]):
            return {"message": "Question not found"}, 404

        response = ResponseModel(**data, user_id=user_id)

        try:
            response.save_to_db()
            return response.json(), 201
        except:
            return {"message": "An error occurred creating the response."}, 500


class ResponseNumResponse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "description", type=str, required=False, help="This field cannot be blank."
    )

    @jwt_required()
    def put(self, response_num):
        data = ResponseNumResponse.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        response = ResponseModel.find_by_num_response(response_num)

        if response is None:
            return {"message": "Response not found"}, 404

        if response.user_id != user_id:
            return {"message": "Response not found"}, 404

        if data["description"]:
            response.description = data["description"]

        try:
            response.save_to_db()
            return response.json(), 200
        except:
            return {"message": "An error occurred updating the response."}, 500

    @jwt_required()
    def delete(self, response_num):
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        response = ResponseModel.find_by_num_response(response_num)

        if response is None:
            return {"message": "Response not found"}, 404

        if response.user_id != user_id:
            return {"message": "Response not found"}, 404

        try:
            response.delete_from_db()
            return {"message": "Response deleted"}, 200
        except:
            return {"message": "An error occurred deleting the response."}, 500


class ResponseListByQuestion(Resource):
    @jwt_required()
    def get(self, question_id):
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if not QuestionModel.find_by_id(question_id):
            return {"message": "Question not found"}, 404
        if not UserModel.find_by_id(user_id):
            return {"message": "User not found"}, 404

        responses = ResponseModel.find_by_question(question_id)
        if responses is None:
            return {"message": "Responses not found"}, 404

        return {"responses": [response.json() for response in responses]}, 200
