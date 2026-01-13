"""Homoglyph substitution method."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from gibberifire.data.confusables import CYRILLIC_TO_LATIN, LATIN_TO_CYRILLIC
from gibberifire.methods.base import BaseMethod

if TYPE_CHECKING:
    from gibberifire.core.models import HomoglyphParams


class HomoglyphMethod(BaseMethod):
    """Homoglyph substitution method."""

    name = 'homoglyph'

    # Create translation table for removal (more efficient than loop)
    _REMOVE_TRANS_TABLE = str.maketrans(CYRILLIC_TO_LATIN)

    def apply(self, text: str) -> str:
        """Replace some Latin characters with Cyrillic lookalikes."""
        if not text:
            return text

        params = cast('HomoglyphParams', self._params)
        probability = params.probability

        # Optimization: if probability is 0, return immediately
        if probability <= 0:
            return text

        result = []

        for char in text:
            # We only replace if it's in our map AND random check passes
            if char in LATIN_TO_CYRILLIC and self._rng.random() < probability:
                result.append(LATIN_TO_CYRILLIC[char])
            else:
                result.append(char)

        return ''.join(result)

    def remove(self, text: str) -> str:
        """Replace Cyrillic lookalikes back to Latin."""
        # Using translate is C-optimized and much faster
        return text.translate(self._REMOVE_TRANS_TABLE)

    def detect(self, text: str) -> bool:
        """Check if text contains Cyrillic lookalikes in Latin context."""
        # any() with generator is efficient enough here,
        # but iterating over set intersection might be faster for very long texts
        # For now, simple iteration is acceptable.
        return any(char in CYRILLIC_TO_LATIN for char in text)
