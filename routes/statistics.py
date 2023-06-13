from controllers.Statistics import QuestionsPerCommunity, NumberOfUsersPerCommunity


def add_resources(api):
    api.add_resource(QuestionsPerCommunity, "/api/statistics/questions_per_comm/")
    api.add_resource(NumberOfUsersPerCommunity, "/api/statistics/num_users_per_comm/")
