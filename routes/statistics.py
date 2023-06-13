from controllers.Statistics import (
    QuestionsPerCommunity,
    CommunitiesPerLabel
), NumberOfUsersPerCommunity
from controllers.Statistics import UsersPerCommunity
from controllers.Statistics import TopicsPerCommunity


def add_resources(api):
    api.add_resource(QuestionsPerCommunity, "/api/statistics/questions_per_comm")
    api.add_resource(CommunitiesPerLabel, "/api/statistics/communities_per_label")
    api.add_resource(NumberOfUsersPerCommunity, "/api/statistics/num_users_per_comm/")
    api.add_resource(TopicsPerCommunity, "/api/statistics/topics_per_comm/")
    api.add_resource(UsersPerCommunity, "/api/statistics/users_per_comm/")
