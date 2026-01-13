"""Combining characters method."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, cast

from gibberifire.data.combining import ALL_COMBINING_MARKS, COMBINING_MARKS
from gibberifire.methods.base import BaseMethod

if TYPE_CHECKING:
    from gibberifire.core.models import CombiningParams


class CombiningMethod(BaseMethod):
    """Combining characters method."""

    name = 'combining'

    # Pre-compile regex for removal and detection
    _REMOVE_PATTERN = re.compile(f'[{"".join(ALL_COMBINING_MARKS)}]')

    def apply(self, text: str) -> str:
        """Add combining marks to characters."""
        if not text:
            return text

        params = cast('CombiningParams', self._params)
        probability = params.probability

        if probability <= 0:
            return text

        result = []

        for char in text:
            result.append(char)

            # Only add combining marks to letters
            if char.isalpha() and self._rng.random() < probability:
                mark = self._rng.choice(COMBINING_MARKS)
                result.append(mark)

        return ''.join(result)

    def remove(self, text: str) -> str:
        """Remove all combining marks from text."""
        return self._REMOVE_PATTERN.sub('', text)

    def detect(self, text: str) -> bool:
        """Check if text contains combining marks."""
        return bool(self._REMOVE_PATTERN.search(text))
