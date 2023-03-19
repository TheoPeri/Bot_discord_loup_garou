# create class Game
import random

class LGgame:
    def __init__(self):
        print("Game created")
        self.started = False
        self.users = []
        self.all_roles = ['Loup-Garou', 'Voyante', 'Sorcière', 'Salvateur', 'Chasseur', 'Corbeau', 'Cupidon', 'Pirate', 'Villageois']
        self.roles = {}

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)

    def start_game(self):
        self.started = True
        #self.assign_roles()

    def generate_default_roles(self):
        nb_players = len(self.users)

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

        self.roles['Voaynte'] = 1
        self.roles['Sorcière'] = 1

        nb_assigned_roles = 0
        for role in self.roles:
            nb_assigned_roles += self.roles[role]

        nb_roles_to_assign = nb_players - nb_assigned_roles
        
        for i in range(nb_roles_to_assign if nb_roles_to_assign < 5 else 5):
            self.roles[self.all_roles[3 + i]] += 1

        for i in range(nb_roles_to_assign - 5):
            self.roles['Villageois'] += 1

