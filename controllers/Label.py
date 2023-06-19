from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.label import LabelModel


class LabelList(Resource):
    def get(self):
        labels_res = LabelModel.find_all()
        return {"labels": [label.json() for label in labels_res]}, 200
