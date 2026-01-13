"""Core execution engine for publish command.

This module contains the shared execution logic used by both the main command
and legacy compatibility layer to eliminate code duplication.
"""

import argparse
import asyncio
from typing import Any, Dict, List, Union

from ...exceptions import CommandError
from ...utils.logging import log_error, log_info
from .argument_parser import PublishArgumentParser
from .packager import Packager
from .upload_handler import UploadHandler
from .version_manager import VersionManager


class PublishExecutor:
    """Core execution engine for publish functionality."""

    def __init__(self) -> None:
        """Initialize the publish executor."""
        self.argument_parser = PublishArgumentParser()
        self.version_manager = VersionManager()
        self.packager = Packager()
        self.upload_handler = UploadHandler()

    def parse_arguments(self, method: str = "parser", **kwargs: Any) -> dict[str, Any]:
        """Parse arguments using specified method."""
        if method == "parser":
            # Use dedicated argument parser
            parser = argparse.ArgumentParser()
            self.argument_parser.add_arguments(parser)

            # Convert kwargs to arg format
            arg_list = self._kwargs_to_args(kwargs)
            parsed = parser.parse_args(arg_list)
            return vars(parsed)
        else:
            # Use kwargs directly (for legacy compatibility)
            return self.argument_parser.parse_arguments(**kwargs)

    def _kwargs_to_args(self, kwargs: dict[str, Any]) -> list[str]:
        """Convert keyword arguments to command line args format."""
        arg_list = []
        for key, value in kwargs.items():
            # Convert underscore to dash for CLI args
            cli_key = f"--{key.replace('_', '-')}"

            if isinstance(value, bool):
                if value:
                    arg_list.append(cli_key)
            elif value is not None:
                arg_list.extend([cli_key, str(value)])

        return arg_list

    async def execute_publish_workflow(
        self, parsed_args: dict[str, Any], is_legacy_mode: bool = False
    ) -> None:
        """Execute the complete publish workflow."""
        try:
            # Get current version
            current_version = self._get_current_version()
            log_info(f"Current local version: {current_version}")

            # Check version against PyPI unless explicitly skipped
            if not parsed_args.get("skip_version_check", False):
                try:
                    await self.version_manager.check_pypi_version_async(
                        parsed_args.get("repository", "pypi"), current_version
                    )
                except Exception as e:
                    # Version check failed, but we should continue execution
                    log_error(f"Version check failed: {e}")
                    log_error(f"版本检查失败: {e}", lang="zh")
                    # Continue with the publish process
                    pass

            # Auto increment version unless explicitly disabled
            if not parsed_args.get("no_auto_increment", False):
                await self.version_manager.increment_version_async(
                    no_auto_increment=False, dry_run=parsed_args.get("dry_run", False)
                )

            # Determine if rebuild is needed after version increment
            skip_build = parsed_args.get("skip_build", False)
            if not parsed_args.get("no_auto_increment", False):
                if self.version_manager.should_rebuild_after_increment(
                    no_auto_increment=False
                ):
                    skip_build = False

            # Build the project if not skipped and not doing dry run
            if not skip_build and not parsed_args.get("dry_run", False):
                self.packager.build_distribution_packages(
                    skip_build, parsed_args.get("dry_run", False)
                )

            # Process distribution files
            wheel_files = self.packager.process_dist_files(
                [], skip_build, parsed_args.get("dry_run", False)
            )

            # Upload to PyPI
            if not parsed_args.get("dry_run", False):
                await self.upload_handler.upload_to_pypi_async(
                    parsed_args.get("repository", "pypi"),
                    wheel_files,
                    parsed_args.get("dry_run", False),
                    parsed_args.get("username", "") or "",
                    parsed_args.get("password", "") or "",
                )

        except Exception as e:
            error_message = str(e) if e is not None else "Unknown error occurred"
            log_error(f"Publish failed: {error_message}")
            log_error(f"发布失败: {error_message}", lang="zh")
            raise CommandError(f"Publish failed: {error_message}")

    def _get_current_version(self) -> str:
        """Get current version."""
        return self.version_manager.get_current_version()

    # Legacy compatibility methods
    async def legacy_execute(self, **kwargs: Any) -> None:
        """Execute publish with legacy argument format."""
        parsed_args = self.parse_arguments("legacy", **kwargs)
        await self.execute_publish_workflow(parsed_args, is_legacy_mode=True)

    def build_distribution_packages(self) -> None:
        """Build distribution packages - legacy compatibility."""
        self.packager.build_distribution_packages(skip_build=False, dry_run=False)

    def get_dist_files(self) -> list:
        """Get distribution files - legacy compatibility."""
        return self.packager.process_dist_files([], skip_build=False, dry_run=False)

    def process_dist_files(
        self, dist_files: list, skip_build: bool = False, dry_run: bool = False
    ) -> list:
        """Process distribution files - legacy compatibility."""
        return self.packager.process_dist_files(dist_files, skip_build, dry_run)

    async def handle_upload(
        self,
        repository: str,
        wheel_files: list,
        dry_run: bool = False,
        username: str = "",
        password: str = "",
    ) -> None:
        """Handle upload to PyPI - legacy compatibility."""
        if not dry_run:
            await self.upload_handler.upload_to_pypi_async(
                repository, wheel_files, dry_run, username, password
            )

    def extract_wheel_files(self, dist_files: list) -> list:
        """Extract wheel files - legacy compatibility."""
        import pathlib

        wheel_files = []
        for file in dist_files:
            if isinstance(file, pathlib.Path):
                if file.suffix == ".whl":
                    wheel_files.append(file)
            elif hasattr(file, "name") and str(file.name).endswith(".whl"):
                wheel_files.append(file)
            elif hasattr(file, "suffix") and str(file.suffix) == ".whl":
                wheel_files.append(file)
        return wheel_files

    async def increment_version_async(
        self, no_auto_increment: bool = False, dry_run: bool = False
    ) -> None:
        """Increment version - legacy compatibility."""
        await self.version_manager.increment_version_async(
            no_auto_increment=no_auto_increment, dry_run=dry_run
        )

    async def check_pypi_version_async(
        self, repository: str, current_version: str
    ) -> None:
        """Check PyPI version - legacy compatibility."""
        try:
            await self.version_manager.check_pypi_version_async(
                repository, current_version
            )
        except Exception:
            # Version check failed, but continue execution
            pass

    # Property accessors for backward compatibility
    @property
    def version_service(self):
        """Return version service - legacy compatibility."""
        return self.version_manager.version_service

    @property
    def package_builder(self):
        """Return package builder - legacy compatibility."""
        return self.packager

    @property
    def uploader(self):
        """Return uploader - legacy compatibility."""
        return self.upload_handler
