#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main module pour le projet de protocole graphique.
Ce fichier contient un exemple d'utilisation des classes EncodingMatrix et MatrixRenderer.
"""

import os
from encoder.matrix import EncodingMatrix
from encoder.renderer import MatrixRenderer

def main():
    """
    Exemple d'utilisation des classes EncodingMatrix et MatrixRenderer.
    Encode un texte dans une matrice et génère l'image correspondante.
    """
    # Texte plus long à encoder
    text = """Ce projet implémente un protocole de communication graphique 
    inspiré des QR codes. Il permet d'encoder des messages texte dans une matrice 
    qui peut être facilement scannée et décodée. Cette version supporte plusieurs 
    tailles de matrices pour accommoder des messages plus longs."""
    
    print(f"Longueur du texte: {len(text)} caractères")
    print(f"Texte à encoder:\n{text}\n")
    
    try:
        # Création de la matrice avec le texte
        # On utilise le niveau de correction d'erreur 'L' pour maximiser la capacité
        matrix = EncodingMatrix(text=text, error_correction='L')
        
        print(f"Version QR Code utilisée: {matrix.version.version_number}")
        print(f"Taille de la matrice: {matrix.version.size}x{matrix.version.size}")
        
        # Création du renderer avec des paramètres personnalisés
        renderer = MatrixRenderer(
            matrix=matrix,
            module_size=10,  # Taille réduite pour les grandes matrices
            margin=4,        # Marge en nombre de modules
            color_background=(255, 255, 255),  # Blanc
            color_module=(0, 0, 0)             # Noir
        )
        
        # Génération de l'image et sauvegarde dans le dossier output
        output_path = renderer.render(filename="encoded_long_text", output_dir="output")
        
        print(f"\nImage générée avec succès: {output_path}")
        
    except ValueError as e:
        print(f"\nErreur lors de l'encodage: {e}")


if __name__ == "__main__":
    main()
