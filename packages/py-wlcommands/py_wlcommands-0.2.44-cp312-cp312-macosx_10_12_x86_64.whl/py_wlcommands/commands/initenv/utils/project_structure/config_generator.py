"""WL configuration generator."""

import os
import shutil
from pathlib import Path

from .....utils.logging import log_info
from ..config_manager import ConfigManager


class ConfigGenerator:
    """Generate configuration files in .wl directory."""

    def __init__(self):
        self.config_manager = ConfigManager()

    def generate_configs(self) -> None:
        """Generate configuration files in .wl directory."""
        wl_dir = Path(".wl")
        log_dir = wl_dir / "log"
        config_file = wl_dir / "config.json"

        # Create log directory if it doesn't exist
        log_dir.mkdir(parents=True, exist_ok=True)
        log_info("✓ Created .wl/log directory")
        log_info("✓ 创建 .wl/log 目录", lang="zh")

        # Create default config file if it doesn't exist
        if not config_file.exists():
            try:
                # Create default config using the global config manager
                from .....utils.config import get_config_manager

                config_manager = get_config_manager()
                # Just accessing the config manager will create the default config file
                config = config_manager.get_all()
                log_info(f"✓ Created default config file at {config_file}")
                log_info(f"✓ 在 {config_file} 创建默认配置文件", lang="zh")
            except Exception as e:
                log_info(f"Warning: Failed to create default config file: {e}")
                log_info(f"警告: 创建默认配置文件失败: {e}", lang="zh")

        # Copy .codespellrc from vendors/config
        codespell_src = self.config_manager.get_vendor_config_path(
            "config/.codespellrc"
        )
        codespell_dest = wl_dir / ".codespellrc"
        if not codespell_dest.exists() and codespell_src.exists():
            shutil.copy2(codespell_src, codespell_dest)
            log_info("✓ Copied .wl/.codespellrc from template")
            log_info("✓ 从模板复制 .wl/.codespellrc", lang="zh")

        # Copy mypy.ini from vendors/config
        mypy_src = self.config_manager.get_vendor_config_path("config/mypy.ini")
        mypy_dest = wl_dir / "mypy.ini"
        # Copy if destination doesn't exist or is empty
        if mypy_src.exists() and (
            not mypy_dest.exists() or mypy_dest.stat().st_size == 0
        ):
            shutil.copy2(mypy_src, mypy_dest)
            log_info("✓ Copied .wl/mypy.ini from template")
            log_info("✓ 从模板复制 .wl/mypy.ini", lang="zh")

        # Copy .pre-commit-config.yaml from vendors/git
        precommit_src = self.config_manager.get_vendor_config_path(
            "git/.pre-commit-config.yaml"
        )
        precommit_dest = wl_dir / ".pre-commit-config.yaml"
        root_precommit = Path(".pre-commit-config.yaml")

        # Ensure .wl/.pre-commit-config.yaml exists
        if not precommit_dest.exists() and precommit_src.exists():
            shutil.copy2(precommit_src, precommit_dest)
            log_info("✓ Copied .wl/.pre-commit-config.yaml from template")
            log_info("✓ 从模板复制 .wl/.pre-commit-config.yaml", lang="zh")

        # Create hardlink to project root if it doesn't exist
        if not root_precommit.exists() and precommit_dest.exists():
            try:
                os.link(precommit_dest, root_precommit)
                log_info(
                    "✓ Created hardlink to .pre-commit-config.yaml in project root"
                )
                log_info("✓ 在项目根目录创建 .pre-commit-config.yaml 硬链接", lang="zh")
            except Exception as e:
                log_info(f"Warning: Failed to create hardlink: {e}")
                log_info(f"警告: 创建硬链接失败: {e}", lang="zh")
                # Fallback: Copy the file if hardlink fails
                shutil.copy2(precommit_dest, root_precommit)
                log_info("✓ Copied .pre-commit-config.yaml to project root (fallback)")
                log_info(
                    "✓ 复制 .pre-commit-config.yaml 到项目根目录 (备用方案)", lang="zh"
                )

        # Copy and configure git hooks from vendors/hooks to .wl/hooks
        from .hooks_manager import _copy_and_configure_hooks

        _copy_and_configure_hooks()
