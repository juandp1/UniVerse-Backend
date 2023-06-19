from controllers.Label import (
    LabelList,
)

def add_resources(api):
    api.add_resource(LabelList, "/api/labels")