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
