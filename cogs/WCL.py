from discord.ext import commands
import discord

class WCL(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def something(self, ctx):
        await ctx.send("something")
