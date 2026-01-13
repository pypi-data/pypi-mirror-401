# 模型适配器包
from .base import BaseModelAdapter
from .openai import OpenAIAdapter
from .doubao import DoubaoAdapter
from .zhipu import ZhipuAdapter
from .ollama import OllamaAdapter
from .gemini import GeminiAdapter
from .qwen import QwenAdapter
from .ernie import ErnieAdapter
from .spark import SparkAdapter
from .kimi import KimiAdapter
from .deepseek import DeepSeekAdapter
from .minimax import MiniMaxAdapter
from .yi import YiAdapter
from .nvidia import NvidiaAdapter

__all__ = [
    'BaseModelAdapter',
    'OpenAIAdapter',
    'DoubaoAdapter',
    'ZhipuAdapter',
    'OllamaAdapter',
    'GeminiAdapter',
    'QwenAdapter',
    'ErnieAdapter',
    'SparkAdapter',
    'KimiAdapter',
    'DeepSeekAdapter',
    'MiniMaxAdapter',
    'YiAdapter',
    'NvidiaAdapter'
]
