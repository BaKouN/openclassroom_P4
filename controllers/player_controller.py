from collections import namedtuple
from enum import IntEnum

from models.player import Player
from views.player_view import PlayerView
from utils.data_manager import load_data, save_data


PLAYERS_FILE = "data/players.json"


class PlayerMenu(IntEnum):
    """Choix du menu des joueurs."""
    ADD_PLAYER = 1
    LIST_PLAYERS = 2
    EXIT = 3


MenuItem = namedtuple("MenuItem", ["value", "label", "action"])


class PlayerController:
    """Gere la logique metier des joueurs."""

    def __init__(self):
        self.view = PlayerView()
        self.players = self._load_players()

    def _load_players(self):
        players_data = load_data(PLAYERS_FILE)
        return [Player.from_dict(data) for data in players_data]

    def _save_players(self):
        players_data = [player.to_dict() for player in self.players]
        save_data(PLAYERS_FILE, players_data)

    def run(self):
        menu = [
            MenuItem(PlayerMenu.ADD_PLAYER, "Ajouter un joueur", self.add_player),
            MenuItem(PlayerMenu.LIST_PLAYERS, "Lister les joueurs", self.list_players),
            MenuItem(PlayerMenu.EXIT, "Retour", None),
        ]
        choices = [(item.value, item.label) for item in menu]
        actions = {item.value: item.action for item in menu if item.action}

        while (choice := self.view.get_menu_choice(
            "Que voulez-vous faire ?", choices
        )) != PlayerMenu.EXIT:
            actions.get(choice)()

    def add_player(self):
        player_info = self.view.get_player_info()
        player = Player(
            last_name=player_info["last_name"],
            first_name=player_info["first_name"],
            birth_date=player_info["birth_date"],
            national_id=player_info["national_id"],
        )
        self.players.append(player)
        self._save_players()
        self.view.display_success(
            f"Joueur {player} ajoute avec succes."
        )

    def list_players(self):
        sorted_players = sorted(
            self.players, key=lambda player: player.last_name.lower()
        )
        self.view.display_players(sorted_players)
