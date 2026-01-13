"""Package processing for publish command."""

import shutil
from pathlib import Path
from typing import Any, List

from ...utils.logging import log_error, log_info
from ...utils.subprocess_utils import SubprocessExecutor
from .package_builder import PackageBuilder


class Packager:
    """Handle package processing for publish command."""

    def __init__(self) -> None:
        """Initialize the packager."""
        self.package_builder = PackageBuilder()
        self.executor = SubprocessExecutor()

    def process_dist_files(
        self, dist_files: list[Any], skip_build: bool, dry_run: bool
    ) -> list[Any]:
        """Process distribution files and return wheel files."""
        log_info(f"Processing dist files. Count: {len(dist_files)}")
        log_info(f"Files: {[str(f) for f in dist_files]}")

        files = self._collect_dist_files(dist_files)
        log_info(f"After checking dist/, files count: {len(files)}")

        if not skip_build and not dry_run and not files:
            from ...exceptions import CommandError

            raise CommandError("No distribution files found in dist/ directory")

        wheel_files = self._extract_wheel_files(files)
        log_info(f"Wheel files count: {len(wheel_files)}")

        if not wheel_files and not skip_build and not dry_run:
            from ...exceptions import CommandError

            raise CommandError(
                "No wheel files found in dist/ directory. Run 'wl build dist' first."
            )

        if wheel_files:
            log_info(f"Found {len(wheel_files)} wheel files to upload")
            for f in wheel_files:
                log_info(f"  - {getattr(f, 'name', str(f))}")

        return wheel_files

    def build_distribution_packages(
        self, skip_build: bool = False, dry_run: bool = False
    ) -> None:
        """Build distribution packages if not skipped."""
        if not skip_build and not dry_run:
            # Clean and create dist directory
            self.clean_dist_directory()

            log_info("Building distribution packages with 'wl build dist'...")
            log_info("使用 'wl build dist' 构建分发包...", lang="zh")
            log_info("Running: wl build dist")

            try:
                result = self.executor.run(["wl", "build", "dist"], quiet=False)
                if result.success:
                    log_info(
                        "✓ Distribution packages built successfully with 'wl build dist'"
                    )
                    log_info("✓ 分发包通过 'wl build dist' 成功构建", lang="zh")
                else:
                    raise Exception(f"Build failed: {result.stderr}")
            except Exception as e:
                log_error(f"Build failed: {str(e)}")
                from ...exceptions import CommandError

                raise CommandError(f"Build failed: {str(e)}")
        elif not skip_build and dry_run:
            # Clean and create dist directory for dry run
            self.clean_dist_directory()

            log_info(
                "Dry run mode: Would build distribution packages with 'wl build dist'"
            )
            log_info("Dry run mode: 将使用 'wl build dist' 构建分发包...", lang="zh")
            log_info(
                "Dry run mode: Distribution packages would be created in dist/ directory"
            )

    def clean_dist_directory(self) -> None:
        """Clean the dist directory."""
        dist_path = Path("dist")
        if dist_path.exists():
            shutil.rmtree(dist_path)
        dist_path.mkdir(exist_ok=True)

    def get_dist_files(self) -> list[Any]:
        """Get distribution files from dist directory."""
        dist_path = Path("dist")
        if not dist_path.exists():
            dist_path.mkdir(exist_ok=True)
            return []

        return list(dist_path.iterdir())

    def collect_dist_files(self, files: list[Any] | None = None) -> list[Any]:
        """Collect distribution files."""
        if files:
            return files

        return self.get_dist_files()

    def _collect_dist_files(self, dist_files: list[Any]) -> list[Any]:
        """Collect distribution files from provided list or dist directory."""
        if dist_files:
            return dist_files

        dist_path = Path("dist")
        if dist_path.exists():
            direct_files = list(dist_path.glob("*.whl")) + list(
                dist_path.glob("*.tar.gz")
            )
            if direct_files:
                return direct_files
        return []

    def _extract_wheel_files(self, files: list[Any]) -> list[Any]:
        """Extract wheel files from a list of files."""
        wheels: list[Any] = []
        for f in files:
            if isinstance(f, Path) and f.suffix == ".whl":
                wheels.append(f)
            elif hasattr(f, "name") and str(getattr(f, "name", f)).endswith(".whl"):
                wheels.append(f)
            elif getattr(f, "suffix", None) == ".whl":
                wheels.append(f)
        return wheels

    def extract_wheel_files(self, files: list[Any]) -> list[Any]:
        """Extract wheel files from a list of files (public method)."""
        return self._extract_wheel_files(files)
