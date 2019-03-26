import discord
import os
import json
import STATICS

os.chdir(STATICS.BOT_DIRECTORY)

async def ex(message, client):
    id_to_rank = {}
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

    for i in range(0, (sorted_list.__len__()-1)):
        key = sorted_list[i][0]
        value = i + 1
        temp = {key: value}
        id_to_rank.update(temp)

    try:
        str_message = 'Your rank is: %s' % id_to_rank[message.author.id]
        await client.send_message(message.channel,
                                  embed=discord.Embed(color=discord.Color.green(), description=str_message))
    except:
        await client.send_message(message.channel,
                                  embed=discord.Embed(color=discord.Color.green(), description='An error occured getting your rank'))

