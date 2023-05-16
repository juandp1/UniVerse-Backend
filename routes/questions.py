from controllers.Forum import Questions, QuestionId, QuestionsByCommunityAndTopic


def add_resources(api):
    api.add_resource(Questions, "/api/questions")
    api.add_resource(QuestionId, "/api/question/<int:id_question>")
    api.add_resource(
        QuestionsByCommunityAndTopic,
        "/api/community/<int:community_id>/topic/<int:topic_id>/questions",
    )
