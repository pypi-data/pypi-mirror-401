"""Publish command implementation for WL Commands.

This module serves as the entry point for the modularized publish functionality.
主要功能委托给专门的模块以获得更好的组织结构。
"""

import argparse
import asyncio
from typing import Any

from ...commands import Command, register_command
from ...exceptions import CommandError
from ...utils.logging import log_error, log_info
from .publish_executor import PublishExecutor


@register_command("publish")
class PublishCommand(Command):
    """Publish command for WL Commands - coordinator for specialized modules."""

    def __init__(self) -> None:
        """Initialize the publish command."""
        self.executor = PublishExecutor()

    @property
    def name(self) -> str:
        """Return the command name."""
        return "publish"

    @property
    def help(self) -> str:
        """Return the command help text."""
        return "Publish the project to PyPI"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add arguments to the parser."""
        self.executor.argument_parser.add_arguments(parser)

    def execute(self, *args: Any, **kwargs: Any) -> None:
        """Execute the publish command."""
        try:
            asyncio.run(self._execute_async(*args, **kwargs))
        except Exception as e:
            # 确保我们处理的是一个有效的异常对象
            error_message = str(e) if e is not None else "Unknown error occurred"
            log_error(f"Publish failed: {error_message}")
            log_error(f"发布失败: {error_message}", lang="zh")
            raise CommandError(f"Publish failed: {error_message}")

    async def _execute_async(self, *args: Any, **kwargs: Any) -> None:
        """Async implementation of the publish command."""
        # Parse arguments using the specialized parser
        parsed_args = self.executor.parse_arguments("parser", **kwargs)

        # Execute the complete publish workflow
        await self.executor.execute_publish_workflow(parsed_args, is_legacy_mode=False)
