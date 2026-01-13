"""Data module containing Unicode character tables."""

from gibberifire.data.bidi import ALL_BIDI_MARKERS
from gibberifire.data.combining import COMBINING_MARKS
from gibberifire.data.confusables import CYRILLIC_TO_LATIN, LATIN_TO_CYRILLIC
from gibberifire.data.emoji_alphabet import EMOJI_ALPHABET
from gibberifire.data.zwsp_chars import ZWSP_CHARACTERS

__all__ = [
    'ALL_BIDI_MARKERS',
    'COMBINING_MARKS',
    'CYRILLIC_TO_LATIN',
    'EMOJI_ALPHABET',
    'LATIN_TO_CYRILLIC',
    'ZWSP_CHARACTERS',
]
