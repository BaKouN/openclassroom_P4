import random

from models.round import Round


class Tournament:
    """Represente un tournoi d'echecs."""

    DEFAULT_NUMBER_OF_ROUNDS = 4

    def __init__(self, name, location, start_date, end_date,
                 description="", number_of_rounds=None):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = (
            number_of_rounds or self.DEFAULT_NUMBER_OF_ROUNDS
        )
        self.current_round_number = 0
        self.rounds = []
        self.players = []
        self.description = description

    def add_player(self, player):
        self.players.append(player)

    def add_round(self, round_instance):
        self.rounds.append(round_instance)
        self.current_round_number = len(self.rounds)

    def is_finished(self):
        return self.current_round_number >= self.number_of_rounds

    def _get_player_score(self, player):
        score = 0
        for round_instance in self.rounds:
            if round_instance.exempt_player_id == player.national_id:
                score += 1
            for match in round_instance.matches:
                if not match.is_played():
                    continue
                if match.player1.national_id == player.national_id:
                    score += match.player1_score
                elif match.player2.national_id == player.national_id:
                    score += match.player2_score
        return score

    def _get_already_played(self):
        return {
            frozenset([match.player1.national_id, match.player2.national_id])
            for round_instance in self.rounds
            for match in round_instance.matches
        }

    def get_standings(self):
        standings = [
            (player, self._get_player_score(player))
            for player in self.players
        ]
        return sorted(standings, key=lambda item: item[1], reverse=True)

    def generate_pairs(self):
        players = list(self.players)
        random.shuffle(players)
        if self.current_round_number > 0:
            players.sort(
                key=lambda player: self._get_player_score(player),
                reverse=True,
            )

        already_played = self._get_already_played()
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

    def __str__(self):
        return (
            f"{self.name} - {self.location} "
            f"({self.start_date} / {self.end_date})"
        )

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round_number": self.current_round_number,
            "rounds": [
                round_instance.to_dict()
                for round_instance in self.rounds
            ],
            "players": [
                player.national_id for player in self.players
            ],
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data, all_players):
        tournament = cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data["description"],
        )
        tournament.number_of_rounds = data["number_of_rounds"]
        tournament.current_round_number = data["current_round_number"]

        for player_id in data["players"]:
            for player in all_players:
                if player.national_id == player_id:
                    tournament.players.append(player)
                    break

        for round_data in data["rounds"]:
            round_instance = Round.from_dict(
                round_data, tournament.players
            )
            tournament.rounds.append(round_instance)

        return tournament
