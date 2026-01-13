"""Configuration manager."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from gibberifire.core.exceptions import ConfigurationError
from gibberifire.core.models import DEFAULT_PROFILES, ConfigFile


class ConfigManager:
    """Manages loading and saving of configuration profiles."""

    DEFAULT_PATH = Path.home() / '.config' / 'gibberifire' / 'profiles.yaml'

    def __init__(self, config_path: str | Path | None = None) -> None:
        """
        Initialize ConfigManager.

        :param config_path: Path to configuration file. If None, uses default path.
        """
        if config_path:
            self.path = Path(config_path)
            self.is_custom_path = True
        else:
            self.path = self.DEFAULT_PATH
            self.is_custom_path = False

    def load(self) -> ConfigFile:
        """
        Load configuration from file.

        If default file doesn't exist, creates it with default profiles.
        """
        if not self.path.exists():
            if self.is_custom_path:
                message = f'Configuration file not found: {self.path}'
                raise ConfigurationError(message)
            self._create_default()

        try:
            # Safe load YAML
            data = yaml.safe_load(self.path.read_text(encoding='utf-8'))
            # Pydantic handles validation and polymorphic parsing
            return ConfigFile(**data)
        except yaml.YAMLError as exc:
            message = 'Invalid YAML in config file'
            raise ConfigurationError(message) from exc
        except ValidationError as exc:
            message = 'Invalid configuration structure'
            raise ConfigurationError(message) from exc
        except OSError as exc:
            message = 'Failed to read configuration file'
            raise ConfigurationError(message) from exc

    def _create_default(self) -> None:
        """Create default configuration file."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            config = ConfigFile(profiles=DEFAULT_PROFILES)

            # Dump Pydantic model to dict (mode='json' ensures clean standard types)
            config_dict = config.model_dump(mode='json')

            with self.path.open('w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        except OSError as exc:
            message = 'Failed to create default config'
            raise ConfigurationError(message) from exc
