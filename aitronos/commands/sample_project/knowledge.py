import json
import optional


class Knowledge:
    user_token: optional[str]

    def __init__(self):
        # all data will be extracted from the knowledge.json file
        self.data = self.get_data()

    def get_data(self):
        with open('knowledge.json', 'r') as file:
            data = json.load(file)
        return data