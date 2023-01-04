from discord.ext import commands, tasks
import discord
from adapters.minecraft import Minecraft_Embed, Stats


class Minecraft(commands.Cog):
    def __init__(self, bot, mc_api) -> None:
        self.bot = bot
        self.mc_api = mc_api

    @commands.command()
    async def biggest_killer(self, ctx, particular_entity:str = ""):
        miners = {}
        response = ""
        data = self.mc_api.get_stats()
        if not data:
            return

        if not particular_entity:
            for player in data.keys():
                sum_of_mining = 0
                try:
                    all_things_mined = data[player]['stats']['minecraft:killed']
                    for thing in all_things_mined.keys():
                        sum_of_mining += all_things_mined[thing]
                except:
                    continue
                miners[player] = sum_of_mining

            sorted_miners = sorted(miners.items(), key = lambda x: x[1], reverse=True)
            n = 0
            for player in sorted_miners:
                n+=1
                response += f"#{n} {player[0]} with {player[1]} total kills\n"

        else:
            for player in data.keys():
                sum_of_mining = 0
                try:
                    all_things_mined = data[player]['stats']['minecraft:killed']
                    for thing in all_things_mined.keys():
                        if particular_entity in thing:
                            sum_of_mining += all_things_mined[thing]
                except:
                    continue
                miners[player] = sum_of_mining

            sorted_miners = sorted(miners.items(), key = lambda x: x[1], reverse=True)
            n = 0
            for player in sorted_miners:
                n+=1
                response += f"#{n} {player[0]} killed {particular_entity} {player[1]} times\n"

        await ctx.send(response)

    @commands.command()
    async def biggest_miner(self, ctx, particular_block:str = ""):
        miners = {}
        response = ""
        data = self.mc_api.get_stats()
        if not data:
            return

        if not particular_block:
            for player in data.keys():
                sum_of_mining = 0
                try:
                    all_things_mined = data[player]['stats']['minecraft:mined']
                    for thing in all_things_mined.keys():
                        sum_of_mining += all_things_mined[thing]
                except:
                    continue
                miners[player] = sum_of_mining

            sorted_miners = sorted(miners.items(), key = lambda x: x[1], reverse=True)
            n = 0
            for player in sorted_miners:
                n+=1
                response += f"#{n} {player[0]} with {player[1]} total blocks mined\n"

        else:
            for player in data.keys():
                sum_of_mining = 0
                try:
                    all_things_mined = data[player]['stats']['minecraft:mined']
                    for thing in all_things_mined.keys():
                        if particular_block in thing:
                            sum_of_mining += all_things_mined[thing]
                except:
                    continue
                miners[player] = sum_of_mining

            sorted_miners = sorted(miners.items(), key = lambda x: x[1], reverse=True)
            n = 0
            for player in sorted_miners:
                n+=1
                response += f"#{n} {player[0]} with {player[1]} total blocks of '{particular_block}' mined\n"

        await ctx.send(response)

    @commands.command()
    async def stats(self, ctx, player=""):
        response = ""
        if not player:
            response = "please provide a player name."
        else:
            stats = self.mc_api.get_stats(player)
            if not stats:
                response = "didn't find a player with that name."
            else:
                stats = stats['stats']
                for category in stats.keys():
                    response += f"**{category.replace('minecraft:', '')}:**\n"
                    for key in stats[category].keys():
                        value = stats[category][key]
                        response += f"{key.replace('minecraft:', '').replace('_', ' ')}: {value}\n"

        await ctx.send(response)

    @commands.command()
    async def summary(self, ctx, player=""):
        mcstats = Stats()
        if not player:
            await ctx.send("please provide a player.")
            return

        stats = self.mc_api.get_stats(player)
        if not stats:
            await ctx.send("player not found")
            return
        stats = stats['stats']
        for keys in stats.keys():
            if keys == 'minecraft:mined':
                mcstats.mined = stats[keys]
            if keys == 'minecraft:broken':
                mcstats.broken = stats[keys]
            if keys == 'minecraft:crafted':
                mcstats.crafted = stats[keys]
            if keys == 'minecraft:killed':
                mcstats.killed = stats[keys]
            if keys == 'minecraft:killed_by':
                mcstats.killed_by = stats[keys]
            if keys == 'minecraft:dropped':
                mcstats.dropped = stats[keys]
            if keys == 'minecraft:picked_up':
                mcstats.picked_up = stats[keys]
            if keys == 'minecraft:used':
                mcstats.used = stats[keys]
            if keys == 'minecraft:custom':
                mcstats.custom = stats[keys]

        embed = Minecraft_Embed()
        #embed.set_author(name=f"{player}")
        embed.title = f"summary for {player.lower().capitalize()}"
        embed.add_highest_mined_field(mcstats.highest_mined())
        embed.add_most_picked_up_field(mcstats.most_picked_up())
        embed.add_most_crafted_field(mcstats.most_crafted())
        embed.add_most_killed_field(mcstats.most_killed())
        await ctx.send(embed=embed)


    @commands.command()
    async def deaths(self, ctx, player: str = ""):
        if player == "":
            await ctx.send("give player name")
            return None
        
        data = self.mc_api.get_stats(player)
        if data == False:
            await ctx.send(f"couldn't find player with name '{player}'")
            return None
        stats = data["stats"]
        try:
            deathcount = stats["minecraft:custom"]["minecraft:deaths"]
        except KeyError:
            await ctx.send("player has not died yet!😁") 
            return None

        response = f"{player}: {deathcount} deaths" 
        await ctx.send(response)