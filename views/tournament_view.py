class TournamentView:
    """Gere l'affichage et la saisie pour les tournois."""

    def display_tournament_menu(self):
        print("\n=== Gestion des Tournois ===\n")
        print("1. Creer un tournoi")
        print("2. Reprendre un tournoi")
        print("3. Retour")

    def get_tournament_info(self):
        print("\n--- Nouveau tournoi ---\n")
        name = input("Nom du tournoi : ")
        location = input("Lieu : ")
        start_date = input("Date de debut (JJ/MM/AAAA) : ")
        end_date = input("Date de fin (JJ/MM/AAAA) : ")
        description = input("Description (optionnel) : ")
        number_of_rounds = input("Nombre de tours (defaut: 4) : ")
        if not number_of_rounds:
            number_of_rounds = 4
        else:
            number_of_rounds = int(number_of_rounds)
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "number_of_rounds": number_of_rounds,
        }

    def display_tournaments(self, tournaments):
        if not tournaments:
            print("\nAucun tournoi enregistre.")
            return
        print("\n=== Liste des tournois ===\n")
        for index, tournament in enumerate(tournaments, start=1):
            print(f"  {index}. {tournament}")

    def select_tournament(self, tournaments):
        self.display_tournaments(tournaments)
        if not tournaments:
            return None
        while True:
            choice = input("\nChoisir un tournoi (numero) : ")
            if choice.isdigit() and 1 <= int(choice) <= len(tournaments):
                return tournaments[int(choice) - 1]
            print("Choix invalide.")

    def display_available_players(self, players):
        print("\n=== Joueurs disponibles ===\n")
        for index, player in enumerate(players, start=1):
            print(f"  {index}. {player}")

    def select_players_for_tournament(self, players):
        self.display_available_players(players)
        while True:
            selected_ids = input(
                "\nEntrez les numeros de la liste "
                "(ex: 1,2,3) : "
            )
            try:
                indices = [
                    int(number.strip()) - 1
                    for number in selected_ids.split(",")
                ]
                selected = [players[index] for index in indices]
                if selected:
                    return selected
                print("Selectionnez au moins un joueur.")
            except (ValueError, IndexError):
                print("Saisie invalide. Utilisez les numeros de la liste.")

    def display_match_result_prompt(self, match):
        print(f"\n{match.player1} vs {match.player2}")
        print("1. Victoire joueur 1")
        print("2. Victoire joueur 2")
        print("3. Match nul")

    def get_match_result(self):
        while True:
            choice = input("> ")
            if choice == "1":
                return 1, 0
            elif choice == "2":
                return 0, 1
            elif choice == "3":
                return 0.5, 0.5
            print("Choix invalide. Entrez 1, 2 ou 3.")

    def display_round_info(self, round_instance):
        print(f"\n=== {round_instance.name} ===")
        print(f"Debut : {round_instance.start_datetime}")
        if round_instance.is_finished():
            print(f"Fin : {round_instance.end_datetime}")
        for match in round_instance.matches:
            print(f"  {match}")

    def display_tournament_results(self, tournament, standings):
        print(f"\n=== Resultats : {tournament.name} ===\n")
        for rank, (player, score) in enumerate(standings, start=1):
            print(f"  {rank}. {player} - {score} pts")

    def display_message(self, message):
        print(f"\n{message}")
