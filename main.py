import random, discord, asyncio, os
from discord.ext import commands, tasks
from secret import TOKEN
from itertools import cycle

client = commands.Bot(command_prefix='.')
status = cycle(["Killing Jaeler", 'Falling down holes','Enchanting weapon', 'Missing tyrant ramp'])

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_ready():
    change_status.start()
    print('Logged in as', client.user.name)
    current_guild = client.guilds[0]
    target_voice_chat = current_guild.voice_channels[0]
    # print(current_guild)
    # print(target_voice_chat)
    # print(current_guild.members)

    await target_voice_chat.connect()

@client.command(aliases=['raidtime'])
async def raid_time(ctx):
    """ An officer can call this command to move all active voice raid members to raid chat """
    if 'officer' in [c.name.lower() for c in ctx.author.roles]: 
        members = []

        """ Adds all members from specific channels to a list"""
        for channel in client.guilds[0].channels:
            if channel.name.lower() in ['trial raider', 'raider', 'raider trial'] or channel.id in [960743045849038849]:
                for m in channel.members:
                    if m.voice is not None:
                        members.append(m)

        """ Determines the target voice channel to move all members to """
        for channel in client.guilds[0].voice_channels:
            if channel.id == 648591623638220830:
                target_voice_chat = channel
                break
            else:        
                target_voice_chat = client.guilds[0].voice_channels[0]
        """ Moving all members to target channel """
        for member in members:
            if member not in target_voice_chat.members:
                print(f"Moving {member} to {target_voice_chat}")
                await member.move_to(target_voice_chat, reason="Raid time!")
    else:
        await ctx.send('Nice try fool.')
if "__main__" == __name__:
    client.run(TOKEN)