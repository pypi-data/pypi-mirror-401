"""Zero-width space injection method."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, cast

from gibberifire.data.zwsp_chars import ZWSP_CHARACTERS

from .base import BaseMethod

if TYPE_CHECKING:
    from gibberifire.core.models import ZWSPParams


class ZWSPMethod(BaseMethod):
    """Zero-Width Space injection method."""

    name = 'zwsp'

    # Zero-width characters for injection
    CHARS: ClassVar[list[str]] = ZWSP_CHARACTERS

    # Pre-compile regex for removal and detection
    # Escape characters to ensure safe regex construction
    _ESCAPED_CHARS: ClassVar[list[str]] = [re.escape(c) for c in CHARS]
    _REMOVE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(f'[{"".join(_ESCAPED_CHARS)}]')

    def apply(self, text: str) -> str:
        """Insert zero-width characters between regular characters."""
        if not text:
            return text

        params = cast('ZWSPParams', self._params)

        result = []

        # Optional: Add initial burst at the start
        if params.use_initial_burst:
            initial_burst = self._rng.randint(params.initial_burst_min, params.initial_burst_max)
            result.extend(self._rng.choice(self.CHARS) for _ in range(initial_burst))

        for i, char in enumerate(text):
            result.append(char)

            # Do not add inside emoji sequences
            if params.preserve_emoji and self._is_emoji_part(text, i):
                continue

            # Determine burst size for this position
            count = self._rng.randint(params.min_burst, params.max_burst)

            # Inject burst of invisible characters
            result.extend(self._rng.choice(self.CHARS) for _ in range(count))

        return ''.join(result)

    def remove(self, text: str) -> str:
        """Remove all zero-width characters from text."""
        return self._REMOVE_PATTERN.sub('', text)

    def detect(self, text: str) -> bool:
        """Check if text contains zero-width characters."""
        # Using regex search is generally faster than any(...) for pre-compiled pattern
        return bool(self._REMOVE_PATTERN.search(text))

    def _is_emoji_part(self, text: str, index: int) -> bool:
        """Check if character at index is part of emoji sequence."""
        # Simplified check - ZWJ is used in emoji sequences
        if index + 1 < len(text):
            next_char = text[index + 1]
            # Check if next char is emoji modifier or ZWJ
            if ord(next_char) in range(0x1F3FB, 0x1F3FF + 1):  # Skin tone modifiers
                return True
            if next_char == '\u200d':  # ZWJ
                return True
        return False
