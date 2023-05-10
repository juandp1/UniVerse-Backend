from routes.user import add_resources as add_user_resources
from routes.auth import add_resources as add_auth_resources
from routes.community import add_resources as add_community_resources


def start_routes(api):
    add_auth_resources(api)
    add_user_resources(api)
    add_community_resources(api)
