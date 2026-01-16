"""SOP file generator."""

import shutil
from pathlib import Path

from .....utils.logging import log_info
from ..config_manager import ConfigManager


class SopGenerator:
    """Generate SOP files for Rust-Python integration."""

    def __init__(self):
        self.config_manager = ConfigManager()

    def generate_sop_files(self, project_name: str) -> None:
        """Generate SOP files for Rust-Python integration."""
        try:
            # Generate Rust README SOP
            rust_readme_src = self.config_manager.get_vendor_config_path(
                "sop_doc/rust-readme.md"
            )
            rust_readme_dest = Path("rust/README.md")
            if rust_readme_src.exists() and not rust_readme_dest.exists():
                shutil.copy2(rust_readme_src, rust_readme_dest)
                log_info("✓ Generated Rust-Python integration SOP in rust/README.md")
                log_info("✓ 在 rust/README.md 生成 Rust-Python 集成 SOP", lang="zh")

            # Generate Python SOP for Rust extension
            python_sop_src = self.config_manager.get_vendor_config_path(
                "sop_doc/python-sop.md"
            )
            python_sop_dest = Path(f"src/{project_name}/lib/sop.md")
            if python_sop_src.exists() and not python_sop_dest.exists():
                shutil.copy2(python_sop_src, python_sop_dest)
                log_info(
                    f"✓ Generated Python SOP for Rust extension in src/{project_name}/lib/sop.md"
                )
                log_info(
                    f"✓ 在 src/{project_name}/lib/sop.md 生成 Python 引入 Rust 扩展 SOP",
                    lang="zh",
                )
        except Exception as e:
            log_info(f"Warning: Failed to generate SOP files: {e}")
            log_info(f"警告: 生成 SOP 文件失败: {e}", lang="zh")
