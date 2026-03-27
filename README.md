# Centre d'Echecs - Gestionnaire de Tournois

Application en ligne de commande pour gerer des tournois d'echecs selon le systeme suisse.

Developpee dans le cadre du projet 4 du parcours Developpeur d'Application Python - OpenClassrooms.

## Fonctionnalites

- Gestion des joueurs (ajout, liste alphabetique)
- Creation et gestion de tournois avec appariement automatique (systeme suisse)
- Sauvegarde automatique en JSON apres chaque action
- Reprise de tournoi interrompu
- 5 rapports : joueurs, tournois, details, joueurs par tournoi, tours et matchs
- Interface terminal interactive (menus navigables, tableaux formates, validation des saisies)

## Technologies

- **Python 3.x**
- **Rich** : affichage enrichi dans le terminal (tableaux, couleurs, panneaux)
- **Questionary** : menus interactifs avec navigation au clavier (fleches, checkboxes)
- **flake8** + **flake8-html** : conformite PEP 8

## Prerequis

- Python 3.x

## Installation

```bash
git clone <url-du-repo>
cd P4
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Utilisation

```bash
source venv/bin/activate
python main.py
```

## Lancer les tests

```bash
source venv/bin/activate
python -m unittest discover tests/ -v
```

## Generer le rapport flake8

```bash
source venv/bin/activate
flake8 --format=html --htmldir=flake8_rapport models/ views/ controllers/ utils/ main.py
```

Le rapport est disponible dans `flake8_rapport/index.html`.

## Structure du projet

```
P4/
├── main.py                  # Point d'entree
├── models/                  # Modeles de donnees
│   ├── player.py            # Joueur
│   ├── match.py             # Match
│   ├── round.py             # Tour
│   └── tournament.py        # Tournoi
├── views/                   # Affichage console
│   ├── menu_view.py         # Menu principal
│   ├── player_view.py       # Vues joueurs
│   ├── tournament_view.py   # Vues tournois
│   └── report_view.py       # Vues rapports
├── controllers/             # Logique metier
│   ├── main_controller.py   # Orchestrateur
│   ├── player_controller.py # Gestion joueurs
│   ├── tournament_controller.py # Gestion tournois
│   └── report_controller.py # Rapports
├── utils/
│   └── data_manager.py      # Persistance JSON
├── data/                    # Donnees JSON
├── tests/                   # Tests unitaires
├── flake8_rapport/          # Rapport PEP 8
├── requirements.txt
└── setup.cfg                # Config flake8
```
