from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.label import LabelModel


class LabelList(Resource):
    @jwt_required
    def get(self):
        labels = LabelModel.find_all()
        return {"labels": [label.json() for label in labels]}, 200
