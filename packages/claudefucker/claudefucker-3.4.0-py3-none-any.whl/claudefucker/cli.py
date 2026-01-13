#!/usr/bin/env python3
"""
claudefucker CLI入口点
支持参数:
  -new, --new: 强制重新配置
"""
import argparse
from claudefucker.main import main

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='ClaudeFucker - Anthropic格式AI代理服务器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  claudefuck              # 使用已有配置启动
  claudefuck -new         # 强制重新配置
  claudefuck --new        # 强制重新配置
        """
    )
    parser.add_argument(
        '-n', '--new',
        action='store_true',
        help='强制重新配置，忽略已有配置文件'
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(force_new_config=args.new)
