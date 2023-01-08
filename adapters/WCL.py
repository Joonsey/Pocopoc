import requests, os

token_url = "https://www.warcraftlogs.com/oauth/token"

class WCL_adapter():
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.token_url = token_url
        self.token = self.get_token(client_id, client_secret)

    def get_token(self, client_id, client_secret):
        data = {'grant_type':'client_credentials'}
        auth = (client_id, client_secret)
        with requests.session() as session:
            response = session.post(self.token_url, data=data, auth=auth)
        return response

