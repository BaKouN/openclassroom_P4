from collections import namedtuple
from enum import IntEnum

from views.report_view import ReportView


class ReportMenu(IntEnum):
    """Choix du menu des rapports."""
    ALL_PLAYERS = 1
    ALL_TOURNAMENTS = 2
    TOURNAMENT_DETAILS = 3
    TOURNAMENT_PLAYERS = 4
    TOURNAMENT_ROUNDS = 5
    EXIT = 6


MenuItem = namedtuple("MenuItem", ["value", "label", "action"])


class ReportController:
    """Gere la logique des rapports."""

    def __init__(self, players, tournaments):
        self.view = ReportView()
        self.players = players
        self.tournaments = tournaments

    def run(self):
        menu = [
            MenuItem(ReportMenu.ALL_PLAYERS, "Tous les joueurs (alphabetique)", self.report_all_players),
            MenuItem(ReportMenu.ALL_TOURNAMENTS, "Tous les tournois", self.report_all_tournaments),
            MenuItem(ReportMenu.TOURNAMENT_DETAILS, "Detail d'un tournoi", self.report_tournament_details),
            MenuItem(ReportMenu.TOURNAMENT_PLAYERS, "Joueurs d'un tournoi", self.report_tournament_players),
            MenuItem(ReportMenu.TOURNAMENT_ROUNDS, "Tours et matchs d'un tournoi", self.report_tournament_rounds),
            MenuItem(ReportMenu.EXIT, "Retour", None),
        ]
        choices = [(item.value, item.label) for item in menu]
        actions = {item.value: item.action for item in menu if item.action}

        while (choice := self.view.get_menu_choice(
            "Quel rapport ?", choices
        )) != ReportMenu.EXIT:
            actions.get(choice)()

    def report_all_players(self):
        sorted_players = sorted(
            self.players,
            key=lambda player: player.last_name.lower(),
        )
        self.view.display_all_players(sorted_players)

    def report_all_tournaments(self):
        self.view.display_all_tournaments(self.tournaments)

    def report_tournament_details(self):
        tournament = self.view.select_tournament(
            self.tournaments
        )
        if tournament:
            self.view.display_tournament_details(tournament)

    def report_tournament_players(self):
        tournament = self.view.select_tournament(
            self.tournaments
        )
        if tournament:
            sorted_players = sorted(
                tournament.players,
                key=lambda player: player.last_name.lower(),
            )
            self.view.display_tournament_players(
                tournament, sorted_players
            )

    def report_tournament_rounds(self):
        tournament = self.view.select_tournament(
            self.tournaments
        )
        if tournament:
            self.view.display_tournament_rounds(tournament)
