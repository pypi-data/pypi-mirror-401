"""Git初始化处理器"""

from py_wlcommands.commands.initenv.utils.git_initializer import GitInitializer
from py_wlcommands.commands.initenv.utils.platform_adapter import PlatformAdapter
from py_wlcommands.utils.logging import log_info


class InitGitHandler:
    """处理Git初始化的类"""

    @staticmethod
    def initialize() -> None:
        """
        初始化Git仓库
        """
        log_info("=== Starting Git Repository Initialization ===")
        log_info("=== 开始 Git 仓库初始化 ===", lang="zh")

        # 检测平台
        env = PlatformAdapter.get_env()
        git_initializer = GitInitializer(env)

        # 初始化Git仓库
        git_initializer.initialize()

        log_info("Git Repository Initialization completed!")
        log_info("Git 仓库初始化已完成！", lang="zh")
