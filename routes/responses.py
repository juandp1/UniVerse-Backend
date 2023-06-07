from controllers.Forum import (
Responses,
ResponseNumResponse,
ResponseListByQuestion
)

def add_resources(api):
    api.add_resource(Responses, "/api/responses")
    api.add_resource(ResponseNumResponse, "/api/response/<int:response_num>")
    api.add_resource(ResponseListByQuestion, "/api/question/<int:question_id>/responses")
