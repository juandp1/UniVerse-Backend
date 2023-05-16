# Import resources
from controllers.User import User
from controllers.User_Community import UserEnterCommunity, UserLeaveCommunity


# Add resources to the API
def add_resources(api):
    api.add_resource(User, "/api/user/<int:id>")
    api.add_resource(UserEnterCommunity, "/api/enter_community")
    api.add_resource(UserLeaveCommunity, "/api/leave_community")
