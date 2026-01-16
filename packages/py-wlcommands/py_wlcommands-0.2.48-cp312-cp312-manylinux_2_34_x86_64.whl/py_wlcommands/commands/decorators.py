"""Command decorators for easy command registration."""

from functools import wraps
from typing import Callable, List, Optional


class CommandMetadata:
    """Command metadata container."""

    def __init__(
        self,
        name: str,
        help_text: str,
        group: str | None = None,
        aliases: list[str] | None = None,
    ):
        self.name = name
        self.help = help_text
        self.group = group
        self.aliases = aliases or []


class GroupMetadata:
    """Command group metadata container."""

    def __init__(self, name: str, help_text: str):
        self.name = name
        self.help = help_text


def command(
    name: str,
    help_text: str,
    group: str | None = None,
    aliases: list[str] | None = None,
) -> Callable:
    """
    命令装饰器，用于注册命令。

    Args:
        name (str): 命令名称
        help_text (str): 命令帮助文本
        group (Optional[str]): 命令所属分组
        aliases (Optional[List[str]]): 命令别名列表

    Returns:
        Callable: 装饰后的函数
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # 为函数添加命令元数据
        wrapper.__command_metadata__ = CommandMetadata(
            name=name, help_text=help_text, group=group, aliases=aliases
        )

        return wrapper

    return decorator


def command_group(name: str, help_text: str) -> Callable:
    """
    命令组装饰器，用于注册命令组。

    Args:
        name (str): 命令组名称
        help_text (str): 命令组帮助文本

    Returns:
        Callable: 装饰后的函数
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # 为函数添加命令组元数据
        wrapper.__group_metadata__ = GroupMetadata(name=name, help_text=help_text)

        return wrapper

    return decorator


def get_command_metadata(func: Callable) -> CommandMetadata | None:
    """
    获取函数的命令元数据。

    Args:
        func (Callable): 函数对象

    Returns:
        Optional[CommandMetadata]: 命令元数据
    """
    return getattr(func, "__command_metadata__", None)


def get_group_metadata(func: Callable) -> GroupMetadata | None:
    """
    获取函数的命令组元数据。

    Args:
        func (Callable): 函数对象

    Returns:
        Optional[GroupMetadata]: 命令组元数据
    """
    return getattr(func, "__group_metadata__", None)
