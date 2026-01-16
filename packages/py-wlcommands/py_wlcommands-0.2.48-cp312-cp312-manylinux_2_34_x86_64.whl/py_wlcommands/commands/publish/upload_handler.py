"""Upload handling for publish command."""

import asyncio
from typing import Any, List

from ...utils.logging import log_info
from .pypi_uploader import PyPIUploader


class UploadHandler:
    """Handle package upload to PyPI."""

    def __init__(self) -> None:
        """Initialize the upload handler."""
        self.uploader = PyPIUploader()

    async def handle_upload(
        self,
        repository: str,
        wheel_files: list[Any],
        dry_run: bool,
        username: str,
        password: str,
    ) -> None:
        """Handle the upload process."""
        if dry_run:
            log_info("Dry run: No files will be uploaded.")
            return

        if wheel_files:
            # upload_to_pypi is currently sync, but we can call it directly in async context
            self.uploader.upload_to_pypi(repository, wheel_files, username, password)

    def upload_to_pypi(
        self,
        repository: str,
        wheel_files: list[Any],
        dry_run: bool,
        username: str,
        password: str,
    ) -> None:
        """Sync wrapper for upload handling - for backward compatibility with tests."""
        # Call the async version synchronously for backward compatibility
        asyncio.run(
            self.upload_to_pypi_async(
                repository, wheel_files, dry_run, username, password
            )
        )

    async def upload_to_pypi_async(
        self,
        repository: str,
        wheel_files: list[Any],
        dry_run: bool,
        username: str,
        password: str,
    ) -> None:
        """Async wrapper for upload handling."""
        if dry_run:
            log_info("Dry run mode: Would upload to PyPI")
            log_info("Dry run mode: 将上传到 PyPI", lang="zh")
            log_info("✓ Dry run completed successfully!")
            log_info("✓ 干运行完成！", lang="zh")
            return

        await self.handle_upload(repository, wheel_files, dry_run, username, password)
        log_info("✓ Package published successfully!")
        log_info("✓ 包发布成功！", lang="zh")
