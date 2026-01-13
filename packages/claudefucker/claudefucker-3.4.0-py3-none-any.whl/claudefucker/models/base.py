"""
基础模型适配器
所有模型适配器的基类
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Generator


class BaseModelAdapter(ABC):
    """模型适配器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化适配器
        
        Args:
            config: 模型配置字典
        """
        self.config = config
        self.api_key = config.get('api_key', '')
        self.base_url = config.get('base_url', '')
        self.model = config.get('model', '')
        self.enabled = config.get('enabled', False)
    
    @abstractmethod
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        非流式聊天补全
        
        Args:
            messages: 对话消息列表
            temperature: 温度参数 (0-2)
            max_tokens: 最大token数
            stream: 是否流式输出
            **kwargs: 其他参数
            
        Returns:
            响应字典
        """
        pass
    
    @abstractmethod
    def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Generator[Dict[str, Any], None, None]:
        """
        流式聊天补全
        
        Args:
            messages: 对话消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Yields:
            响应片段字典
        """
        pass
    
    def format_response(self, content: str, model: str = None, **metadata) -> Dict[str, Any]:
        """
        格式化为统一响应格式（OpenAI兼容）
        
        Args:
            content: 生成的内容
            model: 模型名称
            **metadata: 其他元数据
            
        Returns:
            格式化后的响应
        """
        return {
            "id": f"chatcmpl-{hash(content) % 1000000}",
            "object": "chat.completion",
            "created": int(__import__('time').time()),
            "model": model or self.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            },
            **metadata
        }
    
    def format_stream_chunk(self, content: str, model: str = None, finish_reason: str = None) -> Dict[str, Any]:
        """
        格式化流式响应片段
        
        Args:
            content: 片段内容
            model: 模型名称
            finish_reason: 完成原因
            
        Returns:
            格式化后的流式片段
        """
        return {
            "id": f"chatcmpl-{hash(content) % 1000000}",
            "object": "chat.completion.chunk",
            "created": int(__import__('time').time()),
            "model": model or self.model,
            "choices": [{
                "index": 0,
                "delta": {
                    "content": content
                },
                "finish_reason": finish_reason
            }]
        }
