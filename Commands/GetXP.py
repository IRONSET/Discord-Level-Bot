import json
import os
import discord
import LevelManager
import STATICS

os.chdir(STATICS.BOT_DIRECTORY)

async def ex(message, client):
    #if the command is entered without a mention it just gets your own level
    if message.mentions == []:
        user = message.author
    #You can mention someone with @*Name*
    else:
        user = message.mentions[0]

    with open('users.json', 'r') as f:
        users = json.load(f)

    level = users[user.id]['level']
    hours = float(users[user.id]['xp'] / 12)
    hours_to_next = float(LevelManager.calculate_hours(level) - hours)

    str_hours = '%.2f' % round(hours, 2)
    str_hours_to_next = '%.2f'  % round(hours_to_next, 2)

    if not user.nick == None:
        str_name = user.nick
    else:
        temp = str(user)
        temp = temp.split('#')
        str_name = temp[0]

    str_message = 'Name: %s \n current level: %s \n total hours: %s \n hours to next level: %s' %(str_name, level, str_hours, str_hours_to_next)

    await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=str_message))