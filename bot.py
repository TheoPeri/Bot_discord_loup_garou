import discord
import game_lg
import hellper
import os

def run_discord_bot():
    # get token from env variable
    TOKEN = os.getenv('TOKEN')
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

        if user_message and user_message[0] == '!':
            user_message = user_message[1:]

            if user_message == 'script':
                commandes = ['!create']
                for i in range(4):
                    commandes.append(f'!add_user test{i}')

                for i in ['!add_user théop.']:
                    commandes.append(i)

                for msg in commandes:
                    message.content = msg
                    await on_message(message)
                return

            if user_message == 'help':
                await hellper.send_message(message,'HELP' , hellper.create_help(), False)
                return

            if user_name not in games:
                if user_message == 'create':
                    games[user_name] = game_lg.LGgame()
                    await hellper.send_simple_message(message, f'Game created for user {user_name}', False)
                else:
                    await hellper.send_simple_message(message, f'You need to create a game first (!create)', False)
                return

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
                        game.remove_user(user.lower().replace(" ", ""))
                        await hellper.send_message(message, f'Users in game', game.users, False)
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
                    elif user_message == 'start':
                        good, my_msg = game.start_game()
                        if good:
                            await hellper.send_message(message, f'Roles assigned', my_msg, False)
                            if game.real_users is not None:
                                sended = await hellper.send_roles(game.real_users, game.game, user_name)
                                await hellper.send_simple_message(message, 'Private messages sended to: ' + ", ".join(sended), False)
                            else:
                                await hellper.send_simple_message(message, f'No private messages sends', False)
                            await hellper.send_message(message, f'La partie peux commencer !', '', False)
                        else:
                            await hellper.send_simple_message(message, f'Number of roles different of number of players {my_msg}', False)
                    elif user_message == 'restart':
                        users = game.users
                        roles = game.roles
                        del games[user_name]
                        games[user_name] = game_lg.LGgame()
                        game = games[user_name]
                        game.users = users
                        game.roles = roles
                        await hellper.send_message(message, "RESTART GAME", "Game restart with same users and roles", False)
                        message.content = '!status'
                        await on_message(message)

                    elif user_message == 'hard_restart':
                        del games[user_name]
                        games[user_name] = game_lg.LGgame()
                        await hellper.send_message(message, "HARD RESTART GAME", "Game restart with no users and no roles", False)
                    
                    elif user_message == 'status':
                        await hellper.send_message(message, f'Users in game', game.users, False)
                        await hellper.send_message(message, f'Roles', game.roles, False)

                    else:
                        print("uncknown command " + user_message)
                        await hellper.send_message(message,'HELP' , hellper.create_help(), False)

                else:
                    if user_message == 'status':
                        await hellper.send_message(message, f'Users in game', game.game, False)
                    elif user_message == 'restart':
                        users = game.users
                        roles = game.roles
                        del games[user_name]
                        games[user_name] = game_lg.LGgame()
                        game = games[user_name]
                        game.users = users
                        game.roles = roles
                        await hellper.send_message(message, "RESTART GAME", "Game restart with same users and roles", False)
                        message.content = '!status'
                        await on_message(message)

                    elif user_message == 'hard_restart':
                        del games[user_name]
                        games[user_name] = game_lg.LGgame()
                        await hellper.send_message(message, "HARD RESTART GAME", "Game restart with no users and no roles", False)
                    else:
                        print("uncknown command " + user_message)
                        await hellper.send_message(message,'HELP' , hellper.create_help(), False)



    client.run(TOKEN)