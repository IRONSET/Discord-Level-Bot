import discord

async def init(users, user, name):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['nickname'] = name
        users[user.id]['xp'] = 0
        users[user.id]['level'] = 1

async def update_data(users, user, client, txt_channel, name):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['nickname'] = name
        users[user.id]['xp'] = 0
        users[user.id]['level'] = 1
    else:
        await add_experience(users, user, name)
        await level_up(users, user, txt_channel, client, name)
        await set_color(user, client, users)

async def add_experience(users, user, name):
    users[user.id]['xp'] += 1
    users[user.id]['nickname'] = name

async def level_up(users, user, txt_channel, client, name):
    xp = users[user.id]['xp']
    level = calculate_level(xp, users[user.id]['level'])
    if users[user.id]['level'] < level:
        await client.send_message(txt_channel, embed=discord.Embed(color=discord.Color.green(), description="%s leveled up to level %s!" %(name, level)))
    users[user.id]['level'] = level

async def set_color(user, client, users):
    for r in user.roles:
        if "lvl" in r.name and not r.name.strip('lvl') == str(users[user.id]['level']):
            try:
                await client.remove_roles(user, r)
            except:
                print('failed to remove role')
                pass
    try:
        lvl_role = discord.utils.get(user.server.roles, name=('lvl%s' %users[user.id]['level']))
        await client.add_roles(user, lvl_role)
    except:
        print('failed to add role')
        pass

def calculate_level(xp, current_lvl):
    if current_lvl < 24:
        if xp >= 12 * calculate_hours(current_lvl):
            return (current_lvl + 1)
        return current_lvl
    return 24

#Calculates the amount of hours needed for the next level
def calculate_hours(current_lvl):
    if current_lvl < 11:
        return (5 * ( current_lvl * (( current_lvl + 1 ) / 2)))
    return ((75 / 2) * (current_lvl ** 2) + ((-1425 / 2) * current_lvl) + 3650)