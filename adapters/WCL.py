import requests, os, json
from dataclasses import dataclass

@dataclass
class Fight(object):
    id: int
    name : str
    startTime : float
    endTime : float
    fightPercentage : float
    lastPhase : int
    size : int

    def __str__(self):
        return f"fighting {self.name}, ending at {self.fightPercentage} with {self.size} people"

@dataclass
class Report(object):
    startTime : float
    fights : list[Fight]
    
    def __str__(self):
        return "\n".join(str(x) for x in self.fights)

token_url = "https://www.warcraftlogs.com/oauth/token"
api_url = "https://www.warcraftlogs.com/api/v2/client"
private_api_url = "https://www.warcraftlogs.com/api/v2/user"
class WCL_adapter():
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.token_url = token_url
        self.response = self.get_token(client_id, client_secret)
        self.token = self.response.get("access_token") if self.response != None else None

    def get_data(self, query: str, **kwargs):
        data = {"query": query, "variables": kwargs}
        with requests.session() as session:
            session.headers = self.retrieve_headers()
            response = session.get(api_url, json=data)
            return response.json()

    def get_token(self, client_id, client_secret):
        """recieves token from warcraftlogs"""
        data = {'grant_type':'client_credentials'}
        auth = (client_id, client_secret)
        with requests.session() as session:
            response = session.post(self.token_url, data=data, auth=auth)
        return response.json()

    def store_credentials(self):
        """stores token to local file"""
        try:
            with open(".credentials.json", "w+", encoding = "utf-8") as f:
                json.dump(self.resposne.json(), f)
        except OSError as e:
            print(e)
            return None

    def read_token(self):
        """reads token from locally stored file"""
        try:
            with open(".credentials.json", "r+", encoding = "utf-8") as f:
                access_token = json.load(f)
                return access_token.get("access_token")
        except OSError as e:
            print(e)
            return None

    def retrieve_headers(self):
        return {"Authorization" : f"Bearer {self.token}"}


    def get_report(self, code: str) -> Report:
        query = """query($code:String) { 
            reportData{
                report(code:$code){
                    startTime
                    fights(killType:Encounters){
                        id
                        name
                        startTime
                        endTime
                        fightPercentage
                        lastPhase
                        size
                    }
                }
            }
        }
        """
        response = self.get_data(query, code = code)
        data = response["data"]["reportData"]
        fightData = response["data"]["reportData"]['report']['fights']
        fights = []
        for fight in fightData :
            fights.append(Fight(
                fight['id'],
                fight['name'],
                fight['startTime'],
                fight['endTime'],
                fight['fightPercentage'],
                fight['lastPhase'],
                fight['size']
            ))
        report = Report(data['report']['startTime'], fights)
        
        return report