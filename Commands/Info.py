import discord
import LevelManager

async def ex(message, client):
    str_message = ''
    for i in range(1, 25):
        str_message += 'level %s - %s hours \n' %((i+1), LevelManager.calculate_hours(i))

    await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=str_message))