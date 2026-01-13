"""
MiniMax模型适配器
支持MiniMax abab6.5s、abab6.5、abab5.5s、abab5.5等模型
"""
from openai import OpenAI
from typing import Dict, List, Optional, Any, Generator
from .base import BaseModelAdapter


class MiniMaxAdapter(BaseModelAdapter):
    """MiniMax模型适配器 - 使用OpenAI兼容API"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.minimax.chat/v1"
        )
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        MiniMax聊天补全（非流式）
        """
        try:
            kwargs_params = {
                "temperature": temperature,
                "stream": stream
            }
            
            if max_tokens:
                kwargs_params["max_tokens"] = max_tokens
            
            if kwargs:
                kwargs_params.update(kwargs)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs_params
            )
            
            content = response.choices[0].message.content
            
            return self.format_response(
                content=content,
                model=self.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
        except Exception as e:
            return {
                "error": {
                    "message": str(e),
                    "type": "api_error"
                }
            }
    
    def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Generator[Dict[str, Any], None, None]:
        """
        MiniMax聊天补全（流式）
        """
        try:
            kwargs_params = {
                "temperature": temperature,
                "stream": True
            }
            
            if max_tokens:
                kwargs_params["max_tokens"] = max_tokens
            
            if kwargs:
                kwargs_params.update(kwargs)
            
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs_params
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield self.format_stream_chunk(content=chunk.choices[0].delta.content)
            
            yield self.format_stream_chunk("", finish_reason="stop")
        except Exception as e:
            yield {
                "error": {
                    "message": str(e),
                    "type": "api_error"
                }
            }
