import requests, os, json
from dataclasses import dataclass


@dataclass
class Ranking():
    role : str
    name : str
    spec : str
    amount : float
    bracketData : int
    rank : str
    best : str
    totalParses : int
    bracketPercent : int
    rankPercent : int

@dataclass
class Fight():
    id: int
    difficulty: int
    name : str
    startTime : float
    endTime : float
    fightPercentage : float
    lastPhase : int
    size : int
    kill : int
    rankings : list[Ranking]

    def __str__(self):
        return f"fighting {self.name}, ending at {self.fightPercentage} with {self.size} people"

@dataclass
class Report():
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


    def get_guildrank(self, id, zoneId=14030):
        query = """query($id:Int, $zoneId:Int) { 
            guildData {
                guild(id:$id) {
                    zoneRanking(zoneId:$zoneId) {
                        progress(size:20) {
                            worldRank
                            {
                                number
                                percentile
                                color
                            }
                            regionRank
                            {
                                number
                                percentile
                                color
                            }
                            serverRank
                            {
                                number
                                percentile
                                color
                            }
                        }
                    }
                }
            }
        }
        """
        response = self.get_data(query, id = int(id), zoneId = zoneId)
        return response


    def get_report(self, code: str, byBracket: bool = False) -> Report:
        query = """query($code:String) { 
            reportData{
                report(code:$code){
                    rankings
                    startTime
                    fights(killType:Encounters){
                        id
                        difficulty
                        name
                        startTime
                        endTime
                        fightPercentage
                        lastPhase
                        size
                        kill
                    }
                }
            }
        }
        """
        response = self.get_data(query, code = code, byBracket = byBracket)
        data = response["data"]["reportData"]
        fightData = response["data"]["reportData"]['report']['fights']
        rankingData = data["report"]["rankings"]["data"]

        fights = []
        for fight in fightData :
            fights.append(Fight(
                fight['id'],
                fight['difficulty'],
                fight['name'],
                fight['startTime'],
                fight['endTime'],
                fight['fightPercentage'],
                fight['lastPhase'],
                fight['size'],
                fight['kill'],
                rankings = []
            ))


        for ranking in rankingData:
            new_rankings = []
            for role in ranking['roles']:
                for character in ranking['roles'][role]["characters"]:
                    new_rankings.append(Ranking(
                        role,
                        character['name'],
                        character['spec'],
                        character['amount'],
                        character['bracketData'],
                        character['rank'],
                        character['best'],
                        character['totalParses'],
                        character['bracketPercent'],
                        character['rankPercent']
                    ))
            fight_id = ranking['fightID']
            fight = next(fight for fight in fights if fight.id == fight_id)
            fight.rankings = new_rankings

        return Report(data['report']['startTime'], fights)