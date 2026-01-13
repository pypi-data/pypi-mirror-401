"""
Core cleaning utilities for clean command.
"""

import os
import shutil

from py_wlcommands.utils.logging import log_info


def remove_directories(dirs_to_remove: list[str], dry_run: bool = False) -> None:
    """Remove specific directories."""
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                if dry_run:
                    log_info(f"Would remove directory: {dir_name}", lang="en")
                    log_info(f"将删除目录: {dir_name}", lang="zh")
                else:
                    shutil.rmtree(dir_name)
                    log_info(f"Removed directory: {dir_name}", lang="en")
                    log_info(f"已删除目录: {dir_name}", lang="zh")
            except Exception as e:
                log_info(f"Failed to remove directory {dir_name}: {e}", lang="en")
                log_info(f"删除目录 {dir_name} 失败: {e}", lang="zh")


def remove_files(files_to_remove: list[str], dry_run: bool = False) -> None:
    """Remove specific files."""
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                if dry_run:
                    log_info(f"Would remove file: {file_name}", lang="en")
                    log_info(f"将删除文件: {file_name}", lang="zh")
                else:
                    os.remove(file_name)
                    log_info(f"Removed file: {file_name}", lang="en")
                    log_info(f"已删除文件: {file_name}", lang="zh")
            except Exception as e:
                log_info(f"Failed to remove file {file_name}: {e}", lang="en")
                log_info(f"删除文件 {file_name} 失败: {e}", lang="zh")
