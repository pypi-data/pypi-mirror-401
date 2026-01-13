"""Type stubs generation and management utilities."""

import os
import shutil
from pathlib import Path

from ....commands.format.python_formatter import generate_type_stubs
from ....utils.logging import log_error, log_info
from ....utils.uv_tool import is_running_in_uv_tool


class StubsManager:
    """Manage type stubs generation and copying."""

    @staticmethod
    def generate_and_copy_stubs() -> None:
        """Generate type stubs and copy them to the appropriate locations."""
        try:
            root = Path.cwd()
            src_path = root / "src"
            typings_path = root / "typings"

            if not src_path.exists():
                if not is_running_in_uv_tool():
                    log_info(f"Target {src_path} does not exist, skipping...")
                return

            log_info(f"Generating type stubs for {src_path} -> {typings_path}")
            generate_type_stubs(
                str(src_path), str(typings_path), os.environ.copy(), quiet=False
            )
            log_info("✓ Type stubs generated")

            package_root = src_path / "py_wlcommands"
            stub_root = typings_path / "py_wlcommands"

            if stub_root.exists():
                for pyi in stub_root.rglob("*.pyi"):
                    rel = pyi.relative_to(stub_root)
                    dest = package_root / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(pyi, dest)
                log_info("✓ Type stubs copied into package source")
            else:
                for pyi in typings_path.rglob("*.pyi"):
                    try:
                        parts = list(pyi.parts)
                        if "py_wlcommands" in parts:
                            idx = parts.index("py_wlcommands")
                            rel = Path(*parts[idx + 1 :])
                            dest = package_root / rel
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(pyi, dest)
                    except Exception:
                        continue

        except Exception as e:
            log_error(f"Failed to generate type stubs: {e}")
