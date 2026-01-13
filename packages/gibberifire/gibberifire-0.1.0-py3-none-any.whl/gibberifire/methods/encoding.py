"""Encoding method to make text human-hard but LLM-friendly."""

from __future__ import annotations

import binascii
import re
from typing import TYPE_CHECKING, ClassVar, Literal, cast

from gibberifire.data.emoji_alphabet import EMOJI_ALPHABET as ENCODING_EMOJI_ALPHABET
from gibberifire.methods.base import BaseMethod

if TYPE_CHECKING:
    from gibberifire.core.models import EncodingParams

Scheme = Literal['hex', 'emoji']


class EncodingMethod(BaseMethod):
    """Encode text into alternate representations."""

    name = 'encoding'

    # Invisible prefix to mark encoded payload. Uses a long sequence to avoid accidental matches
    MARKER_PREFIX: ClassVar[str] = '\u2063\u2062\u2064\u2061'

    # Invisible scheme markers (Variation Selectors) to keep scheme hints out of visible text
    SCHEME_MARKERS: ClassVar[dict[Scheme, str]] = cast(
        'dict[Scheme, str]',
        {
            'hex': '\ufe00',
            'emoji': '\ufe01',
        },
    )

    # Regex to detect presence of encoding marker
    _DETECT_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        rf'^{re.escape(MARKER_PREFIX)}[{"".join(SCHEME_MARKERS.values())}]',
    )

    # 16 emoji for nibble encoding (order matters for decode)
    EMOJI_ALPHABET: ClassVar[list[str]] = ENCODING_EMOJI_ALPHABET
    _EMOJI_TO_NIBBLE: ClassVar[dict[str, int]] = {emoji: idx for idx, emoji in enumerate(ENCODING_EMOJI_ALPHABET)}

    def apply(self, text: str) -> str:
        """Encode text using the configured scheme."""
        if not text:
            return text

        params = cast('EncodingParams', self._params)
        scheme = params.scheme
        marker = self._build_marker(scheme)

        encoded = self._encode(text, scheme)
        return f'{marker}{encoded}'

    def remove(self, text: str) -> str:
        """Decode text if it was encoded by this method."""
        scheme = self._extract_scheme(text)
        if scheme is None:
            return text

        marker_length = len(self._build_marker(scheme))
        payload = text[marker_length:]

        try:
            return self._decode(payload, scheme)
        except (binascii.Error, ValueError, UnicodeDecodeError):
            # If decoding fails, return original text to avoid data loss
            return text

    def detect(self, text: str) -> bool:
        """Check if text carries the encoding marker."""
        return bool(self._DETECT_PATTERN.match(text))

    def _build_marker(self, scheme: Scheme) -> str:
        """Construct an invisible marker for the given scheme."""
        return f'{self.MARKER_PREFIX}{self.SCHEME_MARKERS[scheme]}'

    def _extract_scheme(self, text: str) -> Scheme | None:
        """Extract scheme from the encoded text marker."""
        if not text.startswith(self.MARKER_PREFIX):
            return None

        if len(text) <= len(self.MARKER_PREFIX):
            return None

        scheme_marker = text[len(self.MARKER_PREFIX)]
        for scheme, marker in self.SCHEME_MARKERS.items():
            if scheme_marker == marker:
                return scheme
        return None

    def _encode(self, text: str, scheme: Scheme) -> str:
        """Encode text according to scheme."""
        if scheme == 'hex':
            return text.encode('utf-8').hex()
        if scheme == 'emoji':
            return self._encode_emoji(text)
        message = f'Unsupported encoding scheme: {scheme}'
        raise ValueError(message)

    def _decode(self, payload: str, scheme: Scheme) -> str:
        """Decode payload according to scheme."""
        if scheme == 'hex':
            raw = bytes.fromhex(payload)
            return raw.decode('utf-8')
        if scheme == 'emoji':
            return self._decode_emoji(payload)
        message = f'Unsupported encoding scheme: {scheme}'
        raise ValueError(message)

    def _encode_emoji(self, text: str) -> str:
        """Encode text into emoji nibbles."""
        data = text.encode('utf-8')
        emojis: list[str] = []
        for byte in data:
            high = byte >> 4
            low = byte & 0x0F
            emojis.append(self.EMOJI_ALPHABET[high])
            emojis.append(self.EMOJI_ALPHABET[low])
        return ''.join(emojis)

    def _decode_emoji(self, payload: str) -> str:
        """Decode emoji-encoded nibbles back to text."""
        if len(payload) % 2 != 0:
            message = 'Invalid emoji payload length'
            raise ValueError(message)

        bytes_out = bytearray()
        for i in range(0, len(payload), 2):
            high_emoji = payload[i]
            low_emoji = payload[i + 1]
            if high_emoji not in self._EMOJI_TO_NIBBLE or low_emoji not in self._EMOJI_TO_NIBBLE:
                message = 'Invalid emoji characters in payload'
                raise ValueError(message)
            high = self._EMOJI_TO_NIBBLE[high_emoji]
            low = self._EMOJI_TO_NIBBLE[low_emoji]
            bytes_out.append((high << 4) | low)
        return bytes_out.decode('utf-8')
