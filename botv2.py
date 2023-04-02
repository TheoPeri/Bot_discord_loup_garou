import discord
import game_lg
import hellper
import os
from discord.ext import commands
from discord.ui import View, Button

# Role button
class RoleButton(Button):
    def __init__(self, game, role, to_add, parent_view):
        self.game = game
        self.role = role
        self.to_add = to_add
        self.parent_view = parent_view

        if to_add:
            style = discord.ButtonStyle.green
        else:
            style = discord.ButtonStyle.red

        super().__init__(label="[" + str(game.roles[role] if role in game.roles else 0) + "] " + role, style=style)

    async def callback(self, interaction: discord.Interaction):
        # check if user is the game creator
        if interaction.user != self.game.creator:
            await interaction.response.send_message("Tu fait quoi frero ? Touche pas a ça è_é", ephemeral=True)
            return

        if self.to_add:
            self.game.add_role(self.role)
        else:
            self.game.remove_role(self.role)
        role_buttons = [item for item in self.parent_view.children if item.label not in ["Menu", "Recommencer", "Génération auto"] and item.role == self.role]
        for button in role_buttons:
            button.label = "[" + str(self.game.roles[self.role] if self.role in self.game.roles else 0) + "] " + self.role
        await interaction.response.edit_message(view=self.view)

class RecommencerButton(Button):
    def __init__(self, game, parent_view):
        self.game = game
        self.parent_view = parent_view

        super().__init__(label="Recommencer", style=discord.ButtonStyle.primary, emoji="🗑️")

    async def callback(self, interaction: discord.Interaction):
        # check if user is the game creator
        if interaction.user != self.game.creator:
            await interaction.response.send_message("Tu fait quoi frero ? Touche pas a ça è_é", ephemeral=True)
            return

        self.game.roles = {}

        role_buttons = [item for item in self.parent_view.children if item.label not in ["Menu", "Recommencer", "Génération auto"]]
        for button in role_buttons:
            button.label = "[0] " + button.role
        await interaction.response.edit_message(view=self.view)

class GenerateButton(Button):
    def __init__(self, game, parent_view):
        self.game = game
        self.parent_view = parent_view

        super().__init__(label="Génération auto", style=discord.ButtonStyle.primary, emoji="🎲")

    async def callback(self, interaction: discord.Interaction):
        # check if user is the game creator
        if interaction.user != self.game.creator:
            await interaction.response.send_message("Tu fait quoi frero ? Touche pas a ça è_é", ephemeral=True)
            return

        self.game.roles = {}
        self.game.generate_default_roles()

        role_buttons = [item for item in self.parent_view.children if item.label not in ["Menu", "Recommencer", "Génération auto"]]
        for button in role_buttons:
            button.label = "[" + str(self.game.roles[button.role] if button.role in self.game.roles else 0) + "] " + button.role
        await interaction.response.edit_message(view=self.view)

class RoleView(View):
    def __init__(self, game, context, mybot):
        super().__init__()
        self.game = game
        self.context = context
        self.mybot = mybot

        for role in game.all_roles:
            button_role = RoleButton(game, role, True, self)
            self.add_item(button_role)

        # add Menu button
        button_menu = CallerButton(game, self, "Menu", "🏠", "home")
        self.add_item(button_menu)

        # add Delete button
        button_delete = RecommencerButton(game, self)
        self.add_item(button_delete)

        # add generate button
        button_generate = GenerateButton(game, self)
        self.add_item(button_generate)

        for role in game.all_roles[-1:] + game.all_roles[:-1]:
            button_role = RoleButton(game, role, False, self)
            self.add_item(button_role)

