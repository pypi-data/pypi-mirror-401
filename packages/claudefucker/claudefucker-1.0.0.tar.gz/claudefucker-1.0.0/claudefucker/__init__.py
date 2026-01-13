"""
claudefucker - Anthropic格式AI代理服务器

将Claude Code的Anthropic格式请求转换为各厂商格式
"""
__version__ = "1.0.0"
__author__ = "python学霸"

from .main import app, main as run_server

__all__ = ['app', 'run_server']
