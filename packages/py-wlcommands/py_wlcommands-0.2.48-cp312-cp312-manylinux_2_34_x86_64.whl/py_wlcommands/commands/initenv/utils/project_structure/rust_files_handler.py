"""Rust example files handler."""

import shutil
from pathlib import Path

from .....utils.logging import log_info
from ..config_manager import ConfigManager


class RustFilesHandler:
    """Copy Rust example files from vendors to project."""

    def __init__(self):
        self.config_manager = ConfigManager()

    def copy_rust_files(self, project_name: str) -> None:
        """Copy Rust example files from vendors to project."""
        try:
            # Copy lib files
            vendor_lib_dir = self.config_manager.get_vendor_config_path("rust/lib")
            target_lib_dir = Path(f"src/{project_name}/lib")

            for file_name in ["__init__.py", "rust_utils.py"]:
                src_file = vendor_lib_dir / file_name
                dest_file = target_lib_dir / file_name
                if src_file.exists() and not dest_file.exists():
                    if file_name == "rust_utils.py":
                        # Read template content and replace project_name placeholder
                        with open(src_file, encoding="utf-8") as f:
                            content = f.read()
                        content = content.replace("{project_name}", project_name)
                        # Write modified content to dest_file
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        with open(dest_file, "w", encoding="utf-8") as f:
                            f.write(content)
                    else:
                        # For other files, use direct copy
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, dest_file)
                    log_info(f"✓ Copied {file_name} to {target_lib_dir}")
                    log_info(f"✓ 复制 {file_name} 到 {target_lib_dir}", lang="zh")

            # Copy test file
            vendor_test_dir = self.config_manager.get_vendor_config_path("rust/tests")
            target_test_dir = Path("tests")

            test_file = "test_rust_fallback.py"
            src_test = vendor_test_dir / test_file
            dest_test = target_test_dir / test_file
            if src_test.exists() and not dest_test.exists():
                shutil.copy2(src_test, dest_test)
                log_info(f"✓ Copied {test_file} to {target_test_dir}")
                log_info(f"✓ 复制 {test_file} 到 {target_test_dir}", lang="zh")

        except Exception as e:
            log_info(f"Warning: Failed to copy Rust example files: {e}")
            log_info(f"警告: 复制 Rust 示例文件失败: {e}", lang="zh")
