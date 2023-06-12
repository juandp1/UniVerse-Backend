from controllers.Statistics import QuestionsPerCommunity


def add_resources(api):
    api.add_resource(QuestionsPerCommunity, "/api/statistics/questions_per_comm/")
