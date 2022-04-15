import random, discord, asyncio, os
from discord.ext import commands, tasks
from secret import TOKEN
from itertools import cycle

OFFICER_TEXT_CHAT = 648544127352307719
OFFICER_VOICE_CHAT = 648591145617588244

RAID_TEXT_CHAT = 648591575810834445
RAID_VOICE_CHAT = 648591623638220830

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
    change_status.start()
    print('Logged in as', client.user.name)

@client.command()
async def move(ctx, _from, to ):
    if 'officer' in [c.name.lower() for c in ctx.author.roles]:
        members = []

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

        
if "__main__" == __name__:
    client.run(TOKEN)