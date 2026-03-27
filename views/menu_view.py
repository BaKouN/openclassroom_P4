import questionary
from questionary import Choice
from rich.console import Console
from rich.panel import Panel

console = Console()


class MenuView:
    """Gere l'affichage des menus et la saisie du choix utilisateur."""

    def get_main_menu_choice(self):
        console.print()
        console.print(
            Panel("Centre d'Echecs", style="bold cyan", expand=False)
        )
        return questionary.select(
            "Que voulez-vous faire ?",
            choices=[
                Choice("Gerer les joueurs", value=1),
                Choice("Gerer les tournois", value=2),
                Choice("Rapports", value=3),
                Choice("Quitter", value=4),
            ],
            instruction="(Fleches pour naviguer)",
        ).ask()

    def display_goodbye(self):
        console.print("\n[bold cyan]Merci et a bientot ![/bold cyan]")
