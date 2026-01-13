"""
Google Gemini模型适配器
支持Gemini系列模型
"""
import google.generativeai as genai
from typing import Dict, List, Optional, Any, Generator
from .base import BaseModelAdapter


class GeminiAdapter(BaseModelAdapter):
    """Gemini模型适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
    
    def _convert_messages(self, messages: List[Dict[str, str]]) -> List:
        """转换消息格式为Gemini格式"""
        gemini_messages = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            
            # Gemini使用user和model角色
            if role == 'assistant':
                role = 'model'
            elif role == 'system':
                # Gemini将系统提示作为第一条消息
                gemini_messages.append({
                    'role': 'user',
                    'parts': [f"System: {content}"]
                })
                continue
            
            gemini_messages.append({
                'role': role,
                'parts': [content]
            })
        
        return gemini_messages
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Gemini聊天补全（非流式）
        """
        try:
            gemini_messages = self._convert_messages(messages)
            
            # 配置生成参数
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            
            response = self.client.generate_content(
                gemini_messages,
                generation_config=generation_config,
                **kwargs
            )
            
            content = response.text
            
            return self.format_response(
                content=content,
                model=self.model,
                usage={
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
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
        Gemini聊天补全（流式）
        """
        try:
            gemini_messages = self._convert_messages(messages)
            
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            
            response = self.client.generate_content(
                gemini_messages,
                generation_config=generation_config,
                stream=True,
                **kwargs
            )
            
            for chunk in response:
                if chunk.text:
                    yield self.format_stream_chunk(content=chunk.text)
            
            yield self.format_stream_chunk("", finish_reason="stop")
        except Exception as e:
            yield {
                "error": {
                    "message": str(e),
                    "type": "api_error"
                }
            }
