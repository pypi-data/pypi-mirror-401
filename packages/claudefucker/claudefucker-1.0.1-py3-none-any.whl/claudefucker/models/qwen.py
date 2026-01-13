"""
通义千问模型适配器
支持阿里云通义千问系列模型
"""
import dashscope
from typing import Dict, List, Optional, Any, Generator
from .base import BaseModelAdapter


class QwenAdapter(BaseModelAdapter):
    """通义千问模型适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        dashscope.api_key = self.api_key
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        通义千问聊天补全（非流式）
        """
        try:
            response = dashscope.Generation.call(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                result_format='message',
                **kwargs
            )
            
            if response.status_code == 200:
                content = response.output.choices[0]['message']['content']
                
                return self.format_response(
                    content=content,
                    model=self.model,
                    usage={
                        "prompt_tokens": response.usage.input_tokens,
                        "completion_tokens": response.usage.output_tokens,
                        "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                    }
                )
            else:
                return {
                    "error": {
                        "message": response.message,
                        "type": "api_error",
                        "code": response.code
                    }
                }
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
        通义千问聊天补全（流式）
        """
        try:
            response = dashscope.Generation.call(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                result_format='message',
                stream=True,
                **kwargs
            )
            
            for chunk in response:
                if chunk.status_code == 200:
                    if chunk.output.choices:
                        content = chunk.output.choices[0]['message']['content']
                        if content:
                            yield self.format_stream_chunk(content=content)
                    
                    # 检查是否完成
                    if chunk.output.finish_reason:
                        yield self.format_stream_chunk("", finish_reason=chunk.output.finish_reason)
                        break
                else:
                    yield {
                        "error": {
                            "message": chunk.message,
                            "type": "api_error",
                            "code": chunk.code
                        }
                    }
                    break
        except Exception as e:
            yield {
                "error": {
                    "message": str(e),
                    "type": "api_error"
                }
            }
