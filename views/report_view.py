class ReportView:
    """Gere l'affichage des rapports."""

    def display_report_menu(self):
        print("\n=== Rapports ===\n")
        print("1. Tous les joueurs (alphabetique)")
        print("2. Tous les tournois")
        print("3. Detail d'un tournoi (nom et dates)")
        print("4. Joueurs d'un tournoi (alphabetique)")
        print("5. Tours et matchs d'un tournoi")
        print("6. Retour")

    def display_all_players(self, players):
        print("\n=== Tous les joueurs ===\n")
        if not players:
            print("  Aucun joueur enregistre.")
            return
        for player in players:
            print(f"  {player.last_name}, {player.first_name}"
                  f" ({player.national_id})")

    def display_all_tournaments(self, tournaments):
        print("\n=== Tous les tournois ===\n")
        if not tournaments:
            print("  Aucun tournoi enregistre.")
            return
        for tournament in tournaments:
            print(f"  {tournament}")

    def display_tournament_details(self, tournament):
        print(f"\n=== {tournament.name} ===\n")
        print(f"  Lieu       : {tournament.location}")
        print(f"  Debut      : {tournament.start_date}")
        print(f"  Fin        : {tournament.end_date}")
        print(f"  Tours      : {tournament.current_round_number}"
              f"/{tournament.number_of_rounds}")
        print(f"  Description: {tournament.description}")

    def display_tournament_players(self, tournament, players):
        print(f"\n=== Joueurs de {tournament.name} ===\n")
        if not players:
            print("  Aucun joueur inscrit.")
            return
        for player in players:
            print(f"  {player.last_name}, {player.first_name}"
                  f" ({player.national_id})")

    def display_tournament_rounds(self, tournament):
        print(f"\n=== Tours de {tournament.name} ===\n")
        if not tournament.rounds:
            print("  Aucun tour joue.")
            return
        for round_instance in tournament.rounds:
            status = "Termine" if round_instance.is_finished() else "En cours"
            print(f"  --- {round_instance.name} ({status}) ---")
            print(f"  Debut : {round_instance.start_datetime}")
            if round_instance.end_datetime:
                print(f"  Fin   : {round_instance.end_datetime}")
            for match in round_instance.matches:
                print(f"    {match}")
            print()

    def select_tournament(self, tournaments):
        if not tournaments:
            print("\nAucun tournoi enregistre.")
            return None
        print("\n=== Choisir un tournoi ===\n")
        for index, tournament in enumerate(tournaments, start=1):
            print(f"  {index}. {tournament}")
        while True:
            choice = input("\nNumero du tournoi : ")
            if choice.isdigit() and 1 <= int(choice) <= len(tournaments):
                return tournaments[int(choice) - 1]
            print("Choix invalide.")
