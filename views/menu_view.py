class MenuView:
    """Gere l'affichage des menus et la saisie du choix utilisateur."""

    def display_main_menu(self):
        print("\n=== Centre d'Echecs ===\n")
        print("1. Gerer les joueurs")
        print("2. Gerer les tournois")
        print("3. Rapports")
        print("4. Quitter")

    def get_user_choice(self, max_choice):
        while True:
            choice = input("\n> ")
            if choice.isdigit() and 1 <= int(choice) <= max_choice:
                return int(choice)
            print(f"Choix invalide. Entrez un nombre entre 1 et {max_choice}.")
