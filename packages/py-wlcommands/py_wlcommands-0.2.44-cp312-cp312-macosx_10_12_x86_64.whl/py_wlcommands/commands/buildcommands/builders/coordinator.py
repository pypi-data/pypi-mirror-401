"""Build coordination logic for different platforms and scenarios."""

import sys

from ....exceptions import CommandError
from ....utils.logging import log_error, log_info
from ....utils.subprocess import run_command
from .cleanup import CleanupManager
from .environment import EnvironmentDetector
from .rust_builder import RustBuilder
from .stubs import StubsManager


class BuildCoordinator:
    """Coordinate build operations across different platforms and scenarios."""

    def __init__(self):
        self.environment_detector = EnvironmentDetector()
        self.stubs_manager = StubsManager()
        self.rust_builder = RustBuilder()
        self.cleanup_manager = CleanupManager()

    def build_project_full(self) -> None:
        """Perform a full project build."""
        rust_enabled = self.environment_detector.is_rust_enabled()

        try:
            if rust_enabled:
                log_info("Using maturin build for full compilation...")
                log_info("使用 maturin build 进行完整编译...", lang="zh")

                python_executable, is_workspace = (
                    self.environment_detector.resolve_python_executable()
                )
                self.stubs_manager.generate_and_copy_stubs()
                self.rust_builder.build_full(python_executable)
                self.cleanup_manager.cleanup_after_build(is_workspace)
            else:
                log_info(
                    "Pure Python project, using uv pip install -e . for installation..."
                )
                log_info(
                    "纯 Python 项目，使用 uv pip install -e . 进行安装...", lang="zh"
                )
                run_command(
                    ["uv", "pip", "install", "--link-mode=copy", "-e", "."],
                    capture_output=False,
                )

            log_info("✓ Full build completed successfully")
            log_info("✓ 完整构建成功完成", lang="zh")
        except Exception as e:
            log_error(f"Full build failed: {e}")
            log_error(f"完整构建失败: {e}", lang="zh")
            raise CommandError(f"Full build failed: {e}")

    def build_windows(self) -> None:
        """Build the project on Windows."""
        rust_enabled = self.environment_detector.is_rust_enabled()

        try:
            if rust_enabled:
                self.rust_builder.build_incremental()
            else:
                log_info(
                    "Pure Python project, using uv pip install -e . for installation..."
                )
                log_info(
                    "纯 Python 项目，使用 uv pip install -e . 进行安装...", lang="zh"
                )
                run_command(
                    ["uv", "pip", "install", "--link-mode=copy", "-e", "."],
                    capture_output=False,
                )

            log_info("✓ Build completed successfully")
            log_info("✓ 构建成功完成", lang="zh")
        except CommandError as e:
            log_error(f"Build failed: {e}")
            log_error(f"构建失败: {e}", lang="zh")
            raise
        except Exception as e:
            log_error(f"Unexpected error during build: {e}")
            log_error(f"构建过程中出现意外错误: {e}", lang="zh")
            raise CommandError(f"Build failed: {e}")

    def build_unix(self) -> None:
        """Build the project on Unix-like systems."""
        rust_enabled = self.environment_detector.is_rust_enabled()

        try:
            if rust_enabled:
                self.rust_builder.build_incremental()
            else:
                log_info(
                    "Pure Python project, using uv pip install -e . for installation..."
                )
                log_info(
                    "纯 Python 项目，使用 uv pip install -e . 进行安装...", lang="zh"
                )
                run_command(
                    ["uv", "pip", "install", "--link-mode=copy", "-e", "."],
                    capture_output=False,
                )

            log_info("✓ Build completed successfully")
            log_info("✓ 构建成功完成", lang="zh")
        except CommandError as e:
            log_error(f"Build failed: {e}")
            log_error(f"构建失败: {e}", lang="zh")
            raise
        except Exception as e:
            log_error(f"Unexpected error during build: {e}")
            log_error(f"构建过程中出现意外错误: {e}", lang="zh")
            raise CommandError(f"Build failed: {e}")

    def build_project(self) -> None:
        """Build the project based on the current platform."""
        if sys.platform.startswith("win"):
            self.build_windows()
        else:
            self.build_unix()
