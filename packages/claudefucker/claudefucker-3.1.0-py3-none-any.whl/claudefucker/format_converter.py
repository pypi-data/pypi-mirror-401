"""
格式转换器
用于在Anthropic格式和OpenAI格式之间转换
"""
from typing import Dict, List, Any, Generator


class FormatConverter:
    """Anthropic和OpenAI格式转换器"""
    
    @staticmethod
    def anthropic_to_openai_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将Anthropic格式的请求转换为OpenAI格式
        
        Args:
            request_data: Anthropic格式的请求数据
            
        Returns:
            OpenAI格式的请求数据
        """
        # 转换messages
        messages = FormatConverter._convert_anthropic_messages_to_openai(
            request_data.get('messages', [])
        )
        
        # 转换参数
        openai_request = {
            'model': request_data.get('model'),
            'messages': messages,
            'stream': request_data.get('stream', False)
        }
        
        # 转换温度
        if 'max_tokens' in request_data:
            openai_request['max_tokens'] = request_data['max_tokens']
        elif 'max_tokens_to_sample' in request_data:
            openai_request['max_tokens'] = request_data['max_tokens_to_sample']
        
        # 转换温度
        if 'temperature' in request_data:
            openai_request['temperature'] = request_data['temperature']
        else:
            openai_request['temperature'] = 1.0
        
        # 转换top_p
        if 'top_p' in request_data:
            openai_request['top_p'] = request_data['top_p']
        
        # 转换top_k
        if 'top_k' in request_data:
            openai_request['top_k'] = request_data['top_k']
        
        return openai_request
    
    @staticmethod
    def _convert_anthropic_messages_to_openai(
        anthropic_messages: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        转换消息格式
        Anthropic使用role/content结构，OpenAI也使用role/content，但可能有细微差别
        
        Args:
            anthropic_messages: Anthropic格式消息列表
            
        Returns:
            OpenAI格式消息列表
        """
        openai_messages = []
        
        for msg in anthropic_messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            
            # 处理内容格式
            if isinstance(content, str):
                # 简单文本消息
                openai_messages.append({
                    'role': role,
                    'content': content
                })
            elif isinstance(content, list):
                # 多模态内容（图片+文本）
                openai_content = []
                for item in content:
                    if isinstance(item, dict):
                        if item.get('type') == 'text':
                            openai_content.append({
                                'type': 'text',
                                'text': item.get('text', '')
                            })
                        elif item.get('type') == 'image':
                            # Anthropic的image格式
                            source = item.get('source', {})
                            if source:
                                openai_content.append({
                                    'type': 'image_url',
                                    'image_url': {
                                        'url': source.get('data', '')
                                    }
                                })
                
                if openai_content:
                    openai_messages.append({
                        'role': role,
                        'content': openai_content
                    })
        
        return openai_messages
    
    @staticmethod
    def openai_to_anthropic_response(
        openai_response: Dict[str, Any],
        model: str = None
    ) -> Dict[str, Any]:
        """
        将OpenAI格式的响应转换为Anthropic格式
        
        Args:
            openai_response: OpenAI格式的响应数据
            model: 模型名称
            
        Returns:
            Anthropic格式的响应数据
        """
        # 处理错误响应
        if 'error' in openai_response:
            return {
                'type': 'error',
                'error': openai_response['error']
            }
        
        # 转换成功响应
        choices = openai_response.get('choices', [])
        if not choices:
            return {
                'type': 'error',
                'error': {
                    'type': 'invalid_request_error',
                    'message': 'No choices in response'
                }
            }
        
        message = choices[0].get('message', {})
        content = message.get('content', '')
        
        anthropic_response = {
            'id': openai_response.get('id', ''),
            'type': 'message',
            'role': 'assistant',
            'content': [
                {
                    'type': 'text',
                    'text': content
                }
            ],
            'model': model or openai_response.get('model', ''),
            'stop_reason': choices[0].get('finish_reason', 'end_turn'),
            'stop_sequence': None,
            'usage': {
                'input_tokens': openai_response.get('usage', {}).get('prompt_tokens', 0),
                'output_tokens': openai_response.get('usage', {}).get('completion_tokens', 0)
            }
        }
        
        return anthropic_response
    
    @staticmethod
    def openai_to_anthropic_stream_chunk(
        openai_chunk: Dict[str, Any],
        model: str = None
    ) -> Dict[str, Any]:
        """
        将OpenAI格式的流式响应片段转换为Anthropic格式
        
        Args:
            openai_chunk: OpenAI格式的流式片段
            model: 模型名称
            
        Returns:
            Anthropic格式的流式片段
        """
        # 处理错误片段
        if 'error' in openai_chunk:
            return {
                'type': 'error',
                'error': openai_chunk['error']
            }
        
        choices = openai_chunk.get('choices', [])
        if not choices:
            return None
        
        delta = choices[0].get('delta', {})
        content = delta.get('content', '')
        finish_reason = choices[0].get('finish_reason', None)
        
        # 构建Anthropic格式的流式事件
        if content:
            return {
                'type': 'content_block_delta',
                'index': 0,
                'delta': {
                    'type': 'text_delta',
                    'text': content
                }
            }
        elif finish_reason:
            return {
                'type': 'message_stop',
                'stop_reason': finish_reason
            }
        
        return None
    
    @staticmethod
    def list_models_to_anthropic(
        models_info: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        将模型列表转换为Anthropic格式
        
        Args:
            models_info: 模型信息字典
            
        Returns:
            Anthropic格式的模型列表
        """
        models = []
        
        for vendor_name, vendor_info in models_info.items():
            for model_name in vendor_info.get('models', []):
                models.append(model_name)
        
        return {
            'data': [
                {
                    'id': model,
                    'name': model,
                    'display_name': model,
                    'type': 'model'
                }
                for model in models
            ],
            'object': 'list'
        }
