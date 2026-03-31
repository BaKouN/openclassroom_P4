from datetime import datetime, timedelta

import questionary
from questionary import Choice
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

INSTRUCTION_SELECT = "(Fleches pour naviguer)"
INSTRUCTION_CHECKBOX = (
    "(Fleches + Espace = cocher, Entree = valider)"
)


def _format_date(val):
    """Accepte JJMMAAAA ou JJ/MM/AAAA, retourne JJ/MM/AAAA."""
    clean = val.replace("/", "")
    if len(clean) == 8 and clean.isdigit():
        return f"{clean[:2]}/{clean[2:4]}/{clean[4:]}"
    return val


def _validate_date(val):
    formatted = _format_date(val)
    try:
        datetime.strptime(formatted, "%d/%m/%Y")
        return True
    except ValueError:
        return "Format: JJ/MM/AAAA ou JJMMAAAA"


class TournamentView:
    """Gere l'affichage et la saisie pour les tournois."""

    def get_menu_choice(self, question, choices):
        console.print()
        console.print(
            "[bold blue]--- Gestion des Tournois ---[/bold blue]"
        )
        return questionary.select(
            question,
            choices=[
                Choice(title=label, value=value)
                for value, label in choices
            ],
            instruction=INSTRUCTION_SELECT,
        ).ask()

    def get_tournament_info(self):
        console.print("\n[bold]Nouveau tournoi[/bold]")
        today = datetime.now()
        default_start = today.strftime("%d/%m/%Y")
        default_end = (
            (today + timedelta(days=7)).strftime("%d/%m/%Y")
        )

        name = questionary.text("Nom du tournoi :").ask()
        location = questionary.text("Lieu :").ask()
        start_date = _format_date(questionary.text(
            "Date de debut (JJ/MM/AAAA ou JJMMAAAA) :",
            default=default_start,
            validate=_validate_date,
        ).ask())
        end_date = _format_date(questionary.text(
            "Date de fin (JJ/MM/AAAA ou JJMMAAAA) :",
            default=default_end,
            validate=_validate_date,
        ).ask())
        description = questionary.text(
            "Description (optionnel) :",
            default="",
        ).ask()
        number_of_rounds = questionary.text(
            "Nombre de tours :",
            default="4",
        ).ask()
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "number_of_rounds": int(number_of_rounds),
        }

    def select_tournament(self, tournaments):
        if not tournaments:
            console.print(
                "\n[yellow]Aucun tournoi enregistre.[/yellow]"
            )
            return None
        return questionary.select(
            "Choisir un tournoi",
            choices=[
                Choice(str(t), value=t) for t in tournaments
            ],
            instruction=INSTRUCTION_SELECT,
        ).ask()

    def select_players_for_tournament(self, players):
        selected = questionary.checkbox(
            "Selectionnez les joueurs",
            choices=[
                Choice(str(player), value=player)
                for player in players
            ],
            instruction=INSTRUCTION_CHECKBOX,
        ).ask()
        while not selected:
            console.print(
                "[red]Selectionnez au moins un joueur.[/red]"
            )
            selected = questionary.checkbox(
                "Selectionnez les joueurs",
                choices=[
                    Choice(str(player), value=player)
                    for player in players
                ],
                instruction=INSTRUCTION_CHECKBOX,
            ).ask()
        return selected

    def get_match_result(self, match):
        console.print(
            f"\n[bold]{match.player1}[/bold]"
            f" vs [bold]{match.player2}[/bold]"
        )
        return questionary.select(
            "Resultat",
            choices=[
                Choice(
                    f"Victoire {match.player1.first_name}",
                    value=(1, 0),
                ),
                Choice(
                    f"Victoire {match.player2.first_name}",
                    value=(0, 1),
                ),
                Choice("Match nul", value=(0.5, 0.5)),
            ],
            instruction=INSTRUCTION_SELECT,
        ).ask()

    def ask_start_tournament(self):
        return questionary.select(
            "Lancer le premier round ?",
            choices=[
                Choice("Oui", value=True),
                Choice("Non", value=False),
            ],
            instruction=INSTRUCTION_SELECT,
        ).ask()

    def ask_next_round(self):
        return questionary.select(
            "Lancer le round suivant ?",
            choices=[
                Choice("Oui", value=True),
                Choice("Non", value=False),
            ],
            instruction=INSTRUCTION_SELECT,
        ).ask()

    def display_round_info(self, round_instance):
        console.print()
        console.print(
            Panel(
                round_instance.name,
                style="bold magenta",
                expand=False,
            )
        )
        console.print(
            f"  Debut : {round_instance.start_datetime}"
        )
        if round_instance.is_finished():
            console.print(
                f"  Fin   : {round_instance.end_datetime}"
            )
        for match in round_instance.matches:
            console.print(f"  {match}")

    def display_tournament_results(self, tournament, standings):
        console.print()
        table = Table(
            title=f"Resultats : {tournament.name}",
            style="bold yellow",
        )
        table.add_column("Rang", justify="center", style="bold")
        table.add_column("Joueur")
        table.add_column(
            "Score", justify="center", style="cyan"
        )
        for rank, (player, score) in enumerate(
            standings, start=1
        ):
            table.add_row(
                str(rank), str(player), f"{score} pts"
            )
        console.print(table)

    def display_message(self, message):
        console.print(f"\n{message}")
