"""Main Gibberifire class."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from gibberifire.core.exceptions import FileOperationError, InvalidMethodError
from gibberifire.core.models import Profile
from gibberifire.methods import BaseMethod, BidiMethod, CombiningMethod, EncodingMethod, HomoglyphMethod, ZWSPMethod


class Gibberifire:
    """
    Main class for text protection using invisible Unicode characters.

    :param profile: Configuration Profile object. Must be provided.
    """

    # Registry of available methods
    METHOD_REGISTRY: ClassVar[dict[str, type[BaseMethod]]] = {
        'zwsp': ZWSPMethod,
        'homoglyph': HomoglyphMethod,
        'combining': CombiningMethod,
        'bidi': BidiMethod,
        'encoding': EncodingMethod,
    }

    def __init__(
        self,
        profile: Profile,
    ) -> None:
        """Initialize Gibberifire with a profile."""
        if not isinstance(profile, Profile):
            message = f'profile must be an instance of Profile, got {type(profile)}'
            raise TypeError(message)

        self._profile = profile
        self._methods = self._init_methods()

    def _init_methods(self) -> list[BaseMethod]:
        """Initialize protection methods based on profile pipeline."""
        methods = []
        for step in self._profile.pipeline:
            name = step.method
            if name not in self.METHOD_REGISTRY:
                message = f'Unknown method: {name}'
                raise InvalidMethodError(message)

            method_class = self.METHOD_REGISTRY[name]
            # Each method handles its own initialization and seeding via params
            methods.append(method_class(params=step.params))
        return methods

    def protect(self, text: str) -> str:
        """
        Apply protection to text.

        :param text: Original text to protect
        :return: Protected text with invisible characters
        """
        if not text:
            return text

        result = text
        for method in self._methods:
            result = method.apply(result)
        return result

    def clean(self, text: str) -> str:
        """
        Remove protection from text.

        :param text: Protected text
        :return: Cleaned original text
        """
        if not text:
            return text

        result = text
        # Apply methods in reverse order
        for method in reversed(self._methods):
            result = method.remove(result)
        return result

    def is_protected(self, text: str) -> bool:
        """
        Check if text contains protection markers.

        :param text: Text to check
        :return: True if protection detected
        """
        return any(method.detect(text) for method in self._methods)

    def protect_file(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
        encoding: str = 'utf-8',
    ) -> Path:
        """
        Protect text in a file.

        :param input_path: Path to input file
        :param output_path: Path to output file (default: input_path with .protected suffix)
        :param encoding: File encoding
        :return: Path to output file
        """
        input_path = Path(input_path)
        if not input_path.exists():
            message = f'Input file not found: {input_path}'
            raise FileOperationError(message)

        if output_path is None:
            output_path = input_path.with_suffix(f'.protected{input_path.suffix}')
        else:
            output_path = Path(output_path)

        try:
            text = input_path.read_text(encoding=encoding)
            protected = self.protect(text)
            output_path.write_text(protected, encoding=encoding)
        except (OSError, UnicodeError) as exc:
            message = 'Failed to protect file'
            raise FileOperationError(message) from exc

        return output_path

    def clean_file(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
        encoding: str = 'utf-8',
    ) -> Path:
        """
        Clean protected text in a file.

        :param input_path: Path to protected file
        :param output_path: Path to output file (default: input_path with .cleaned suffix)
        :param encoding: File encoding
        :return: Path to output file
        """
        input_path = Path(input_path)
        if not input_path.exists():
            message = f'Input file not found: {input_path}'
            raise FileOperationError(message)

        if output_path is None:
            output_path = input_path.with_suffix(f'.cleaned{input_path.suffix}')
        else:
            output_path = Path(output_path)

        try:
            text = input_path.read_text(encoding=encoding)
            cleaned = self.clean(text)
            output_path.write_text(cleaned, encoding=encoding)
        except (OSError, UnicodeError) as exc:
            message = 'Failed to clean file'
            raise FileOperationError(message) from exc

        return output_path

    @property
    def profile(self) -> Profile:
        """Get current configuration profile."""
        return self._profile

    @property
    def methods(self) -> tuple[BaseMethod, ...]:
        """Get the initialized protection methods."""
        return tuple(self._methods)

    def __repr__(self) -> str:
        """Return a debug representation with enabled methods."""
        return f'Gibberifire(pipeline={[m.name for m in self._methods]})'
