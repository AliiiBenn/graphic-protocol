import unittest
import os
import shutil
from PIL import Image
from src.encoder.matrix import EncodingMatrix
from src.encoder.renderer import MatrixRenderer

class TestMatrixRenderer(unittest.TestCase):
    """
    Tests unitaires pour la classe MatrixRenderer.
    """
    
    def setUp(self):
        """Initialisation commune à tous les tests."""
        self.matrix = EncodingMatrix(size=21)
        self.test_output_dir = "test_output"
        
        # Créer le dossier de test s'il n'existe pas
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def tearDown(self):
        """Nettoyage après chaque test."""
        # Suppression du dossier de test et de son contenu
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
    
    def test_renderer_initialization(self):
        """Test que le renderer s'initialise correctement avec une matrice."""
        renderer = MatrixRenderer(self.matrix)
        self.assertEqual(renderer.matrix, self.matrix)
        self.assertEqual(renderer.module_size, 10)  # valeur par défaut
        self.assertEqual(renderer.margin, 4)        # valeur par défaut
        self.assertEqual(renderer.color_background, (255, 255, 255))  # blanc par défaut
        self.assertEqual(renderer.color_module, (0, 0, 0))            # noir par défaut
    
    def test_renderer_with_custom_params(self):
        """Test que le renderer accepte les paramètres personnalisés."""
        custom_module_size = 15
        custom_margin = 2
        custom_bg_color = (240, 240, 240)
        custom_module_color = (30, 30, 30)
        
        renderer = MatrixRenderer(
            self.matrix,
            module_size=custom_module_size,
            margin=custom_margin,
            color_background=custom_bg_color,
            color_module=custom_module_color
        )
        
        self.assertEqual(renderer.module_size, custom_module_size)
        self.assertEqual(renderer.margin, custom_margin)
        self.assertEqual(renderer.color_background, custom_bg_color)
        self.assertEqual(renderer.color_module, custom_module_color)
    
    def test_render_creates_file(self):
        """Test que la méthode render crée un fichier image."""
        renderer = MatrixRenderer(self.matrix)
        file_path = renderer.render(output_dir=self.test_output_dir)
        
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(file_path.endswith(".png"))
    
    def test_render_with_custom_filename(self):
        """Test que la méthode render accepte un nom de fichier personnalisé."""
        custom_filename = "custom_test_image"
        renderer = MatrixRenderer(self.matrix)
        file_path = renderer.render(filename=custom_filename, output_dir=self.test_output_dir)
        
        expected_path = os.path.join(self.test_output_dir, f"{custom_filename}.png")
        self.assertEqual(file_path, expected_path)
        self.assertTrue(os.path.exists(expected_path))
    
    def test_render_to_image(self):
        """Test que la méthode render_to_image retourne une instance de PIL.Image."""
        renderer = MatrixRenderer(self.matrix)
        image = renderer.render_to_image()
        
        self.assertIsInstance(image, Image.Image)
        
        # Vérifier que l'image a les dimensions attendues
        expected_size = (21 + 2 * 4) * 10  # (matrix_size + 2 * margin) * module_size
        self.assertEqual(image.size, (expected_size, expected_size))
    
    def test_invalid_matrix_type(self):
        """Test que le renderer rejette les types de matrice non valides."""
        with self.assertRaises(TypeError):
            MatrixRenderer(matrix=[[1, 0], [0, 1]])  # Liste 2D, pas une EncodingMatrix


if __name__ == "__main__":
    unittest.main() 