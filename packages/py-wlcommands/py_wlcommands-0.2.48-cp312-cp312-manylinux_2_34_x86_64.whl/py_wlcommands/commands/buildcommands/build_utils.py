"""Build utilities for WL Commands.

This module serves as the entry point for the modularized build functionality.
主要功能委托给专门的模块以获得更好的组织结构。
"""

import shutil

from .builders.cleanup import CleanupManager
from .builders.coordinator import BuildCoordinator
from .builders.environment import EnvironmentDetector
from .builders.rust_builder import RustBuilder
from .builders.stubs import StubsManager


# Backward compatibility: re-export all the main functions
def is_rust_enabled() -> bool:
    """Check if Rust is enabled for this project."""
    return EnvironmentDetector.is_rust_enabled()


def build_project_full() -> None:
    """Perform a full project build."""
    coordinator = BuildCoordinator()
    coordinator.build_project_full()


def build_windows() -> None:
    """Build the project on Windows."""
    try:
        coordinator = BuildCoordinator()
        coordinator.build_windows()
    except Exception as e:
        from py_wlcommands.exceptions import CommandError

        raise CommandError(f"Build failed: {e}")


def build_unix() -> None:
    """Build the project on Unix-like systems."""
    try:
        coordinator = BuildCoordinator()
        coordinator.build_unix()
    except Exception as e:
        from py_wlcommands.exceptions import CommandError

        raise CommandError(f"Build failed: {e}")


def build_project() -> None:
    """Build the project based on the current platform."""
    try:
        coordinator = BuildCoordinator()
        coordinator.build_project()
    except Exception as e:
        from py_wlcommands.exceptions import CommandError

        raise CommandError(f"Build failed: {e}")


# Re-export classes for advanced usage
__all__ = [
    "is_rust_enabled",
    "build_project_full",
    "build_windows",
    "build_unix",
    "build_project",
    "EnvironmentDetector",
    "StubsManager",
    "RustBuilder",
    "CleanupManager",
    "BuildCoordinator",
]
