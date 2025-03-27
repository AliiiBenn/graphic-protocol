from image_detector import ImageDetector
from matrix_decoder import MatrixDecoder

def decode_from_image(image_path: str) -> str:
    """
    Décode le texte contenu dans une image.
    
    Args:
        image_path: Chemin vers l'image à décoder
        
    Returns:
        str: Texte décodé
    """
    # Détecter et extraire la matrice
    detector = ImageDetector()
    matrix = detector.detect_from_image(image_path)
    if matrix is None:
        raise ValueError("Aucune matrice détectée dans l'image")
    
    # Décoder la matrice en texte
    decoder = MatrixDecoder()
    text = decoder.decode(matrix)
    
    return text

if __name__ == "__main__":
    # Exemple d'utilisation
    try:
        image_path = "example.png"  # Remplacer par le chemin de votre image
        text = decode_from_image(image_path)
        print(f"Texte décodé : {text}")
    except Exception as e:
        print(f"Erreur lors du décodage : {e}") 