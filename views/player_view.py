class PlayerView:
    """Gere l'affichage et la saisie pour les joueurs."""

    def display_player_menu(self):
        print("\n=== Gestion des Joueurs ===\n")
        print("1. Ajouter un joueur")
        print("2. Lister les joueurs")
        print("3. Retour")

    def get_player_info(self):
        print("\n--- Nouveau joueur ---\n")
        last_name = input("Nom de famille : ")
        first_name = input("Prenom : ")
        birth_date = input("Date de naissance (JJ/MM/AAAA) : ")
        national_id = input("Identifiant national (ex: AB12345) : ")
        return {
            "last_name": last_name,
            "first_name": first_name,
            "birth_date": birth_date,
            "national_id": national_id,
        }

    def display_players(self, players):
        if not players:
            print("\nAucun joueur enregistre.")
            return
        print("\n=== Liste des joueurs ===\n")
        for player in players:
            print(f"  {player}")

    def display_success(self, message):
        print(f"\n{message}")
