"""Bidirectional markers data."""

# Safe Bidi markers (less likely to cause visual artifacts in LTR context)
SAFE_BIDI: list[str] = [
    '\u200e',  # Left-to-Right Mark (LRM)
]

# All Directional formatting characters
ALL_BIDI_MARKERS: list[str] = [
    '\u200e',  # Left-to-Right Mark (LRM)
    '\u200f',  # Right-to-Left Mark (RLM)
    '\u202a',  # Left-to-Right Embedding (LRE)
    '\u202b',  # Right-to-Left Embedding (RLE)
    '\u202c',  # Pop Directional Formatting (PDF)
    '\u202d',  # Left-to-Right Override (LRO)
    '\u202e',  # Right-to-Left Override (RLO)
]
