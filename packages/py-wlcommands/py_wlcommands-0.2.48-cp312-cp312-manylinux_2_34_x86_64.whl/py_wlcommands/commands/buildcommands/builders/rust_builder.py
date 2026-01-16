"""Rust build utilities using maturin."""

import subprocess

from ....exceptions import CommandError
from ....utils.logging import log_error, log_info
from ....utils.subprocess import run_command


class RustBuilder:
    """Handle Rust build processes using maturin."""

    @staticmethod
    def run_maturin_build(python_executable: str | None) -> None:
        """Run maturin build process."""
        command = ["maturin", "build", "--release", "--out", "dist"]
        if python_executable:
            command.extend(["-i", python_executable])
        log_info(f"Trying to build with: {' '.join(command)}")
        subprocess.run(command, check=True, capture_output=False, text=True)

    @staticmethod
    def run_maturin_develop() -> None:
        """Run maturin develop for incremental builds."""
        log_info("Using maturin develop to build and install editable package...")
        log_info("使用 maturin develop 构建和安装可编辑包...", lang="zh")
        # 使用maturin的原生增量编译功能
        run_command(["maturin", "develop", "--skip-install"], capture_output=False)

    @staticmethod
    def build_full(python_executable: str | None) -> None:
        """Perform a full build with maturin."""
        RustBuilder.run_maturin_build(python_executable)

    @staticmethod
    def build_incremental() -> None:
        """Perform an incremental build with maturin develop."""
        RustBuilder.run_maturin_develop()
