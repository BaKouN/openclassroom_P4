from enum import IntEnum
from views.report_view import ReportView

class ReportControllerChoice(IntEnum):
    REPORT_ALL_PLAYERS = 1
    REPORT_ALL_TOURNAMENTS = 2
    REPORT_TOURNAMENT_DETAILS = 3
    REPORT_TOURNAMENT_PLAYERS = 4
    REPORT_TOURNAMENT_ROUNDS = 5
    EXIT = 6

class ReportController:
    """Gere la logique des rapports."""

    def __init__(self, players, tournaments):
        self.view = ReportView()
        self.players = players
        self.tournaments = tournaments

    def run(self):
        options = (
            (ReportControllerChoice.REPORT_ALL_PLAYERS, lambda _: self.report_all_players()),
            (ReportControllerChoice.REPORT_ALL_TOURNAMENTS, lambda _: self.report_all_tournaments()),
            (ReportControllerChoice.REPORT_TOURNAMENT_DETAILS, lambda _: self.report_tournament_details()),
            (ReportControllerChoice.REPORT_TOURNAMENT_PLAYERS, lambda _: self.report_tournament_players()),
            (ReportControllerChoice.REPORT_TOURNAMENT_ROUNDS, lambda _: self.report_tournament_rounds()),
        )

        while (choice := self.view.get_report_menu_choice()) != ReportControllerChoice.EXIT:
            for option in options:
                if choice == option[0]:
                    option[1](self)

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
