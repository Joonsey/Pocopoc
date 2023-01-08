from discord.ext import commands
import discord

class WCL(commands.Cog):
    def __init__(self, bot, wcl_adapter) -> None:
        self.bot = bot
        self.adapter = wcl_adapter

    @commands.command()
    async def something(self, ctx):
        await ctx.send("something")


