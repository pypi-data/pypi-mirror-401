"""Backward compatibility module for config utilities.

This module has been refactored. Use py_wlcommands.utils.config instead.
"""

from py_wlcommands.utils.config import (
    ConfigManager,
    get_config,
    get_config_manager,
    reload_config,
)

__all__ = [
    "ConfigManager",
    "get_config",
    "get_config_manager",
    "reload_config",
]
