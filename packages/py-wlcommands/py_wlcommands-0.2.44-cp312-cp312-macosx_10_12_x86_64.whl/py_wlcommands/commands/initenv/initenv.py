"""初始化项目命令"""

from typing import Any

from ...exceptions import CommandError
from ...utils.logging import log_error
from .. import Command, register_command
from .handlers.init_environment_handler import InitEnvironmentHandler
from .handlers.init_git_handler import InitGitHandler
from .handlers.init_lfs_handler import InitLfsHandler
from .handlers.init_project_handler import InitProjectHandler
from .handlers.init_work_handler import InitWorkHandler
from .utils.exceptions import InitEnvError


@register_command("init")
class InitCommand(Command):
    """用于初始化项目环境的命令"""

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        """返回命令名称"""
        return "init"

    @property
    def help(self) -> str:
        """返回命令帮助文本"""
        return "Initialize project environment or project structure"

    @classmethod
    def add_arguments(cls, parser) -> None:
        """添加命令参数"""
        subparsers = parser.add_subparsers(dest="init_type", help="Initialization type")

        # Environment initialization subcommand
        env_parser = subparsers.add_parser("env", help="Initialize project environment")
        env_parser.add_argument(
            "--log-level",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Set the log level for the project",
        )
        env_parser.add_argument(
            "--log-console",
            action="store_true",
            help="Enable console logging",
        )
        env_parser.add_argument(
            "--log-file",
            help="Set the log file path",
        )

        # Project structure initialization subcommand
        subparsers.add_parser("project", help="Initialize project structure")

        # Work initialization subcommand
        work_parser = subparsers.add_parser(
            "work", help="Initialize Git Flow work environment"
        )
        work_parser.add_argument(
            "work_type",
            choices=["feature", "fix", "hotfix", "release"],
            help="Type of work to initialize: feature, fix, hotfix, or release",
        )

        # Git initialization subcommand
        subparsers.add_parser("git", help="Initialize Git repository")

        # Git LFS initialization subcommand
        lfs_parser = subparsers.add_parser("lfs", help="Initialize Git LFS")
        lfs_parser.add_argument(
            "--fix",
            action="store_true",
            help="Automatically fix issues like nested .git directories when initializing LFS",
        )

    def execute(self, *args: Any, **kwargs: Any) -> None:
        """
        执行初始化命令

        Args:
            args: 位置参数
            kwargs: 关键字参数
        """
        init_type = kwargs.get("init_type", "env")

        if init_type == "project":
            self._init_project_structure()
        elif init_type == "work":
            work_type = kwargs.get("work_type")
            if not work_type:
                raise CommandError(
                    "Work type is required when using 'init work'. Please specify: feature, fix, hotfix, or release"
                )
            self._init_work(work_type)
        elif init_type == "git":
            self._init_git()
        elif init_type == "lfs":
            self._init_lfs(**kwargs)
        else:
            # 将所有kwargs传递给_init_environment方法，包括日志配置参数
            self._init_environment(**kwargs)

    def _init_environment(self, **kwargs) -> None:
        """初始化完整的项目环境"""
        try:
            InitEnvironmentHandler.initialize(**kwargs)
        except InitEnvError as e:
            log_error(f"Initialization error: {e}")
            log_error(f"初始化错误: {e}", lang="zh")
            raise CommandError(f"Project initialization failed: {e}")
        except Exception as e:
            log_error(f"Error initializing project: {e}")
            log_error(f"错误：初始化项目失败: {e}", lang="zh")
            raise CommandError(f"Project initialization failed: {e}")

    def _init_work(self, work_type: str) -> None:
        """初始化Git Flow工作环境"""
        try:
            InitWorkHandler.initialize(work_type)
        except Exception as e:
            log_error(f"Initialization error: {e}")
            log_error(f"初始化错误: {e}", lang="zh")
            raise CommandError(f"Work initialization failed: {e}")

    def _init_project_structure(self) -> None:
        """初始化项目结构"""
        try:
            InitProjectHandler.initialize()
        except Exception as e:
            raise CommandError(f"Project initialization failed: {e}")

    def _init_git(self) -> None:
        """初始化Git仓库"""
        try:
            InitGitHandler.initialize()
        except Exception as e:
            raise CommandError(f"Git initialization failed: {e}")

    def _init_lfs(self, **kwargs) -> None:
        """初始化Git LFS"""
        try:
            # 获取--fix参数值
            auto_fix = kwargs.get("fix", False)
            InitLfsHandler.initialize(auto_fix=auto_fix)
        except Exception as e:
            raise CommandError(f"Git LFS initialization failed: {e}")
