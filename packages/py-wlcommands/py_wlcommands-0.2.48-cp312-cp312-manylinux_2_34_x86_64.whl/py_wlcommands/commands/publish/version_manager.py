"""Version management for publish command."""

import asyncio
from typing import Any

from ...utils.logging import log_info
from ...utils.version import VersionService


class VersionManager:
    """Handle version operations for publish command."""

    def __init__(self) -> None:
        """Initialize the version manager."""
        self.version_service = VersionService()

    async def check_pypi_version_async(
        self, repository: str, current_version: str
    ) -> None:
        """Check version against PyPI server."""
        try:
            await self.version_service.check_version_with_pypi_async(
                repository, current_version
            )
        except Exception as e:
            # If version check fails, we should still allow publishing if explicitly requested
            log_info(f"Warning: Version check failed: {e}")

    async def increment_version_async(
        self, no_auto_increment: bool, dry_run: bool
    ) -> None:
        """Increment version if auto-increment is enabled."""
        if not no_auto_increment and not dry_run:
            log_info("Incrementing version...")
            await self.version_service.increment_version_async(dry_run=False)
        elif not no_auto_increment and dry_run:
            log_info("Dry run mode: Would increment version")
            log_info("Dry run mode: 将递增版本号", lang="zh")
            # For dry run, we can use the sync method since no actual changes are made
            self.version_service.increment_version(dry_run=True)

    def get_current_version(self) -> str:
        """Get current version."""
        return self.version_service.get_current_version()

    def should_rebuild_after_increment(self, no_auto_increment: bool) -> bool:
        """Determine if rebuild is needed after version increment."""
        return not no_auto_increment

    def check_version_with_pypi(self, repository: str, current_version: str) -> None:
        """Check version against PyPI server (sync version for backward compatibility)."""
        # For backward compatibility with tests, this calls the sync version directly
        try:
            self.version_service.check_version_with_pypi(repository, current_version)
        except Exception as e:
            # If version check fails, we should still allow publishing if explicitly requested
            log_info(f"Warning: Version check failed: {e}")

    def increment_version(self, dry_run: bool = False) -> None:
        """Increment version (sync version for backward compatibility)."""
        # For backward compatibility with tests, this calls the sync version directly
        self.version_service.increment_version(dry_run=dry_run)
