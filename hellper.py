# get user in discord channel
async def get_user_voice_channel(message):
    try:
        # get user voice channel
        user = message.author
        channel = user.voice.channel
        # get all users in channel
        users = channel.members
        # get only member name
        users = [str(user.name).lower().replace(" ", "") for user in users]
        # remove bot and user
        users.remove(str(user.name).lower().replace(" ", ""))
        return users
    
    except Exception as e:
        print(e)
        return None

# send role to user

async def send_message(message, to_send, is_private):
    try:
        await message.author.send(to_send) if is_private else await message.channel.send(to_send)

    except Exception as e:
        print(e)
