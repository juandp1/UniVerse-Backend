# Import resources
from controllers.User import UserRegister, UserLogin


# Add resources to the API
def add_resources(api):
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserRegister, "/register")
