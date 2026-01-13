"""Configuration management for structured logging."""

import os
from typing import Any

from ..log_levels import LogLevel


class LoggingConfig:
    """Manages configuration for structured logging."""

    def __init__(self) -> None:
        """Initialize logging configuration."""
        self._config_functions = self._get_config_functions()

    def _get_config_functions(self):
        """Get configuration functions with fallbacks."""
        try:
            from ..config import get_config

            return get_config
        except ImportError:
            # Fallback if config is not available
            def config(key: str, default: Any = None) -> Any:
                return default

            return config

    def get_log_level(self, min_level: int | None = None) -> int:
        """
        Get log level from config or parameter.

        Args:
            min_level: Explicit log level. If None, get from config.

        Returns:
            Log level as integer.
        """
        if min_level is not None:
            return min_level

        level_value = self._config_functions("log_level", "INFO")
        # Handle both string and numeric log levels
        if isinstance(level_value, str):
            level_name = level_value.upper()
            return getattr(LogLevel, level_name, LogLevel.INFO)
        else:
            return level_value

    def get_log_file(self, log_file: str | None = None) -> str | None:
        """
        Get log file path.

        Args:
            log_file: Explicit log file path. If None, get from config.

        Returns:
            Log file path or None.
        """
        if log_file is not None:
            return log_file

        return self._config_functions("log_file")

    def get_console_settings(self) -> tuple[bool, str]:
        """
        Get console output settings.

        Returns:
            Tuple of (enable_console, console_format).
        """
        enable_console = self._config_functions("log_console", False)
        console_format = self._config_functions("log_console_format", "colored")
        return enable_console, console_format

    def get_file_format_settings(self) -> str:
        """
        Get log file format setting.

        Returns:
            Log file format ('human' or 'json').
        """
        return self._config_functions("log_file_format", "human")

    def get_rotation_settings(self) -> dict[str, Any]:
        """
        Get log rotation settings.

        Returns:
            Dictionary with rotation settings.
        """
        return {
            "max_size": self._config_functions("log_max_size", 10 * 1024 * 1024),
            "max_backups": self._config_functions("log_max_backups", 5),
            "rotate_days": self._config_functions("log_rotate_days", 7),
        }
