class Match:
    """Represente un match entre deux joueurs."""

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.player1_score = None
        self.player2_score = None

    def is_played(self):
        return self.player1_score is not None

    def set_result(self, player1_score, player2_score):
        self.player1_score = player1_score
        self.player2_score = player2_score

    def to_tuple(self):
        return (
            [self.player1.national_id, self.player1_score],
            [self.player2.national_id, self.player2_score],
        )

    def __str__(self):
        return (
            f"{self.player1} ({self.player1_score}) "
            f"vs {self.player2} ({self.player2_score})"
        )

    def to_dict(self):
        return {
            "player1_id": self.player1.national_id,
            "player2_id": self.player2.national_id,
            "player1_score": self.player1_score,
            "player2_score": self.player2_score,
        }

    @staticmethod
    def _find_player(players, national_id):
        for player in players:
            if player.national_id == national_id:
                return player

    @classmethod
    def from_dict(cls, data, players):
        player1 = cls._find_player(players, data["player1_id"])
        player2 = cls._find_player(players, data["player2_id"])
        match = cls(player1, player2)
        match.player1_score = data["player1_score"]
        match.player2_score = data["player2_score"]
        return match
