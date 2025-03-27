import os
from PIL import Image, ImageDraw
from pathlib import Path
from .matrix import EncodingMatrix

class MatrixRenderer:
    """
    Classe qui génère une image à partir d'une matrice d'encodage (EncodingMatrix)
    et la sauvegarde dans un dossier output.
    """

    def __init__(self, matrix, module_size=10, margin=4, color_background=(255, 255, 255), color_module=(0, 0, 0)):
        """
        Initialise le renderer avec une matrice et des paramètres de rendu.

        Args:
            matrix (EncodingMatrix): La matrice d'encodage à rendre
            module_size (int): Taille en pixels de chaque module (cellule)
            margin (int): Marge en nombre de modules autour de la matrice
            color_background (tuple): Couleur RGB de l'arrière-plan (blanc par défaut)
            color_module (tuple): Couleur RGB des modules actifs (noir par défaut)
        """
        if not isinstance(matrix, EncodingMatrix):
            raise TypeError("Le paramètre 'matrix' doit être une instance de EncodingMatrix")
        
        self.matrix = matrix
        self.module_size = module_size
        self.margin = margin
        self.color_background = color_background
        self.color_module = color_module

    def render(self, filename=None, output_dir="output"):
        """
        Génère une image à partir de la matrice et la sauvegarde dans le dossier output.

        Args:
            filename (str, optional): Nom du fichier de sortie (sans extension). Si non fourni, 
                                     un nom par défaut sera généré.
            output_dir (str): Chemin du dossier de sortie (relatif ou absolu)

        Returns:
            str: Chemin complet du fichier sauvegardé
        """
        # Calcul des dimensions de l'image
        matrix_data = self.matrix.get_matrix()
        matrix_size = len(matrix_data)
        
        # Taille totale en pixels avec marges
        total_size = (matrix_size + 2 * self.margin) * self.module_size
        
        # Création d'une nouvelle image
        image = Image.new("RGB", (total_size, total_size), self.color_background)
        draw = ImageDraw.Draw(image)
        
        # Dessiner les modules
        for i in range(matrix_size):
            for j in range(matrix_size):
                if matrix_data[i][j] == 1:  # Module noir/actif
                    # Calcul des coordonnées du rectangle à dessiner
                    x0 = (j + self.margin) * self.module_size
                    y0 = (i + self.margin) * self.module_size
                    x1 = x0 + self.module_size - 1
                    y1 = y0 + self.module_size - 1
                    
                    # Dessin du rectangle
                    draw.rectangle([x0, y0, x1, y1], fill=self.color_module)
        
        # Création du dossier output s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
        
        # Génération du nom de fichier s'il n'est pas fourni
        if filename is None:
            filename = f"matrix_{matrix_size}x{matrix_size}"
        
        # Chemin complet du fichier
        file_path = os.path.join(output_dir, f"{filename}.png")
        
        # Sauvegarde de l'image
        image.save(file_path)
        
        return file_path

    def render_to_image(self):
        """
        Génère une image PIL à partir de la matrice sans la sauvegarder.

        Returns:
            PIL.Image: L'image générée
        """
        # Calcul des dimensions de l'image
        matrix_data = self.matrix.get_matrix()
        matrix_size = len(matrix_data)
        
        # Taille totale en pixels avec marges
        total_size = (matrix_size + 2 * self.margin) * self.module_size
        
        # Création d'une nouvelle image
        image = Image.new("RGB", (total_size, total_size), self.color_background)
        draw = ImageDraw.Draw(image)
        
        # Dessiner les modules
        for i in range(matrix_size):
            for j in range(matrix_size):
                if matrix_data[i][j] == 1:  # Module noir/actif
                    # Calcul des coordonnées du rectangle à dessiner
                    x0 = (j + self.margin) * self.module_size
                    y0 = (i + self.margin) * self.module_size
                    x1 = x0 + self.module_size - 1
                    y1 = y0 + self.module_size - 1
                    
                    # Dessin du rectangle
                    draw.rectangle([x0, y0, x1, y1], fill=self.color_module)
        
        return image 