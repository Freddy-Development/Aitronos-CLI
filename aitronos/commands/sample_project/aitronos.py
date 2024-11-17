import FreddyApi
from knowledge import Knowledge

class Aitronos:
    token: str
    freddy_api = FreddyApi.FreddyApi(
        token
    )
    def __init__(self, token: optional[str] = None):
        knowledge = Knowledge()

        if token is None:
            self.token = knowledge.user_token
