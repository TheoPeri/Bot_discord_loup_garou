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

async def send_roles(real_users, roles, mg):
    role_url = {
        'Salvateur': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103625274335292/salvateur.jpg',
        'Villageois': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103625622474822/villageois.jpg',
        'Loup-Garou': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103625920250047/loupGarou.jpg',
        'Voyante': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103626226442250/voyante.jpg',
        'Cupidon': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103627149189211/cupidon.jpg',
        'Corbeau': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103700943781988/le_corbeau.jpg',
        'Chasseur': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103701841367050/chasseur.jpg',
        'Sorcière': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103703011578017/sorciere.jpg',
        'Maire': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103702663430197/maire.jpg',
        'Pirate': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087106860504580187/SPOILER_pirate.jpg',
        'Ancien': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103702311125123/ancien.jpg',
        'BoucEmissaire': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103701275115640/boucEmissaire.jpg',
        'Voleur': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103626830413834/voleur.jpg',
        'PetiteFille': 'https://cdn.discordapp.com/attachments/1066452874055385128/1087103626524250262/petitefille.jpg',
    }
    for personne, role in roles.items():
        for user in real_users:
            if str(user.name).lower().replace(" ", "") == personne:
                await send_message(user, f'Pour la partie de {mg}', f'Tu es {role}', True, role_url[role] if role in role_url else None, special=True)

