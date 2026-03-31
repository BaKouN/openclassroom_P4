from collections import namedtuple
from enum import IntEnum

from views.menu_view import MenuView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController


class MainMenu(IntEnum):
    """Choix du menu principal."""
    PLAYERS = 1
    TOURNAMENTS = 2
    REPORTS = 3
    EXIT = 4


MenuItem = namedtuple("MenuItem", ["value", "label", "action"])


class MainController:
    """Point d'entree de l'application. Orchestre les controleurs."""

    def __init__(self):
        self.menu_view = MenuView()
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController(
            self.player_controller.players
        )
        self.report_controller = ReportController(
            self.player_controller.players,
            self.tournament_controller.tournaments,
        )

    def run(self):
        menu = [
            MenuItem(MainMenu.PLAYERS, "Gerer les joueurs", self.player_controller.run),
            MenuItem(MainMenu.TOURNAMENTS, "Gerer les tournois", self.tournament_controller.run),
            MenuItem(MainMenu.REPORTS, "Rapports", self.report_controller.run),
            MenuItem(MainMenu.EXIT, "Quitter", None),
        ]
        choices = [(item.value, item.label) for item in menu]
        actions = {item.value: item.action for item in menu if item.action}

        while (choice := self.menu_view.get_menu_choice(
            "Que voulez-vous faire ?", choices
        )) != MainMenu.EXIT:
            actions.get(choice)()

        self.menu_view.display_goodbye()
