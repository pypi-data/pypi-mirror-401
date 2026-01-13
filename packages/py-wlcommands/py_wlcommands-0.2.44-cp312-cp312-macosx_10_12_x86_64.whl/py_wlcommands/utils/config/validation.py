"""Configuration validation utilities."""

from typing import Any

VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

VALID_CONSOLE_FORMATS = ["colored", "json"]

VALID_FILE_FORMATS = ["json", "human"]


def validate_log_level(log_level: str) -> str:
    """Validate log level value."""
    return log_level.upper() if log_level.upper() in VALID_LOG_LEVELS else "INFO"


def validate_log_max_size(size: int) -> int:
    """Validate log max size value."""
    return size if isinstance(size, int) and size > 0 else 10 * 1024 * 1024


def validate_log_max_backups(count: int) -> int:
    """Validate log max backups value."""
    return count if isinstance(count, int) and count >= 0 else 5


def validate_log_rotate_days(days: int) -> int:
    """Validate log rotate days value."""
    return days if isinstance(days, int) and days > 0 else 7


def validate_log_console(value: bool) -> bool:
    """Validate log console value."""
    return value if isinstance(value, bool) else False


def validate_log_console_format(fmt: str) -> str:
    """Validate log console format value."""
    return fmt.lower() if fmt.lower() in VALID_CONSOLE_FORMATS else "colored"


def validate_log_file_format(fmt: str) -> str:
    """Validate log file format value."""
    return fmt.lower() if fmt.lower() in VALID_FILE_FORMATS else "human"


def validate_config(config: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize configuration values."""
    validated = config.copy()

    if "log_level" in validated:
        validated["log_level"] = validate_log_level(validated["log_level"])
    if "log_max_size" in validated:
        validated["log_max_size"] = validate_log_max_size(validated["log_max_size"])
    if "log_max_backups" in validated:
        validated["log_max_backups"] = validate_log_max_backups(
            validated["log_max_backups"]
        )
    if "log_rotate_days" in validated:
        validated["log_rotate_days"] = validate_log_rotate_days(
            validated["log_rotate_days"]
        )
    if "log_console" in validated:
        validated["log_console"] = validate_log_console(validated["log_console"])
    if "log_console_format" in validated:
        validated["log_console_format"] = validate_log_console_format(
            validated["log_console_format"]
        )
    if "log_file_format" in validated:
        validated["log_file_format"] = validate_log_file_format(
            validated["log_file_format"]
        )

    return validated
