from flask_restful import Resource, reqparse
from models.label import LabelModel


class LabelList(Resource):
    def get(self):
        labels = LabelModel.query.filter_by(is_active=True).all()

        if labels:
            return {"labels": [label.json() for label in labels]}, 200
        return {"message": "Labels not found"}, 404