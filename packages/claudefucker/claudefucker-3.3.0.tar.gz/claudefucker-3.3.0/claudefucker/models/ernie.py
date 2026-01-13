"""
文心一言模型适配器
支持百度文心一言系列模型
"""
import requests
import json
from typing import Dict, List, Optional, Any, Generator
from .base import BaseModelAdapter


class ErnieAdapter(BaseModelAdapter):
    """文心一言模型适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.access_token = self.api_key
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def _get_access_token(self) -> str:
        """获取访问令牌（如果使用API Key和Secret Key）"""
        # 如果self.api_key是API Key格式，需要获取access token
        if '.' in self.api_key:
            return self.api_key  # 已经是access token
        
        # 如果需要从API Key获取，实现获取逻辑
        return self.api_key
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        文心一言聊天补全（非流式）
        """
        url = f"{self.base_url}/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{self.model}?access_token={self.access_token}"
        
        data = {
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        
        if max_tokens:
            data["max_output_tokens"] = max_tokens
        
        if kwargs:
            data.update(kwargs)
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            
            if 'error_code' in result and result['error_code'] != 0:
                return {
                    "error": {
                        "message": result.get('error_msg', 'Unknown error'),
                        "type": "api_error",
                        "code": result.get('error_code')
                    }
                }
            
            content = result['result']
            
            return self.format_response(
                content=content,
                model=self.model,
                usage={
                    "prompt_tokens": result.get('usage', {}).get('prompt_tokens', 0),
                    "completion_tokens": result.get('usage', {}).get('completion_tokens', 0),
                    "total_tokens": result.get('usage', {}).get('total_tokens', 0)
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
        文心一言聊天补全（流式）
        """
        url = f"{self.base_url}/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{self.model}?access_token={self.access_token}"
        
        data = {
            "messages": messages,
            "temperature": temperature,
            "stream": True
        }
        
        if max_tokens:
            data["max_output_tokens"] = max_tokens
        
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
                        
                        try:
                            chunk = json.loads(data_str)
                            
                            # 检查错误
                            if 'error_code' in chunk and chunk['error_code'] != 0:
                                yield {
                                    "error": {
                                        "message": chunk.get('error_msg', 'Unknown error'),
                                        "type": "api_error",
                                        "code": chunk.get('error_code')
                                    }
                                }
                                break
                            
                            # 提取内容
                            if 'result' in chunk:
                                yield self.format_stream_chunk(content=chunk['result'])
                            
                            # 检查是否结束
                            if chunk.get('is_end', False):
                                yield self.format_stream_chunk("", finish_reason="stop")
                                break
                                
                        except json.JSONDecodeError:
                            continue
        except requests.exceptions.RequestException as e:
            yield {
                "error": {
                    "message": str(e),
                    "type": "api_error"
                }
            }
