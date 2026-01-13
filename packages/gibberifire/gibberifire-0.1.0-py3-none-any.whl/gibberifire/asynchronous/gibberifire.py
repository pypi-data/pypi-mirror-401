"""Async wrapper for Gibberifire."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from typing_extensions import Self  # noqa: UP035

from gibberifire.core.gibberifire import Gibberifire

if TYPE_CHECKING:
    from pathlib import Path
    from types import TracebackType

    from gibberifire.core.models import Profile


class AsyncGibberifire:
    """
    Async wrapper for Gibberifire.

    Example::

        async with AsyncGibberifire(profile=profile) as gf:
            protected = await gf.protect('Hello, World!')
    """

    def __init__(
        self,
        profile: Profile,
    ) -> None:
        """Create an async wrapper around the synchronous Gibberifire."""
        self._sync = Gibberifire(
            profile=profile,
        )

    async def protect(self, text: str) -> str:
        """Async version of protect."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync.protect, text)

    async def clean(self, text: str) -> str:
        """Async version of clean."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync.clean, text)

    async def is_protected(self, text: str) -> bool:
        """Async version of is_protected."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync.is_protected, text)

    async def protect_file(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
        encoding: str = 'utf-8',
    ) -> Path:
        """Async version of protect_file."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync.protect_file, input_path, output_path, encoding)

    async def clean_file(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
        encoding: str = 'utf-8',
    ) -> Path:
        """Async version of clean_file."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync.clean_file, input_path, output_path, encoding)

    async def __aenter__(self) -> Self:
        """Enter async context."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Exit async context.

        No cleanup required.
        """
