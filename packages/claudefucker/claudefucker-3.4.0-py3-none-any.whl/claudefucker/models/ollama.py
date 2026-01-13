"""
Ollama模型适配器
支持本地部署的开源模型
"""
import requests
from typing import Dict, List, Optional, Any, Generator
import json
from .base import BaseModelAdapter


class OllamaAdapter(BaseModelAdapter):
    """Ollama模型适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.headers = {
            "Content-Type": "application/json"
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
        Ollama聊天补全（非流式）
        """
        url = f"{self.base_url}/api/chat"
        
        data = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if max_tokens:
            data["options"]["num_predict"] = max_tokens
        
        if kwargs:
            data["options"].update(kwargs)
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            content = result["message"]["content"]
            
            return self.format_response(
                content=content,
                model=self.model,
                usage={
                    "prompt_tokens": result.get("prompt_eval_count", 0),
                    "completion_tokens": result.get("eval_count", 0),
                    "total_tokens": result.get("prompt_eval_count", 0) + result.get("eval_count", 0)
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
        Ollama聊天补全（流式）
        """
        url = f"{self.base_url}/api/chat"
        
        data = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature
            }
        }
        
        if max_tokens:
            data["options"]["num_predict"] = max_tokens
        
        if kwargs:
            data["options"].update(kwargs)
        
        try:
            response = requests.post(url, headers=self.headers, json=data, stream=True, timeout=120)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    if chunk.get('done'):
                        yield self.format_stream_chunk("", finish_reason="stop")
                        break
                    else:
                        content = chunk.get('message', {}).get('content', '')
                        if content:
                            yield self.format_stream_chunk(content=content)
        except requests.exceptions.RequestException as e:
            yield {
                "error": {
                    "message": str(e),
                    "type": "api_error"
                }
            }
