from controllers.Forum import (
    ResponseVoted,
    MostVotedResponse,
)


def add_resources(api):
    api.add_resource(ResponseVoted, "/api/questions/<int:id_response>")
    api.add_resource(MostVotedResponse, "/api/questions/voted_response")
