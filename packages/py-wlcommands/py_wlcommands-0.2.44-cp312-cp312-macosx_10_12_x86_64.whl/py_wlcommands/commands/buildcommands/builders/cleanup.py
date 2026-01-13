"""Build cleanup utilities."""

import shutil
from pathlib import Path

from ....utils.logging import log_error, log_info


class CleanupManager:
    """Handle post-build cleanup operations."""

    @staticmethod
    def cleanup_after_build(is_workspace: bool) -> None:
        """Clean up temporary files and directories after build."""
        try:
            root = Path.cwd()
            typings_path = root / "typings"
            if typings_path.exists():
                shutil.rmtree(typings_path, ignore_errors=True)
                log_info("✓ typings directory removed")

            src_path = root / "src"
            if src_path.exists():
                removed = 0
                for p in src_path.rglob("*.pyi"):
                    try:
                        p.unlink()
                        removed += 1
                    except Exception:
                        pass
                if removed:
                    log_info(f"✓ Removed {removed} .pyi files from src")

        except Exception as e:
            log_error(f"Failed to cleanup stubs: {e}")
