# Import resources
from controllers.Community import CommunityId, CommunityName, CommunityList


# Add resources to the API
def add_resources(api):
    api.add_resource(CommunityList, "/communities")
    api.add_resource(CommunityId, "/community/id/<int:id>")
    api.add_resource(CommunityName, "/community/name/<string:name>")
