import unittest

from models.player import Player


class TestPlayer(unittest.TestCase):
    """Tests pour le modele Player."""

    def setUp(self):
        """Cree un joueur de test avant chaque test."""
        self.player = Player(
            last_name="Dupont",
            first_name="Jean",
            birth_date="15/01/1990",
            national_id="AB12345",
        )

    def test_str(self):
        """Verifie l'affichage du joueur."""
        result = str(self.player)
        self.assertEqual(result, "Jean Dupont (AB12345)")

    def test_to_dict_structure(self):
        """Verifie que to_dict produit les bonnes cles."""
        player_dict = self.player.to_dict()
        expected_keys = {"last_name", "first_name", "birth_date", "national_id"}
        self.assertEqual(set(player_dict.keys()), expected_keys)

    def test_to_dict_then_from_dict(self):
        """Verifie le cycle complet : objet -> dict -> objet."""
        player_dict = self.player.to_dict()
        recreated_player = Player.from_dict(player_dict)
        self.assertEqual(recreated_player.last_name, self.player.last_name)
        self.assertEqual(recreated_player.first_name, self.player.first_name)
        self.assertEqual(recreated_player.birth_date, self.player.birth_date)
        self.assertEqual(
            recreated_player.national_id, self.player.national_id
        )


if __name__ == "__main__":
    unittest.main()
