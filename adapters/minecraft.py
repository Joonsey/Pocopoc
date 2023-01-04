import requests as re
import discord
import os.path

DEFAULT_LENGTH = 10
default = "http://helheim.online"

def sort(data: dict):
    return sorted(data.items(), key = lambda x: x[1], reverse=True)

def format_key(key: str):
    if "minecraft:" in key:
        return key.replace("minecraft:","").replace("_", " ")

def trunc_list(input_list: list[tuple], size : int):
    if len(input_list) > size :
        return input_list[:10]
    return input_list

class Minecraft_Embed(discord.Embed):
    def __init__(self):
        super().__init__()

    def add_highest_mined_field(self, blocks: list[tuple]):
        if not blocks:
            return
        blocks = trunc_list(blocks, DEFAULT_LENGTH)
        value = "\n".join([f"{format_key(block[0])} mined {block[1]} times!" for block in blocks])
        self.add_field(
            name="mined",
            value= value
        )

    def add_most_picked_up_field(self, items: list[tuple]):
        if not items:
            return
        items = trunc_list(items, DEFAULT_LENGTH)
        value = "\n".join([f"{format_key(item[0])} picked up {item[1]} times!" for item in items])
        self.add_field(
            name="picked up",
            value=value
        )

    def add_most_crafted_field(self, items: list[tuple]):
        if not items:
            return
        items = trunc_list(items, DEFAULT_LENGTH)
        value = "\n".join([f"{format_key(item[0])} crafted {item[1]} times!" for item in items])
        self.add_field(
            name="crafts",
            value=value
        )

    def add_most_killed_field(self, entities: list[tuple]):
        if not entities:
            return
        entities = trunc_list(entities, DEFAULT_LENGTH)
        value = "\n".join([f"{format_key(entity[0])} killed {entity[1]} times!" for entity in entities])
        self.add_field(
            name="kills",
            value=value
        )

class Stats():
    def __init__(self) -> None:
        self.mined: dict = {}
        self.broken : dict = {}
        self.crafted : dict = {}
        self.killed : dict = {}
        self.killed_by : dict = {}
        self.dropped  : dict = {}
        self.picked_up : dict = {}
        self.used : dict = {}
        self.custom : dict = {}

    def most_crafted(self):
        if not self.crafted:
            return 0, 0
        return sort(self.crafted)

    def most_killed(self):
        if not self.killed:
            return 0, 0
        return sort(self.killed)

    def highest_mined(self):
        if not self.mined:
            return 0, 0
        return sort(self.mined)

    def most_picked_up(self):
        if not self.picked_up:
            return 0, 0
        return sort(self.picked_up)

class Minecraftapi_adapter():
    def __init__(self, url: str) -> None:
        self.base_url = url

    def get_advancements(self, player: str=""):
        #response = re.get(os.path.join(self.base_url, "advancements",player)) if player else re.get(os.path.join(self.base_url, "advancements"))
        response = f"{self.base_url}/stats/{player}" if player else f"{self.base_url}/stats"
        try:
            return response.json()
        except:
            return False

    def get_stats(self, player: str=""):
        #response = re.get(os.path.join(self.base_url, "stats",player)) if player else re.get(os.path.join(self.base_url, "stats"))
        response = re.get(f"{self.base_url}/stats/{player}" if player else f"{self.base_url}/stats")
        try:
            return response.json()
        except:
            return False

if __name__ == "__main__":
    mc_api = Minecraftapi_adapter(default)
    #print(mc_api.get_advancements("joonsey"))
    #print(mc_api.get_stats("Joonsey"))
