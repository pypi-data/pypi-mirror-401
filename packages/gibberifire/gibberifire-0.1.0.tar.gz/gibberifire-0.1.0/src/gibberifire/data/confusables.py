"""
Homoglyph mapping tables.

Based on Unicode TR39 confusables data.
"""

# Mapping intentionally uses confusable Unicode characters

# Latin to Cyrillic mapping (visually identical)
LATIN_TO_CYRILLIC: dict[str, str] = {
    # Uppercase
    'A': 'А',  # U+0041 -> U+0410
    'B': 'В',  # U+0042 -> U+0412
    'C': 'С',  # U+0043 -> U+0421
    'E': 'Е',  # U+0045 -> U+0415
    'H': 'Н',  # U+0048 -> U+041D
    'K': 'К',  # U+004B -> U+041A
    'M': 'М',  # U+004D -> U+041C
    'O': 'О',  # U+004F -> U+041E
    'P': 'Р',  # U+0050 -> U+0420
    'T': 'Т',  # U+0054 -> U+0422
    'X': 'Х',  # U+0058 -> U+0425
    # Lowercase
    'a': 'а',  # U+0061 -> U+0430
    'c': 'с',  # U+0063 -> U+0441
    'e': 'е',  # U+0065 -> U+0435
    'o': 'о',  # U+006F -> U+043E
    'p': 'р',  # U+0070 -> U+0440
    'x': 'х',  # U+0078 -> U+0445
    'y': 'у',  # U+0079 -> U+0443
}

# Reverse mapping
CYRILLIC_TO_LATIN: dict[str, str] = {v: k for k, v in LATIN_TO_CYRILLIC.items()}
