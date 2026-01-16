"""Environment detection and Python executable resolution utilities."""

import os
import subprocess
import sys
from pathlib import Path

from ....exceptions import CommandError
from ....utils.logging import log_error, log_info
from ....utils.workspace_detector import WorkspaceDetectionError, WorkspaceDetector


class EnvironmentDetector:
    """Detect project environment and resolve Python executable paths."""

    @staticmethod
    def is_rust_enabled() -> bool:
        """
        Check if Rust is enabled for this project.

        Returns:
            bool: True if Rust is enabled, False otherwise.
        """
        rust_dir = os.path.join(os.getcwd(), "rust")
        cargo_toml = os.path.join(rust_dir, "Cargo.toml")
        return os.path.exists(cargo_toml)

    @staticmethod
    def _create_venv() -> None:
        """Create virtual environment using uv."""
        try:
            # Use uv to create virtual environment
            cmd = ["uv", "venv"]
            subprocess.run(
                cmd,
                check=True,
                capture_output=False,
                text=True,
            )
            log_info("✓ Virtual environment created successfully")
        except subprocess.CalledProcessError as e:
            log_error(f"Failed to create virtual environment: {e}")
            raise CommandError(f"Failed to create virtual environment: {e}")
        except Exception as e:
            log_error(f"Unexpected error creating virtual environment: {e}")
            raise CommandError(f"Failed to create virtual environment: {e}")

    def resolve_python_executable(self) -> tuple[str | None, bool]:
        """
        Resolve the appropriate Python executable for the current environment.

        Returns:
            tuple: (python_executable_path, is_workspace) where:
                - python_executable_path: Path to Python executable or None
                - is_workspace: True if running in a workspace environment
        """
        detector = WorkspaceDetector()
        is_workspace = detector.detect(Path.cwd())

        if not is_workspace:
            log_info("Not in uv workspace environment")
            return "python", False

        log_info("✓ uv workspace environment detected")
        venv_root = detector.get_venv_path(Path.cwd())

        if venv_root is None:
            try:
                venv_str = detector.get_active_venv_path_str(Path.cwd())
                venv_root = Path(venv_str)
            except Exception:
                venv_root = None

        if venv_root is None:
            log_info("No venv found, creating local .venv for build...")
            self._create_venv()
            venv_root = Path(".venv")

        if sys.platform.startswith("win"):
            return str((venv_root / "Scripts" / "python.exe").resolve()), True
        return str((venv_root / "bin" / "python").resolve()), True
