"""Protection methods module."""

from gibberifire.methods.base import BaseMethod
from gibberifire.methods.bidi import BidiMethod
from gibberifire.methods.combining import CombiningMethod
from gibberifire.methods.encoding import EncodingMethod
from gibberifire.methods.homoglyph import HomoglyphMethod
from gibberifire.methods.zwsp import ZWSPMethod

__all__ = [
    'BaseMethod',
    'BidiMethod',
    'CombiningMethod',
    'EncodingMethod',
    'HomoglyphMethod',
    'ZWSPMethod',
]
