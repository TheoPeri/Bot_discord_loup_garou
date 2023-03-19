import discord
import game_lg
import hellper

def run_discord_bot():
    # get token from token.txt file
    TOKEN = open('token.txt', 'r').read()
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

                for i in ['!fake_add_users_in_channel', '!add_user théop.', '!generate_default_roles', '!start', '!next']:
                    commandes.append(i)

                for msg in commandes:
                    message.content = msg
                    await on_message(message)

            if user_message == 'help':
                await hellper.send_message(message,'HELP' , '''
                Hey ! I'm the **LG bot**, here are the commands you can use:

                > !help `- show this message`
                > !create `- create a game`
                
                If game not started:
                > !status                     `- show users in game`
                > !start                      `- start the game`
                > !restart                    `- restart the game`

                > !add_users_in_channel       `- add all users in your voice channel`
                > !add_user <user>            `- add user to game`
                > !remove_user <user>         `- remove user from game`

                > !generate_default_roles     `- generate default roles`
                > !add_role <role>            `- add role to game`
                > !remove_role <role>         `- remove role from game`

                If game started:
                > !next or !n                 `- next turn`
                > !again                      `- restart game with same people and roles`
                > !restart                    `- restart (full flush) the game`
                > !status                     `- show users in game and their roles`

                > !vote <user>                `- vote for user`
                > !eat <user>                 `- eat user`
                > !see <user>                 `- see user`
                > !save <user>                `- save user`
                > !poison <user>              `- poison user`
                > !shoot <user>               `- shoot user`
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
                    elif user_message == 'fake_add_users_in_channel':
                        users, real_users = await hellper.get_user_voice_channel(message)
                        if users is not None:
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
                        await hellper.send_message(message, f'Roles', game.roles, False)
                    elif user_message == 'start':
                        good, my_msg = game.start_game()
                        if good:
                            await hellper.send_message(message, f'Roles assigned', my_msg, False)
                            await hellper.send_roles(game.real_users, game.game, user_name)
                            await hellper.send_simple_message(message, f'Private messages sends', False)
                            await hellper.send_message(message, f'La partie peux commencer !', '', False)
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
                
                else:
                    if user_message == 'status':
                        await hellper.send_message(message, f'Users in game', game.game, False)
                    elif user_message == 'next' or user_message == 'n':
                        title, description = game.check_end()
                        if title is not None:
                            await hellper.send_message(message, title, description, False)
                        else:
                            title, description = game.next_step()
                            await hellper.send_message(message, title, description, False)
                    elif user_message.startswith('vote'):
                        user = user_message.split(' ')[1]
                        title, description = game.vote_user(user)
                        await hellper.send_message(message, title, description, False)
                    elif user_message.startswith('eat'):
                        user = user_message.split(' ')[1]
                        title, description = game.eat_user(user)
                        await hellper.send_message(message, title, description, False)
                    elif user_message.startswith('see'):
                        user = user_message.split(' ')[1]
                        title, description = game.see_user(user)
                        await hellper.send_message(message, title, description, False)
                    elif user_message.startswith('save'):
                        user = user_message.split(' ')[1]
                        title, description = game.save_user(user)
                        await hellper.send_message(message, title, description, False)
                    elif user_message.startswith('poison'):
                        user = user_message.split(' ')[1]
                        title, description = game.poison_user(user)
                        await hellper.send_message(message, title, description, False)
                    elif user_message.startswith('shoot'):
                        user = user_message.split(' ')[1]
                        title, description = game.shoot_user(user)
                        await hellper.send_message(message, title, description, False)
                    elif user_message == 'restart':
                        del games[user_name]
                        message.content = '!create'
                        await on_message(message)
                    elif user_message == 'again':
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

    client.run(TOKEN)