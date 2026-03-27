import unittest

from models.player import Player
from models.match import Match
from models.round import Round


class TestRound(unittest.TestCase):
    """Tests pour le modele Round."""

    def setUp(self):
        """Cree un round avec 4 joueurs et 2 matchs."""
        self.player1 = Player(
            last_name="Dupont",
            first_name="Jean",
            birth_date="15/01/1990",
            national_id="AB12345",
        )
        self.player2 = Player(
            last_name="Martin",
            first_name="Sophie",
            birth_date="20/06/1985",
            national_id="CD67890",
        )
        self.player3 = Player(
            last_name="Durand",
            first_name="Pierre",
            birth_date="10/03/1995",
            national_id="EF11111",
        )
        self.player4 = Player(
            last_name="Leroy",
            first_name="Marie",
            birth_date="05/12/1988",
            national_id="GH22222",
        )
        self.all_players = [
            self.player1, self.player2,
            self.player3, self.player4,
        ]
        self.round = Round("Round 1")
        self.match1 = Match(self.player1, self.player2)
        self.match1.set_result(1, 0)
        self.match2 = Match(self.player3, self.player4)
        self.match2.set_result(0.5, 0.5)

    def test_add_match(self):
        """Verifie que les matchs sont bien ajoutes au round."""
        self.round.add_match(self.match1)
        self.round.add_match(self.match2)
        self.assertEqual(len(self.round.matches), 2)

    def test_is_not_finished_by_default(self):
        """Verifie qu'un round n'est pas termine a la creation."""
        self.assertFalse(self.round.is_finished())
        self.assertIsNone(self.round.end_datetime)

    def test_finish_sets_end_datetime(self):
        """Verifie que finish() remplit la date de fin."""
        self.round.finish()
        self.assertTrue(self.round.is_finished())
        self.assertIsNotNone(self.round.end_datetime)

    def test_str_in_progress(self):
        """Verifie l'affichage d'un round en cours."""
        self.assertIn("En cours", str(self.round))

    def test_str_finished(self):
        """Verifie l'affichage d'un round termine."""
        self.round.finish()
        self.assertIn("Termine", str(self.round))

    def test_to_dict_then_from_dict(self):
        """Verifie le cycle complet avec plusieurs matchs."""
        self.round.add_match(self.match1)
        self.round.add_match(self.match2)
        self.round.finish()
        round_dict = self.round.to_dict()
        recreated_round = Round.from_dict(round_dict, self.all_players)
        self.assertEqual(recreated_round.name, "Round 1")
        self.assertEqual(len(recreated_round.matches), 2)
        self.assertIsNotNone(recreated_round.end_datetime)
        self.assertEqual(
            recreated_round.matches[0].player1.national_id, "AB12345"
        )
        self.assertEqual(
            recreated_round.matches[1].player1.national_id, "EF11111"
        )


if __name__ == "__main__":
    unittest.main()