class PlayerButton(Button):
    def __init__(self, game, user_name):
        self.game = game
        self.added = user_name in game.users

        super().__init__(label=user_name, style=discord.ButtonStyle.red if not self.added else discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        # check if user is the game creator
        if interaction.user != self.game.creator:
            await interaction.response.send_message("Tu fait quoi frero ? Touche pas a ça è_é", ephemeral=True)
            return
        if self.added:
            self.game.remove_user(self.label)
            self.added = False
            self.style = discord.ButtonStyle.red
        else:
            self.game.add_user(self.label)
            self.added = True
            self.style = discord.ButtonStyle.green
        await interaction.response.edit_message(view=self.view)

class PlayerView(View):
    def __init__(self, game, context, mybot):
        super().__init__()
        self.game = game
        self.context = context
        self.mybot = mybot

        # add Home button
        button_home = CallerButton(game, self, "Menu", "🏠", "home")
        self.add_item(button_home)

        # add Reload button
        button_reload = CallerButton(game, self, "Recharger", "🔄", "player")
        self.add_item(button_reload)

        # add Invite button
        button_invite = CallerButton(game, self, "Inviter", "👥", "invite", False)
        self.add_item(button_invite)

        for user_name, _ in game.all_users:
            try:
                button_player = PlayerButton(game, user_name)
                self.add_item(button_player)
            except:
                break

class CallerButton(Button):
    def __init__(self, game, parent_view, label, emoji, command, delete_msg=True):
        self.game = game
        self.parent_view = parent_view
        self.command = command
        self.delete_msg = delete_msg
        super().__init__(label=label, style=discord.ButtonStyle.primary, emoji=emoji)

    async def callback(self, interaction: discord.Interaction):
        # check if user is the game creator
        if interaction.user != self.game.creator:
            await interaction.response.send_message("Tu fait quoi frero ? Touche pas a ça è_é", ephemeral=True)
            return
        
        if self.delete_msg:
            await self.parent_view.msg.delete()
        await self.parent_view.context.invoke(self.parent_view.mybot.get_command(self.command))
        await interaction.response.defer()

class HomeView(View):
    def __init__(self, game, context, mybot):
        super().__init__()
        self.context = context
        self.mybot = mybot

        # add button
        button_player = CallerButton(game, self, "Gestion joueurs", "👥", "player")
        button_role = CallerButton(game, self, "Gestion roles", "👹", "role")
        button_start = CallerButton(game, self, "Commencer", "🎮", "start")

        if len(game.users) == 0 or not game.check_roles():
            button_start.disabled = True
        
        self.add_item(button_player)
        self.add_item(button_role)
        self.add_item(button_start)

class InviteButton(Button):
    def __init__(self, game):
        self.game = game
        super().__init__(label="JE JOUE !", style=discord.ButtonStyle.green, emoji="👍")

    async def callback(self, interaction: discord.Interaction):
        # get user
        user = interaction.user
        # add user to game
        self.game.add_user_all(user)
        # send message
        await interaction.response.send_message("Vous avez rejoint la partie !", ephemeral=True)

class InviteView(View):
    def __init__(self, game):
        super().__init__()
        self.game = game

        # add button
        button_invite = InviteButton(game)
        self.add_item(button_invite)

class GameView(View):
    def __init__(self, game, context, mybot):
        super().__init__()
        self.game = game
        self.context = context
        self.mybot = mybot

        # add button
        button_role = CallerButton(game, self, "Roles assignés", "👹", "role")
        self.add_item(button_role)

        # recommencer button
        button_recommencer = CallerButton(game, self, "Recommencer", "🔄", "restart")
        self.add_item(button_recommencer)

class PlayerRoleButton(Button):
    def __init__(self, game, role, users):
        self.game = game
        self.role = role
        self.users = users
        label = role + " : " + ", ".join(users)
        super().__init__(label=label, style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        # check if user is the game creator
        if interaction.user != self.game.creator:
            await interaction.response.send_message("Tu fait quoi frero ? Touche pas a ça è_é", ephemeral=True)
            return
        
        # do nothing
        await interaction.response.defer()

class GameRoleView(View):
    def __init__(self, game, context, mybot):
        super().__init__()
        self.game = game
        self.context = context
        self.mybot = mybot

        # add Home button
        button_home = CallerButton(game, self, "Menu", "🏠", "home")
        self.add_item(button_home)

        to_show = {}
        for user, role in game.game.items():
            if role not in to_show:
                to_show[role] = []
            to_show[role].append(user)

        for role, users in to_show.items():
            button_player = PlayerRoleButton(game, role, users)
            self.add_item(button_player)


def run_discord_bot():
    # get token from env variable
    TOKEN = os.getenv('TOKEN')
    bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
    bot.remove_command('help')

    games = {}

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

    @bot.command()
    async def help(ctx):
        await hellper.send_message(ctx, 'HELP' , hellper.create_help_v2(), False)

    @bot.command()
    async def invite(ctx):
        if str(ctx.author) in games:
            game = games[str(ctx.author)]
            if game.started:
                await hellper.send_message(ctx, 'Erreur' , 'La partie est déjà lancée !', False)
            else:
                View = InviteView(game)

                txt = '''
                REJOINS LA PARTIE EN CLIQUANT SUR LE BOUTON CI-DESSOUS
                '''

                embed = discord.Embed(title=f"Invitation pour la partie de " + str(ctx.author), description=txt, color=0xe69038)
                embed.set_image(url="https://cdn.discordapp.com/attachments/933309657206902866/1092092306984800276/invite.jpg")

                msg = await ctx.send(embed=embed, view=View)
        else:
            await hellper.send_message(ctx, 'Erreur' , 'Aucune partie en cours !', False)

    @bot.command()
    async def player(ctx):
        if str(ctx.author) in games:
            game = games[str(ctx.author)]
            if game.started:
                await hellper.send_message(ctx, 'Erreur' , 'La partie est déjà lancée !', False)
            else:
                view = PlayerView(game, ctx, bot)

                txt = '''
                Tu peux:
                > Ajouter un joueur en cliquant sur un joueur rouge
                > Retirer un joueur en cliquant sur un joueur vert
                > Revenir au menu en cliquant sur le bouton Menu 🏠
                '''                

                embed = discord.Embed(title=f"Gestion des joueurs", description=txt, color=0xe69038)
                embed.set_image(url="https://cdn.discordapp.com/attachments/933309657206902866/1092062047048572958/joueurs.jpg")

                msg = await ctx.send(embed=embed, view=view)
                view.msg = msg
        else:
            await hellper.send_message(ctx, 'Erreur' , 'Aucune partie en cours !', False)

    @bot.command()
    async def role(ctx):
        if str(ctx.author) in games:
            game = games[str(ctx.author)]
            if game.started:
                view = GameRoleView(game, ctx, bot)
                embeded = discord.Embed(title=f"Roles assignés", description="Voici les roles assignés aux joueurs", color=0xe69038)

                msg = await ctx.send(embed=embeded, view=view)
                view.msg = msg
            else:
                view = RoleView(game, ctx, bot)

                txt = '''
                Tu peux:
                > Ajouter un role en cliquant sur un bouton vert
                > Retirer un role en cliquant sur un bouton rouge
                > Revenir au menu en cliquant sur le bouton Menu 🏠
                '''                

                embed = discord.Embed(title=f"Gestion des roles", description=txt, color=0xe69038)
                embed.set_image(url="https://cdn.discordapp.com/attachments/933309657206902866/1092062047451222026/roles.jpg")

                msg = await ctx.send(embed=embed, view=view)
                view.msg = msg
        else:
            await hellper.send_message(ctx, 'Erreur' , 'Aucune partie en cours !', False)

    @bot.command()
    async def create(ctx):
        games[str(ctx.author)] = game_lg.LGgame(ctx.author)
        await ctx.invoke(bot.get_command('home'	))

    @bot.command()
    async def home(ctx):
        if str(ctx.author) in games:
            game = games[str(ctx.author)]

            if game.started:
                view = GameView(game, ctx, bot)

                embed = discord.Embed(title=f"Partie de {ctx.author}", description="La partie a commencé !", color=0xe69038)
                embed.set_image(url="https://cdn.discordapp.com/attachments/933309657206902866/1092089624530268231/game.jpg")

                msg = await ctx.send(embed=embed, view=view)
                view.msg = msg
            else:
                view = HomeView(game, ctx, bot)

                embed = discord.Embed(title=f"Partie crée par {ctx.author}", description="Que le jeu commence !!! Tu peux inviter des joueur avec la commande !invite", color=0xe69038)
                embed.set_image(url="https://cdn.discordapp.com/attachments/933309657206902866/1092036913935941662/lobby.jpg")

                msg = await ctx.send(embed=embed, view=view)
                view.msg = msg
        else:
            await hellper.send_message(ctx, 'Erreur' , 'Aucune partie en cours !', False)

    @bot.command()
    async def start(ctx):
        if str(ctx.author) in games:
            game = games[str(ctx.author)]
            if game.started:
                await hellper.send_message(ctx, 'Erreur' , 'La partie est déjà lancée !', False)
            else:
                good, msg = game.start_game()
                if not good:
                    await hellper.send_message(ctx, 'Erreur' , msg, False)
                else:
                    await hellper.send_roles(game.all_users, game.game, str(ctx.author))
                    await ctx.invoke(bot.get_command('home'))
        else:
            await hellper.send_message(ctx, 'Erreur' , 'Aucune partie en cours !', False)

    @bot.command()
    async def restart(ctx):
        if str(ctx.author) in games:
            game = games[str(ctx.author)]
            if not game.started:
                await hellper.send_message(ctx, 'Erreur' , 'La partie n\'est pas lancée !', False)
            else:
                all_users = game.all_users
                users = game.users
                roles = game.roles

                games[str(ctx.author)] = game_lg.LGgame(ctx.author)

                game = games[str(ctx.author)]
                game.users = users
                game.roles = roles
                game.all_users = all_users

                await ctx.invoke(bot.get_command('home'))
        else:
            await hellper.send_message(ctx, 'Erreur' , 'Aucune partie en cours !', False)



    bot.run(TOKEN)