from routes.user import add_resources as add_user_resources
from routes.auth import add_resources as add_auth_resources
from routes.community import add_resources as add_community_resources
from routes.meeting import add_resources as add_meeting_resources
from routes.questions import add_resources as add_questions_resources


def start_routes(api):
    add_auth_resources(api)
    add_user_resources(api)
    add_community_resources(api)
    add_meeting_resources(api)
    add_questions_resources(api)
