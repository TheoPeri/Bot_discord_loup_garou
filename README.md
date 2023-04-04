# LOUP GAROU HELPER

## Intro

Je suis un bot discord qui permet de faire des parties de loup garou via Discord !

Ce Bot permet de:
- ajouter des joueurs (les joueurs devront clicker sur un bouton via une invite faite avec !invite)
- ajouter des roles
- lancer la partie (les joueurs reçevrons par MP leur rôle)
- (pour le MJ) voir les roles des joueurs

Ce Bot ne permet pas de:
- faire une partie complete avec gestion des tour de jeu et tout (implémentable si beaucoup de demande)

En gros, ce bot a pour seule utilité d'alléger le travail du MJ.

Le bot a pour but d'être le plus userfrendly possible ! (pas besoin de lire de doc ou de !help long et chiant)
Si vous trouvez un bug ou une fonctionnalité pas très intuitive merci de me le dire :3

## Quick start

Requirements.txt => il faut juste installer le package python discord !

Il faut également mettre le token de votre bot dans la variable d'environnement TOKEN
exemple: export TOKEN=MYSUPERLONGTOKENXXXXXXXXXXXXXXXXXXXXXXXXX

Et lancé le main.py

Et voila !!! :3 (lancez la commande !help pour commencer)

## Motivation

On a voulu faire ce bot car:
- Je me faisait chier
- On galérait a faire des parties rapidement

Made by @TheoPeri for the Foxy community with <3

Discord de Foxy: https://discord.gg/BTHB2BrcTf
Venez nous faire un coucou ou faire une partie avec nous !

## Participer au dévelopement

Faite un fork suivie d'une PR.
Parlez avec moi pour tout question ou si vous êtes perdu !

### TODO

A faire:
- ajouter une fonctionnalité de confirmation de reception des roles avec page pour le MJ pour voir que tout le monde l'a reçu (difficulté: facile)
- refacto le code car c'est le bordel (difficulté: moyen / chiant)
- Faire la gestion complette d une game avec bouton (difficulté: difficile / aled / SOS)

### Architecture du code

main.py => appel botv2.py
botv2.py => gere les interaction discord pour les communiquer au game\_lg
game\_lg.py => gere la game en tant que tel
hellper.py => petites fonction utiles
