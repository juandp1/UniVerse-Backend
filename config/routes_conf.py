from routes.auth import add_resources as add_auth_resources
from routes.community import add_resources as add_community_resources
from routes.encyclopedia import add_resources as add_encyclopedia_resources
from routes.label import add_resources as add_label_resources
from routes.meeting import add_resources as add_meeting_resources
from routes.questions import add_resources as add_questions_resources
from routes.responses import add_resources as add_responses_resources
from routes.statistics import add_resources as add_statistics_resources
from routes.topic import add_resources as add_topic_resources
from routes.user import add_resources as add_user_resources


def start_routes(api):
    add_auth_resources(api)
    add_community_resources(api)
    add_encyclopedia_resources(api)
    add_label_resources(api)
    add_meeting_resources(api)
    add_questions_resources(api)
    add_responses_resources(api)
    add_statistics_resources(api)
    add_topic_resources(api)
    add_user_resources(api)
