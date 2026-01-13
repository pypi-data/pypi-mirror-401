"""Default configuration constants and helper functions."""

import os
from typing import Any

from py_wlcommands import __version__

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_LOG_FILE = ".wl/log/wl_action.log"

DEFAULT_LOG_CONSOLE = False

DEFAULT_LOG_CONSOLE_FORMAT = "colored"

DEFAULT_LOG_FILE_FORMAT = "human"

DEFAULT_LOG_MAX_SIZE = 10 * 1024 * 1024

DEFAULT_LOG_MAX_BACKUPS = 5

DEFAULT_LOG_ROTATE_DAYS = 7

DEFAULT_LANGUAGE = "auto"

DEFAULT_ALIASES = {}

DEFAULT_VERSION = __version__


def get_default_config() -> dict[str, Any]:
    """Get default configuration dictionary."""
    return {
        "log_level": DEFAULT_LOG_LEVEL,
        "log_file": DEFAULT_LOG_FILE,
        "log_console": DEFAULT_LOG_CONSOLE,
        "log_console_format": DEFAULT_LOG_CONSOLE_FORMAT,
        "log_file_format": DEFAULT_LOG_FILE_FORMAT,
        "log_max_size": DEFAULT_LOG_MAX_SIZE,
        "log_max_backups": DEFAULT_LOG_MAX_BACKUPS,
        "log_rotate_days": DEFAULT_LOG_ROTATE_DAYS,
        "language": DEFAULT_LANGUAGE,
        "aliases": DEFAULT_ALIASES,
        "version": DEFAULT_VERSION,
    }
