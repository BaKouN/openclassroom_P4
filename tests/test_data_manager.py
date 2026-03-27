import os
import unittest
import tempfile
import shutil

from utils.data_manager import load_data, save_data


class TestDataManager(unittest.TestCase):
    """Tests pour le data manager (persistance JSON)."""

    def setUp(self):
        """Cree un dossier temporaire pour les tests."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Supprime le dossier temporaire apres chaque test."""
        shutil.rmtree(self.test_dir)

    def test_load_nonexistent_file_returns_empty_list(self):
        """Verifie qu'on recoit une liste vide si le fichier n'existe pas."""
        filepath = os.path.join(self.test_dir, "inexistant.json")
        result = load_data(filepath)
        self.assertEqual(result, [])

    def test_save_then_load(self):
        """Verifie que la donnee est intacte apres ecriture puis relecture."""
        filepath = os.path.join(self.test_dir, "test.json")
        data = [
            {"name": "Dupont", "score": 1},
            {"name": "Martin", "score": 0.5},
        ]
        save_data(filepath, data)
        loaded_data = load_data(filepath)
        self.assertEqual(loaded_data, data)

    def test_save_creates_missing_directories(self):
        """Verifie que save_data cree les dossiers manquants."""
        filepath = os.path.join(
            self.test_dir, "sous", "dossier", "test.json"
        )
        save_data(filepath, [{"test": True}])
        self.assertTrue(os.path.exists(filepath))


if __name__ == "__main__":
    unittest.main()
