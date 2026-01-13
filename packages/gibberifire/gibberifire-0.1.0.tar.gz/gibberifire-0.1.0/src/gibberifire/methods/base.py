"""Base abstractions for protection methods."""

from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gibberifire.core.models import BaseMethodParams


class BaseMethod(ABC):
    """Base class for protection methods."""

    name: str = 'base'

    def __init__(self, params: BaseMethodParams) -> None:
        """Store params and seed a deterministic RNG for reproducible behavior."""
        self._params = params
        self._rng = random.Random(self._params.seed)  # noqa: S311

    @abstractmethod
    def apply(self, text: str) -> str:
        """Apply protection method to text."""
        ...

    @abstractmethod
    def remove(self, text: str) -> str:
        """Remove protection from text."""
        ...

    @abstractmethod
    def detect(self, text: str) -> bool:
        """Detect if text has this protection applied."""
        ...
