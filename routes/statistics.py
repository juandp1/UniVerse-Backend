from controllers.Statistics import (
    QuestionsPerCommunity,
    NumberOfUsersPerCommunity,
    CommunitiesPerLabel,
    TopicsPerCommunity,
    NumUserPerCommunityId,
)


def add_resources(api):
    api.add_resource(QuestionsPerCommunity, "/api/statistics/questions_per_comm")
    api.add_resource(CommunitiesPerLabel, "/api/statistics/communities_per_label")
    api.add_resource(NumberOfUsersPerCommunity, "/api/statistics/num_users_per_comm/")
    api.add_resource(TopicsPerCommunity, "/api/statistics/topics_per_comm/")
    api.add_resource(
        NumUserPerCommunityId, "/api/statistics/users_per_comm/<int:community_id>"
    )
