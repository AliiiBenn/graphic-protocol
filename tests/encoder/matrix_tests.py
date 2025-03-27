import unittest
from src.encoder.matrix import EncodingMatrix

class TestEncodingMatrix(unittest.TestCase):

    def test_matrix_creation_valid_size(self):
        """Test de la création de matrice avec une taille valide."""
        size = 21
        matrix = EncodingMatrix(size)
        self.assertEqual(matrix.size, size)
        self.assertEqual(len(matrix.get_matrix()), size)
        self.assertEqual(len(matrix.get_matrix()[0]), size)

    def test_matrix_creation_invalid_size(self):
        """Test de la création de matrice avec une taille invalide (trop petite)."""
        with self.assertRaises(ValueError):
            EncodingMatrix(size=20)

    def test_position_markers_presence(self):
        """Test de la présence des marqueurs de position dans les coins."""
        matrix = EncodingMatrix(size=21)
        matrix_data = matrix.get_matrix()

        # Vérification du marqueur en haut à gauche (coin supérieur gauche à 1)
        self.assertEqual(matrix_data[0][0], 1)
        self.assertEqual(matrix_data[6][6], 1)

        # Vérification du marqueur en haut à droite (coin supérieur droit à 1)
        self.assertEqual(matrix_data[0][20], 1) # size - 1
        self.assertEqual(matrix_data[6][14], 1) # size - 7 -1 + 6 = size - 2

        # Vérification du marqueur en bas à gauche (coin inférieur gauche à 1)
        self.assertEqual(matrix_data[20][0], 1) # size - 1
        self.assertEqual(matrix_data[14][6], 1) # size - 7 -1 + 6 = size - 2

    def test_position_marker_structure(self):
        """Test de la structure basique d'un marqueur de position (7x7)."""
        matrix = EncodingMatrix(size=21)
        matrix_data = matrix.get_matrix()

        # Vérification d'une cellule à l'intérieur du carré blanc (devrait être 0) du marqueur haut-gauche
        self.assertEqual(matrix_data[3][3], 0)

        # Vérification d'une cellule sur le bord noir (devrait être 1) du marqueur haut-gauche
        self.assertEqual(matrix_data[0][0], 1)
        self.assertEqual(matrix_data[0][6], 1)
        self.assertEqual(matrix_data[6][0], 1)
        self.assertEqual(matrix_data[6][6], 1)


if __name__ == '__main__':
    unittest.main()
