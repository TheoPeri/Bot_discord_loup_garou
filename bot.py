import discord
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
                for i in range(7):
                    commandes.append(f'!add_user test{i}')

                for i in ['!add_users_in_channel', '!add_user théop.', '!generate_default_roles']:
                    commandes.append(i)

                for msg in commandes:
                    message.content = msg
                    await on_message(message)

            if user_message == 'help':
                await hellper.send_message(message,'HELP' , '''
                Hey ! I'm the LG bot, here are the commands you can use:

                !help - show this message

                !create - create a game
                
                If game not started:
                    !start - start the game
                    !restart - restart the game
                    !add_users_in_channel - add all users in your voice channel
                    !add_user <user> - add user to game
                    !remove_user <user> - remove user from game
                    !generate_default_roles - generate default roles
                    !add_role <role> - add role to game
                    !remove_role <role> - remove role from game
                    !status - show users in game

                If game started:
                ''', False)

            if user_name not in games:
                if user_message == 'create':
                    games[user_name] = game_lg.LGgame()
                    await hellper.send_simple_message(message, f'Game created for user {user_name}', False)
                else:
                    await hellper.send_simple_message(message, f'You need to create a game first (!create)', False)

            if user_name in games:
                game = games[user_name]

                if not game.started:
                    if user_message == 'add_users_in_channel':
                        users, real_users = await hellper.get_user_voice_channel(message)
                        if users is not None:
                            for user in users:
                                game.add_user(user)
                            await hellper.send_message(message, f'Users in game', game.users, False)
                            game.real_users = real_users
                        else:
                            await hellper.send_simple_message(message, f'You need to be in a voice channel', False)
                    elif user_message.startswith('add_user'):
                        user = user_message.split(' ')[1]
                        game.add_user(user.lower().replace(" ", ""))
                        await hellper.send_message(message, f'Users in game', game.users, False)
                    elif user_message.startswith('remove_user'):
                        user = user_message.split(' ')[1]
                        game.remove_user(user)
                        await hellper.send_message(message, f'Users in game', game.users, False)
                    elif user_message == 'status':
                        await hellper.send_message(message, f'Users in game', game.users, False)
                    elif user_message == 'start':
                        good, my_msg = game.start_game()
                        if good:
                            await hellper.send_message(message, f'Roles assigned', my_msg, False)
                            await hellper.send_roles(game.real_users, game.game, user_name)
                            await hellper.send_simple_message(message, f'Private messages sends', False)
                        else:
                            await hellper.send_simple_message(message, f'Number of roles different of number of players {my_msg}', False)
                    elif user_message == 'restart':
                        del games[user_name]
                        message.content = '!create'
                        await on_message(message)
                    elif user_message == 'generate_default_roles':
                        game.generate_default_roles()
                        await hellper.send_message(message, f'Roles', game.roles, False)
                    elif user_message.startswith('add_role'):
                        role = user_message.split(' ')[1]
                        game.add_role(role)
                        await hellper.send_message(message, f'Roles', game.roles, False)
                    elif user_message.startswith('remove_role'):
                        role = user_message.split(' ')[1]
                        game.remove_role(role)
                        await hellper.send_message(message, f'Roles', game.roles, False)


    client.run(TOKEN)