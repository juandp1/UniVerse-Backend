from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.topic import TopicModel
from models.administrator import AdministratorModel


class TopicList(Resource):
    @jwt_required()
    def get(self):
        topics = TopicModel.query.filter_by(is_active=True).all()

        if topics:
            return {"topics": [topic.json() for topic in topics]}, 200
        return {"message": "Topic not found"}, 404


class TopicId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def get(self, topic_id):
        topic = TopicModel.find_by_id(topic_id)

        if topic:
            return topic.json(), 200
        return {"message": "Topic not found"}, 404

    @jwt_required()
    def delete(self, topic_id):
        topic = TopicModel.find_by_id(topic_id)

        if topic:
            topic.delete_from_db()
            return {"message": "Topic deleted."}, 200
        return {"message": "Topic not found."}, 404

    @jwt_required()
    def put(self, topic_id):
        data = TopicId.parser.parse_args()
        topic = TopicModel.find_by_id(topic_id)

        if topic:
            topic.name = data["name"]
            try:
                topic.save_to_db()
                return topic.json(), 200
            except:
                return {"message": "An error occurred updating the topic."}, 500
        return {"message": "Topic not found."}, 404


class TopicName(Resource):
    @jwt_required()
    def get(self, name):
        topic = TopicModel.find_by_name(name)

        if topic:
            return topic.json(), 200
        return {"message": "Topic not found"}, 404


class Topic(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self):
        data = Topic.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if AdministratorModel.find_by_id(user_id):
            if TopicModel.find_by_name(data["name"]):
                return {"message": "Topic already exists"}, 400

            topic = TopicModel(**data)

            try:
                topic.save_to_db()
                return topic.json(), 201
            except:
                return {"message": "An error occurred creating the topic."}, 500
