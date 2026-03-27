from views.menu_view import MenuView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController


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
        while True:
            self.menu_view.display_main_menu()
            choice = self.menu_view.get_user_choice(4)
            if choice == 1:
                self.player_controller.run()
            elif choice == 2:
                self.tournament_controller.run()
            elif choice == 3:
                self.report_controller.run()
            elif choice == 4:
                print("\nMerci et a bientot !")
                break
