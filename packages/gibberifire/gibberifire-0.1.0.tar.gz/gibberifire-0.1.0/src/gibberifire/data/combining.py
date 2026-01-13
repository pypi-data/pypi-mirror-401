"""Combining Unicode characters (diacritical marks)."""

# Combining diacritical marks that are invisible or nearly invisible
COMBINING_MARKS: list[str] = [
    '\u0300',  # Combining Grave Accent
    '\u0301',  # Combining Acute Accent
    '\u0302',  # Combining Circumflex Accent
    '\u0303',  # Combining Tilde
    '\u0304',  # Combining Macron
    '\u0305',  # Combining Overline
    '\u0306',  # Combining Breve
    '\u0307',  # Combining Dot Above
    '\u0308',  # Combining Diaeresis
    '\u030a',  # Combining Ring Above
    '\u030b',  # Combining Double Acute Accent
    '\u030c',  # Combining Caron
    '\u0323',  # Combining Dot Below
    '\u0324',  # Combining Diaeresis Below
    '\u0325',  # Combining Ring Below
    '\u0331',  # Combining Macron Below
    '\u0332',  # Combining Low Line
    '\u0333',  # Combining Double Low Line
    '\u0334',  # Combining Tilde Overlay
    '\u0335',  # Combining Short Stroke Overlay
    '\u0336',  # Combining Long Stroke Overlay
    '\u0337',  # Combining Short Solidus Overlay
    '\u0338',  # Combining Long Solidus Overlay
]

# Invisible combining marks (truly invisible)
INVISIBLE_COMBINING: list[str] = [
    '\u034f',  # Combining Grapheme Joiner
    '\u0358',  # Combining Dot Above Right (very small)
    '\u035c',  # Combining Double Breve Below
    '\u035d',  # Combining Double Breve
    '\u035e',  # Combining Double Macron
    '\u035f',  # Combining Double Macron Below
]

# Cyrillic combining marks
CYRILLIC_COMBINING: list[str] = [
    '\u0483',  # Combining Cyrillic Titlo
    '\u0484',  # Combining Cyrillic Palatalization
    '\u0485',  # Combining Cyrillic Dasia Pneumata
    '\u0486',  # Combining Cyrillic Psili Pneumata
    '\u0487',  # Combining Cyrillic Pokrytie
    '\u0488',  # Combining Cyrillic Hundred Thousands Sign
    '\u0489',  # Combining Cyrillic Millions Sign
]

# All combining marks for detection
ALL_COMBINING_MARKS: set[str] = set(COMBINING_MARKS + INVISIBLE_COMBINING + CYRILLIC_COMBINING)
