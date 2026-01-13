"""
豆包模型适配器
支持火山引擎豆包模型
"""
import requests
from typing import Dict, List, Optional, Any, Generator
import json
from .base import BaseModelAdapter


class DoubaoAdapter(BaseModelAdapter):
    """豆包模型适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        豆包聊天补全（非流式）
        """
        url = f"{self.base_url}/chat/completions"
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        
        if max_tokens:
            data["max_tokens"] = max_tokens
        
        # 额外参数
        if kwargs:
            data.update(kwargs)
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            # 提取内容
            content = result["choices"][0]["message"]["content"]
            
            # 转换为统一格式
            return self.format_response(
                content=content,
                model=self.model,
                usage=result.get("usage", {})
            )
        except requests.exceptions.RequestException as e:
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
        豆包聊天补全（流式）
        """
        url = f"{self.base_url}/chat/completions"
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True
        }
        
        if max_tokens:
            data["max_tokens"] = max_tokens
        
        if kwargs:
            data.update(kwargs)
        
        try:
            response = requests.post(url, headers=self.headers, json=data, stream=True, timeout=120)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            yield self.format_stream_chunk("", finish_reason="stop")
                            break
                        
                        try:
                            chunk = json.loads(data_str)
                            if chunk.get("choices"):
                                delta = chunk["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield self.format_stream_chunk(content=content)
                        except json.JSONDecodeError:
                            continue
        except requests.exceptions.RequestException as e:
            yield {
                "error": {
                    "message": str(e),
                    "type": "api_error"
                }
            }
