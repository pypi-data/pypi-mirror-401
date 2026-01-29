import argparse
import sys
import os


try:
    from .server import mcp, local_tools
    from .log import log
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from sz_mcp_server.server import mcp, local_tools
    from sz_mcp_server.log import log


def main():
    parser = argparse.ArgumentParser(description='启动MCP Server')
    parser.add_argument('--bot-path', type=str, required=True, help='机器人exe文件路径')
    args = parser.parse_args()
    log.info('Starting server...')
    if args.bot_path:
        log.info(f"机器人路径: {args.bot_path}")
        local_tools.start_bot(args.bot_path)
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
    
    