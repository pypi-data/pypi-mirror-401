"""
统一模型管理器
自动识别API Key并创建对应的适配器
"""
import yaml
from typing import Dict, Any, Optional, Generator
import os
import re

from .models.doubao import DoubaoAdapter
from .models.openai import OpenAIAdapter
from .models.zhipu import ZhipuAdapter
from .models.ollama import OllamaAdapter
from .models.gemini import GeminiAdapter
from .models.qwen import QwenAdapter
from .models.ernie import ErnieAdapter
from .models.spark import SparkAdapter
from .models.kimi import KimiAdapter
from .models.deepseek import DeepSeekAdapter
from .models.minimax import MiniMaxAdapter
from .models.yi import YiAdapter
from .models.nvidia import NvidiaAdapter


class ModelManager:
    """统一模型管理器 - 根据API Key自动识别厂商"""
    
    # 模型名称到厂商的映射 - 共86个模型
    MODEL_MAPPING = {
        # OpenAI - 5个模型
        'gpt-4o': 'openai',
        'gpt-4o-mini': 'openai',
        'gpt-4-turbo': 'openai',
        'gpt-4': 'openai',
        'gpt-3.5-turbo': 'openai',
        
        # 豆包 - 6个模型
        'doubao-pro-256k-250120': 'doubao',
        'doubao-pro-32k-250528': 'doubao',
        'doubao-pro-4k-250528': 'doubao',
        'doubao-lite-32k-250528': 'doubao',
        'doubao-lite-4k-250528': 'doubao',
        'doubao-pro-4k-241515': 'doubao',
        
        # 智谱 - 8个模型
        'glm-4.7-preview': 'zhipu',
        'glm-4.5': 'zhipu',
        'glm-4': 'zhipu',
        'glm-4-plus': 'zhipu',
        'glm-4-air': 'zhipu',
        'glm-4-flash': 'zhipu',
        'glm-4-long': 'zhipu',
        'glm-3-turbo': 'zhipu',
        
        # 通义千问 - 9个模型
        'qwen-max-latest': 'qwen',
        'qwen-plus-latest': 'qwen',
        'qwen-turbo-latest': 'qwen',
        'qwen-max': 'qwen',
        'qwen-plus': 'qwen',
        'qwen-turbo': 'qwen',
        'qwen-long': 'qwen',
        'qwen-vl-max-latest': 'qwen',
        'qwen-vl-plus': 'qwen',
        
        # Gemini - 8个模型
        'gemini-2.5-pro-exp': 'gemini',
        'gemini-2.5-flash-exp': 'gemini',
        'gemini-2.0-flash-exp': 'gemini',
        'gemini-1.5-pro': 'gemini',
        'gemini-1.5-flash': 'gemini',
        'gemini-1.5-flash-8b': 'gemini',
        'gemini-pro': 'gemini',
        'gemini-flash': 'gemini',
        
        # 文心一言 - 8个模型
        'ernie-4.0-8k': 'ernie',
        'ernie-4.0-turbo-8k': 'ernie',
        'ernie-4.0-128k': 'ernie',
        'ernie-3.5-8k': 'ernie',
        'ernie-3.5-128k': 'ernie',
        'ernie-speed-8k': 'ernie',
        'ernie-speed-128k': 'ernie',
        'ernie-tiny-8k': 'ernie',
        
        # 讯飞星火 - 7个模型
        'spark-4.0-ultra': 'spark',
        'spark-max': 'spark',
        'spark-4.0': 'spark',
        'spark-pro-128k': 'spark',
        'spark-pro': 'spark',
        'spark-lite': 'spark',
        'spark-3.5-max': 'spark',
        
        # Kimi - 4个模型
        'moonshot-v1-128k': 'kimi',
        'moonshot-v1-32k': 'kimi',
        'moonshot-v1-8k': 'kimi',
        'moonshot-v1-8k-vision': 'kimi',
        
        # Claude - 6个模型
        'claude-3-7-sonnet-20250219': 'claude',
        'claude-3-5-sonnet-20241022': 'claude',
        'claude-3-5-haiku-20241022': 'claude',
        'claude-3-opus-20240229': 'claude',
        'claude-3-sonnet-20240229': 'claude',
        'claude-3-haiku-20240307': 'claude',
        
        # NVIDIA NIM - 34个模型
        'zhipuai/glm-4.7': 'nvidia',
        'minimax/MiniMax-M2.1': 'nvidia',
        'meta/llama-3.3-70b-instruct': 'nvidia',
        'meta/llama-3.1-405b-instruct': 'nvidia',
        'meta/llama-3.1-70b-instruct': 'nvidia',
        'meta/llama-3.1-8b-instruct': 'nvidia',
        'meta/llama-3.2-90b-vision-instruct': 'nvidia',
        'meta/llama-3.2-11b-vision-instruct': 'nvidia',
        'meta/llama-3.2-3b-instruct': 'nvidia',
        'meta/llama-3.2-1b-instruct': 'nvidia',
        'mistralai/mistral-large@2407': 'nvidia',
        'mistralai/mixtral-8x7b-instruct-v0.1': 'nvidia',
        'mistralai/mixtral-8x22b-instruct-v0.1': 'nvidia',
        'mistralai/mistral-nemo@2407': 'nvidia',
        'google/gemma-2-27b-it': 'nvidia',
        'google/gemma-2-9b-it': 'nvidia',
        'google/gemma-2-2b-it': 'nvidia',
        'nvidia/llama-3.1-nemotron-70b-instruct': 'nvidia',
        'nvidia/llama-3.1-nemotron-70b-rewind-instruct': 'nvidia',
        'nvidia/llama-3.1-nemotron-51b-instruct': 'nvidia',
        'nvidia/llama-3.1-nemotron-15b-instruct-hf': 'nvidia',
        'nvidia/cosmos-1-7b-instruct': 'nvidia',
        'snowflake/arctic': 'nvidia',
        'meta/codellama-70b': 'nvidia',
        'meta/codellama-34b': 'nvidia',
        'meta/llama-2-70b-chat': 'nvidia',
        'databricks/dbrx-instruct': 'nvidia',
        'microsoft/phi-3-medium-128k-instruct': 'nvidia',
        'microsoft/phi-3-mini-128k-instruct': 'nvidia',
        'qwen/qwen-2-72b-instruct': 'nvidia',
        'qwen/qwen-2.5-72b-instruct': 'nvidia',
        '01-ai/yi-1.5-34b-chat': 'nvidia',
        
        # MiniMax - 4个模型
        'abab6.5s-chat': 'minimax',
        'abab6.5-chat': 'minimax',
        'abab5.5s-chat': 'minimax',
        'abab5.5-chat': 'minimax',
        
        # 零一万物 - 6个模型
        'yi-lightning': 'yi',
        'yi-large-turbo': 'yi',
        'yi-large': 'yi',
        'yi-medium': 'yi',
        'yi-spark': 'yi',
        'yi-vl-plus': 'yi',
        
        # DeepSeek - 3个模型
        'deepseek-chat': 'deepseek',
        'deepseek-coder': 'deepseek',
        'deepseek-reasoner': 'deepseek',
    }
    
    # 厂商配置映射
    VENDOR_CONFIGS = {
        'doubao': {
            'class': DoubaoAdapter,
            'default_model': 'doubao-pro-32k-250528',
            'base_url': 'https://ark.cn-beijing.volces.com/api/v3'
        },
        'openai': {
            'class': OpenAIAdapter,
            'default_model': 'gpt-4o',
            'base_url': 'https://api.openai.com/v1'
        },
        'nvidia': {
            'class': OpenAIAdapter,
            'default_model': 'meta/llama-3.1-70b-instruct',
            'base_url': 'https://integrate.api.nvidia.com/v1'
        },
        'zhipu': {
            'class': ZhipuAdapter,
            'default_model': 'glm-4',
        },
        'qwen': {
            'class': QwenAdapter,
            'default_model': 'qwen-plus',
        },
        'gemini': {
            'class': GeminiAdapter,
            'default_model': 'gemini-1.5-pro',
        },
        'ernie': {
            'class': ErnieAdapter,
            'default_model': 'ernie-4.0-8k',
            'base_url': 'https://aip.baidubce.com'
        },
        'spark': {
            'class': SparkAdapter,
            'default_model': 'spark-4.0',
            'base_url': 'wss://spark-api.xf-yun.com/v4.0'
        },
        'kimi': {
            'class': KimiAdapter,
            'default_model': 'moonshot-v1-32k',
            'base_url': 'https://api.moonshot.cn/v1'
        },
        'claude': {
            'class': OpenAIAdapter,
            'default_model': 'claude-3-5-sonnet-20241022',
            'base_url': 'https://api.anthropic.com/v1'
        },
        'ollama': {
            'class': OllamaAdapter,
            'default_model': 'llama3',
            'base_url': 'http://localhost:11434'
        },
        'minimax': {
            'class': MiniMaxAdapter,
            'default_model': 'abab6.5s-chat',
            'base_url': 'https://api.minimax.chat/v1'
        },
        'yi': {
            'class': YiAdapter,
            'default_model': 'yi-large',
            'base_url': 'https://api.lingyiwanwu.com/v1'
        },
        'deepseek': {
            'class': DeepSeekAdapter,
            'default_model': 'deepseek-chat',
            'base_url': 'https://api.deepseek.com'
        },
        'nvidia': {
            'class': NvidiaAdapter,
            'default_model': 'meta/llama-3.1-70b-instruct',
            'base_url': 'https://integrate.api.nvidia.com/v1'
        }
    }
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        初始化模型管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.adapters: Dict[str, Any] = {}
        self.api_key = self.config.get('api_key', '')
        self.default_model = self.config.get('model', '')
        
        # 设置当前厂商
        self.current_vendor = self._detect_vendor_from_model(self.default_model) if self.default_model else None
        if not self.current_vendor and self.api_key:
            self.current_vendor = self._detect_vendor_from_api_key(self.api_key)
        
        # 如果没有指定模型，自动识别默认模型
        if not self.default_model and self.api_key:
            self.default_model = self._detect_default_model(self.api_key)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(config_path):
            return {}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _detect_vendor_from_model(self, model_name: str) -> Optional[str]:
        """
        根据模型名称检测厂商
        
        Args:
            model_name: 模型名称
            
        Returns:
            厂商名称
        """
        # 检查是否为自定义模型（以custom:或manual:开头）
        if model_name.startswith(('custom:', 'manual:')):
            # 返回None，需要从API密钥推断
            return None
        
        return self.MODEL_MAPPING.get(model_name)
    
    def _detect_vendor_from_api_key(self, api_key: str) -> Optional[str]:
        """
        根据API Key格式自动识别厂商
        
        Args:
            api_key: API密钥
            
        Returns:
            厂商名称
        """
        if not api_key:
            return None
        
        # Claude: sk-ant-开头
        if api_key.startswith('sk-ant-'):
            return 'claude'
        
        # OpenAI: sk-开头，但不包含点号分隔的智谱格式
        if api_key.startswith('sk-') and '.' not in api_key:
            # 进一步区分OpenAI和Kimi
            if len(api_key) > 51:  # OpenAI通常更长
                return 'openai'
            else:
                return 'kimi'
        
        # 智谱: 包含点号分隔
        if '.' in api_key and api_key.count('.') == 1:
            return 'zhipu'
        
        # 通义千问: sk-开头，通常较长
        if api_key.startswith('sk-') and len(api_key) > 30:
            return 'qwen'
        
        # 豆包: 格式较为特殊，通常较长
        if len(api_key) > 40 and '-' in api_key:
            return 'doubao'
        
        # NVIDIA: nvapi-开头
        if api_key.startswith('nvapi-'):
            return 'nvidia'
        
        # Gemini: 通常较长且无特定前缀
        if len(api_key) > 30 and not api_key.startswith(('sk-', 'Bearer', 'nvapi-')):
            return 'gemini'
        
        # 默认返回None，需要用户明确指定
        return None
    
    def _detect_default_model(self, api_key: str) -> str:
        """
        根据API Key自动选择默认模型
        
        Args:
            api_key: API密钥
            
        Returns:
            默认模型名称
        """
        vendor = self._detect_vendor_from_api_key(api_key)
        
        if vendor and vendor in self.VENDOR_CONFIGS:
            return self.VENDOR_CONFIGS[vendor]['default_model']
        
        # 默认使用豆包
        return 'doubao-pro-4k'
    
    def _get_vendor_from_model(self, model_name: str) -> Optional[str]:
        """
        根据模型名称获取厂商
        
        Args:
            model_name: 模型名称
            
        Returns:
            厂商名称或None（表示自定义模型）
        """
        # 检查是否为自定义模型（以custom:或manual:开头）
        if model_name.startswith(('custom:', 'manual:')):
            # 返回None，表示需要从API密钥推断厂商
            return None
        
        return self.MODEL_MAPPING.get(model_name)
    
    def _create_adapter(self, vendor: str, model_name: str) -> Any:
        """
        创建适配器实例
        
        Args:
            vendor: 厂商名称
            model_name: 模型名称
            
        Returns:
            适配器实例
        """
        if vendor not in self.VENDOR_CONFIGS:
            raise ValueError(f"不支持的厂商: {vendor}")
        
        vendor_config = self.VENDOR_CONFIGS[vendor]
        
        # 构建适配器配置
        adapter_config = {
            'api_key': self.api_key,
            'model': model_name,
            'enabled': True
        }
        
        # 添加base_url（如果厂商有）
        if 'base_url' in vendor_config:
            adapter_config['base_url'] = vendor_config['base_url']
        
        # 创建适配器
        adapter_class = vendor_config['class']
        return adapter_class(adapter_config)
    
    def get_adapter(self, model_name: Optional[str] = None) -> Any:
        """
        获取模型适配器
        
        Args:
            model_name: 模型名称，如果为None则使用默认模型
            
        Returns:
            模型适配器实例
        """
        if model_name is None:
            model_name = self.default_model
        
        if not model_name:
            raise ValueError("未指定模型名称，请在配置文件中设置model或在请求中指定model参数")
        
        # 检查是否为自定义模型（以custom:或manual:开头）
        actual_model_name = model_name
        is_custom_model = model_name.startswith(('custom:', 'manual:'))
        
        if is_custom_model:
            # 去掉前缀，得到实际的模型名称
            actual_model_name = model_name.split(':', 1)[1]
            
            # 从API密钥推断厂商
            vendor = self._detect_vendor_from_api_key(self.api_key)
            if vendor is None:
                raise ValueError(
                    f"自定义模型 '{actual_model_name}' 需要明确指定厂商。"
                    f"请确保API密钥格式正确，或使用已知格式的模型名称。"
                )
        else:
            # 获取厂商
            vendor = self._get_vendor_from_model(model_name)
            
            if vendor is None:
                # 尝试从API Key推断
                vendor = self._detect_vendor_from_api_key(self.api_key)
                if vendor is None:
                    raise ValueError(
                        f"无法识别模型 '{model_name}' 的厂商。"
                        f"支持的模型: {', '.join(list(self.MODEL_MAPPING.keys())[:10])}..."
                    )
        
        # 检查缓存
        cache_key = f"{vendor}_{actual_model_name}"
        if cache_key not in self.adapters:
            self.adapters[cache_key] = self._create_adapter(vendor, actual_model_name)
        
        return self.adapters[cache_key]
    
    def list_models(self) -> Dict[str, Dict[str, Any]]:
        """
        列出所有支持的模型
        
        Returns:
            模型信息字典
        """
        models_info = {}
        
        for model_name, vendor in self.MODEL_MAPPING.items():
            if vendor not in models_info:
                models_info[vendor] = {
                    'vendor': vendor,
                    'models': []
                }
            
            models_info[vendor]['models'].append(model_name)
        
        return models_info
    
    def chat_completion(
        self,
        messages: list,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        统一聊天补全接口（非流式）
        
        Args:
            messages: 对话消息列表
            model_name: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            stream: 是否流式输出
            **kwargs: 其他参数
            
        Returns:
            响应字典
        """
        adapter = self.get_adapter(model_name)
        return adapter.chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            **kwargs
        )
    
    def chat_completion_stream(
        self,
        messages: list,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Generator[Dict[str, Any], None, None]:
        """
        统一聊天补全接口（流式）
        
        Args:
            messages: 对话消息列表
            model_name: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Yields:
            响应片段
        """
        adapter = self.get_adapter(model_name)
        yield from adapter.chat_completion_stream(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        self.default_model = model_name
        return {'status': 'success', 'default_model': model_name}
