import FreddyApi
from knowledge import Knowledge

class Aitronos:
    token: str
    freddy_api = FreddyApi.FreddyApi(
        token
    )

    def __init__(self):
        knowledge = Knowledge()
        self.token = knowledge.user_token
