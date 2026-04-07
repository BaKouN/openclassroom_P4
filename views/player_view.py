import re
from datetime import datetime

import questionary

from questionary import Choice
from rich.console import Console
from rich.table import Table

console = Console()


def _format_birth_date(val):
    """Accepte JJMMAAAA ou JJ/MM/AAAA, retourne JJ/MM/AAAA."""
    clean = val.replace("/", "")
    if len(clean) == 8 and clean.isdigit():
        return f"{clean[:2]}/{clean[2:4]}/{clean[4:]}"
    return val


def _validate_birth_date(val):
    formatted = _format_birth_date(val)
    try:
        datetime.strptime(formatted, "%d/%m/%Y")
        return True
    except ValueError:
        return "Format attendu : JJ/MM/AAAA ou JJMMAAAA"


def _validate_national_id(val):
    if re.match(r"^[A-Z]{2}\d{5}$", val):
        return True
    return "Format: 2 lettres + 5 chiffres (ex: AB12345)"


class PlayerView:
    """Gere l'affichage et la saisie pour les joueurs."""

    def get_menu_choice(self, question, choices):
        console.print()
        console.print(
            "[bold green]--- Gestion des Joueurs ---[/bold green]"
        )
        return questionary.select(
            question,
            choices=[
                Choice(title=label, value=value)
                for value, label in choices
            ],
            instruction="(Fleches pour naviguer)",
        ).ask()

    def get_player_info(self):
        console.print("\n[bold]Nouveau joueur[/bold]")
        last_name = questionary.text("Nom de famille").ask()
        first_name = questionary.text("Prénom").ask()
        birth_date = _format_birth_date(questionary.text(
            "Date de naissance (JJ/MM/AAAA ou JJMMAAAA)",
            validate=_validate_birth_date,
        ).ask())
        national_id = questionary.text(
            "Identifiant National",
            validate=_validate_national_id,
            filter=str.upper,
        ).ask()

        return {
            "last_name": last_name,
            "first_name": first_name,
            "birth_date": birth_date,
            "national_id": national_id
        }

    def display_players(self, players):
        if not players:
            console.print("\n[yellow]Aucun joueur enregistre.[/yellow]")
            return
        table = Table(title="Liste des joueurs", style="cyan")
        table.add_column("Nom", style="bold")
        table.add_column("Prenom")
        table.add_column("Date de naissance")
        table.add_column("ID National", style="dim")
        for player in players:
            table.add_row(
                player.last_name,
                player.first_name,
                player.birth_date,
                player.national_id,
            )
        console.print()
        console.print(table)

    def display_success(self, message):
        console.print(f"\n[bold green]{message}[/bold green]")
