"""
Build Artifacts Cleaner
构建产物清理器

This module handles cleaning of build artifacts, cache directories, logs, and virtual environments.
此模块处理构建产物、缓存目录、日志和虚拟环境的清理。
"""

from py_wlcommands.commands.clean.utils import (
    remove_auto_activation_scripts,
    remove_directories,
    remove_egg_info_dirs,
    remove_files,
    remove_log_files,
    remove_pycache_dirs,
    remove_rust_analyzer_dirs,
    remove_uv_lock,
    remove_virtual_environments,
)
from py_wlcommands.utils.logging import log_info


def clean_build_artifacts(dry_run: bool = False, config: str | None = None) -> None:
    """
    Clean build artifacts and temporary files
    清理构建产物和临时文件
    """
    log_info("Cleaning build artifacts and temporary files...", lang="en")
    log_info("正在清理构建产物和临时文件...", lang="zh")

    # Remove build directories
    build_dirs = [
        "build",
        "dist",
        "results",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "logs",
        "todos",
    ]
    remove_directories(build_dirs, dry_run=dry_run)

    # Remove specific files
    files_to_remove = [".coverage"]
    remove_files(files_to_remove, dry_run=dry_run)

    # Remove log files
    remove_log_files(dry_run=dry_run)

    # Remove pycache directories only in project directory
    remove_pycache_dirs(dry_run=dry_run)

    # Remove egg-info directories
    remove_egg_info_dirs(dry_run=dry_run)

    # Remove rust-analyzer directories
    remove_rust_analyzer_dirs(dry_run=dry_run)

    log_info("Build artifacts and temporary files cleaning completed.", lang="en")
    log_info("构建产物和临时文件清理完成。", lang="zh")


def clean_venv_artifacts(dry_run: bool = False, config: str | None = None) -> None:
    """
    Clean virtual environment artifacts
    清理虚拟环境产物
    """
    log_info("Cleaning virtual environment...", lang="en")
    log_info("正在清理虚拟环境...", lang="zh")

    # Remove virtual environments
    remove_virtual_environments(dry_run=dry_run)

    # Remove auto-activation scripts
    remove_auto_activation_scripts(dry_run=dry_run)

    log_info("Virtual environment cleaning completed.", lang="en")
    log_info("虚拟环境清理完成。", lang="zh")


def clean_cache_artifacts(dry_run: bool = False, config: str | None = None) -> None:
    """
    Clean cache directories
    清理缓存目录
    """
    log_info("Cleaning cache directories...", lang="en")
    log_info("正在清理缓存目录...", lang="zh")

    # Remove cache directories
    cache_dirs = [
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".git/hooks",
    ]
    remove_directories(cache_dirs, dry_run=dry_run)

    # Remove pycache directories
    remove_pycache_dirs(dry_run=dry_run)

    log_info("Cache directories cleaning completed.", lang="en")
    log_info("缓存目录清理完成。", lang="zh")


def clean_logs_artifacts(dry_run: bool = False, config: str | None = None) -> None:
    """
    Clean log files and directories
    清理日志文件和目录
    """
    log_info("Cleaning log files and directories...", lang="en")
    log_info("正在清理日志文件和目录...", lang="zh")

    # Remove log directories
    log_dirs = ["logs"]
    remove_directories(log_dirs, dry_run=dry_run)

    # Remove log files
    remove_log_files(dry_run=dry_run)

    log_info("Log files and directories cleaning completed.", lang="en")
    log_info("日志文件和目录清理完成。", lang="zh")
