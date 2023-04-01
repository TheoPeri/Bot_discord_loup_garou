import discord

# get user in discord channel
async def get_user_voice_channel(message):
    try:
        # get user voice channel
        user = message.author
        channel = user.voice.channel
        # get all users in channel
        real_users = channel.members
        # get only member name
        users = [str(user.name).lower().replace(" ", "") for user in real_users]
        # remove bot and user
        users.remove(str(user.name).lower().replace(" ", ""))
        return users, real_users
    
    except Exception as e:
        print(e)
        return None

# send role to user

async def send_simple_message(message, to_send, is_private):
    try:
        await message.author.send(to_send) if is_private else await message.channel.send(to_send)

    except Exception as e:
        print(e)

# send embed message
async def send_message(message, title, description, is_private, image=None, special=False):
    try:
        if type(description) is list:
            description = '\n'.join(["- " + str(i) for i in description])
        elif type(description) is dict:
            description = '\n'.join(["- " + str(key) + " : " + str(value) for key, value in description.items()])

        embed = discord.Embed(title=title, description=description, color=0xe69038)
        if image is not None:
            embed.set_image(url=image)
        if special:
            await message.send(embed=embed)
        else:
            await message.author.send(embed=embed) if is_private else await message.channel.send(embed=embed)

    except Exception as e:
        print(e)

async def send_roles(real_users, roles, admin):
    role_url = {
        'Ancien':           'https://cdn.discordapp.com/attachments/933309657206902866/1091704230647185428/Ancien.jpg',
        'Ange':             'https://cdn.discordapp.com/attachments/933309657206902866/1091704231066620004/Ange.jpg',
        'BoucEmissaire':    'https://cdn.discordapp.com/attachments/933309657206902866/1091704231360213093/BoucEmissaire.jpg',
        'Chasseur':         'https://cdn.discordapp.com/attachments/933309657206902866/1091704231775453265/Chasseur.jpg',
        'Corbeau':          'https://cdn.discordapp.com/attachments/933309657206902866/1091704232148750397/Corbeau.jpg',
        'Cupidon':          'https://cdn.discordapp.com/attachments/933309657206902866/1091704232526229615/Cupidon.jpg',
        'Idiot':            'https://cdn.discordapp.com/attachments/933309657206902866/1091704232878555136/Idiot.jpg',
        'JoueurFlute':      'https://cdn.discordapp.com/attachments/933309657206902866/1091704299538620557/JoueurFlute.jpg',
        'Loup-Garou':       'https://cdn.discordapp.com/attachments/933309657206902866/1091704299882545252/Loup-Garou.jpg',
        'Maire':            'https://cdn.discordapp.com/attachments/933309657206902866/1091704300473950318/Maire.jpg',
        'PetiteFille':      'https://cdn.discordapp.com/attachments/933309657206902866/1091704304479502407/PetiteFille.jpg',
        'Pirate':           'https://cdn.discordapp.com/attachments/933309657206902866/1091704304919908395/Pirate.jpg',
        'Salvateur':        'https://cdn.discordapp.com/attachments/933309657206902866/1091704305674887269/Salvateur.jpg',
        'Sorcière':         'https://cdn.discordapp.com/attachments/933309657206902866/1091704306207555634/Sorciere.jpg',
        'Villageois':       'https://cdn.discordapp.com/attachments/933309657206902866/1091704306647965746/Villageois.jpg',
        'Voleur':           'https://cdn.discordapp.com/attachments/933309657206902866/1091704307209994320/Voleur.jpg',
        'Voyante':          'https://cdn.discordapp.com/attachments/933309657206902866/1091704307780423710/Voyante.jpg',
        'Error':            'https://cdn.discordapp.com/attachments/933309657206902866/1091726397287977030/image.png',
    }

    users_sended = []

    for personne, role in roles.items():
        for user in real_users:
            if str(user.name).lower().replace(" ", "") == personne:
                users_sended.append(personne)
                await send_message(user, f'Pour la partie de {admin}', f'Tu es {role}', True, role_url[role] if role in role_url else role_url["Error"], special=True)

    return users_sended

# help message
def create_help():
    txt = '''
                Hey ! I'm the **LG bot**, here are the commands you can use:
                
                # First, create a game
                > !create `- create a game`
                
                # Next, add the users 
                > !add_users_in_channel       `- add all users in your voice channel`
                > !add_user <user>            `- add user to game`
                > !remove_user <user>         `- remove user from game`

                # Add the roles
                ## authomatically
                > !generate_default_roles     `- generate default roles`
                ## manually (or modify the roles generated authomatically)
                > !add_role <role>            `- add role to game`
                > !remove_role <role>         `- remove role from game`

                # Start the game !
                > !start                      `- start the game`

                # The game is finished ? restart it !
                > !restart                    `- restart the game (it will keep the users and roles)`
                > !hard_restart                `- restart the game (create an empty game / no roles and users kept)`

                # Other commands
                > !status                     `- show users in game`
                '''
    
    return txt