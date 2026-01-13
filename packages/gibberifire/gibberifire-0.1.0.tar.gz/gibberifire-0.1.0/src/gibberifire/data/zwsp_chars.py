"""Zero-width characters data."""

ZWSP_CHARACTERS: list[str] = [
    '\u200b',  # Zero Width Space
    '\u200c',  # Zero Width Non-Joiner
    '\u2060',  # Word Joiner
    '\ufeff',  # Zero Width No-Break Space (BOM)
    '\u180e',  # Mongolian Vowel Separator
    '\u2061',  # Function Application
    '\u2062',  # Invisible Times
    '\u2063',  # Invisible Separator
    '\u2064',  # Invisible Plus
]

# Variation Selectors (VS1 - VS16)
ZWSP_CHARACTERS.extend(chr(i) for i in range(0xFE00, 0xFE0F + 1))

# Tags (Language Tags, etc. - often invisible)
# Adding a range of tag characters
ZWSP_CHARACTERS.extend(chr(i) for i in range(0xE0020, 0xE007F + 1))
