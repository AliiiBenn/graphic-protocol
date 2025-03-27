import numpy as np
import cv2
from typing import Tuple, Optional, List
from PIL import Image

class ImageDetector:
    """
    Classe responsable de la détection et de l'extraction de la matrice depuis une image.
    Utilise OpenCV pour la détection des marqueurs de position et la transformation perspective.
    """

    def __init__(self):
        """Initialise le détecteur d'image."""
        pass

    def detect_from_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Détecte et extrait la matrice depuis une image.
        
        Args:
            image_path: Chemin vers l'image à analyser
            
        Returns:
            numpy.ndarray: Matrice binaire extraite, ou None si aucune matrice n'est détectée
        """
        # Charger l'image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Impossible de charger l'image: {image_path}")
            
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Appliquer un seuil adaptatif pour binariser l'image
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Trouver les marqueurs de position
        markers = self._find_position_markers(binary)
        if len(markers) != 3:
            return None
            
        # Extraire la matrice
        matrix = self._extract_matrix(binary, markers)
        return matrix

    def _find_position_markers(self, binary_image: np.ndarray) -> List[Tuple[int, int]]:
        """
        Trouve les trois marqueurs de position dans l'image binaire.
        
        Args:
            binary_image: Image binaire à analyser
            
        Returns:
            Liste des coordonnées (x, y) des centres des marqueurs de position
        """
        # Trouver les contours
        contours, _ = cv2.findContours(
            binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filtrer les contours qui ressemblent à des marqueurs de position
        markers = []
        for contour in contours:
            # Calculer les propriétés du contour
            area = cv2.contourArea(contour)
            if area < 100:  # Ignorer les petits contours
                continue
                
            # Approximer le contour en polygone
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            
            # Les marqueurs de position sont carrés (4 côtés)
            if len(approx) == 4:
                # Calculer le centre du contour
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    markers.append((cx, cy))
        
        return markers[:3]  # Retourner les 3 premiers marqueurs trouvés

    def _extract_matrix(self, binary_image: np.ndarray, markers: List[Tuple[int, int]]) -> np.ndarray:
        """
        Extrait la matrice à partir de l'image binaire et des marqueurs de position.
        
        Args:
            binary_image: Image binaire
            markers: Liste des coordonnées des marqueurs de position
            
        Returns:
            numpy.ndarray: Matrice binaire extraite
        """
        # Pour l'instant, on retourne une version simplifiée
        # TODO: Implémenter la transformation perspective et l'extraction précise
        height, width = binary_image.shape
        size = min(height, width)
        matrix = np.zeros((size, size), dtype=np.uint8)
        
        # Convertir en matrice binaire (0 et 1)
        matrix = (binary_image[0:size, 0:size] > 127).astype(np.uint8)
        
        return matrix 