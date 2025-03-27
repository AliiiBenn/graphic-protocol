from typing import List, Optional, Union, cast
from encoder.data_encoder import DataEncoder, Version






class EncodingMatrix:
    """
    Représente la matrice d'encodage pour un protocole graphique (type QR Code).
    """

    def __init__(self, text: Optional[str] = None, size: Optional[int] = None, error_correction: str = 'M'):
        """
        Initialise une matrice pour encoder un message.
        
        Args:
            text: Le texte à encoder. Si None, crée une matrice vide de taille donnée.
            size: Taille de la matrice. Requis si text est None.
            error_correction: Niveau de correction d'erreur ('L', 'M', 'Q', 'H')
        """
        if text is None and size is None:
            raise ValueError("Soit text soit size doit être fourni")
            
        if text is not None:
            # Encoder le texte et obtenir la version nécessaire
            self.encoder = DataEncoder(text, error_correction=error_correction)
            self.bits, self.version = self.encoder.encode()
            self.size = self.version.size
        else:
            size = cast(int, size)  # On sait que size n'est pas None ici
            if size < 21:  # Taille minimale pour QR Code version 1
                raise ValueError("La taille de la matrice doit être au minimum 21.")
            self.size = size
            self.bits = []
            self.version = Version(1, size, {})  # Version factice pour matrice vide
            
        # Initialiser la matrice avec None
        self.matrix: List[List[Optional[bool]]] = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        # Ajouter les éléments fixes
        self._add_position_markers()
        if text is not None:
            self._place_data()

    def _add_position_markers(self) -> None:
        """
        Ajoute les marqueurs de positionnement aux coins de la matrice.
        """
        marker_size = 7
        # Marqueur en haut à gauche
        self._draw_square(0, 0, marker_size)
        # Marqueur en haut à droite
        self._draw_square(0, self.size - marker_size, marker_size)
        # Marqueur en bas à gauche
        self._draw_square(self.size - marker_size, 0, marker_size)

    def _draw_square(self, row_start: int, col_start: int, square_size: int) -> None:
        """
        Dessine un carré de position avec le motif standard QR Code.
        """
        for i in range(square_size):
            for j in range(square_size):
                if (i < 1 or i > square_size - 2) or (j < 1 or j > square_size - 2):
                    self.matrix[row_start + i][col_start + j] = True  # Bordure noire
                elif (i < 2 or i > square_size - 3) or (j < 2 or j > square_size - 3):
                    self.matrix[row_start + i][col_start + j] = False  # Anneau blanc
                else:
                    self.matrix[row_start + i][col_start + j] = True  # Centre noir

    def _place_data(self) -> None:
        """
        Place les bits de données dans la matrice selon le motif en zigzag.
        Pour l'instant, utilise un motif simple de gauche à droite, de bas en haut.
        """
        if not self.bits:
            return
            
        bit_index = 0
        # Parcourir la matrice de bas en haut, de droite à gauche
        for col in range(self.size - 1, -1, -2):  # Commencer par la dernière colonne
            for row in range(self.size - 1, -1, -1):  # De bas en haut
                for x in range(2):  # Traiter deux colonnes à la fois
                    current_col = col - x
                    if current_col < 0:
                        continue
                        
                    # Vérifier si la cellule est disponible (pas un marqueur de position)
                    if self.matrix[row][current_col] is None:
                        if bit_index < len(self.bits):
                            self.matrix[row][current_col] = self.bits[bit_index]
                            bit_index += 1

    def get_matrix(self) -> List[List[Optional[bool]]]:
        """
        Retourne la matrice actuelle.
        """
        return self.matrix

    def __str__(self) -> str:
        """
        Retourne une représentation string de la matrice.
        """
        matrix_str = ""
        for row in self.matrix:
            row_str = "".join(['1' if cell is True else '0' if cell is False else ' ' for cell in row])
            matrix_str += row_str + "\n"
        return matrix_str
