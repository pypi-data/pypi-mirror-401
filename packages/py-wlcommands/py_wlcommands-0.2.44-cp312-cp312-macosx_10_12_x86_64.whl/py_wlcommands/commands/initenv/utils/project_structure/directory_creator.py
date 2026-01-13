"""Project directory structure creator."""

import re
from pathlib import Path

from py_wlcommands.commands.initenv.utils.config_manager import ConfigManager

from .....utils.logging import log_info


def _normalize_project_name(project_name: str) -> str:
    """Normalize project name for directory usage by converting hyphens to underscores."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", project_name)


def _create_required_directories(project_name: str) -> None:
    """Create required project directories."""
    normalized_name = _normalize_project_name(project_name)
    directories = [
        "src",
        f"src/{normalized_name}",
        f"src/{normalized_name}/lib",  # 添加lib目录以支持Rust扩展
        "tests",
        "docs",
        "examples",
        "rust",
        "dist",
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def _create_init_files(project_name: str) -> None:
    """Create __init__.py files for Python packages."""
    normalized_name = _normalize_project_name(project_name)
    directories = [
        "src",
        f"src/{normalized_name}",
        f"src/{normalized_name}/lib",  # 添加lib目录以支持Rust扩展
        "tests",
    ]

    for directory in directories:
        if Path(directory).exists():
            init_file = Path(directory) / "__init__.py"
            if not init_file.exists():
                init_file.touch()


def _create_readme(project_name: str) -> None:
    """Create README.md file if it doesn't exist or is empty."""
    readme_file = Path("README.md")

    # Only create README if it doesn't exist or is empty
    should_create = (
        not readme_file.exists()
        or readme_file.read_text(encoding="utf-8").strip() == ""
    )

    if should_create:
        # Try to get project description from config
        try:
            config_manager = ConfigManager()
            description = config_manager.get(
                "project_description", f"A Python project: {project_name}"
            )
        except Exception:
            # Fallback to default description if config fails
            description = f"A Python project: {project_name}"

        readme_content = f"""# {project_name}

{description}

## Installation

```bash
pip install {project_name}
```

## Usage

```python
import {project_name}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT
"""

        readme_file.write_text(readme_content, encoding="utf-8")
        log_info("✓ README.md created successfully")
        log_info("✓ README.md 创建成功", lang="zh")


def setup_project_structure(project_name: str) -> None:
    """Setup complete project structure by calling all required functions."""
    _create_required_directories(project_name)
    _create_init_files(project_name)
    _create_readme(project_name)

    # Copy and configure git hooks
    from .hooks_manager import _copy_and_configure_hooks

    _copy_and_configure_hooks()


class DirectoryCreator:
    """Create project directory structure."""

    def create_structure(self, project_name: str) -> None:
        """Create main project directory structure."""
        _create_required_directories(project_name)
        _create_init_files(project_name)

        log_info("✓ Project structure created successfully")
        log_info("✓ 项目结构创建成功", lang="zh")
