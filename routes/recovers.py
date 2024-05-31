# Import resources
from controllers.Recovers import SendRecoverEmail, Recover2FA, VerifyRecoveryCode


# Add resources to the API
def add_resources(api):
    api.add_resource(SendRecoverEmail, "/api/sendemail")
    api.add_resource(Recover2FA, "/api/recover2fa")
    api.add_resource(VerifyRecoveryCode, "/api/verifycode")
