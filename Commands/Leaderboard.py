import json
import os
import discord
import STATICS

os.chdir(STATICS.BOT_DIRECTORY)

async def ex(message, client):
    str_message = ''
    with open('users.json', 'r') as f:
        users = json.load(f)

    id_list = {}
    servers = client.servers
    for s in servers:
        if s.name == STATICS.SERVER_NAME:
            server = s

    x = 0
    for m in server.members:
        temp_list = {m.id: users[m.id]['xp']}
        id_list.update(temp_list)
        x+=1

    sorted_list = sorted(id_list.items(), key=lambda kv:kv[1], reverse=True)

    value = 0
    rank = 1
    while value < 5:
        hours = float(users[sorted_list[value][0]]['xp'] / 12)
        str_hours = '%.2f' % round(hours, 2)
        str_message += 'rank: %s \n name: %s \n hours: %s \n level: %s \n\n' % (rank, users[sorted_list[value][0]]['nickname'], str_hours, users[sorted_list[value][0]]['level'])
        rank += 1
        value += 1

    await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=str_message))