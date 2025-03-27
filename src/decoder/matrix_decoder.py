from typing import List, Optional, Tuple
import numpy as np
from encoder.data_encoder import EncodingMode, Version

class MatrixDecoder:
    """
    Décode une matrice binaire en texte selon le protocole graphique.
    """

    def __init__(self):
        """Initialise le décodeur de matrice."""
        pass

    def decode(self, matrix: np.ndarray) -> str:
        """
        Décode une matrice binaire en texte.
        
        Args:
            matrix: Matrice binaire numpy (0 et 1)
            
        Returns:
            str: Texte décodé
            
        Raises:
            ValueError: Si la matrice ne peut pas être décodée
        """
        # Vérifier la taille de la matrice
        size = matrix.shape[0]
        if size < 21:  # Taille minimale pour version 1
            raise ValueError("Matrice trop petite pour être un code valide")
            
        # Extraire les bits de données
        bits = self._extract_data_bits(matrix)
        if not bits:
            raise ValueError("Impossible d'extraire les bits de données")
            
        # Décoder les bits en texte
        text = self._decode_bits(bits)
        return text

    def _extract_data_bits(self, matrix: np.ndarray) -> List[bool]:
        """
        Extrait les bits de données de la matrice en suivant le motif en zigzag.
        
        Args:
            matrix: Matrice binaire numpy
            
        Returns:
            Liste de bits (booléens)
        """
        bits = []
        size = matrix.shape[0]
        
        # Parcourir la matrice dans le même ordre que l'encodage
        for col in range(size - 1, -1, -2):
            for row in range(size - 1, -1, -1):
                for x in range(2):
                    current_col = col - x
                    if current_col < 0:
                        continue
                        
                    # Vérifier si la cellule n'est pas un marqueur de position
                    if not self._is_position_marker(row, current_col, size):
                        bits.append(bool(matrix[row, current_col]))
        
        return bits

    def _is_position_marker(self, row: int, col: int, size: int) -> bool:
        """
        Vérifie si une cellule fait partie d'un marqueur de position.
        
        Args:
            row: Index de ligne
            col: Index de colonne
            size: Taille de la matrice
            
        Returns:
            bool: True si la cellule fait partie d'un marqueur de position
        """
        marker_size = 7
        
        # Vérifier les trois coins
        if (row < marker_size and col < marker_size) or \
           (row < marker_size and col >= size - marker_size) or \
           (row >= size - marker_size and col < marker_size):
            return True
            
        return False

    def _decode_bits(self, bits: List[bool]) -> str:
        """
        Décode une liste de bits en texte.
        
        Args:
            bits: Liste de bits (booléens)
            
        Returns:
            str: Texte décodé
        """
        # Extraire le mode d'encodage (4 premiers bits)
        if len(bits) < 4:
            raise ValueError("Pas assez de bits pour décoder le mode")
            
        mode_bits = bits[:4]
        mode_value = self._bits_to_int(mode_bits)
        mode = EncodingMode(mode_value)
        
        # Extraire la longueur des données
        current_pos = 4
        length_bits_count = 8  # Pour version 1-9
        if len(bits) < current_pos + length_bits_count:
            raise ValueError("Pas assez de bits pour décoder la longueur")
            
        length_bits = bits[current_pos:current_pos + length_bits_count]
        data_length = self._bits_to_int(length_bits)
        current_pos += length_bits_count
        
        # Extraire et décoder les données
        if mode == EncodingMode.BYTE:
            return self._decode_byte_mode(bits[current_pos:], data_length)
        else:
            raise NotImplementedError(f"Mode d'encodage {mode} non supporté")

    def _bits_to_int(self, bits: List[bool]) -> int:
        """Convertit une liste de bits en entier."""
        return int(''.join('1' if bit else '0' for bit in bits), 2)

    def _decode_byte_mode(self, bits: List[bool], length: int) -> str:
        """
        Décode les bits en mode BYTE.
        
        Args:
            bits: Liste de bits à décoder
            length: Nombre de caractères à décoder
            
        Returns:
            str: Texte décodé
        """
        if len(bits) < length * 8:
            raise ValueError("Pas assez de bits pour décoder les données")
            
        text = ""
        for i in range(length):
            char_bits = bits[i * 8:(i + 1) * 8]
            char_value = self._bits_to_int(char_bits)
            text += chr(char_value)
            
        return text 