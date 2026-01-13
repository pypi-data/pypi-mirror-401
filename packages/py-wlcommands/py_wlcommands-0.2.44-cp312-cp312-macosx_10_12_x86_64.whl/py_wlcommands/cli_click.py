#!/usr/bin/env python3
"""Command line interface entry point based on Click."""

import sys
from argparse import ArgumentParser
from typing import List, Optional

import click

from . import __version__
from .commands import get_command, list_commands
from .commands.base import CommandBase
from .utils.error_handler import ErrorHandler
from .utils.logging import log_error, log_info
from .utils.wl_dir_updater import check_and_update_wl_dir


@click.group(
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(
    version=__version__, prog_name="wl", message="%(prog)s %(version)s"
)
def wl():
    """WL Commands - A command-line tool for project management."""
    ctx = click.get_current_context()

    # 检查并更新 .wl 目录
    check_and_update_wl_dir()

    # 如果没有指定命令，显示帮助信息
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


def create_command_function(command_class):
    """Create a Click command function from a command class."""

    def command_func(**kwargs):
        """Command function wrapper."""
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


def setup_commands():
    """设置命令，将注册的命令添加到Click命令组中。"""
    from .commands.registry import _ALIASES

    # 获取所有命令
    commands = list_commands()

    def create_wrapped_command(name, command_class):
        """创建包装命令函数，解决闭包变量问题"""

        @click.command(name=name, help=command_class.__doc__ or "No help available")
        @click.argument("args", nargs=-1)
        def wrapped_command(args):
            """包装命令，处理参数"""
            # 将命令名和参数转换为命令行参数列表
            argv = [name] + list(args)
            # 调用原始命令函数
            from py_wlcommands.cli import main as argparse_main

            return argparse_main(argv)

        return wrapped_command

    # 添加每个命令到Click命令组
    for name, command_class in commands.items():
        # 创建包装命令函数
        wrapped_command = create_wrapped_command(name, command_class)

        # 添加命令到主命令组
        wl.add_command(wrapped_command)

        # 添加命令别名
        for alias, actual_name in _ALIASES.items():
            if actual_name == name:
                # 为别名创建新的包装命令，使用原始命令类
                alias_wrapped = create_wrapped_command(alias, command_class)
                wl.add_command(alias_wrapped, name=alias)


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    if argv is None:
        argv = sys.argv[1:]

    try:
        # 设置命令
        setup_commands()

        # 执行命令
        wl.main(args=argv, standalone_mode=False)
        return 0
    except click.ClickException as e:
        log_error(str(e))
        return 1
    except Exception as e:
        log_error(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
