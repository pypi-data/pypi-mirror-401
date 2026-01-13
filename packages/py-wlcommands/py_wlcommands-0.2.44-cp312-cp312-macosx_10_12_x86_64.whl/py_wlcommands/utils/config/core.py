"""Configuration management utilities for WL Commands."""

import json
import os
import sys
import time
from typing import Any

from .defaults import get_default_config
from .validation import validate_config

if sys.platform != "win32":
    PlatformAdapter = None
else:
    try:
        from ..platform_adapter import PlatformAdapter
    except ImportError:
        PlatformAdapter = None


class ConfigManager:
    """Manage application configuration with auto-reload support."""

    def __init__(self, config_file: str | None = None) -> None:
        """
        Initialize configuration manager.

        Args:
            config_file (str, optional): Path to configuration file.
        """
        self.config_file = config_file or self._get_default_config_path()
        self._config: dict[str, Any] = {}
        self._last_modified_time: float = 0.0
        self._load_config()

    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        config_path = os.environ.get("WL_CONFIG_PATH")
        if config_path:
            return config_path

        try:
            from ..project_root import find_project_root

            project_root = find_project_root()
        except (ImportError, FileNotFoundError, RuntimeError, OSError):
            project_root = os.getcwd()

        return os.path.join(project_root, ".wl", "config.json")

    def _get_user_home_dir(self) -> str:
        """Get user home directory in a cross-platform way."""
        home_dir = os.path.expanduser("~")

        if PlatformAdapter is not None and PlatformAdapter.is_windows():
            if not home_dir or home_dir == "~":
                home_dir = os.environ.get("USERPROFILE", "")
                if not home_dir:
                    home_drive = os.environ.get("HOMEDRIVE", "")
                    home_path = os.environ.get("HOMEPATH", "")
                    if home_drive and home_path:
                        home_dir = os.path.join(home_drive, home_path)

        if not home_dir or home_dir == "~":
            home_dir = os.getcwd()

        return home_dir

    def _get_default_config(self) -> dict[str, Any]:
        """Get default configuration dictionary."""
        return get_default_config()

    def _load_config(self) -> None:
        """Load configuration from file."""
        if not os.path.exists(self.config_file):
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            self._config = get_default_config()
            self._config = validate_config(self._config)
            self._save_config()
            self._last_modified_time = time.time()
            return

        try:
            with open(self.config_file, encoding="utf-8") as f:
                self._config = json.load(f)
            self._last_modified_time = os.path.getmtime(self.config_file)
            self._config = validate_config(self._config)
        except (OSError, json.JSONDecodeError):
            self._config = get_default_config()
            self._config = validate_config(self._config)
            self._last_modified_time = time.time()

    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
                f.write("\n")
            self._last_modified_time = time.time()
        except OSError:
            pass

    def _should_reload(self) -> bool:
        """Check if configuration should be reloaded based on file modification time."""
        try:
            if os.path.exists(self.config_file):
                current_mtime = os.path.getmtime(self.config_file)
                return current_mtime > self._last_modified_time
        except OSError:
            pass
        return False

    def get(self, key: str, default: Any = None, auto_reload: bool = True) -> Any:
        """
        Get configuration value.

        Args:
            key (str): Configuration key.
            default (Any, optional): Default value if key not found.
            auto_reload (bool, optional): Whether to automatically reload if config file changed.

        Returns:
            Any: Configuration value.
        """
        if auto_reload and self._should_reload():
            self._load_config()

        value = self._config.get(key, default)

        if key == "log_file" and value:
            if os.path.isabs(value):
                return value
            if value == ".wl/log/wl_action.log":
                return value
            config_dir = os.path.dirname(self.config_file)
            return os.path.join(config_dir, value)

        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
        self._save_config()

    def get_all(self, auto_reload: bool = True) -> dict[str, Any]:
        """Get all configuration."""
        if auto_reload and self._should_reload():
            self._load_config()
        return self._config.copy()

    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()

    def hot_reload(self) -> bool:
        """
        Hot reload configuration from file.

        Returns:
            bool: True if configuration was reloaded, False otherwise.
        """
        if self._should_reload():
            self._load_config()
            return True
        return False


_config_manager: ConfigManager | None = None


def get_config_manager() -> ConfigManager:
    """Get global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value from global manager with auto-reload."""
    return get_config_manager().get(key, default)


def reload_config() -> bool:
    """Reload global configuration."""
    return get_config_manager().hot_reload()
