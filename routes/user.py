# Import resources
from controllers.User import User


# Add resources to the API
def add_resources(api):
    api.add_resource(User, "/api/user/<int:id>")
