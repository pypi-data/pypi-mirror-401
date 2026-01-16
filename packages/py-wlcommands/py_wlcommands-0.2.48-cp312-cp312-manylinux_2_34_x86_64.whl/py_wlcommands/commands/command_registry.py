"""Command registration and management module."""

from typing import Any, Callable, Dict, Optional


class CommandRegistry:
    """统一的命令注册和管理中心"""

    def __init__(self):
        """初始化命令注册中心"""
        self._commands: dict[str, dict[str, Any]] = {}
        self._aliases: dict[str, str] = {}
        self._command_groups: dict[str, dict[str, Any]] = {}

    def register_command(
        self,
        name: str,
        func: Callable,
        group: str | None = None,
        aliases: list[str] | None = None,
    ) -> None:
        """
        注册命令

        Args:
            name (str): 命令名称
            func (Callable): 命令执行函数
            group (Optional[str]): 命令所属分组
            aliases (Optional[list[str]]): 命令别名列表
        """
        self._commands[name] = {
            "name": name,
            "func": func,
            "group": group,
            "aliases": aliases or [],
        }

        # 注册别名
        if aliases:
            for alias in aliases:
                self.register_alias(alias, name)

    def register_group(self, name: str, help_text: str) -> None:
        """
        注册命令组

        Args:
            name (str): 命令组名称
            help_text (str): 命令组帮助文本
        """
        self._command_groups[name] = {"name": name, "help": help_text}

    def register_alias(self, alias: str, command_name: str) -> None:
        """
        注册命令别名

        Args:
            alias (str): 命令别名
            command_name (str): 命令名称
        """
        self._aliases[alias] = command_name

    def get_command(self, name: str) -> dict[str, Any] | None:
        """
        获取命令信息

        Args:
            name (str): 命令名称或别名

        Returns:
            Optional[Dict[str, Any]]: 命令信息字典
        """
        # 解析别名
        resolved_name = self._aliases.get(name, name)
        return self._commands.get(resolved_name)

    def list_commands(self, group: str | None = None) -> dict[str, dict[str, Any]]:
        """
        列出命令

        Args:
            group (Optional[str]): 命令分组，None表示列出所有命令

        Returns:
            Dict[str, Dict[str, Any]]: 命令信息字典
        """
        if group:
            return {
                name: cmd
                for name, cmd in self._commands.items()
                if cmd["group"] == group
            }
        return self._commands.copy()

    def get_command_groups(self) -> dict[str, dict[str, Any]]:
        """
        获取命令分组

        Returns:
            Dict[str, Dict[str, Any]]: 命令分组字典
        """
        return self._command_groups.copy()
