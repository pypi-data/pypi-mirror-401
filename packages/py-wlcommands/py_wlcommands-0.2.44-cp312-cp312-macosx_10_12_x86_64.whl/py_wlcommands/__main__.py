#!/usr/bin/env python3

"""
Main entry point for WL Commands.
"""

# 配置是否使用新的Click CLI
USE_CLICK_CLI = False


def main() -> None:
    """Main entry point for WL Commands."""
    # 根据配置选择使用哪种CLI
    if USE_CLICK_CLI:
        # 尝试使用新的Click CLI
        try:
            # Local import to avoid import issues
            from .cli_click import main as cli_main
        except ImportError:
            # Fallback for cases where relative imports don't work
            from py_wlcommands.cli_click import main as cli_main
    else:
        # 使用旧的argparse CLI
        try:
            # Local import to avoid import issues
            from .cli import main as cli_main
        except ImportError:
            # Fallback for cases where relative imports don't work
            from py_wlcommands.cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
