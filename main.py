import random, discord, asyncio, os
from adapters.minecraft import Minecraftapi_adapter, Stats, Minecraft_Embed
from discord.ext import commands, tasks
from secret import TOKEN
from itertools import cycle
from settings import *

#ADAPTERS
mc_api = Minecraftapi_adapter(MINECRAFT_API_PATH)


#DISCORD INITIALIZATION
intents = discord.Intents().all()
client = commands.Bot(command_prefix='.', intents=intents)
status = cycle(["Killing Jaeler", 'Falling down holes','Enchanting weapon', 'Missing tyrant ramp'])

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def change_prefix(ctx, pref):
    """
    changes the expected prefix for the bot, 
    this can now be changed to ANY combination of characters. This is retarded.
    Just don't abuse it please.
    """
    if 'officer' in [c.name.lower() for c in ctx.author.roles]:
        client.command_prefix = pref
        await ctx.reply(f'command prefix changed to {pref}')



@client.event
async def on_ready():
    await client.add_cog(Minecraft(client))
    change_status.start()
    print('Logged in as', client.user.name)

@client.command()
async def move(ctx, _from, to ):
    if 'officer' in [c.name.lower() for c in ctx.author.roles]:
        members = []
        prev_channel, target_voice_chat = ""
        for channel in ctx.guild.voice_channels:
            if _from in channel.name.lower():
                prev_channel = _from
                for member in channel.members:
                    members.append(member)

        for channel in ctx.guild.voice_channels:
            if to in channel.name.lower():
                target_voice_chat = channel

        for member in members:
            print(f"Moving {member} from {prev_channel} to {target_voice_chat}")
            await member.move_to(target_voice_chat)



@client.command(aliases=["officerchat"])
async def officer_chat_move(ctx):
    if 'officer' in [c.name.lower() for c in ctx.author.roles]:
        members = []
        target_voice_chat = 0

        """ Adds all members from specific channels to a list"""
        for channel in ctx.guild.channels:
            if channel.id == OFFICER_TEXT_CHAT: # officer text chat id
                for m in channel.members:
                    if m.voice is not None:
                        members.append(m)

        """ Determines the target voice channel to move all members to """
        for channel in ctx.guild.voice_channels:
            if channel.id == OFFICER_VOICE_CHAT: # target officer voice chat
                target_voice_chat = channel
                break
            else:
                target_voice_chat = ctx.guild.voice_channels[0]

        """ Moving all members to target channel """
        for member in members:
            if member not in target_voice_chat.members:
                print(f"Moving {member} to {target_voice_chat}")
                await member.move_to(target_voice_chat, reason="Raid time!")
    else:
        await ctx.send('Nice try, fool.')
        await ctx.message.delete()

@client.command(aliases=['raidtime'])
async def raid_time(ctx):
    target_voice_chat = ""
    print('Task recieved')
    """ An officer can call this command to move all active voice raid members to raid chat """
    if 'officer' in [c.name.lower() for c in ctx.author.roles]:
        members = []

        """ Adds all members from specific channels to a list"""
        for channel in ctx.guild.channels:
            if channel.id == RAID_TEXT_CHAT: # raid member text chat id
                for m in channel.members:
                    if m.voice is not None:
                        members.append(m)

        """ Determines the target voice channel to move all members to """
        for channel in ctx.guild.voice_channels:
            if channel.id == RAID_VOICE_CHAT: # raid voice chat id
                target_voice_chat = channel
                break
            else:
                target_voice_chat = ctx.guild.voice_channels[0]

        """ Moving all members to target channel """
        for member in members:
            if member not in target_voice_chat.members:
                print(f"Moving {member} to {target_voice_chat}")
                await member.move_to(target_voice_chat, reason="Raid time!")
    else:
        await ctx.send('Nice try, fool.')
        await ctx.message.delete()

class WCL(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

class Minecraft(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def biggest_killer(self, ctx, particular_entity:str = ""):
        miners = {}
        response = ""
        data = mc_api.get_stats()
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
        data = mc_api.get_stats()
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
            stats = mc_api.get_stats(player)
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

        stats = mc_api.get_stats(player)
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

if "__main__" == __name__:
    client.run(TOKEN)
