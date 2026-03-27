import random

from models.tournament import Tournament
from models.round import Round
from models.match import Match
from views.tournament_view import TournamentView
from views.menu_view import MenuView
from utils.data_manager import load_data, save_data


TOURNAMENTS_FILE = "data/tournaments.json"


class TournamentController:
    """Gere la logique metier des tournois."""

    def __init__(self, players):
        self.view = TournamentView()
        self.menu_view = MenuView()
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
        while True:
            self.view.display_tournament_menu()
            choice = self.menu_view.get_user_choice(3)
            if choice == 1:
                self.create_tournament()
            elif choice == 2:
                self.resume_tournament()
            elif choice == 3:
                break

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
            f"Tournoi '{tournament.name}' cree avec {len(selected_players)} joueurs."
        )

    def resume_tournament(self):
        active_tournaments = [
            tournament for tournament in self.tournaments
            if not tournament.is_finished()
        ]
        if not active_tournaments:
            self.view.display_message("Aucun tournoi en cours.")
            return
        tournament = self.view.select_tournament(active_tournaments)
        if tournament is None:
            return
        self._play_round(tournament)

    def _play_round(self, tournament):
        round_number = tournament.current_round_number + 1
        round_name = f"Round {round_number}"
        new_round = Round(round_name)

        pairs, exempt_player = self._generate_pairs(tournament)

        if exempt_player:
            new_round.exempt_player_id = exempt_player.national_id
            self.view.display_message(
                f"{exempt_player} est exempt ce round et recoit 1 point."
            )

        for player1, player2 in pairs:
            match = Match(player1, player2)
            self.view.display_match_result_prompt(match)
            player1_score, player2_score = self.view.get_match_result()
            match.set_result(player1_score, player2_score)
            new_round.add_match(match)

        new_round.finish()
        tournament.add_round(new_round)
        self._save_tournaments()

        self.view.display_round_info(new_round)

        if tournament.is_finished():
            standings = self._get_standings(tournament)
            self.view.display_tournament_results(tournament, standings)
        else:
            self.view.display_message(
                f"{round_name} termine. "
                f"Round {round_number + 1}/{tournament.number_of_rounds} a suivre."
            )

    def _generate_pairs(self, tournament):
        players = list(tournament.players)

        if tournament.current_round_number == 0:
            random.shuffle(players)
        else:
            random.shuffle(players)
            players.sort(
                key=lambda player: self._get_player_score(
                    tournament, player
                ),
                reverse=True,
            )

        already_played = self._get_already_played(tournament)
        pairs = []
        available = list(players)

        while len(available) >= 2:
            player1 = available.pop(0)
            for i, player2 in enumerate(available):
                pair = frozenset([
                    player1.national_id,
                    player2.national_id,
                ])
                if pair not in already_played:
                    available.pop(i)
                    pairs.append((player1, player2))
                    break
            else:
                player2 = available.pop(0)
                pairs.append((player1, player2))

        exempt_player = available[0] if available else None
        return pairs, exempt_player

    def _get_player_score(self, tournament, player):
        score = 0
        for round_instance in tournament.rounds:
            if round_instance.exempt_player_id == player.national_id:
                score += 1
            for match in round_instance.matches:
                if match.player1.national_id == player.national_id:
                    score += match.player1_score
                elif match.player2.national_id == player.national_id:
                    score += match.player2_score
        return score

    def _get_already_played(self, tournament):
        played = set()
        for round_instance in tournament.rounds:
            for match in round_instance.matches:
                pair = frozenset([
                    match.player1.national_id,
                    match.player2.national_id,
                ])
                played.add(pair)
        return played

    def _get_standings(self, tournament):
        standings = []
        for player in tournament.players:
            score = self._get_player_score(tournament, player)
            standings.append((player, score))
        standings.sort(key=lambda item: item[1], reverse=True)
        return standings
