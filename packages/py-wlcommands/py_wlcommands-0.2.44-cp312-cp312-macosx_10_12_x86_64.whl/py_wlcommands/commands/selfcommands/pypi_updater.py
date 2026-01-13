"""
PyPI updater for self update command.
"""

import subprocess
import sys

from py_wlcommands.commands.selfcommands.installation_manager import InstallationManager


class PypiUpdater:
    """Updater for updating the wl command from PyPI."""

    def update(self, uv_path: str, env: dict) -> None:
        """
        Update wl command from PyPI using the same installation method as current.

        Args:
            uv_path (str): Path to the uv executable.
            env (dict): Environment variables to use for the update.
        """
        from py_wlcommands.utils.logging import log_info
        from py_wlcommands.utils.version.pypi_version_checker import PyPIVersionChecker
        from py_wlcommands.utils.version.version_comparator import VersionComparator
        from py_wlcommands.utils.version.version_detectors import VersionDetector

        installation_manager = InstallationManager()
        install_method = installation_manager.detect_installation_method()

        detector = VersionDetector()
        checker = PyPIVersionChecker()
        comparator = VersionComparator()

        current_version = detector.get_current_version(comparator)
        log_info(f"Current local version: {current_version}")
        log_info(f"当前本地版本: {current_version}", lang="zh")

        pypi_version = checker._get_pypi_version()
        if pypi_version is None:
            log_info("Failed to get PyPI version. Skipping update.")
            log_info("无法获取PyPI版本。跳过更新。", lang="zh")
            return

        log_info(f"Latest PyPI version: {pypi_version}")
        log_info(f"最新PyPI版本: {pypi_version}", lang="zh")

        if not comparator.is_version_greater(pypi_version, current_version):
            log_info(
                f"Local version {current_version} is already up to date with PyPI version {pypi_version}."
            )
            log_info(
                f"本地版本 {current_version} 已经与PyPI版本 {pypi_version} 保持最新。",
                lang="zh",
            )
            return

        log_info(f"Updating from version {current_version} to {pypi_version}...")
        log_info(f"正在从版本 {current_version} 更新到 {pypi_version}...", lang="zh")

        try:
            if install_method == "uv_tool":
                cmd = [uv_path, "tool", "install", "py_wlcommands"]
                log_info(f"Running: {' '.join(cmd)}")
                subprocess.run(
                    cmd,
                    check=True,
                    capture_output=False,
                    text=True,
                    encoding="utf-8" if sys.platform.startswith("win") else None,
                    env=env,
                )
            elif install_method == "uv_pip":
                cmd = [
                    uv_path,
                    "pip",
                    "install",
                    "--upgrade",
                    "--system",
                    "py_wlcommands",
                ]
                log_info(f"Running: {' '.join(cmd)}")
                subprocess.run(
                    cmd,
                    check=True,
                    capture_output=False,
                    text=True,
                    encoding="utf-8" if sys.platform.startswith("win") else None,
                    env=env,
                )
            elif install_method == "pip":
                cmd = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "py_wlcommands",
                ]
                log_info(f"Running: {' '.join(cmd)}")
                subprocess.run(
                    cmd,
                    check=True,
                    capture_output=False,
                    text=True,
                    encoding="utf-8" if sys.platform.startswith("win") else None,
                    env=env,
                )
            else:
                log_info(
                    f"Unknown installation method: {install_method}, falling back to uv tool install."
                )
                log_info(
                    f"未知安装方法: {install_method}，回退到uv tool安装。", lang="zh"
                )
                cmd = [uv_path, "tool", "install", "py_wlcommands"]
                log_info(f"Running: {' '.join(cmd)}")
                subprocess.run(
                    cmd,
                    check=True,
                    capture_output=False,
                    text=True,
                    encoding="utf-8" if sys.platform.startswith("win") else None,
                    env=env,
                )

            log_info("Successfully updated from PyPI!")
            log_info("成功从PyPI更新！", lang="zh")
        except subprocess.CalledProcessError as e:
            log_info(f"Failed to update from PyPI: {e}")
            log_info(f"从PyPI更新失败: {e}", lang="zh")
            raise
