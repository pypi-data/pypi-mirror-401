"""Command adapter for backward compatibility."""

from typing import Any, Callable, Dict, Optional

from ..utils.error_handler import ErrorHandler
from .base import CommandBase


class CommandAdapter:
    """命令适配器，将现有命令类转换为Click命令函数。"""

    @staticmethod
    def adapt_command(command_class: type[CommandBase]) -> Callable:
        """
        将命令类转换为Click命令函数。

        Args:
            command_class (type[CommandBase]): 命令类

        Returns:
            Callable: 适配后的命令函数
        """

        def command_func(*args, **kwargs):
            """适配后的命令函数。"""
            # 创建命令实例
            command_instance = command_class()

            # 处理未知参数
            unknown_args = kwargs.pop("unknown_args", [])
            if unknown_args:
                kwargs["unknown_args"] = unknown_args

            # 执行命令
            return ErrorHandler.wrap_command_execution(command_instance.run, **kwargs)

        # 设置函数文档字符串
        command_func.__doc__ = command_class.__doc__ or "No help available"

        return command_func

    @staticmethod
    def adapt_all_commands(
        commands: dict[str, type[CommandBase]],
    ) -> dict[str, Callable]:
        """
        适配所有命令类。

        Args:
            commands (Dict[str, type[CommandBase]]): 命令类字典

        Returns:
            Dict[str, Callable]: 适配后的命令函数字典
        """
        adapted_commands = {}

        for cmd_name, cmd_class in commands.items():
            adapted_commands[cmd_name] = CommandAdapter.adapt_command(cmd_class)

        return adapted_commands
