"""Filtering and level checking for structured logging."""

import datetime
from typing import Any, Callable

from ..log_levels import LogLevel


class LogLevelChecker:
    """Manages filtering and level checking for structured logging."""

    def __init__(self, min_level: int) -> None:
        """
        Initialize log level checker.

        Args:
            min_level: Minimum log level.
        """
        self.min_level = min_level
        self.filters: list[Callable[[dict[str, Any]], bool]] = []

    def add_filter(self, filter_func: Callable[[dict[str, Any]], bool]) -> None:
        """
        Add a filter function.

        Args:
            filter_func: Function that takes a log record and returns bool.
        """
        self.filters.append(filter_func)

    def should_log(self, level: int, **kwargs) -> bool:
        """
        Check if log should be processed based on level and filters.

        Args:
            level: Log level.
            **kwargs: Log record fields.

        Returns:
            True if log should be processed.
        """
        if level < self.min_level:
            return False

        record = {
            "level": level,
            "timestamp": datetime.datetime.now().isoformat(),
            **kwargs,
        }
        return all(f(record) for f in self.filters)

    def get_level_name(self, level: int) -> str:
        """
        Convert level number to name.

        Args:
            level: Log level number.

        Returns:
            Log level name as string.
        """
        level_names = {
            LogLevel.DEBUG: "DEBUG",
            LogLevel.INFO: "INFO",
            LogLevel.WARNING: "WARNING",
            LogLevel.ERROR: "ERROR",
            LogLevel.CRITICAL: "CRITICAL",
        }
        return level_names.get(level, "UNKNOWN")
