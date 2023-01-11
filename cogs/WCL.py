from discord.ext import commands
from enum import Enum
import discord

class WCL(commands.Cog):
    def __init__(self, bot, wcl_adapter) -> None:
        self.bot = bot
        self.adapter = wcl_adapter

    #@commands.command()
    #async def something(self, ctx, id):
        #response = self.adapter.get_guildrank(id, zoneId=14030)
        #print(response)
        #await ctx.send(response)

    @commands.command()
    async def report(self, ctx, code, person: str):

        difficulty: list[str]= [
            "",
            "",
            "lfr",
            "normal",
            "heroic",
            "mythic",
        ]

        report = self.adapter.get_report(code)
        response = ""

        for fight in report.fights:
            for character in fight.rankings:
                if (character.name.lower() == person.lower()) and fight.kill:
                    response += str(character.rankPercent) + f" on {fight.name} {difficulty[fight.difficulty].capitalize()}\n"

        if not response:
            response = "could not find that player."

        await ctx.send(response)


    @commands.command()
    async def thing(self, ctx, guildId: str):
        #codes: list[str] = self.adapter.get_all_guild_reportcodes(int(guildId))
        #reports = [self.adapter.get_report(code) for code in codes]
        reports = self.adapter.get_all_guild_reports(guildId)
        print(reports[0].deaths)
        
    @commands.command()
    async def deathers(self, ctx, code, person: str = ""):
        response=""
        report = self.adapter.get_report(code)

        for fight in report.fights:
            if not fight.kill:
                continue
            for deaths in fight.deaths:
                response += f"{deaths.name} died on {fight.name}\n"

        await ctx.send(response)