from models.player import Player
from views.player_view import PlayerView
from views.menu_view import MenuView
from utils.data_manager import load_data, save_data


PLAYERS_FILE = "data/players.json"


class PlayerController:
    """Gere la logique metier des joueurs."""

    def __init__(self):
        self.view = PlayerView()
        self.menu_view = MenuView()
        self.players = self._load_players()

    def _load_players(self):
        players_data = load_data(PLAYERS_FILE)
        return [Player.from_dict(data) for data in players_data]

    def _save_players(self):
        players_data = [player.to_dict() for player in self.players]
        save_data(PLAYERS_FILE, players_data)

    def run(self):
        while True:
            self.view.display_player_menu()
            choice = self.menu_view.get_user_choice(3)
            if choice == 1:
                self.add_player()
            elif choice == 2:
                self.list_players()
            elif choice == 3:
                break

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
