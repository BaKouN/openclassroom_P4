import unittest

from models.player import Player
from models.match import Match


class TestMatch(unittest.TestCase):
    """Tests pour le modele Match."""

    def setUp(self):
        """Cree deux joueurs et un match avant chaque test."""
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
        self.match = Match(self.player1, self.player2)

    def test_set_result_player1_wins(self):
        """Verifie les scores apres une victoire du joueur 1."""
        self.match.set_result(1, 0)
        self.assertEqual(self.match.player1_score, 1)
        self.assertEqual(self.match.player2_score, 0)

    def test_set_result_player2_wins(self):
        """Verifie les scores apres une victoire du joueur 2."""
        self.match.set_result(0, 1)
        self.assertEqual(self.match.player1_score, 0)
        self.assertEqual(self.match.player2_score, 1)

    def test_set_result_draw(self):
        """Verifie les scores apres un match nul."""
        self.match.set_result(0.5, 0.5)
        self.assertEqual(self.match.player1_score, 0.5)
        self.assertEqual(self.match.player2_score, 0.5)

    def test_to_tuple(self):
        """Verifie le format tuple demande par les specs."""
        self.match.set_result(1, 0)
        result = self.match.to_tuple()
        self.assertEqual(result, (["AB12345", 1], ["CD67890", 0]))

    def test_to_dict_then_from_dict(self):
        """Verifie le cycle complet : objet -> dict -> objet."""
        self.match.set_result(0.5, 0.5)
        match_dict = self.match.to_dict()
        all_players = [self.player1, self.player2]
        recreated_match = Match.from_dict(match_dict, all_players)
        self.assertEqual(
            recreated_match.player1.national_id, "AB12345"
        )
        self.assertEqual(
            recreated_match.player2.national_id, "CD67890"
        )
        self.assertEqual(recreated_match.player1_score, 0.5)
        self.assertEqual(recreated_match.player2_score, 0.5)


if __name__ == "__main__":
    unittest.main()
