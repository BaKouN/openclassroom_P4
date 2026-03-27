from views.report_view import ReportView


class ReportController:
    """Gere la logique des rapports."""

    def __init__(self, players, tournaments):
        self.view = ReportView()
        self.players = players
        self.tournaments = tournaments

    def run(self):
        while True:
            choice = self.view.get_report_menu_choice()
            if choice == 1:
                self.report_all_players()
            elif choice == 2:
                self.report_all_tournaments()
            elif choice == 3:
                self.report_tournament_details()
            elif choice == 4:
                self.report_tournament_players()
            elif choice == 5:
                self.report_tournament_rounds()
            elif choice == 6:
                break

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
