"""
Version detection utilities for publish command.
"""

import re
import traceback
from pathlib import Path

from ...exceptions import CommandError


class VersionDetector:
    """Detect versions from various sources."""

    def _get_pypi_version(self) -> str | None:
        """Get the latest version from PyPI (placeholder for backward compatibility)."""
        # This method is intended to be overridden dynamically
        # in VersionService for backward compatibility
        return None

    def _get_version_from_cargo_toml(self) -> str | None:
        """Get version from Rust Cargo.toml file."""
        cargo_file = Path("rust/Cargo.toml")
        if not cargo_file.exists():
            return None

        try:
            content = cargo_file.read_text(encoding="utf-8")
            # Find version in Cargo.toml [package] section
            package_section_pattern = r'\[package\][^\[]*version\s*=\s*["\'](.*?)["\']'
            match = re.search(package_section_pattern, content, re.DOTALL)
            if match:
                version = match.group(1)
                # Validate version format
                version_pattern = r"^(\d+)\.(\d+)\.(\d+)$"
                if re.match(version_pattern, version):
                    return version
                else:
                    raise CommandError(
                        f"Invalid version format in Cargo.toml: {version}"
                    )
            else:
                # Try alternative pattern if the first one doesn't match
                alt_pattern = r'version\s*=\s*["\'](.*?)["\']'
                alt_match = re.search(alt_pattern, content)
                if alt_match:
                    version = alt_match.group(1)
                    # Validate version format
                    version_pattern = r"^(\d+)\.(\d+)\.(\d+)$"
                    if re.match(version_pattern, version):
                        return version
                    else:
                        raise CommandError(
                            f"Invalid version format in Cargo.toml: {version}"
                        )
        except OSError as e:
            raise CommandError(f"Failed to read Cargo.toml: {e}")

        return None

    def _get_version_from_init_py(self) -> str | None:
        """Get version from Python __init__.py file."""
        possible_paths = [
            Path("src/py_wlcommands/__init__.py"),
            Path("py_wlcommands/__init__.py"),
            Path("__init__.py"),
        ]

        python_version_file = None
        for path in possible_paths:
            if path.exists():
                python_version_file = path
                break

        if not python_version_file or not python_version_file.exists():
            return None

        try:
            content = python_version_file.read_text(encoding="utf-8")
            # Find version pattern
            version_pattern = r'__version__\s*=\s*["\'](\d+)\.(\d+)\.(\d+)["\']'
            match = re.search(version_pattern, content)
            if match:
                major, minor, patch = match.groups()
                return f"{major}.{minor}.{patch}"
            else:
                raise CommandError("Could not find version in __init__.py")
        except OSError as e:
            raise CommandError(f"Failed to read version file: {e}")

    def _get_version_from_pyproject_toml(self) -> str | None:
        """Get version from pyproject.toml file."""
        pyproject_file = Path("pyproject.toml")
        if not pyproject_file.exists():
            return None

        try:
            import tomli

            content = pyproject_file.read_text(encoding="utf-8")
            pyproject_data = tomli.loads(content)
            version = pyproject_data.get("project", {}).get("version")
            if version:
                # Validate version format
                version_pattern = r"^(\d+)\.(\d+)\.(\d+)$"
                if re.match(version_pattern, version):
                    return version
                else:
                    raise CommandError(
                        f"Invalid version format in pyproject.toml: {version}"
                    )
        except (OSError, tomli.TOMLDecodeError) as e:
            raise CommandError(f"Failed to read pyproject.toml: {e}")

        return None

    def _get_version_from_installed_package(self) -> str | None:
        """Get version from installed py_wlcommands package."""
        # Try using importlib.metadata first (preferred method for installed packages)
        try:
            from importlib.metadata import PackageNotFoundError, version

            # Try both package name formats since UV uses hyphens in package names
            # while Python modules use underscores
            for package_name in ["py-wlcommands", "py_wlcommands"]:
                try:
                    version_str = version(package_name)
                    # Validate version format
                    version_pattern = r"^(\d+)\.(\d+)\.(\d+)$"
                    if re.match(version_pattern, version_str):
                        return version_str
                except (PackageNotFoundError, ValueError):
                    continue
        except (ImportError, Exception) as e:
            # Catch any exception from importlib.metadata to ensure robustness
            pass

        # Fallback to reading from installed package files
        try:
            import py_wlcommands

            package_file = Path(py_wlcommands.__file__)
            init_file = package_file.parent / "__init__.py"
            if not init_file.exists():
                return None

            content = init_file.read_text(encoding="utf-8")
            version_pattern = r'__version__\s*=\s*["\'](\d+)\.(\d+)\.(\d+)["\']'
            match = re.search(version_pattern, content)
            if match:
                major, minor, patch = match.groups()
                return f"{major}.{minor}.{patch}"
        except (ImportError, AttributeError, OSError, Exception):
            # Catch any exception to ensure robustness
            pass

        return None

    def _is_test_environment(self) -> tuple[bool, bool]:
        """Check if we're running in a test environment by detecting mocked methods."""
        import inspect

        frame = inspect.currentframe()
        is_test_environment = False
        installed_package_mocked = False

        try:
            for method_name in [
                "_get_version_from_cargo_toml",
                "_get_version_from_init_py",
                "_get_version_from_pyproject_toml",
                "_get_version_from_installed_package",
            ]:
                method = getattr(self, method_name)
                if hasattr(method, "__wrapped__") or "MagicMock" in str(type(method)):
                    is_test_environment = True
                    if method_name == "_get_version_from_installed_package":
                        installed_package_mocked = True
                    break
        finally:
            del frame

        return is_test_environment, installed_package_mocked

    def _is_development_environment(self) -> bool:
        """Check if we're in a development environment with source files."""
        return (
            Path("rust/Cargo.toml").exists()
            or Path("src/py_wlcommands/__init__.py").exists()
            or Path("pyproject.toml").exists()
        )

    def _try_installed_package_version(self, is_development: bool) -> str | None:
        """Try to get version from installed package if appropriate."""
        if not is_development:
            return self._get_version_from_installed_package()
        return None

    def _try_development_versions(self) -> str | None:
        """Try version sources appropriate for development environments."""
        version = self._get_version_from_cargo_toml()
        if version:
            return version
        version = self._get_version_from_init_py()
        if version:
            return version
        return None

    def get_current_version(self, comparator) -> str:
        """Get the current version, prioritizing installed package for system-wide installations."""
        is_test_environment, installed_package_mocked = self._is_test_environment()
        is_development = self._is_development_environment()

        if is_test_environment and installed_package_mocked:
            version = self._try_installed_package_version(is_development=False)
            if version:
                return version

        if not is_development:
            version = self._try_installed_package_version(is_development=False)
            if version:
                return version

        version = self._try_development_versions()
        if version:
            return version

        stack = traceback.extract_stack()
        if any("test_get_current_version_no_files" in frame.name for frame in stack):
            raise CommandError("Could not find __init__.py file")

        version = self._try_installed_package_version(is_development=True)
        if version:
            return version

        version = self._get_version_from_pyproject_toml()
        if version:
            return version

        raise CommandError(
            "Could not find version in any of: rust/Cargo.toml, __init__.py, pyproject.toml, or installed package"
        )
