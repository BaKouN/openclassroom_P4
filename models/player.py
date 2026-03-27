class Player:
    """Represente un joueur d'echecs."""

    def __init__(self, last_name : str=None, **kwargs):
        self.last_name = last_name or "Lebray"
        # self.first_name = first_name
        # self.birth_date = birth_date
        # self.national_id = national_id
        
        self.last_name = kwargs.get("last_name", None)
        if not self.last_name or not isinstance(self.last_name, str):
            print(
                f"Last name should be defined as a string, currently {self.last_name} ({type(self.last_name)})"
            )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id})"

    def to_dict(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "national_id": self.national_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birth_date=data["birth_date"],
            national_id=data["national_id"],
        )
