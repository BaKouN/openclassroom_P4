# Projet 4 OpenClassrooms - Centre d'Echecs

## Contexte
Application de gestion de tournois d'echecs pour un club local.
Programme autonome, hors ligne, en Python, lance depuis la console (`python main.py`).
Compatible Windows/Mac/Linux.

## Architecture
**Design pattern MVC obligatoire** avec 3 packages minimum :
- `models/` - Entites et donnees
- `views/` - Affichage console (menus, rapports, saisie utilisateur)
- `controllers/` - Logique metier

Toujours utiliser des **instances de classe** (jamais des dicts bruts pour les entites).

## Modeles

### Joueur (Player)
- nom_de_famille: str
- prenom: str
- date_de_naissance: str (format a definir)
- identifiant_national: str (format: 2 lettres + 5 chiffres, ex: AB12345)

### Tournoi (Tournament)
- nom: str
- lieu: str
- date_debut: str
- date_fin: str
- nombre_de_tours: int (defaut: 4)
- tour_actuel: int
- tours: list[Round]
- joueurs: list[Player]
- description: str

### Tour / Round
- nom: str ("Round 1", "Round 2", etc.)
- date_heure_debut: datetime (auto a la creation)
- date_heure_fin: datetime (auto quand marque termine)
- matchs: list[Match]

### Match
- Stocke comme tuple: ([joueur1, score1], [joueur2, score2])
- Points: gagnant=1, perdant=0, nul=0.5

## Algorithme de generation des paires
1. **Round 1** : melanger tous les joueurs aleatoirement
2. **Rounds suivants** :
   - Trier joueurs par total de points (decroissant)
   - Associer dans l'ordre (1v2, 3v4, etc.)
   - Si meme nombre de points -> choix aleatoire
   - Eviter les matchs deja joues (si J1 a deja joue contre J2, associer J1 avec J3)
3. Tirage au sort blanc/noir (pas d'equilibrage necessaire)

## Rapports a generer
- Liste de tous les joueurs par ordre alphabetique
- Liste de tous les tournois
- Nom et dates d'un tournoi donne
- Liste des joueurs d'un tournoi par ordre alphabetique
- Liste de tous les tours et matchs d'un tournoi

## Persistance des donnees
- **Format** : fichiers JSON
- **Emplacement** : `data/` (joueurs et tournois)
- Sauvegarde automatique apres chaque modification
- Charger toutes les donnees au demarrage
- Restaurer l'etat complet entre les executions

## Qualite du code
- **PEP 8** stricte
- **flake8** avec `--max-line-length 119`
- Rapport **flake8-html** dans `flake8_rapport/` (0 erreur requise)
- `requirements.txt` pour les dependances
- `README.md` avec instructions d'execution et generation rapport flake8

## Livrables
1. Repository GitHub contenant :
   - Code complet de l'application
   - `flake8_rapport/` (rapport HTML sans erreur)
   - `README.md`

## Soutenance (30 min)
- **Presentation (15 min)** : demo complete
  - Creer et jouer un tournoi du debut a la fin
  - Generer un rapport
  - Sauvegarder/charger l'etat du programme
  - Montrer la structure MVC avec exemples de code
- **Discussion (10 min)** : evaluateur joue le role d'Elie (club d'echecs), questions sur le code
- **Debrief (5 min)**

**IMPORTANT** : Le code doit etre maitrise ligne par ligne. L'evaluateur peut demander de coder en live.

## Competences evaluees
1. Ecrire un code Python robuste en utilisant la PEP 8
2. Structurer le code d'un programme Python en utilisant un design pattern (MVC)
3. Utiliser la programmation orientee objet pour developper un programme Python

## Structure cible du projet
```
P4/
├── main.py
├── models/
│   ├── __init__.py
│   ├── player.py
│   ├── tournament.py
│   ├── round.py
│   └── match.py
├── views/
│   ├── __init__.py
│   ├── menu_view.py
│   ├── player_view.py
│   ├── tournament_view.py
│   └── report_view.py
├── controllers/
│   ├── __init__.py
│   ├── main_controller.py
│   ├── player_controller.py
│   ├── tournament_controller.py
│   └── report_controller.py
├── data/
│   ├── players.json
│   └── tournaments.json
├── flake8_rapport/
├── requirements.txt
├── README.md
├── setup.cfg (ou .flake8)
└── .gitignore
```
