"""
Command to clean project build artifacts.
"""

import sys

from py_wlcommands.commands import Command, register_command, validate_command_args
from py_wlcommands.utils.logging import log_info

from .clean_utils import (
    clean_all_artifacts,
    clean_build_artifacts,
    clean_cache_artifacts,
    clean_lfs_artifacts,
    clean_logs_artifacts,
    clean_rust_artifacts,
    clean_venv_artifacts,
)


@register_command("clean")
class CleanCommand(Command):
    """Command to clean project build artifacts."""

    @property
    def name(self) -> str:
        return "clean"

    @property
    def help(self) -> str:
        return "Clean project build artifacts"

    @classmethod
    def add_arguments(cls, parser) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "target",
            nargs="?",
            default="build",
            choices=["build", "all", "rust", "lfs", "venv", "cache", "logs"],
            help="Target to clean (build, all, rust, lfs, venv, cache, logs)",
        )
        parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            help="Skip confirmation and proceed directly",
        )
        parser.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            help="Interactive confirmation for each cleaning operation",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview files to be deleted without actually deleting them",
        )
        parser.add_argument(
            "--config",
            type=str,
            help="Path to custom cleaning configuration file",
        )

    def _get_cleaning_function(self, target: str):
        """Get the appropriate cleaning function based on target."""
        cleaning_functions = {
            "all": clean_all_artifacts,
            "rust": clean_rust_artifacts,
            "lfs": clean_lfs_artifacts,
            "venv": clean_venv_artifacts,
            "cache": clean_cache_artifacts,
            "logs": clean_logs_artifacts,
            "build": clean_build_artifacts,
        }
        return cleaning_functions.get(target, clean_build_artifacts)

    def _get_start_messages(self, target: str):
        """Get start messages for different targets."""
        messages = {
            "all": (
                "Cleaning all project artifacts including virtual environment...",
                "正在清理所有项目产物，包括虚拟环境...",
            ),
            "rust": ("Cleaning Rust build artifacts...", "正在清理Rust构建产物..."),
            "lfs": ("Cleaning Git LFS deployment...", "正在清理Git LFS部署..."),
            "venv": ("Cleaning virtual environment...", "正在清理虚拟环境..."),
            "cache": ("Cleaning cache directories...", "正在清理缓存目录..."),
            "logs": ("Cleaning log files...", "正在清理日志文件..."),
            "build": ("Cleaning project build artifacts...", "正在清理项目构建产物..."),
        }
        return messages.get(
            target, ("Cleaning project build artifacts...", "正在清理项目构建产物...")
        )

    def _get_success_messages(self, target: str):
        """Get success messages for different targets."""
        messages = {
            "all": (
                "Complete project cleaning completed successfully!",
                "完整项目清理成功完成！",
            ),
            "rust": ("Rust cleaning completed successfully!", "Rust清理成功完成！"),
            "lfs": (
                "Git LFS cleaning completed successfully!",
                "Git LFS清理成功完成！",
            ),
            "venv": (
                "Virtual environment cleaning completed successfully!",
                "虚拟环境清理成功完成！",
            ),
            "cache": (
                "Cache directories cleaning completed successfully!",
                "缓存目录清理成功完成！",
            ),
            "logs": (
                "Log files cleaning completed successfully!",
                "日志文件清理成功完成！",
            ),
            "build": ("Project cleaning completed successfully!", "项目清理成功完成！"),
        }
        return messages.get(
            target, ("Project cleaning completed successfully!", "项目清理成功完成！")
        )

    @validate_command_args()
    def execute(
        self,
        target: str = "build",
        yes: bool = False,
        interactive: bool = False,
        dry_run: bool = False,
        config: str | None = None,
    ) -> None:
        """
        Clean project - equivalent to make clean
        清理项目 - 等效于 make clean
        """
        # Use simple logging instead of structured logging for user-facing messages
        start_msg_en, start_msg_zh = self._get_start_messages(target)
        log_info(start_msg_en)
        log_info(start_msg_zh, lang="zh")

        # Log dry run mode
        if dry_run:
            log_info("Dry run mode: No files will be deleted.")
            log_info("Dry run模式：不会删除任何文件。", lang="zh")

        try:
            # Get and execute the appropriate cleaning function
            cleaning_function = self._get_cleaning_function(target)
            cleaning_function(dry_run=dry_run, config=config)

            # Log success message
            success_msg_en, success_msg_zh = self._get_success_messages(target)
            log_info(success_msg_en)
            log_info(success_msg_zh, lang="zh")
        except Exception as e:
            log_info(f"Error cleaning project: {e}", lang="en")
            log_info(f"错误：清理项目失败: {e}", lang="zh")
            sys.exit(1)
