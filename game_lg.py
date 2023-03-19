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
        self.planning = [
            self.night,
        #     self.cupidon,
        #     self.amoureux,
        #     self.pirate,
        #     self.corbeau,
            self.voyante,
            self.loup_garou,
            self.sorciere,
        #     self.salvateur,
            self.day,
        ]

        self.current_step = -1
        self.real_users = []

        self.users_to_kill = []

    def next_step(self):
        self.current_step += 1
        if self.current_step >= len(self.planning):
            self.current_step = 0

        return self.planning[self.current_step]()

    def night(self):
        return "NUIT", "Le village s'endort"
    
    def day(self):
        text = "Le village se réveille: " + ", ".join([usr for usr in self.game.keys() if usr not in self.users_to_kill])

        text_chasseur = ""
        for user in self.users_to_kill:
            if self.game[user] == "Chasseur":
                text_chasseur += f"\nLe chasseur {user} est mort, il doit tirer sur un autre joueur => !shoot <user> pour tirer sur qqn"

        if len(self.users_to_kill) > 0:
            text += "\nLes personnes tuées sont : " + ", ".join(self.users_to_kill)
            for user in self.users_to_kill:
                info = self.kill(user)
                if info != "":
                    text += " et " + info
            self.users_to_kill = []

        text += text_chasseur

        text += "\nQui voulez-vous éliminer ? => !vote <user> pour voter qqn, !next pour skip le vote (égalité)"

        return "JOUR", text
    
    def shoot_user(self, user):
        if user not in self.game:
            return "SHOOT ERROR", "Ce joueur n'est pas dans la partie (wrong name???)"
        
        info = self.kill(user)
        text = "Le joueur " + user + " a été tué"
        if info != "":
            text += " et " + info
        return "SHOOT", text
    
    def kill(self, user):
        if user not in self.game:
            return "Ce joueur n'est pas dans la partie (wrong name??? already dead???)"
        
        del self.game[user]
        return ""
        
        
    
    def loup_garou(self):
        text = "Les loups-garous se réveillent : " + ", ".join([usr for usr, pers in self.game.items() if pers == "Loup-Garou"])
        text += "\nQui voulez-vous manger ? => !eat <user> pour manger qqn, !next pour skip le vote (égalité)"
        return "LOUPS-GAROUS", text
    
    def voyante(self):
        text = "La voyante se réveille : " + ", ".join([usr for usr, pers in self.game.items() if pers == "Voyante"])
        text += "\nQui voulez-vous regarder ? => !see <user> pour regarder qqn"
        return "VOYANTE", text
    
    def sorciere(self):
        text = "La sorcière se réveille : " + ", ".join([usr for usr, pers in self.game.items() if pers == "Sorcière"])
        text += "\nLes personnes tuées sont : " + ", ".join(self.users_to_kill)
        text += "\nQui voulez-vous sauver ? => !save <user> pour sauver qqn"
        text += "\nQui voulez-vous empoisonner ? => !poison <user> pour empoisonner qqn"
        return "SORCIERE", text
    
    def save_user(self, user):
        if user not in self.game:
            return "SAVE ERROR", "Ce joueur n'est pas dans la partie (wrong name???)"
        
        if user in self.users_to_kill:
            self.users_to_kill.remove(user)
        return "SAVE", "Le joueur " + user + " a été sauvé !"
    
    def poison_user(self, user):
        if user not in self.game:
            return "POISON ERROR", "Ce joueur n'est pas dans la partie (wrong name???)"
        
        if user not in self.users_to_kill:
            self.users_to_kill.append(user)
        return "POISON", "Le joueur " + user + " a été empoisonné !"
    
    def see_user(self, user):
        if user not in self.game:
            return "SEE ERROR", "Ce joueur n'est pas dans la partie (wrong name???)"
        return "SEE", "Le joueur " + user + " est un " + self.game[user]
    
    def eat_user(self, user):
        if user not in self.game:
            return "EAT ERROR", "Ce joueur n'est pas dans la partie (wrong name???)"
        
        if user not in self.users_to_kill:
            self.users_to_kill.append(user)
        return "EAT", "Le joueur " + user + " a été mangé !"

    
    def vote_user(self, user):
        if user not in self.game:
            return "VOTE ERROR", "Ce joueur n'est pas dans la partie (wrong name???)"
        
        text = "Le joueur " + user + " a été éliminé"
        info = self.kill(user)
        if info != "":
            text += " et " + info
        return "VOTE", text
    
    def check_end(self):
        nb_lg = 0
        nb_villageois = 0
        
        for perso in self.game.values():
            if perso == 'Loup-Garou':
                nb_lg += 1
            else:
                nb_villageois += 1

        if nb_lg == 0:
            return "VILLAGEOIS", "Les villageois ont gagné"
        elif nb_lg >= nb_villageois:
            return "LOUPS-GAROUS", "Les loups-garous ont gagné"
        else:
            return None, None


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
    

