from controllers.Statistics import (
    QuestionsPerCommunity,
    CommunitiesPerLabel
)


def add_resources(api):
    api.add_resource(QuestionsPerCommunity, "/api/statistics/questions_per_comm")
    api.add_resource(CommunitiesPerLabel, "/api/statistics/communities_per_label")
