# Import resources
from controllers.User import UserRegister, UserLogin, UserLogout, User2FA, ChangePassword


# Add resources to the API
def add_resources(api):
    api.add_resource(UserLogin, "/api/login")
    api.add_resource(UserRegister, "/api/register")
    api.add_resource(User2FA, "/api/2fa")
    api.add_resource(UserLogout, "/api/logout")
    api.add_resource(ChangePassword, "/api/changepwd")
