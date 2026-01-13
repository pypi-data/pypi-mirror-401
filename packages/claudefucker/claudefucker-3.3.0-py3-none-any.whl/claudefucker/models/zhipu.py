"""
智谱AI模型适配器
支持GLM系列模型
"""
import zhipuai
from typing import Dict, List, Optional, Any, Generator
from .base import BaseModelAdapter


class ZhipuAdapter(BaseModelAdapter):
    """智谱AI模型适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        zhipuai.api_key = self.api_key
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        智谱聊天补全（非流式）
        """
        try:
            response = zhipuai.model_api.invoke(
                model=self.model,
                messages=messages,
                temperature=temperature,
                **kwargs
            )
            
            if response['code'] == 200:
                content = response['data']['choices'][0]['content']
                
                return self.format_response(
                    content=content,
                    model=self.model,
                    usage={
                        "prompt_tokens": response['data']['usage'].get('prompt_tokens', 0),
                        "completion_tokens": response['data']['usage'].get('completion_tokens', 0),
                        "total_tokens": response['data']['usage'].get('total_tokens', 0)
                    }
                )
            else:
                return {
                    "error": {
                        "message": response['msg'],
                        "type": "api_error"
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
        智谱聊天补全（流式）
        """
        try:
            response = zhipuai.model_api.invoke(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
                **kwargs
            )
            
            for chunk in response:
                if chunk['code'] == 200:
                    event = chunk['event']
                    if event == 'add':
                        content = chunk['data']['choices'][0]['delta']['content']
                        if content:
                            yield self.format_stream_chunk(content=content)
                    elif event == 'finish':
                        yield self.format_stream_chunk("", finish_reason="stop")
                else:
                    yield {
                        "error": {
                            "message": chunk['msg'],
                            "type": "api_error"
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
