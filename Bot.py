import discord
from discord import Game
import STATICS,LevelManager
import json
import os
import asyncio
from Commands import GetXP, Leaderboard, GetRank, Info

os.chdir(STATICS.BOT_DIRECTORY)
client = discord.Client()

commands = {
    'xp': GetXP,
    'top': Leaderboard,
    'rank': GetRank,
    'info': Info,
}

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Dont mind me, just spying"))
    print('started')
    await start_scan()

async def start_scan():
    counter = 0
    channels = {}
    while True:
        for n in STATICS.CHANNELS:
            channels.append(discord.utils.get(client.get_all_channels(), name=n))

        txt_channel = discord.utils.get(client.get_all_channels(), name=STATICS.TEXT_CHANNEL)
        servers = client.servers
        server = None
        for s in servers:
            if s.name == STATICS.SERVER_NAME:
                server = s

        #Scans entire server to add all members to the JSON file
        #Only does this every 8 hours because it takes longer depending on the amount of members
        if counter == 96:
            for m in server.members:
                with open('users.json', 'r') as f:
                    users = json.load(f)
                print('Initializing member: %s') %(m)

                if not m.nick == None:
                    name = m.nick
                else:
                    temp = str(m)
                    temp = temp.split('#')
                    name = temp[0]

                await LevelManager.init(users, m, name)
                await LevelManager.set_color(m, client, users)

                with open('users.json', 'w') as f:
                    json.dump(users, f)
            counter = 0

        members = []
        for c in channels:
            members.extend(c.voice_members)
        for m in members:
            print(m)
            with open('users.json', 'r') as f:
                users = json.load(f)

            if not m.nick == None:
                name = m.nick
            else:
                temp = str(m)
                temp = temp.split('#')
                name = temp[0]

            await LevelManager.update_data(users, m, client, txt_channel, name)

            with open('users.json', 'w') as f:
                json.dump(users, f)

        counter += 1
        await asyncio.sleep(300)

@client.event
async def on_message(message):
    str_message = message.content.lower()
    if str_message.startswith('!xp'):
        await commands.get('xp').ex(message, client)
    if str_message == '!top':
        await commands.get('top').ex(message, client)
    if str_message == '!rank':
        await commands.get('rank').ex(message, client)
    if str_message == '!info':
        await commands.get('info').ex(message, client)

client.run(STATICS.TOKEN)