# create class Game
import random

class LGgame:
    def __init__(self):
        print("Game created")
        self.started = False
        # users in game
        self.users = []
        # roles possible
        self.all_roles = ['Loup-Garou', 'Voyante', 'Sorcière', 'Salvateur', 'Chasseur', 'Corbeau', 'Cupidon', 'Pirate', 'Villageois']
        # roles in game
        self.roles = {}
        
        # assigned roles
        self.game = {}

        self.is_first_night = True

        # game planning
        # self.planning = [
        #     self.night,
        #     self.cupidon,
        #     self.amoureux,
        #     self.pirate,
        #     self.corbeau,
        #     self.voyante,
        #     self.loup_garou,
        #     self.sorciere,
        #     self.salvateur,
        #     self.day
        # ]

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)

    def start_game(self):
        if self.check_roles():
            self.started = True
            self.assign_roles()
            print("Game started")
            return True, self.game
        else:
            return False, "(nb_roles = " + str(self.get_nb_roles()) + ", nb_players = " + str(self.get_nb_players()) + ")"
        
    def assign_roles(self):
        all_roles = []
        for role in self.roles:
            for i in range(self.roles[role]):
                all_roles.append(role)

        random.shuffle(all_roles)

        for user in self.users:
            self.game[user] = all_roles.pop()
        
    def get_nb_players(self):
        return len(self.users)
    
    def get_nb_roles(self):
        nb_roles = 0
        for role in self.roles:
            nb_roles += self.roles[role]
        return nb_roles

    def generate_default_roles(self):
        nb_players = self.get_nb_players()

        self.roles = {}
        for role in self.all_roles:
            self.roles[role] = 0

        if nb_players <= 7:
            self.roles['Loup-Garou'] = 1
        elif nb_players <= 12:
            self.roles['Loup-Garou'] = 2
        elif nb_players <= 17:
            self.roles['Loup-Garou'] = 3
        else:
            self.roles['Loup-Garou'] = 4

        nb_assigned_roles = self.get_nb_roles()

        nb_roles_to_assign = nb_players - nb_assigned_roles
        
        for i in range(nb_roles_to_assign if nb_roles_to_assign < 7 else 7):
            self.roles[self.all_roles[1 + i]] += 1

        for i in range(nb_roles_to_assign - 7):
            self.roles['Villageois'] += 1

    def add_role(self, role):
        self.roles[role] += 1

    def remove_role(self, role):
        self.roles[role] -= 1
        if self.roles[role] < 0:
            self.roles[role] = 0

    def check_roles(self):
        nb_players = len(self.users)
        nb_roles = 0
        for role in self.roles:
            nb_roles += self.roles[role]

        return nb_players == nb_roles
    

