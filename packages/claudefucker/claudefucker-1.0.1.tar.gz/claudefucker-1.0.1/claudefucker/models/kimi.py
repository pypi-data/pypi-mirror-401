"""
Kimi模型适配器
支持月之暗面Kimi系列模型
"""
import requests
from typing import Dict, List, Optional, Any, Generator
from .base import BaseModelAdapter


class KimiAdapter(BaseModelAdapter):
    """Kimi模型适配器"""
    
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
        Kimi聊天补全（非流式）
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
        
        # Kimi支持长文档，添加相关参数
        if kwargs:
            data.update(kwargs)
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            
            if 'error' in result:
                return {
                    "error": {
                        "message": result['error'].get('message', 'Unknown error'),
                        "type": result['error'].get('type', 'api_error'),
                        "code": result['error'].get('code')
                    }
                }
            
            content = result["choices"][0]["message"]["content"]
            
            return self.format_response(
                content=content,
                model=self.model,
                usage={
                    "prompt_tokens": result.get("usage", {}).get("prompt_tokens", 0),
                    "completion_tokens": result.get("usage", {}).get("completion_tokens", 0),
                    "total_tokens": result.get("usage", {}).get("total_tokens", 0)
                }
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
        Kimi聊天补全（流式）
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
                            
                            # 检查错误
                            if 'error' in chunk:
                                yield {
                                    "error": {
                                        "message": chunk['error'].get('message', 'Unknown error'),
                                        "type": chunk['error'].get('type', 'api_error'),
                                        "code": chunk['error'].get('code')
                                    }
                                }
                                break
                            
                            # 提取内容
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
