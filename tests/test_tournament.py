import unittest

from models.player import Player
from models.match import Match
from models.round import Round
from models.tournament import Tournament


class TestTournament(unittest.TestCase):
    """Tests pour le modele Tournament."""

    def setUp(self):
        """Cree un tournoi avec 4 joueurs et un round joue."""
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
        self.tournament = Tournament(
            name="Open de Paris",
            location="Paris",
            start_date="27/03/2026",
            end_date="28/03/2026",
            description="Tournoi amical",
        )
        for player in self.all_players:
            self.tournament.add_player(player)

    def test_add_round_increments_current_round(self):
        """Verifie que add_round incremente le compteur."""
        self.assertEqual(self.tournament.current_round_number, 0)
        round1 = Round("Round 1")
        self.tournament.add_round(round1)
        self.assertEqual(self.tournament.current_round_number, 1)
        round2 = Round("Round 2")
        self.tournament.add_round(round2)
        self.assertEqual(self.tournament.current_round_number, 2)

    def test_is_not_finished_before_all_rounds(self):
        """Verifie que le tournoi n'est pas fini avant le dernier round."""
        round1 = Round("Round 1")
        self.tournament.add_round(round1)
        self.assertFalse(self.tournament.is_finished())

    def test_is_finished_after_all_rounds(self):
        """Verifie que le tournoi est fini apres tous les rounds."""
        for i in range(self.tournament.number_of_rounds):
            self.tournament.add_round(Round(f"Round {i + 1}"))
        self.assertTrue(self.tournament.is_finished())

    def test_to_dict_then_from_dict(self):
        """Verifie le cycle complet avec rounds et matchs."""
        round1 = Round("Round 1")
        match1 = Match(self.player1, self.player2)
        match1.set_result(1, 0)
        match2 = Match(self.player3, self.player4)
        match2.set_result(0.5, 0.5)
        round1.add_match(match1)
        round1.add_match(match2)
        round1.finish()
        self.tournament.add_round(round1)

        tournament_dict = self.tournament.to_dict()
        recreated = Tournament.from_dict(tournament_dict, self.all_players)

        self.assertEqual(recreated.name, "Open de Paris")
        self.assertEqual(recreated.location, "Paris")
        self.assertEqual(recreated.current_round_number, 1)
        self.assertEqual(len(recreated.players), 4)
        self.assertEqual(len(recreated.rounds), 1)
        self.assertEqual(len(recreated.rounds[0].matches), 2)


if __name__ == "__main__":
    unittest.main()
