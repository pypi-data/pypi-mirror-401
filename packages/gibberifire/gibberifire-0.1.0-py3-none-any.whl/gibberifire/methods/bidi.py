"""Bidirectional text markers method."""

from __future__ import annotations

import re

from gibberifire.data.bidi import ALL_BIDI_MARKERS, SAFE_BIDI
from gibberifire.methods.base import BaseMethod


class BidiMethod(BaseMethod):
    """Bidirectional text markers method."""

    name = 'bidi'
    LRM_PROBABILITY = 0.3

    # Pre-compile regex for removal and detection
    _REMOVE_PATTERN = re.compile(f'[{"".join(ALL_BIDI_MARKERS)}]')

    def apply(self, text: str) -> str:
        """Add bidirectional markers to text."""
        if not text:
            return text

        # Use only safe bidi markers to avoid visual artifacts
        result = []

        # Add LRM at word boundaries
        words = text.split()
        for i, word in enumerate(words):
            if i > 0:
                result.append(' ')

            # Add LRM before word
            if self._rng.random() < self.LRM_PROBABILITY:
                result.append(SAFE_BIDI[0])  # LRM

            result.append(word)

            # Add LRM after word
            if self._rng.random() < self.LRM_PROBABILITY:
                result.append(SAFE_BIDI[0])  # LRM

        return ''.join(result)

    def remove(self, text: str) -> str:
        """Remove all bidi markers from text."""
        return self._REMOVE_PATTERN.sub('', text)

    def detect(self, text: str) -> bool:
        """Check if text contains bidi markers."""
        return bool(self._REMOVE_PATTERN.search(text))
