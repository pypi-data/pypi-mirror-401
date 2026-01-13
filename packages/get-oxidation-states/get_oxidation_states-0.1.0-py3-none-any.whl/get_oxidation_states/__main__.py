"""
MCP server 命令行入口点。
"""

import asyncio
import logging
import sys

from get_oxidation_states.server import main as server_main


def main() -> None:
    """命令行入口函数"""
    try:
        asyncio.run(server_main())
    except KeyboardInterrupt:
        print("\n服务器已停止", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        logging.error(f"服务器运行错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
