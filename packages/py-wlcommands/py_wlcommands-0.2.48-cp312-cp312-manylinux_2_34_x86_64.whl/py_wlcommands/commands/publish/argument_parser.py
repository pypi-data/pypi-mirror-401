"""Argument parsing for publish command."""

import argparse
from typing import Any, Dict


class PublishArgumentParser:
    """Handle argument parsing for publish command."""

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser) -> None:
        """Add arguments to the parser."""
        parser.add_argument(
            "--repository",
            "-r",
            default="pypi",
            help="Repository to upload to (default: pypi)",
        )
        parser.add_argument(
            "--skip-build",
            action="store_true",
            help="Skip building the package, use existing dist files",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Perform a dry run without actually uploading",
        )
        parser.add_argument(
            "--username",
            help="Username for uploading to PyPI",
        )
        parser.add_argument(
            "--password",
            help="Password or API token for uploading to PyPI",
        )
        parser.add_argument(
            "--no-auto-increment",
            action="store_true",
            help="Do not automatically increment the patch version before publishing",
        )
        parser.add_argument(
            "--skip-version-check",
            action="store_true",
            help="Skip version check against PyPI server",
        )

    @staticmethod
    def parse_arguments(**kwargs: Any) -> dict[str, Any]:
        """Parse and return arguments as dictionary."""
        return {
            "repository": kwargs.get("repository", "pypi"),
            "skip_build": kwargs.get("skip_build", False),
            "dry_run": kwargs.get("dry_run", False),
            "username": kwargs.get("username"),
            "password": kwargs.get("password"),
            "no_auto_increment": kwargs.get("no_auto_increment", False),
            "skip_version_check": kwargs.get("skip_version_check", False),
        }
