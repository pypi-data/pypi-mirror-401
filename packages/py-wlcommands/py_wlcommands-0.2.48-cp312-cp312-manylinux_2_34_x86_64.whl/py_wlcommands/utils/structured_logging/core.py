"""Core logging functionality for WL Commands.

This module serves as the entry point for the modularized structured logging functionality.
主要功能委托给专门的模块以获得更好的组织结构。
"""

from typing import Any

from ..log_levels import LogLevel
from ..log_rotators import LogRotator
from .config import LoggingConfig
from .filtering import LogLevelChecker
from .formatters import LogFormatter
from .handlers import LogHandler
from .logger import StructuredLoggerCore


# Backward compatibility: re-export all the main components
class StructuredLogger(StructuredLoggerCore):
    """A structured logger that outputs JSON formatted logs."""

    def __init__(
        self, name: str, min_level: int | None = None, log_file: str | None = None
    ) -> None:
        """
        Initialize structured logger.

        Args:
            name (str): Logger name.
            min_level (int, optional): Minimum log level. If None, read from config.
            log_file (Optional[str]): Log file path. If None, read from config.
        """
        super().__init__(name, min_level, log_file)

        # Add backward compatibility properties
        self._min_level = self.filter.min_level
        self._log_file = self.handler.log_file
        self.log_rotator = self.handler.log_rotator
        self.enable_console = self.handler.enable_console
        self.console_format = self.handler.console_format
        self.log_file_format = self.handler.log_file_format
        self.filters = self.filter.filters

    @property
    def min_level(self):
        """Get minimum log level."""
        return self._min_level

    @min_level.setter
    def min_level(self, value):
        """Set minimum log level."""
        self._min_level = value
        self.filter.min_level = value

    @property
    def log_file(self):
        """Get log file path."""
        return self._log_file

    @log_file.setter
    def log_file(self, value):
        """Set log file path."""
        self._log_file = value
        self.handler.log_file = value

    # Override logging methods to call _write_log for backward compatibility with tests
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message - uses _write_log for backward compatibility."""
        if not self.filter.should_log(LogLevel.DEBUG, message=message, **kwargs):
            return

        record = self._build_record(LogLevel.DEBUG, message, **kwargs)
        formatted_message = self.formatter.format_json_log(record)
        self._write_log(formatted_message)

    def info(self, message: str, **kwargs) -> None:
        """Log info message - uses _write_log for backward compatibility."""
        if not self.filter.should_log(LogLevel.INFO, message=message, **kwargs):
            return

        record = self._build_record(LogLevel.INFO, message, **kwargs)
        formatted_message = self.formatter.format_json_log(record)
        self._write_log(formatted_message)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message - uses _write_log for backward compatibility."""
        if not self.filter.should_log(LogLevel.WARNING, message=message, **kwargs):
            return

        record = self._build_record(LogLevel.WARNING, message, **kwargs)
        formatted_message = self.formatter.format_json_log(record)
        self._write_log(formatted_message)

    def error(self, message: str, **kwargs) -> None:
        """Log error message - uses _write_log for backward compatibility."""
        if not self.filter.should_log(LogLevel.ERROR, message=message, **kwargs):
            return

        record = self._build_record(LogLevel.ERROR, message, **kwargs)
        formatted_message = self.formatter.format_json_log(record)
        self._write_log(formatted_message)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message - uses _write_log for backward compatibility."""
        if not self.filter.should_log(LogLevel.CRITICAL, message=message, **kwargs):
            return

        record = self._build_record(LogLevel.CRITICAL, message, **kwargs)
        formatted_message = self.formatter.format_json_log(record)
        self._write_log(formatted_message)

    # Compatibility methods for backward compatibility with tests
    def _write_log(self, message: str) -> None:
        """Write log message to appropriate output (compatibility method)."""
        import json

        # Handle file writing directly for backward compatibility with tests
        if self.log_file:
            # Handle log rotation directly
            if self.log_rotator and self.log_rotator.should_rotate():
                self.log_rotator.do_rotate()

            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(message + "\n")
            except OSError:
                # Ignore file write errors
                pass

        # Handle console output directly for backward compatibility with tests
        if self.enable_console:
            import sys

            try:
                # Determine output stream based on log level in message
                if "CRITICAL" in message or "ERROR" in message:
                    print(message, file=sys.stderr)
                else:
                    print(message, file=sys.stdout)
            except OSError:
                # Ignore console write errors
                pass

    def _write_log_with_rotation(self, message: str) -> None:
        """Write log message with rotation (compatibility method)."""
        self._write_log(message)

    def _format_human_log(self, record: dict[str, Any]) -> str:
        """Format log record for human-readable file output (compatibility method)."""
        return self.formatter.format_human_log(record)

    def _format_console_log(self, record: dict[str, Any]) -> str:
        """Format log record for console output (compatibility method)."""
        return self.formatter.format_console_log(record)

    # Property accessors for backward compatibility
    @property
    def _COLORS(self) -> dict[str, str]:  # noqa: N802 - Property name kept uppercase for backward compatibility
        """Get color codes (compatibility property)."""
        return self.formatter._COLORS

    @_COLORS.setter
    def _COLORS(self, value: dict[str, str]) -> None:  # noqa: N802 - Property name kept uppercase for backward compatibility
        """Set color codes (compatibility property)."""
        self.formatter._COLORS = value

    def _should_log(self, level: int, **kwargs) -> bool:
        """Check if log should be processed based on level and filters (compatibility method)."""
        return self.filter.should_log(level, **kwargs)

    def _get_level_name(self, level: int) -> str:
        """Convert level number to name (compatibility method)."""
        return self.filter.get_level_name(level)

    @property
    def filters(self):
        """Get filters for backward compatibility."""
        return self.filter.filters

    @filters.setter
    def filters(self, value):
        """Set filters for backward compatibility."""
        self.filter.filters = value


# Re-export classes for advanced usage
__all__ = [
    "StructuredLogger",
    "StructuredLoggerCore",
    "LoggingConfig",
    "LogLevelChecker",
    "LogFormatter",
    "LogHandler",
    "LogRotator",
]
