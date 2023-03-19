import discord
import responses
import game_lg
import hellper

def run_discord_bot():
    TOKEN = 'MTA4NzAzMzc3MjIxOTg0NjczOQ.GeTJYv.X_C02V5EPsPz1eUWvk7bXCMXzrKbSc2J1Jtp8I'
    client = discord.Client(intents = discord.Intents.all())

    games = {}


    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        user_name = str(message.author)
        user_message = str(message.content)

        if user_message[0] == '!':
            user_message = user_message[1:]

            if user_message == 'script':
                commandes = ['!create']
                for i in range(10):
                    commandes.append(f'!add_user test{i}')

                for msg in commandes:
                    message.content = msg
                    await on_message(message)

            if user_message == 'help':
                await hellper.send_message(message, '''
                Hey ! I'm the LG bot, here are the commands you can use:

                !help - show this message

                !create - create a game
                
                If game not started:
                    !start - start the game
                    !add_users_in_channel - add all users in your voice channel
                    !add_user <user> - add user to game
                    !remove_user <user> - remove user from game
                    !status - show users in game

                If game started:
                ''', False)

            if user_name not in games:
                if user_message == 'create':
                    games[user_name] = game_lg.LGgame()
                    await hellper.send_message(message, f'Game created for user {user_name}', False)
                else:
                    await hellper.send_message(message, f'You need to create a game first (!create)', False)

            if user_name in games:
                game = games[user_name]

                if not game.started:
                    if user_message == 'add_users_in_channel':
                        users = await hellper.get_user_voice_channel(message)
                        if users is not None:
                            for user in users:
                                game.add_user(user)
                            await hellper.send_message(message, f'Users in game: {game.users}', False)
                        else:
                            await hellper.send_message(message, f'You need to be in a voice channel', False)
                    elif user_message.startswith('add_user'):
                        user = user_message.split(' ')[1]
                        game.add_user(user.lower().replace(" ", ""))
                        await hellper.send_message(message, f'Users in game: {game.users}', False)
                    elif user_message.startswith('remove_user'):
                        user = user_message.split(' ')[1]
                        game.remove_user(user)
                        await hellper.send_message(message, f'Users in game: {game.users}', False)
                    elif user_message == 'status':
                        await hellper.send_message(message, f'Users in game: {game.users}', False)
                    elif user_message == 'start':
                        game.start_game()
                        await hellper.send_message(message, f'Game started !!!', False)
                        await hellper.send_message(message, f'Roles: {game.roles}', False)



    client.run(TOKEN)