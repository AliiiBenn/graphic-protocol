from typing import List, Tuple, Dict, cast
from enum import Enum

class EncodingMode(Enum):
    """Modes d'encodage supportés par le QR Code."""
    NUMERIC = 0b0001      # 0-9
    ALPHANUMERIC = 0b0010 # 0-9, A-Z, espace et $%*+-./:
    BYTE = 0b0100        # ISO-8859-1 / UTF-8
    KANJI = 0b1000       # Shift JIS (non implémenté pour l'instant)

class Version:
    """Représente une version de QR Code avec sa capacité."""
    
    # Table des capacités en octets pour chaque version
    # Format: version: (taille, {mode: {niveau_correction: capacité}})
    CAPACITIES = {
        1:  (21,  {EncodingMode.BYTE: {'L': 17, 'M': 14, 'Q': 11, 'H': 7}}),
        2:  (25,  {EncodingMode.BYTE: {'L': 32, 'M': 26, 'Q': 20, 'H': 14}}),
        3:  (29,  {EncodingMode.BYTE: {'L': 53, 'M': 42, 'Q': 32, 'H': 24}}),
        4:  (33,  {EncodingMode.BYTE: {'L': 78, 'M': 62, 'Q': 46, 'H': 34}}),
        5:  (37,  {EncodingMode.BYTE: {'L': 106, 'M': 84, 'Q': 60, 'H': 44}}),
        6:  (41,  {EncodingMode.BYTE: {'L': 134, 'M': 106, 'Q': 74, 'H': 58}}),
        7:  (45,  {EncodingMode.BYTE: {'L': 154, 'M': 122, 'Q': 86, 'H': 64}}),
        8:  (49,  {EncodingMode.BYTE: {'L': 192, 'M': 152, 'Q': 108, 'H': 84}}),
        9:  (53,  {EncodingMode.BYTE: {'L': 230, 'M': 180, 'Q': 130, 'H': 98}}),
        10: (57,  {EncodingMode.BYTE: {'L': 271, 'M': 213, 'Q': 151, 'H': 119}}),
        11: (61,  {EncodingMode.BYTE: {'L': 321, 'M': 251, 'Q': 177, 'H': 137}}),
        12: (65,  {EncodingMode.BYTE: {'L': 367, 'M': 287, 'Q': 203, 'H': 155}}),
        13: (69,  {EncodingMode.BYTE: {'L': 425, 'M': 331, 'Q': 241, 'H': 177}}),
        14: (73,  {EncodingMode.BYTE: {'L': 458, 'M': 362, 'Q': 258, 'H': 194}}),
        15: (77,  {EncodingMode.BYTE: {'L': 520, 'M': 412, 'Q': 292, 'H': 220}})
    }

    def __init__(self, version_number: int, size: int, capacity: Dict):
        """
        Args:
            version_number: Numéro de version (1-40)
            size: Taille de la matrice
            capacity: Dictionnaire des capacités par mode et niveau de correction
        """
        self.version_number = version_number
        self.size = size
        self.capacity = capacity

    @staticmethod
    def get_version_for_length(text: str, mode: EncodingMode, error_correction: str = 'M') -> 'Version':
        """
        Détermine la version minimale nécessaire pour encoder le texte.
        
        Args:
            text: Le texte à encoder
            mode: Mode d'encodage à utiliser
            error_correction: Niveau de correction d'erreur ('L', 'M', 'Q', 'H')
            
        Returns:
            Version: La version minimale capable de contenir le texte
            
        Raises:
            ValueError: Si le texte est trop long pour être encodé
        """
        text_length = len(text)
        
        # Parcourir les versions dans l'ordre croissant
        for version, (size, capacities) in sorted(Version.CAPACITIES.items()):
            if mode in capacities and error_correction in capacities[mode]:
                if text_length <= capacities[mode][error_correction]:
                    return Version(version, size, capacities[mode])
        
        raise ValueError(
            f"Le texte est trop long ({text_length} caractères) pour être encodé. "
            f"Maximum supporté: {Version.CAPACITIES[max(Version.CAPACITIES.keys())][1][mode][error_correction]} caractères"
        )

class DataEncoder:
    """Encode les données textuelles en bits selon les spécifications QR Code."""

    def __init__(self, text: str, error_correction: str = 'M'):
        """
        Args:
            text: Le texte à encoder
            error_correction: Niveau de correction d'erreur ('L', 'M', 'Q', 'H')
        """
        self.text = text
        self.error_correction = error_correction
        self.mode = self._determine_encoding_mode()
        self.version = Version.get_version_for_length(text, self.mode, error_correction)

    def _determine_encoding_mode(self) -> EncodingMode:
        """
        Détermine le mode d'encodage optimal pour le texte.
        Pour l'instant, on utilise toujours le mode BYTE.
        """
        return EncodingMode.BYTE

    def _encode_byte_mode(self) -> List[bool]:
        """Encode le texte en mode BYTE."""
        bits: List[bool] = []
        
        # Indicateur de mode (4 bits)
        mode_bits = format(EncodingMode.BYTE.value, '04b')
        bits.extend(bool(int(bit)) for bit in mode_bits)
        
        # Longueur des données (8 bits pour version 1-9, 16 bits pour version 10+)
        length_bits_count = 16 if self.version.version_number >= 10 else 8
        length_bits = format(len(self.text), f'0{length_bits_count}b')
        bits.extend(bool(int(bit)) for bit in length_bits)
        
        # Données
        for char in self.text:
            char_bits = format(ord(char), '08b')
            bits.extend(bool(int(bit)) for bit in char_bits)
        
        return bits

    def encode(self) -> Tuple[List[bool], Version]:
        """
        Encode le texte en une séquence de bits.
        
        Returns:
            Tuple contenant:
            - Liste de bits (booléens)
            - Version du QR Code nécessaire
        """
        if self.mode == EncodingMode.BYTE:
            bits = self._encode_byte_mode()
        else:
            raise NotImplementedError(f"Mode {self.mode} non implémenté")
            
        # Ajouter le terminateur (4 bits de 0)
        bits.extend([False, False, False, False])
        
        # Ajouter des 0 jusqu'à ce que la longueur soit multiple de 8
        while len(bits) % 8 != 0:
            bits.append(False)
            
        return bits, self.version 