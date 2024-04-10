# Hex-et-combinatoires

Ce repertoire contient le projet de programmation 30 : Hex-Ta(c)tique

## Choix des langages

Ce projet sera codé en Python principalement pour le code fonctionnel du module Hex et la partie combinatoire.
La partie Web sera codée en Python, mais pourra changer pour du JS ou autre selon les besoins.

## Modules

Le projet sera divisé en plusieurs modules :
  - board: le plateau de jeu sur lequel les donnees vont être modifiées
  - game logic : pour la logique du jeu et les règles pour l'implémentation
  - game ui: l'interface graphique offerte à l'utilisateur pour interagir avec ce jeu
  - d'autres modules pourront être rajoutés par la suite


## Choix de conception

Le projet sera codé en utilisant les principes de la programmation orientée objet pour assurer la modularité
et la lisibilité du code.
L'objet principal sera le plateau de jeu, qui contiendra les données et les méthodes pour les manipuler.
Un objet `hexboard` sera créé pour chaque partie, et les données seront modifiées en fonction des actions des joueurs.
Il contiendra les données du plateau de jeu, les méthodes pour les manipuler, et les méthodes pour vérifier si un joueur
a gagné.

## Tests

De nombreux tests seront mis en place à l'aide d'outils vu au courant du semestre 5 pour assurer la performance 
et le bon fonctionnement du projet


## Comment lancer le projet

Pour lancer le projet, il suffit de suivre les instructions suivantes :
  - Installer python 3.8 ou plus
  - Installer les dépendances avec la commande `pip install -r requirements.txt`
  - Naviguer au bon endroit (`src/main`)
  - Lancer le serveur avec la commande `python app.py`
  - Ouvrir un navigateur et aller à l'adresse `http://localhost:5000/`


## Documentation

Une documentation extensive sera fournie tout au long du projet pour chaque partie de code afin d'assurer
la lisibilité et l'évolution facile du code dans le temps

## Liens utiles

Lien github: https://github.com/Ivan23BG/hex-et-combinatoires.git

Lien discord: https://discord.gg/69Cqp2s4

Lien hex: https://fr.wikipedia.org/wiki/Hex

Lien drive: https://drive.google.com/drive/folders/19xrowJzPldTjy6qT1XCUEM4UbI7ud9vA

Lien TODO list : https://hex-game.atlassian.net/jira/core/projects/HEC/board
