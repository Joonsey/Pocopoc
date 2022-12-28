import requests as re
import os.path

default = "http://helheim.online"

class Minecraftapi_adapter():
    def __init__(self, url: str) -> None:
        self.base_url = url

    def get_advancements(self, player: str=""):
        response = re.get(os.path.join(self.base_url, "advancements",player)) if player else re.get(os.path.join(self.base_url, "advancements"))
        try:
            return response.json()
        except:
            return False

    def get_stats(self, player: str=""):
        response = re.get(os.path.join(self.base_url, "stats",player)) if player else re.get(os.path.join(self.base_url, "stats"))
        try:
            return response.json()
        except:
            return False

if __name__ == "__main__":
    mc_api = Minecraftapi_adapter(default)
    #print(mc_api.get_advancements("joonsey"))
    #print(mc_api.get_stats("Joonsey"))
