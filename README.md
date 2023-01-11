# Pocopoc
 
A discord bot that moves people around in voice chats, good for mass moving people to the correct places.

Cogs 
---
- Warcraft Logs

The discord bot has api integration with Warcraft logs.
I intend to use it as a tool to highlight and identify valuable insight to improve our raid roster in world of warcraft.

- Minecraft
We have a guild server for a very popular blocky game, where I am also hosting a [custom made rest-api](htts://github.com/joonsey/mcapi) that serves various statistic from the game.

Adapters
---
**All cogs** have an adapter to comunicate through the API with and gets dependecy injected into the bot to seemlessly enable cogs / features.
```python
mc_api = Minecraftapi_adapter(MINECRAFT_API_PATH)
wcl_adapter = WCL_adapter(WCL_CLIENT_ID, WCL_CLIENT_SECRET)
...
@client.event
async def on_ready():
    await client.add_cog(Minecraft(client, mc_api))
    await client.add_cog(WCL(client, wcl_adapter, GUILD_ID))
```

All the configurations are served from the *settings.py* file and / or *secret.py* file.

current folder structure:
```bash
setting.py
secret.py
main.py
| cogs
| - cog1
| - cog2
| adapters
| - adapter1
| - adapter2
```
