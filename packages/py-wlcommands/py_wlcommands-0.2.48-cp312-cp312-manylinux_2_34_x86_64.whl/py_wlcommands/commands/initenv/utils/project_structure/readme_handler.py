"""README template handler."""

from pathlib import Path

from .....utils.logging import log_info
from ..config_manager import ConfigManager


class ReadmeHandler:
    """Handle README template processing."""

    def __init__(self):
        self.config_manager = ConfigManager()

    def create_readme(self, project_name: str) -> None:
        """Copy README template and customize it for the project."""
        try:
            # Calculate path to vendors/readme/README.md relative to this file
            template_path = self.config_manager.get_vendor_config_path(
                "readme/README.md"
            )

            if template_path.exists():
                # Read the template
                with open(template_path, encoding="utf-8") as f:
                    template_content = f.read()

                # Customize the template
                customized_content = template_content.format(
                    project_name=project_name,
                    project_description=f"{project_name} - A Python project",
                    cli_command="wl",  # Default CLI command
                )

                # Write to project README.md
                with open("README.md", "w", encoding="utf-8") as f:
                    f.write(customized_content)

                log_info(
                    f"✓ README.md template copied and customized for: {project_name}"
                )
                log_info(f"✓ README.md 模板复制并定制化完成: {project_name}", lang="zh")
            else:
                # Fallback to simple README if template doesn't exist
                with open("README.md", "w", encoding="utf-8") as f:
                    f.write(f"# {project_name}\n")
                log_info(
                    f"✓ Created simple README.md with project name: {project_name}"
                )
                log_info(f"✓ 创建简单 README.md，项目名: {project_name}", lang="zh")
        except Exception as e:
            # Fallback to simple README if customization fails
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(f"# {project_name}\n")
            log_info(f"Warning: Failed to customize README.md, created simple one: {e}")
            log_info(f"警告: 定制 README.md 失败，创建简单版本: {e}", lang="zh")
