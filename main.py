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
    general_voice_chat = current_guild.voice_channels[0]
    # print(current_guild)
    # print(general_voice_chat)
    # print(current_guild.members)
    await general_voice_chat.connect()

@client.command(aliases=['raidtime'])
async def raid_time(ctx):
    members = []

    for role in client.guilds[0].roles:
        if role.name.lower() in ['trial raider', 'raider', 'raider trial'] or role.id in [960743045849038849]:
            for m in role.members:
                if m.voice is not None:
                    members.append(m)

    if ctx.author not in members and ctx.author.voice is not None:
        members.append(ctx.author)
    
    general_voice_chat = client.guilds[0].voice_channels[0]
    for member in members:
        print(f"Moving {member} to {general_voice_chat}")
        await member.move_to(general_voice_chat, reason="Raid time!")

if "__main__" == __name__:
    client.run(TOKEN)