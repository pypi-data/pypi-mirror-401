"""Command loading and discovery module."""

import importlib
import logging
from typing import Any, Dict

from .command_registry import CommandRegistry
from .decorators import get_command_metadata, get_group_metadata


class CommandLoader:
    """命令加载器，负责动态加载和注册命令。"""

    def __init__(self, registry: CommandRegistry):
        """
        初始化命令加载器。

        Args:
            registry (CommandRegistry): 命令注册中心实例
        """
        self.registry = registry
        self.logger = logging.getLogger(__name__)

        # 命令模块映射，键为命令名称，值为模块路径
        self.command_modules = {
            "build": "buildcommands.build",
            "builddist": "buildcommands.dist",
            "buildtest": "buildcommands.test",
            "clean": "clean.clean",
            "config": "config.config",
            "format": "format.format_coordinator",
            "init": "initenv.initenv",
            "initenv": "initenv.initenv",
            "lint": "lint.lint_coordinator",
            "publish": "publish.publish",
            "self": "self.self_update",
            "test": "testcommands.test",
        }

    def load_commands(self) -> None:
        """加载所有命令。"""
        self.logger.info("Loading commands...")

        # 注册内置命令组
        self._register_builtin_groups()

        # 加载所有命令模块
        for cmd_name, module_path in self.command_modules.items():
            self.logger.debug(f"Loading command module: {module_path}")
            self._load_command_module(cmd_name, module_path)

        self.logger.info(f"Loaded {len(self.registry.list_commands())} commands")

    def _register_builtin_groups(self) -> None:
        """注册内置命令组。"""
        groups = {
            "build": "构建相关命令",
            "dev": "开发相关命令",
            "quality": "代码质量相关命令",
            "publish": "发布相关命令",
            "self": "自我管理命令",
            "test": "测试相关命令",
        }

        for group_name, help_text in groups.items():
            self.registry.register_group(group_name, help_text)

    def _load_command_module(self, cmd_name: str, module_path: str) -> None:
        """
        加载单个命令模块。

        Args:
            cmd_name (str): 命令名称
            module_path (str): 模块路径
        """
        # 构建完整模块路径
        full_module_path = f"py_wlcommands.commands.{module_path}"

        try:
            # 导入模块
            module = importlib.import_module(full_module_path)
            self.logger.debug(f"Successfully imported module: {full_module_path}")

            # 扫描模块中的命令
            self._scan_module_for_commands(module)
        except ImportError as e:
            # 尝试导入基础模块
            base_module_path = f"py_wlcommands.commands.{module_path.split('.')[0]}"
            try:
                module = importlib.import_module(base_module_path)
                self.logger.debug(
                    f"Successfully imported base module: {base_module_path}"
                )

                # 扫描模块中的命令
                self._scan_module_for_commands(module)
            except ImportError as base_e:
                # 记录错误并继续
                self.logger.error(
                    f"Failed to import module {full_module_path} or {base_module_path}: {e}"
                )

    def _scan_module_for_commands(self, module: Any) -> None:
        """
        扫描模块中的命令装饰器，注册命令。

        Args:
            module (Any): 模块对象
        """
        # 遍历模块中的所有属性
        for attr_name in dir(module):
            # 跳过私有属性
            if attr_name.startswith("_"):
                continue

            attr = getattr(module, attr_name)

            # 检查是否有命令元数据（新的基于函数的命令）
            cmd_metadata = get_command_metadata(attr)
            if cmd_metadata:
                self.logger.debug(f"Found command: {cmd_metadata.name}")
                self.registry.register_command(
                    name=cmd_metadata.name,
                    func=attr,
                    group=cmd_metadata.group,
                    aliases=cmd_metadata.aliases,
                )

            # 检查是否有命令组元数据
            group_metadata = get_group_metadata(attr)
            if group_metadata:
                self.logger.debug(f"Found command group: {group_metadata.name}")
                self.registry.register_group(
                    name=group_metadata.name, help_text=group_metadata.help
                )

        # 检查模块是否有现有命令类的注册
        # 导入现有命令系统的相关模块
        try:
            from py_wlcommands.commands import list_commands as old_list_commands

            from .command_adapter import CommandAdapter

            # 获取所有现有命令类
            old_commands = old_list_commands()

            # 适配现有命令类为新的命令函数
            adapted_commands = CommandAdapter.adapt_all_commands(old_commands)

            # 注册适配后的命令
            for cmd_name, cmd_func in adapted_commands.items():
                # 为每个命令设置默认分组
                group = self._get_default_group(cmd_name)

                # 注册命令
                self.registry.register_command(
                    name=cmd_name,
                    func=cmd_func,
                    group=group,
                    aliases=self._get_default_aliases(cmd_name),
                )
        except ImportError as e:
            self.logger.debug(f"Failed to import old command system: {e}")

    def _get_default_group(self, cmd_name: str) -> str:
        """
        获取命令的默认分组。

        Args:
            cmd_name (str): 命令名称

        Returns:
            str: 命令分组名称
        """
        group_mapping = {
            "build": "build",
            "builddist": "build",
            "buildtest": "build",
            "clean": "quality",
            "config": "dev",
            "format": "quality",
            "init": "dev",
            "initenv": "dev",
            "lint": "quality",
            "publish": "publish",
            "self": "self",
            "test": "",  # 将 test 命令设置为顶级命令，不再属于 test 命令组
        }

        return group_mapping.get(cmd_name, "")

    def _get_default_aliases(self, cmd_name: str) -> list[str]:
        """
        获取命令的默认别名。

        Args:
            cmd_name (str): 命令名称

        Returns:
            list[str]: 命令别名列表
        """
        alias_mapping = {
            "build": ["b"],
            "clean": ["c"],
            "format": ["f"],
            "init": ["i"],
            "lint": ["l"],
        }

        return alias_mapping.get(cmd_name, [])

    def get_loaded_commands(self) -> dict[str, dict[str, Any]]:
        """
        获取已加载的命令。

        Returns:
            Dict[str, Dict[str, Any]]: 已加载的命令字典
        """
        return self.registry.list_commands()
