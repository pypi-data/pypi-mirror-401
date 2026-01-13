"""
Clean Utils Module
清理工具模块

This module now serves as an entry point for the modularized cleaning functionality.
Main functions are delegated to specialized modules for better organization.
此模块现在作为模块化清理功能的入口点。
主要功能委托给专门的模块以获得更好的组织结构。
"""

# Import all functions from the modularized components
from py_wlcommands.commands.clean.cleaners.build_cleaner import (
    clean_build_artifacts,
    clean_cache_artifacts,
    clean_logs_artifacts,
    clean_venv_artifacts,
)
from py_wlcommands.commands.clean.cleaners.coordinator import clean_all_artifacts
from py_wlcommands.commands.clean.cleaners.lfs_cleaner import clean_lfs_artifacts
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
from py_wlcommands.commands.clean.utils.rust_cleaners import (
    clean_rust_artifacts as _clean_rust_artifacts,
)
from py_wlcommands.utils.logging import log_info

# Keep backward compatibility with tests that import private functions
# 保持与导入私有函数的测试的向后兼容性
_remove_directories = remove_directories
_remove_files = remove_files
_remove_log_files = remove_log_files
_remove_pycache_dirs = remove_pycache_dirs
_remove_egg_info_dirs = remove_egg_info_dirs
_remove_virtual_environments = remove_virtual_environments
_remove_auto_activation_scripts = remove_auto_activation_scripts
_remove_uv_lock = remove_uv_lock


# Public API functions - now delegated to specialized modules
# 公共API函数 - 现在委托给专门的模块


def clean_rust_artifacts(dry_run: bool = False, config: str | None = None) -> None:
    """
    Clean Rust build artifacts
    清理Rust构建产物
    """
    # Pass dry_run parameter to the actual implementation
    # Note: This may need to be updated in the underlying implementation
    _clean_rust_artifacts(dry_run=dry_run)
