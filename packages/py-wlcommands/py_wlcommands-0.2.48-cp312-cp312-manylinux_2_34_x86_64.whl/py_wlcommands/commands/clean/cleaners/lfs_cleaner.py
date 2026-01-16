"""
Git LFS Cleaner
Git LFS清理器

This module handles cleaning of Git LFS deployment artifacts.
此模块处理Git LFS部署产物的清理。
"""

import os
import shutil
import subprocess
from pathlib import Path

from py_wlcommands.utils.logging import log_info


def clean_lfs_artifacts(dry_run: bool = False, config: str | None = None) -> None:
    """
    Clean Git LFS deployment without deleting actual files
    清理Git LFS部署，不删除实际文件
    """
    log_info("Cleaning Git LFS deployment...", lang="en")
    log_info("正在清理Git LFS部署...", lang="zh")

    # 检查并移除嵌套的.git目录
    _handle_nested_git_dirs(dry_run=dry_run)

    # 清理.gitattributes文件中的LFS跟踪规则
    _clean_gitattributes(dry_run=dry_run)

    # 卸载Git LFS钩子
    _uninstall_git_lfs()

    log_info("Git LFS deployment cleaning completed.", lang="en")
    log_info("Git LFS部署清理完成。", lang="zh")


def _find_nested_git_dirs() -> list:
    """查找嵌套的.git目录（不包括根目录的.git）"""
    current_dir = Path.cwd()
    nested_git_dirs = []

    for git_dir in current_dir.glob("**/.git"):
        # 跳过根目录的.git文件夹
        if git_dir.parent == current_dir:
            continue
        # 检查是否是目录
        if git_dir.is_dir():
            nested_git_dirs.append(git_dir)

    return nested_git_dirs


def _remove_nested_git_dirs(nested_git_dirs: list, dry_run: bool = False) -> None:
    """移除嵌套的.git目录"""
    log_info("\nAutomatically removing nested .git directories...", lang="en")
    log_info("\n正在自动移除嵌套的.git目录...", lang="zh")

    for git_dir in nested_git_dirs:
        try:
            if dry_run:
                log_info(f"✓ Would remove: {git_dir}", lang="en")
                log_info(f"✓ 将移除: {git_dir}", lang="zh")
            else:
                shutil.rmtree(git_dir)
                log_info(f"✓ Successfully removed: {git_dir}", lang="en")
                log_info(f"✓ 成功移除: {git_dir}", lang="zh")
        except Exception as e:
            log_info(f"✗ Failed to remove {git_dir}: {e}", lang="en")
            log_info(f"✗ 移除失败 {git_dir}: {e}", lang="zh")


def _handle_nested_git_dirs(dry_run: bool = False) -> None:
    """处理嵌套的.git目录"""
    log_info("Checking for nested .git directories...", lang="en")
    log_info("正在检查嵌套的.git目录...", lang="zh")

    nested_git_dirs = _find_nested_git_dirs()

    if nested_git_dirs:
        log_info(
            "Found nested .git directories, removing them to fix Git operations:",
            lang="en",
        )
        log_info("发现嵌套的.git目录，正在移除它们以修复Git操作：", lang="zh")

        for git_dir in nested_git_dirs:
            log_info(f"  - {git_dir}", lang="en")
            log_info(f"  - {git_dir}", lang="zh")

        _remove_nested_git_dirs(nested_git_dirs, dry_run=dry_run)
    else:
        log_info("✓ No nested .git directories found", lang="en")
        log_info("✓ 未发现嵌套的.git目录", lang="zh")


def _clean_gitattributes(dry_run: bool = False) -> None:
    """清理.gitattributes文件中的LFS跟踪规则"""
    gitattributes_path = Path(".gitattributes")
    if gitattributes_path.exists():
        log_info("Removing Git LFS tracking rules from .gitattributes...", lang="en")
        log_info("正在从.gitattributes中移除Git LFS跟踪规则...", lang="zh")

        # Read the current content
        with open(gitattributes_path) as f:
            lines = f.readlines()

        # Filter out Git LFS tracking rules
        filtered_lines = []
        for line in lines:
            # Check if the line contains Git LFS tracking rules
            if (
                "filter=lfs" not in line
                and "diff=lfs" not in line
                and "merge=lfs" not in line
            ):
                filtered_lines.append(line)

        # Write back the filtered content if not in dry run mode
        if dry_run:
            log_info(
                "✓ Would update .gitattributes to remove LFS tracking rules", lang="en"
            )
            log_info("✓ 将更新.gitattributes以移除LFS跟踪规则", lang="zh")
        else:
            with open(gitattributes_path, "w") as f:
                f.writelines(filtered_lines)
            log_info("✓ Removed Git LFS tracking rules from .gitattributes", lang="en")
            log_info("✓ 已从.gitattributes中移除Git LFS跟踪规则", lang="zh")


def _uninstall_git_lfs() -> None:
    """卸载Git LFS钩子"""
    log_info("Removing Git LFS hooks...", lang="en")
    log_info("正在移除Git LFS钩子...", lang="zh")

    try:
        result = subprocess.run(
            ["git", "lfs", "uninstall"], check=True, capture_output=True, text=True
        )

        # Filter out warning messages from both stdout and stderr
        def filter_warnings(output):
            if not output:
                return ""
            lines = output.strip().split("\n")
            filtered_lines = [line for line in lines if not line.startswith("warning:")]
            return "\n".join(filtered_lines).strip()

        # Filter both stdout and stderr
        filtered_stdout = filter_warnings(result.stdout)
        filtered_stderr = filter_warnings(result.stderr)

        # Combine filtered outputs if both exist
        combined_output = ""
        if filtered_stdout:
            combined_output = filtered_stdout
        if filtered_stderr:
            if combined_output:
                combined_output += f"\n{filtered_stderr}"
            else:
                combined_output = filtered_stderr

        # Only log if there's meaningful output, otherwise just confirm success
        if combined_output:
            log_info(f"✓ Git LFS hooks removed: {combined_output}", lang="en")
            log_info(f"✓ Git LFS钩子已移除: {combined_output}", lang="zh")
        else:
            log_info("✓ Git LFS hooks removed", lang="en")
            log_info("✓ Git LFS钩子已移除", lang="zh")
    except subprocess.CalledProcessError as e:
        # Filter warnings from stderr in case of error too
        stderr_msg = e.stderr.strip() if e.stderr else "Unknown error"
        filtered_stderr = ""
        if stderr_msg:
            lines = stderr_msg.split("\n")
            filtered_lines = [line for line in lines if not line.startswith("warning:")]
            filtered_stderr = "\n".join(filtered_lines).strip()
        log_info(
            f"✗ Failed to remove Git LFS hooks: {filtered_stderr or stderr_msg}",
            lang="en",
        )
        log_info(
            f"✗ 移除Git LFS钩子失败: {filtered_stderr or stderr_msg}",
            lang="zh",
        )
