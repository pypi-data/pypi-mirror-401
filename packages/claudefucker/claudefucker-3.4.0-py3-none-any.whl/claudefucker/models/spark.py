"""
讯飞星火模型适配器
支持科大讯飞星火认知大模型
"""
import requests
import json
import hashlib
import time
import hmac
import base64
from typing import Dict, List, Optional, Any, Generator
from .base import BaseModelAdapter


class SparkAdapter(BaseModelAdapter):
    """讯飞星火模型适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # API格式: app_id:api_key:api_secret
        if ':' in self.api_key:
            parts = self.api_key.split(':')
            self.app_id = parts[0]
            self.api_key_value = parts[1]
            self.api_secret = parts[2] if len(parts) > 2 else ''
        else:
            self.app_id = self.api_key
            self.api_key_value = config.get('api_key_value', '')
            self.api_secret = config.get('api_secret', '')
    
    def _generate_auth_url(self) -> str:
        """生成认证URL"""
        timestamp = str(int(time.time()))
        signature_origin = f"host: {self.base_url.split('://')[-1]}\ndate: {timestamp}\nGET /{self.model} HTTP/1.1"
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = f'api_key="{self.api_key_value}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        url = f"{self.base_url}/{self.model}?authorization={authorization}&date={timestamp}&host={self.base_url.split('://')[-1]}"
        return url
    
    def _build_messages(self, messages: List[Dict[str, str]]) -> Dict:
        """构建请求消息"""
        history = []
        content = ""
        
        for i, msg in enumerate(messages):
            role = msg.get('role', 'user')
            msg_content = msg.get('content', '')
            
            if i == len(messages) - 1:
                content = msg_content
            else:
                history.append({
                    "role": role,
                    "content": msg_content
                })
        
        return {
            "header": {
                "app_id": self.app_id,
                "uid": str(hash(content))
            },
            "parameter": {
                "chat": {
                    "domain": self.model
                }
            },
            "payload": {
                "message": {
                    "text": history + [{"role": "user", "content": content}] if history else [{"role": "user", "content": content}]
                }
            }
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
        讯飞星火聊天补全（非流式）
        """
        url = self._generate_auth_url()
        payload = self._build_messages(messages)
        
        # 设置温度和最大token
        if temperature != 0.7:
            payload["parameter"]["chat"]["temperature"] = temperature
        if max_tokens:
            payload["parameter"]["chat"]["max_tokens"] = max_tokens
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            
            if result['header']['code'] != 0:
                return {
                    "error": {
                        "message": result['header']['message'],
                        "type": "api_error",
                        "code": result['header']['code']
                    }
                }
            
            content = result['payload']['choices']['text'][0]['content']
            
            return self.format_response(
                content=content,
                model=self.model,
                usage={
                    "prompt_tokens": result['payload']['usage']['text']['prompt_tokens'],
                    "completion_tokens": result['payload']['usage']['text']['completion_tokens'],
                    "total_tokens": result['payload']['usage']['text']['total_tokens']
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
        讯飞星火聊天补全（流式）
        """
        url = self._generate_auth_url()
        payload = self._build_messages(messages)
        
        if temperature != 0.7:
            payload["parameter"]["chat"]["temperature"] = temperature
        if max_tokens:
            payload["parameter"]["chat"]["max_tokens"] = max_tokens
        
        try:
            response = requests.post(url, json=payload, stream=True, timeout=120)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        
                        try:
                            chunk = json.loads(data_str)
                            
                            # 检查错误
                            if chunk['header']['code'] != 0:
                                yield {
                                    "error": {
                                        "message": chunk['header']['message'],
                                        "type": "api_error",
                                        "code": chunk['header']['code']
                                    }
                                }
                                break
                            
                            # 提取内容
                            if 'payload' in chunk and 'choices' in chunk['payload']:
                                if chunk['payload']['choices']['text']:
                                    content = chunk['payload']['choices']['text'][0].get('content', '')
                                    if content:
                                        yield self.format_stream_chunk(content=content)
                            
                            # 检查是否结束
                            if chunk['header']['status'] == 2:
                                yield self.format_stream_chunk("", finish_reason="stop")
                                break
                                
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            yield {
                "error": {
                    "message": str(e),
                    "type": "api_error"
                }
            }
