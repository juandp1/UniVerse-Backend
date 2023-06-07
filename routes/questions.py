from controllers.Forum import (
    Questions,
    QuestionId,
    QuestionsByCommunityAndTopic,
    QuestionListByCommunity,
    QuestionListByTopic,
    MostRecentQuestion,
    QuestionVoted,
    MostVotedQuestion,
)


def add_resources(api):
    api.add_resource(Questions, "/api/questions")
    api.add_resource(QuestionId, "/api/question/<int:id_question>")
    api.add_resource(
        QuestionsByCommunityAndTopic,
        "/api/community/<int:community_id>/topic/<int:topic_id>/questions",
    )
    api.add_resource(
        QuestionListByCommunity, "/api/community/<int:community_id>/questions"
    )
    api.add_resource(QuestionListByTopic, "/api/questions/topic/<int:topic_id>")
    api.add_resource(MostRecentQuestion, "/api/questions/recent_question")
    api.add_resource(QuestionVoted, "/api/questions/<int:id_question>")
    api.add_resource(MostVotedQuestion, "/api/questions/voted_quesiton")
