from datetime import datetime

from models.match import Match


class Round:
    """Represente un tour dans un tournoi d'echecs."""

    def __init__(self, name):
        self.name = name
        self.matches = []
        self.start_datetime = datetime.now().isoformat()
        self.end_datetime = None

    def add_match(self, match):
        self.matches.append(match)

    def finish(self):
        self.end_datetime = datetime.now().isoformat()

    def is_finished(self):
        return self.end_datetime is not None

    def __str__(self):
        status = "Termine" if self.is_finished() else "En cours"
        return f"{self.name} - {status} ({len(self.matches)} matchs)"

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
        }

    @classmethod
    def from_dict(cls, data, players):
        round_instance = cls(data["name"])
        round_instance.start_datetime = data["start_datetime"]
        round_instance.end_datetime = data["end_datetime"]
        for match_data in data["matches"]:
            match = Match.from_dict(match_data, players)
            round_instance.matches.append(match)
        return round_instance
