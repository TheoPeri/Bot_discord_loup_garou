# create class Game
import random

class LGgame:
    def __init__(self):
        print("Game created")
        self.started = False
        # users in game
        self.users = []
        # roles possible
        self.all_roles = ['Loup-Garou', 'Voyante', 'Sorcière', 'Salvateur', 'Chasseur', 'Corbeau', 'Cupidon', 'Pirate', 'Villageois', 'Ancien', 'Ange', 'BoucEmissaire', 'Idiot', 'JoueurFlute', 'PetiteFille', 'Voleur']
        # roles in game
        self.roles = {}
        
        # assigned roles
        self.game = {}

        # discord users
        self.real_users = None

    ### user manager

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
        
    def get_nb_players(self):
        return len(self.users)

    ### roles manager

    def add_role(self, role):
        self.roles[role] += 1

    def remove_role(self, role):
        if role in self.roles:
            self.roles[role] -= 1
            if self.roles[role] <= 0:
                del self.roles[role]
    
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

        nb_roles_to_assign = nb_players - self.get_nb_roles()
        
        for i in range(nb_roles_to_assign if nb_roles_to_assign < (len(self.all_roles) - 1) else (len(self.all_roles) - 1)):
            self.roles[self.all_roles[1 + i]] += 1

        nb_roles_to_assign = nb_players - self.get_nb_roles()
        # complete with villageois
        for i in range(nb_roles_to_assign):
            self.roles['Villageois'] += 1
        
    def assign_roles(self):
        all_roles = []
        for role in self.roles:
            for i in range(self.roles[role]):
                all_roles.append(role)

        random.shuffle(all_roles)

        for user in self.users:
            self.game[user] = all_roles.pop()

    ### validity check

    def check_roles(self):
        nb_players = len(self.users)
        nb_roles = 0
        for role in self.roles:
            nb_roles += self.roles[role]

        return nb_players == nb_roles
    
    ### starter

    def start_game(self):
        if self.check_roles():
            self.started = True
            self.assign_roles()
            print("Game started")
            return True, self.game
        else:
            return False, "(nb_roles = " + str(self.get_nb_roles()) + ", nb_players = " + str(self.get_nb_players()) + ")"
    

