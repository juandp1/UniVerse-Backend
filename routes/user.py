# Import resources
from controllers.User import User
from controllers.User_Community import (
    UserEnterCommunity,
    UserLeaveCommunity,
    UserIsAdmin,
    UserIsMember,
)


# Add resources to the API
def add_resources(api):
    api.add_resource(User, "/api/user/<int:id>")
    api.add_resource(UserEnterCommunity, "/api/enter_community")
    api.add_resource(UserLeaveCommunity, "/api/leave_community")
    api.add_resource(UserIsAdmin, "/api/is_admin")
    api.add_resource(UserIsMember, "/api/is_member")
