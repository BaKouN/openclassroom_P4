from collections import namedtuple
from enum import IntEnum

from models.tournament import Tournament
from models.round import Round
from models.match import Match
from views.tournament_view import TournamentView
from utils.data_manager import load_data, save_data


TOURNAMENTS_FILE = "data/tournaments.json"


class TournamentMenu(IntEnum):
    """Choix du menu des tournois."""
    CREATE = 1
    RESUME = 2
    EXIT = 3


MenuItem = namedtuple("MenuItem", ["value", "label", "action"])


class TournamentController:
    """Gere la logique metier des tournois."""

    def __init__(self, players):
        self.view = TournamentView()
        self.players = players
        self.tournaments = self._load_tournaments()

    def _load_tournaments(self):
        tournaments_data = load_data(TOURNAMENTS_FILE)
        return [
            Tournament.from_dict(data, self.players)
            for data in tournaments_data
        ]

    def _save_tournaments(self):
        tournaments_data = [
            tournament.to_dict() for tournament in self.tournaments
        ]
        save_data(TOURNAMENTS_FILE, tournaments_data)

    def run(self):
        menu = [
            MenuItem(TournamentMenu.CREATE, "Creer un tournoi", self.create_tournament),
            MenuItem(TournamentMenu.RESUME, "Reprendre un tournoi", self.resume_tournament),
            MenuItem(TournamentMenu.EXIT, "Retour", None),
        ]
        choices = [(item.value, item.label) for item in menu]
        actions = {item.value: item.action for item in menu if item.action}

        while (choice := self.view.get_menu_choice(
            "Que voulez-vous faire ?", choices
        )) != TournamentMenu.EXIT:
            actions.get(choice)()

    def create_tournament(self):
        tournament_info = self.view.get_tournament_info()
        tournament = Tournament(
            name=tournament_info["name"],
            location=tournament_info["location"],
            start_date=tournament_info["start_date"],
            end_date=tournament_info["end_date"],
            description=tournament_info["description"],
            number_of_rounds=tournament_info["number_of_rounds"],
        )
        selected_players = self.view.select_players_for_tournament(
            self.players
        )
        for player in selected_players:
            tournament.add_player(player)
        self.tournaments.append(tournament)
        self._save_tournaments()
        self.view.display_message(
            f"Tournoi '{tournament.name}' cree avec "
            f"{len(selected_players)} joueurs."
        )
        if self.view.ask_start_tournament():
            self._play_tournament(tournament)

    def resume_tournament(self):
        active_tournaments = [
            tournament for tournament in self.tournaments
            if not tournament.is_finished()
        ]
        if not active_tournaments:
            self.view.display_message("Aucun tournoi en cours.")
            return
        tournament = self.view.select_tournament(
            active_tournaments
        )
        if tournament is None:
            return
        self._play_tournament(tournament)

    def _play_tournament(self, tournament):
        while not tournament.is_finished():
            unfinished = self._get_unfinished_round(tournament)
            if unfinished:
                self._resume_round(tournament, unfinished)
            else:
                self._play_round(tournament)
            if not tournament.is_finished():
                if not self.view.ask_next_round():
                    break

    def _play_round(self, tournament):
        round_number = tournament.current_round_number + 1
        round_name = f"Round {round_number}"
        new_round = Round(round_name)

        pairs, exempt_player = tournament.generate_pairs()

        if exempt_player:
            new_round.exempt_player_id = exempt_player.national_id
            self.view.display_message(
                f"{exempt_player} est exempt ce round "
                f"et recoit 1 point."
            )

        for player1, player2 in pairs:
            match = Match(player1, player2)
            new_round.add_match(match)

        tournament.rounds.append(new_round)
        self._save_tournaments()

        self._play_unfinished_matches(tournament, new_round)

    def _play_unfinished_matches(self, tournament, round_instance):
        for match in round_instance.matches:
            if not match.is_played():
                player1_score, player2_score = (
                    self.view.get_match_result(match)
                )
                match.set_result(player1_score, player2_score)
                self._save_tournaments()

        round_instance.finish()
        tournament.current_round_number = len([
            r for r in tournament.rounds if r.is_finished()
        ])
        self._save_tournaments()

        self.view.display_round_info(round_instance)

        if tournament.is_finished():
            standings = tournament.get_standings()
            self.view.display_tournament_results(
                tournament, standings
            )
        else:
            next_round = tournament.current_round_number + 1
            self.view.display_message(
                f"{round_instance.name} termine. "
                f"Round {next_round}"
                f"/{tournament.number_of_rounds} "
                f"a suivre."
            )

    def _get_unfinished_round(self, tournament):
        for round_instance in tournament.rounds:
            if not round_instance.is_finished():
                return round_instance
        return None

    def _resume_round(self, tournament, unfinished_round):
        played = sum(
            1 for m in unfinished_round.matches
            if m.is_played()
        )
        total = len(unfinished_round.matches)
        self.view.display_message(
            f"Reprise de {unfinished_round.name} "
            f"({played}/{total} matchs joues)."
        )
        self._play_unfinished_matches(
            tournament, unfinished_round
        )
