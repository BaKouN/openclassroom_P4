import questionary
from questionary import Choice
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

INSTRUCTION_SELECT = "(Fleches pour naviguer)"


class ReportView:
    """Gere l'affichage des rapports."""

    def get_menu_choice(self, question, choices):
        console.print()
        console.print(
            "[bold yellow]--- Rapports ---[/bold yellow]"
        )
        return questionary.select(
            question,
            choices=[
                Choice(title=label, value=value)
                for value, label in choices
            ],
            instruction=INSTRUCTION_SELECT,
        ).ask()

    def display_all_players(self, players):
        if not players:
            console.print(
                "\n[yellow]Aucun joueur enregistre.[/yellow]"
            )
            return
        table = Table(title="Tous les joueurs", style="cyan")
        table.add_column("Nom", style="bold")
        table.add_column("Prenom")
        table.add_column("ID National", style="dim")
        for player in players:
            table.add_row(
                player.last_name,
                player.first_name,
                player.national_id,
            )
        console.print()
        console.print(table)

    def display_all_tournaments(self, tournaments):
        if not tournaments:
            console.print(
                "\n[yellow]Aucun tournoi enregistre.[/yellow]"
            )
            return
        table = Table(title="Tous les tournois", style="cyan")
        table.add_column("Nom", style="bold")
        table.add_column("Lieu")
        table.add_column("Debut")
        table.add_column("Fin")
        table.add_column("Tours", justify="center")
        for tournament in tournaments:
            table.add_row(
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date,
                f"{tournament.current_round_number}"
                f"/{tournament.number_of_rounds}",
            )
        console.print()
        console.print(table)

    def display_tournament_details(self, tournament):
        console.print()
        table = Table(
            title=tournament.name,
            style="cyan",
            show_header=False,
        )
        table.add_column("Champ", style="bold")
        table.add_column("Valeur")
        table.add_row("Lieu", tournament.location)
        table.add_row("Debut", tournament.start_date)
        table.add_row("Fin", tournament.end_date)
        table.add_row(
            "Tours",
            f"{tournament.current_round_number}"
            f"/{tournament.number_of_rounds}",
        )
        table.add_row("Description", tournament.description)
        console.print(table)

    def display_tournament_players(self, tournament, players):
        if not players:
            console.print(
                "\n[yellow]Aucun joueur inscrit.[/yellow]"
            )
            return
        table = Table(
            title=f"Joueurs de {tournament.name}",
            style="cyan",
        )
        table.add_column("Nom", style="bold")
        table.add_column("Prenom")
        table.add_column("ID National", style="dim")
        for player in players:
            table.add_row(
                player.last_name,
                player.first_name,
                player.national_id,
            )
        console.print()
        console.print(table)

    def display_tournament_rounds(self, tournament):
        if not tournament.rounds:
            console.print(
                "\n[yellow]Aucun tour joue.[/yellow]"
            )
            return
        console.print()
        console.print(
            Panel(
                f"Tours de {tournament.name}",
                style="bold magenta",
                expand=False,
            )
        )
        for round_instance in tournament.rounds:
            status = (
                "[green]Termine[/green]"
                if round_instance.is_finished()
                else "[yellow]En cours[/yellow]"
            )
            console.print(
                f"\n  [bold]{round_instance.name}[/bold]"
                f" ({status})"
            )
            console.print(
                f"  Debut : {round_instance.start_datetime}"
            )
            if round_instance.end_datetime:
                console.print(
                    f"  Fin   : {round_instance.end_datetime}"
                )
            for match in round_instance.matches:
                console.print(f"    {match}")

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
