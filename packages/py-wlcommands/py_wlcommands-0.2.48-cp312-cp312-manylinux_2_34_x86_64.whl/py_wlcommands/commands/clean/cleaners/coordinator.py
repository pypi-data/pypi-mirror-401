"""
Clean Coordinator
清理协调器

This module coordinates all cleaning operations and provides unified interfaces.
此模块协调所有清理操作并提供统一接口。
"""

from py_wlcommands.commands.clean.utils import (
    remove_auto_activation_scripts,
    remove_rust_analyzer_dirs,
    remove_uv_lock,
    remove_virtual_environments,
)
from py_wlcommands.utils.logging import log_info

from .build_cleaner import (
    clean_build_artifacts,
    clean_cache_artifacts,
    clean_logs_artifacts,
    clean_venv_artifacts,
)
from .lfs_cleaner import clean_lfs_artifacts


def clean_all_artifacts(dry_run: bool = False, config: str | None = None) -> None:
    """
    Clean all artifacts including virtual environment
    清理所有产物，包括虚拟环境
    """
    log_info("Cleaning all artifacts...", lang="en")
    log_info("正在清理所有产物...", lang="zh")

    # Clean build artifacts
    clean_build_artifacts(dry_run=dry_run, config=config)

    # Clean Rust artifacts
    from py_wlcommands.commands.clean.utils.rust_cleaners import (
        clean_rust_artifacts as _clean_rust_artifacts,
    )

    _clean_rust_artifacts(dry_run=dry_run)

    # Remove virtual environment
    remove_virtual_environments(dry_run=dry_run)

    # Remove auto-activation scripts
    remove_auto_activation_scripts(dry_run=dry_run)

    # Remove rust-analyzer directories
    remove_rust_analyzer_dirs(dry_run=dry_run)

    # Remove uv.lock file
    remove_uv_lock(dry_run=dry_run)

    log_info("All artifacts cleaning completed.", lang="en")
    log_info("所有产物清理完成。", lang="zh")
