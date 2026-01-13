"""Legacy compatibility layer for publish command.

This module provides backward compatibility for tests and legacy code
by wrapping the new publish executor with the old interface.
"""

from typing import Any

from .publish_executor import PublishExecutor


class PublishCommandImpl:
    """Legacy compatibility wrapper for tests and old code.

    This class provides the same interface as the original PublishCommand
    but internally uses the new PublishExecutor for all operations.
    """

    def __init__(self) -> None:
        """Initialize the legacy compatibility wrapper."""
        self.executor = PublishExecutor()

    @property
    def name(self) -> str:
        """Return the command name."""
        return "publish"

    @property
    def help(self) -> str:
        """Return the command help text."""
        return "Publish the project to PyPI"

    def add_arguments(self, parser) -> None:
        """Add arguments to the parser."""
        from .argument_parser import PublishArgumentParser

        PublishArgumentParser.add_arguments(parser)

    def execute(self, *args: Any, **kwargs: Any) -> None:
        """Execute the publish command using legacy interface."""
        import asyncio

        try:
            asyncio.run(self.executor.legacy_execute(**kwargs))
        except Exception as e:
            error_message = str(e) if e is not None else "Unknown error occurred"
            from ...exceptions import CommandError
            from ...utils.logging import log_error

            log_error(f"Publish failed: {error_message}")
            log_error(f"发布失败: {error_message}", lang="zh")
            raise CommandError(f"Publish failed: {error_message}")

    # Legacy methods that delegate to executor
    def _get_current_version(self) -> str:
        """Get current version - legacy compatibility."""
        return self.executor._get_current_version()

    async def _increment_version_async(self, dry_run: bool = False) -> None:
        """Increment version asynchronously - legacy compatibility."""
        await self.executor.increment_version_async(dry_run=dry_run)

    def _build_distribution_packages(self) -> None:
        """Build distribution packages - legacy compatibility."""
        self.executor.build_distribution_packages()

    def _get_dist_files(self) -> list:
        """Get distribution files - legacy compatibility."""
        return self.executor.get_dist_files()

    async def _handle_upload(
        self,
        repository: str,
        wheel_files,
        dry_run: bool = False,
        username=None,
        password=None,
    ) -> None:
        """Handle upload to PyPI - legacy compatibility."""
        await self.executor.handle_upload(
            repository, wheel_files, dry_run, username or "", password or ""
        )

    def _process_dist_files(
        self, dist_files, skip_build: bool = False, dry_run: bool = False
    ) -> list:
        """Process distribution files - legacy compatibility."""
        # Get all distribution files first
        all_dist_files = self.executor.process_dist_files(
            dist_files, skip_build, dry_run
        )

        # Extract only wheel files
        wheel_files = self.executor.extract_wheel_files(all_dist_files)
        return wheel_files

    def _collect_dist_files(self, dist_files: list | None = None) -> list:
        """Collect distribution files - legacy compatibility."""
        if dist_files is not None and len(dist_files) > 0:
            return dist_files
        return self.executor.get_dist_files()

    def _extract_wheel_files(self, dist_files: list) -> list:
        """Extract wheel files from distribution files - legacy compatibility."""
        return self.executor.extract_wheel_files(dist_files)

    async def _check_pypi_version_async(
        self, repository: str, current_version: str
    ) -> None:
        """Check version with PyPI asynchronously - legacy compatibility."""
        await self.executor.check_pypi_version_async(repository, current_version)

    # Property accessors for backward compatibility
    @property
    def version_service(self):
        """Return version service - legacy compatibility."""
        return self.executor.version_service

    @property
    def package_builder(self):
        """Return package builder - legacy compatibility."""
        return self.executor.package_builder

    @property
    def uploader(self):
        """Return uploader - legacy compatibility."""
        return self.executor.uploader

    # Additional properties for test compatibility
    @property
    def version_manager(self):
        """Return version manager - legacy compatibility."""
        return self.executor.version_manager

    @property
    def packager(self):
        """Return packager - legacy compatibility."""
        return self.executor.packager

    @property
    def upload_handler(self):
        """Return upload handler - legacy compatibility."""
        return self.executor.upload_handler

    # Allow setting these attributes for test compatibility
    @version_manager.setter
    def version_manager(self, value):
        """Set version manager - legacy compatibility."""
        self.executor.version_manager = value

    @packager.setter
    def packager(self, value):
        """Set packager - legacy compatibility."""
        self.executor.packager = value

    @upload_handler.setter
    def upload_handler(self, value):
        """Set upload handler - legacy compatibility."""
        self.executor.upload_handler = value

    # Legacy async execution method for tests
    async def _execute_async(
        self,
        repository: str = "pypi",
        skip_build: bool = False,
        dry_run: bool = False,
        username: str | None = None,
        password: str | None = None,
        no_auto_increment: bool = False,
        skip_version_check: bool = False,
        **kwargs,
    ) -> None:
        """Execute publish command asynchronously - legacy compatibility."""
        parsed_args = {
            "repository": repository,
            "skip_build": skip_build,
            "dry_run": dry_run,
            "username": username or "",
            "password": password or "",
            "no_auto_increment": no_auto_increment,
            "skip_version_check": skip_version_check,
        }
        parsed_args.update(kwargs)

        await self.executor.execute_publish_workflow(parsed_args, is_legacy_mode=True)
