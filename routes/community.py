# Import resources
from controllers.Community import (
    CommunityId,
    CommunityName,
    CommunityList,
    CreateCommunity,
)


# Add resources to the API
def add_resources(api):
    api.add_resource(CommunityList, "/api/communities")
    api.add_resource(CommunityId, "/api/community/id/<int:id>")
    api.add_resource(CommunityName, "/api/community/name/<string:name>")
    api.add_resource(CreateCommunity, "/api/community")
