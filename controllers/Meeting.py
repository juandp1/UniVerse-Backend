from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.community import CommunityModel
from models.meeting import MeetingModel
from datetime import datetime


class MeetingsList(Resource):
    @jwt_required()
    def get(self):
        meetings = MeetingModel.query.filter_by(is_active=True).all()

        if meetings:
            return {"meetings": [meeting.json() for meeting in meetings]}, 200
        return {"message": "Meeting not found"}, 404


class MeetingCommunity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "description", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "place", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "date", type=str, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def get(self, comm_id):
        meetings = MeetingModel.query.filter_by(
            community_id=comm_id, is_active=True
        ).all()

        if meetings:
            return {"meetings": [meeting.json() for meeting in meetings]}, 200
        return {"message": "Meeting not found"}, 404

    @jwt_required()
    def post(self, comm_id):
        data = MeetingCommunity.parser.parse_args()
        current_user = get_jwt_identity()
        meeting = MeetingModel(**data, community_id=comm_id, user_id=current_user["id"])

        if not CommunityModel.find_by_id(comm_id):
            return {"message": "Community not found"}, 404
        if datetime.strptime(data["date"], "%Y-%M-%D %H:%M:%S.%f") < datetime.now():
            return {"message": "Invalid date"}, 400

        try:
            meeting.save_to_db()
            return meeting.json(), 201
        except Exception as e:
            print(e)
            return {"message": "An error occurred creating the meeting"}, 500


class NextMeeting(Resource):
    @jwt_required()
    def get(self, comm_id):
        if not CommunityModel.find_by_id(comm_id):
            return {"message": "Community not found"}, 404

        meeting = MeetingModel.next_meeting_of_community(comm_id)
        if meeting is None:
            return {"message": "Meeting not found"}, 404
        return meeting.json(), 200


class MeetingId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "description", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "place", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "date", type=str, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        meeting = MeetingModel.find_by_id(id)

        if meeting is None:
            return {"message": "Meeting not found"}, 404
        if current_user["id"] != meeting.user_id:
            return {"message": "Not found"}, 404

        try:
            meeting.delete_from_db()
            return {"message": "Meeting deleted"}, 200
        except:
            return {"message": "An error occurred deleting the meeting."}, 500

    @jwt_required()
    def put(self, id):
        data = MeetingId.parser.parse_args()
        current_user = get_jwt_identity()
        meeting = MeetingModel.find_by_id(id)

        if meeting is None:
            return {"message": "Meeting not found"}, 404
        if current_user["id"] != meeting.user_id:
            return {"message": "Not found"}, 404

        meeting.name = data["name"]
        meeting.description = data["description"]
        meeting.place = data["place"]
        meeting.date = data["date"]

        try:
            meeting.save_to_db()
            return meeting.json(), 200
        except:
            return {"message": "An error occurred updating the meeting."}, 500


class SearchMeetingDate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "initial_date", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "final_date", type=str, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self, comm_id):
        data = SearchMeetingDate.parser.parse_args()
        return {
            "meetings": [
                meeting.json()
                for meeting in MeetingModel.find_by_dates(
                    comm_id, data["initial_date"], data["final_date"]
                )
            ]
        }, 200
