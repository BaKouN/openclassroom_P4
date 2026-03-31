import questionary
from questionary import Choice
from rich.console import Console
from rich.panel import Panel

console = Console()


class MenuView:
    """Gere l'affichage des menus et la saisie du choix utilisateur."""

    def get_menu_choice(self, question, choices):
        console.print()
        console.print(
            Panel("Centre d'Echecs", style="bold cyan", expand=False)
        )
        return questionary.select(
            question,
            choices=[
                Choice(title=label, value=value)
                for value, label in choices
            ],
            instruction="(Fleches pour naviguer)",
        ).ask()

    def display_goodbye(self):
        console.print("\n[bold cyan]Merci et a bientot ![/bold cyan]")
