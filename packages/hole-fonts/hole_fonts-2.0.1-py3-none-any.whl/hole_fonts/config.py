"""Configuration management for HOLE Fonts"""

import os
from pathlib import Path
from typing import Any, Dict, List
import yaml


class Config:
    """Configuration handler for HOLE Fonts"""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration

        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key

        Args:
            key: Configuration key (e.g., 'library.path')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    @property
    def library_path(self) -> Path:
        """Get library path with fallback handling"""
        primary = Path(self.get('library.path'))

        # Check if primary path is accessible
        if primary.exists() and primary.is_dir():
            return primary

        # Use fallback
        fallback = Path(self.get('library.fallback_path', 'Library'))
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback

    @property
    def input_path(self) -> Path:
        """Get input directory path"""
        return Path(self.get('input.path', 'Input'))

    @property
    def output_path(self) -> Path:
        """Get output directory path"""
        path = Path(self.get('output.path', 'Output'))
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def formats(self) -> List[str]:
        """Get list of formats to generate"""
        return self.get('formats', ['ttf', 'otf', 'woff2'])

    @property
    def parallel_workers(self) -> int:
        """Get number of parallel workers"""
        return self.get('processing.parallel_workers', 4)

    @property
    def skip_existing(self) -> bool:
        """Check if should skip existing fonts"""
        return self.get('processing.skip_existing', True)

    def __repr__(self) -> str:
        return f"Config(path={self.config_path})"


# Global config instance
_config: Config | None = None


def get_config(config_path: str = "config.yaml") -> Config:
    """
    Get global configuration instance

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration instance
    """
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config
