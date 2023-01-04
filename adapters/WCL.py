import requests, os

class Minecraftapi_adapter():
    def __init__(self, url: str, client_id: str, client_secret: str) -> None:
        self.base_url = url
        self.token = self.get_token(client_id, client_secret)

    def get_token(self, client_id, client_secret):
        return

