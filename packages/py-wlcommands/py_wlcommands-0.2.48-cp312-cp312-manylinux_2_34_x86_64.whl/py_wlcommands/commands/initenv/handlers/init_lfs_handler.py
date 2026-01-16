"""Git LFS初始化处理器"""

from py_wlcommands.commands.initenv.utils.git.git_lfs_manager import GitLFSManager
from py_wlcommands.commands.initenv.utils.platform_adapter import PlatformAdapter
from py_wlcommands.utils.logging import log_info


class InitLfsHandler:
    """处理Git LFS初始化的类"""

    @staticmethod
    def initialize(auto_fix: bool = False) -> None:
        """
        初始化Git LFS

        Args:
            auto_fix: 是否自动修复问题，如嵌套的.git目录
        """
        log_info("=== Starting Git LFS Initialization ===")
        log_info("=== 开始 Git LFS 初始化 ===", lang="zh")

        # 检测平台
        env = PlatformAdapter.get_env()
        git_lfs_manager = GitLFSManager(env)

        # 初始化Git LFS
        git_lfs_manager.initialize(auto_fix=auto_fix)

        log_info("Git LFS Initialization completed!")
        log_info("Git LFS 初始化已完成！", lang="zh")
