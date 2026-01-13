"""
Anthropic格式AI代理服务器
将Claude Code的Anthropic格式请求转换为各厂商格式
兼容Claude Code使用
"""
import json
import os
import sys
import subprocess


def check_and_install_dependencies():
    """
    检查并自动安装缺失的依赖包
    """
    required_packages = [
        'flask',
        'flask_cors',
        'openai',
        'anthropic',
        'zhipuai',
        'dashscope',
        'google-generativeai',
        'yaml',
        'colorama',
        'dotenv',
        'requests'
    ]

    # 导入映射（包名 -> 导入名）
    import_map = {
        'flask': 'flask',
        'flask_cors': 'flask_cors',
        'openai': 'openai',
        'anthropic': 'anthropic',
        'zhipuai': 'zhipuai',
        'dashscope': 'dashscope',
        'google-generativeai': 'google.generativeai',
        'yaml': 'yaml',
        'colorama': 'colorama',
        'dotenv': 'dotenv',
        'requests': 'requests'
    }

    missing_packages = []

    for package in required_packages:
        try:
            __import__(import_map[package])
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("\n" + "=" * 60)
        print("检测到缺失的依赖包，正在自动安装...")
        print("=" * 60)

        # 安装缺失的包
        for package in missing_packages:
            print(f"正在安装 {package}...")
            try:
                subprocess.check_call([
                    sys.executable,
                    '-m',
                    'pip',
                    'install',
                    package,
                    '--quiet',
                    '--disable-pip-version-check'
                ])
                print(f"✓ {package} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"✗ {package} 安装失败: {e}")
                print("\n请手动运行: pip install " + " ".join(missing_packages))
                sys.exit(1)

        print("\n" + "=" * 60)
        print("所有依赖包已安装完成！")
        print("=" * 60 + "\n")

        # 重新导入包
        from flask import Flask
        from flask import request, jsonify, Response, stream_with_context
        from flask_cors import CORS
        from .model_manager import ModelManager
        from .file_processor import FileProcessor
        from .format_converter import FormatConverter

        return Flask, request, jsonify, Response, stream_with_context, CORS, ModelManager, FileProcessor, FormatConverter

    else:
        from flask import Flask, request, jsonify, Response, stream_with_context
        from flask_cors import CORS
        from .model_manager import ModelManager
        from .file_processor import FileProcessor
        from .format_converter import FormatConverter

        return Flask, request, jsonify, Response, stream_with_context, CORS, ModelManager, FileProcessor, FormatConverter


# 在导入时就检查依赖
Flask, request, jsonify, Response, stream_with_context, CORS, ModelManager, FileProcessor, FormatConverter = check_and_install_dependencies()

# 自定义JSON编码器，支持中文不转义
class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        return super().encode(obj)

# 创建Flask应用
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.json.ensure_ascii = False
CORS(app)

# 配置文件上传
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 全局变量
model_manager = None
current_vendor = None
current_model = None

# 初始化文件处理器
file_processor = FileProcessor(upload_dir="uploads")


def interactive_setup():
    """交互式配置厂商和模型"""
    from .cli_setup import VENDORS_MODELS, print_vendors, print_models, print_header
    
    print_header()
    
    # 第一步：选择厂商
    print_vendors()
    vendor_options = list(VENDORS_MODELS.keys())
    vendor_key = input(f"请输入厂商编号（1-{len(vendor_options)}）: ").strip()
    
    while vendor_key not in vendor_options:
        print("无效输入，请重新选择")
        vendor_key = input(f"请输入厂商编号（1-{len(vendor_options)}）: ").strip()
    
    vendor = VENDORS_MODELS[vendor_key]
    vendor_name = vendor['name']
    env_prefix = vendor['env_prefix']
    default_base_url = vendor['default_base_url']
    
    # 第二步：选择模型
    print_models(vendor_key)
    model_options = [m[0] for m in vendor['models']]
    model_key = input(f"请选择模型编号（0-{len(model_options)}，0=手动输入）: ").strip()
    
    # 检查是否为手动输入
    if model_key == '0':
        selected_model = input("请输入模型名称（例如: meta/llama-3.3-70b-instruct）: ").strip()
        while not selected_model:
            print("模型名称不能为空！")
            selected_model = input("请输入模型名称（例如: meta/llama-3.3-70b-instruct）: ").strip()
    else:
        # 从列表中选择
        while model_key not in model_options:
            print("无效输入，请重新选择")
            model_key = input(f"请选择模型编号（0-{len(model_options)}，0=手动输入）: ").strip()
        
        selected_model = None
        for key, model_id, model_name in vendor['models']:
            if key == model_key:
                selected_model = model_id
                break
    
    # 第三步：输入API Key
    print(f"\n请输入 {vendor_name} 的 API Key:\n")
    api_key = input(f"{env_prefix}_API_KEY: ").strip()
    
    while not api_key:
        print("API Key不能为空！")
        api_key = input(f"{env_prefix}_API_KEY: ").strip()
    
    # 设置环境变量，方便Claude Code使用
    anthropic_base_url = 'http://localhost:5000'
    os.environ['ANTHROPIC_BASE_URL'] = anthropic_base_url
    os.environ['ANTHROPIC_API_KEY'] = api_key
    
    print(f"\n已自动设置环境变量:")
    print(f"  export ANTHROPIC_BASE_URL={anthropic_base_url}")
    print(f"  export ANTHROPIC_API_KEY={api_key}\n")
    
    # 返回配置信息
    return {
        'vendor': vendor_name,
        'vendor_key': vendor_key,
        'model': selected_model,
        'api_key': api_key,
        'base_url': default_base_url,
        'env_prefix': env_prefix
    }


def create_config(config_info):
    """创建配置文件"""
    import yaml
    
    config_content = f"""# Anthropic格式AI代理配置文件
# 由交互式配置工具生成

# 统一API Key
api_key: "{config_info['api_key']}"

# 默认模型
model: "{config_info['model']}"
"""
    
    with open('config.yaml', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    # 写入.env文件
    env_content = f"{config_info['env_prefix']}_BASE_URL={config_info['base_url']}\n"
    env_content += f"{config_info['env_prefix']}_API_KEY={config_info['api_key']}\n"
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'service': 'multi-model-ai'
    })


@app.route('/v1/models', methods=['GET'])
def list_models():
    """
    列出所有可用的模型
    OpenAI兼容接口
    """
    models_info = model_manager.list_models()
    
    # 转换为OpenAI格式
    models = []
    for vendor, info in models_info.items():
        for model_name in info.get('models', []):
            models.append({
                'id': model_name,
                'object': 'model',
                'owned_by': vendor,
                'permission': [],
                'root': model_name,
                'parent': None
            })
    
    return jsonify({
        'object': 'list',
        'data': models
    })


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """
    聊天补全接口
    OpenAI兼容接口
    """
    try:
        data = request.get_json()
        
        # 提取参数
        messages = data.get('messages', [])
        model_name = data.get('model', None)
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', None)
        stream = data.get('stream', False)
        
        # 提取其他参数
        kwargs = {}
        for key in ['top_p', 'frequency_penalty', 'presence_penalty']:
            if key in data:
                kwargs[key] = data[key]
        
        # 流式输出
        if stream:
            return Response(
                stream_with_context(generate_stream(
                    messages=messages,
                    model_name=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )),
                mimetype='text/event-stream'
            )
        else:
            # 非流式输出
            response = model_manager.chat_completion(
                messages=messages,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False,
                **kwargs
            )
            return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': {
                'message': str(e),
                'type': 'internal_error'
            }
        }), 500


def generate_stream(messages, model_name, temperature, max_tokens, **kwargs):
    """生成流式响应（OpenAI格式）"""
    try:
        for chunk in model_manager.chat_completion_stream(
            messages=messages,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        ):
            # 检查是否有错误
            if 'error' in chunk:
                yield f"data: {json.dumps(chunk)}\n\n"
                break
            
            # 转换为SSE格式
            yield f"data: {json.dumps(chunk)}\n\n"
        
        yield "data: [DONE]\n\n"
    except Exception as e:
        error_chunk = {
            'error': {
                'message': str(e),
                'type': 'stream_error'
            }
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"


def generate_anthropic_stream(messages, model_name, temperature, max_tokens, **kwargs):
    """生成流式响应（Anthropic格式）"""
    try:
        # 先开始事件
        message_data = {
            'id': f'msg_{hash(model_name)}',
            'type': 'message',
            'role': 'assistant',
            'content': [],
            'model': model_name,
            'stop_reason': None,
            'stop_sequence': None,
            'usage': {'input_tokens': 0, 'output_tokens': 0}
        }
        yield f"event: message_start\n"
        yield f"data: {json.dumps({'type': 'message_start', 'message': message_data})}\n\n"
        
        # 开始content block
        yield f"event: content_block_start\n"
        yield f"data: {json.dumps({'type': 'content_block_start', 'index': 0, 'content_block': {'type': 'text', 'text': ''}})}\n\n"
        
        for chunk in model_manager.chat_completion_stream(
            messages=messages,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        ):
            # 检查是否有错误
            if 'error' in chunk:
                yield f"event: error\n"
                yield f"data: {json.dumps({'type': 'error', 'error': chunk['error']})}\n\n"
                break
            
            # 转换为Anthropic格式
            anthropic_chunk = FormatConverter.openai_to_anthropic_stream_chunk(chunk, model_name)
            
            if anthropic_chunk:
                event_type = anthropic_chunk.get('type')
                yield f"event: {event_type}\n"
                yield f"data: {json.dumps(anthropic_chunk)}\n\n"
        
        # 结束content block
        yield f"event: content_block_stop\n"
        yield f"data: {json.dumps({'type': 'content_block_stop', 'index': 0})}\n\n"
        
        # 结束消息
        yield f"event: message_stop\n"
        yield f"data: {json.dumps({'type': 'message_stop'})}\n\n"
        
    except Exception as e:
        error_chunk = {
            'type': 'error',
            'error': {
                'type': 'internal_server_error',
                'message': str(e)
            }
        }
        yield f"event: error\n"
        yield f"data: {json.dumps(error_chunk)}\n\n"


@app.route('/v1/messages', methods=['POST'])
def messages():
    """
    聊天补全接口
    Anthropic兼容接口
    """
    try:
        data = request.get_json()
        
        # 转换为OpenAI格式
        openai_request = FormatConverter.anthropic_to_openai_request(data)
        
        messages = openai_request.get('messages', [])
        model_name = openai_request.get('model', None)
        temperature = openai_request.get('temperature', 0.7)
        max_tokens = openai_request.get('max_tokens', None)
        stream = openai_request.get('stream', False)
        
        # 提取其他参数
        kwargs = {}
        for key in ['top_p', 'top_k', 'frequency_penalty', 'presence_penalty']:
            if key in openai_request:
                kwargs[key] = openai_request[key]
        
        # 流式输出
        if stream:
            return Response(
                stream_with_context(generate_anthropic_stream(
                    messages=messages,
                    model_name=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )),
                mimetype='text/event-stream'
            )
        else:
            # 非流式输出
            openai_response = model_manager.chat_completion(
                messages=messages,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False,
                **kwargs
            )
            
            # 转换为Anthropic格式
            anthropic_response = FormatConverter.openai_to_anthropic_response(
                openai_response,
                model_name
            )
            
            return jsonify(anthropic_response)
    
    except Exception as e:
        error_response = {
            'type': 'error',
            'error': {
                'type': 'internal_error',
                'message': str(e)
            }
        }
        return jsonify(error_response), 500


@app.route('/v1/switch_model', methods=['POST'])
def switch_model():
    """
    更新默认模型（仅更新配置文件）
    注意：实际使用时建议在请求中直接指定model参数
    """
    try:
        data = request.get_json()
        model_name = data.get('model')
        
        if not model_name:
            return jsonify({
                'error': {
                    'message': '缺少 model 参数',
                    'type': 'invalid_request_error'
                }
            }), 400
        
        # 更新配置文件
        import yaml
        config_path = "config.yaml"
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            config['model'] = model_name
            
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            # 更新模型管理器的默认模型
            model_manager.default_model = model_name
            
            return jsonify({
                'status': 'success',
                'default_model': model_name,
                'message': '默认模型已更新，建议在请求中直接指定model参数'
            })
        else:
            return jsonify({
                'error': {
                    'message': '配置文件不存在',
                    'type': 'internal_error'
                }
            }), 500
    
    except Exception as e:
        return jsonify({
            'error': {
                'message': str(e),
                'type': 'internal_error'
            }
        }), 500


@app.route('/v1/status', methods=['GET'])
def status():
    """
    获取服务状态
    """
    models_info = model_manager.list_models()
    
    return jsonify({
        'service': 'multi-model-ai',
        'version': '2.0.0',
        'default_model': model_manager.default_model,
        'api_key_configured': bool(model_manager.api_key),
        'supported_models': models_info,
        'usage': '在请求中直接指定model参数即可使用对应的模型'
    })


@app.route('/', methods=['GET'])
def index():
    """首页"""
    return jsonify({
        'current_vendor': current_vendor or 'N/A',
        'current_model': current_model or 'N/A'
    })


@app.route('/v1/files/upload', methods=['POST'])
def upload_file():
    """
    文件上传接口
    支持图像和文档文件
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({
                'error': {
                    'message': '没有文件被上传',
                    'type': 'invalid_request_error'
                }
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': {
                    'message': '文件名为空',
                    'type': 'invalid_request_error'
                }
            }), 400
        
        # 确定文件类型
        file_type = request.form.get('type', 'auto')
        
        if file_type == 'auto':
            # 自动检测文件类型
            file_info = file_processor.get_file_info(file.filename)
            if file_info.get('is_image'):
                file_type = 'image'
            else:
                file_type = 'document'
        
        # 检查文件类型是否允许
        if not file_processor.is_allowed_file(file.filename, file_type):
            return jsonify({
                'error': {
                    'message': f'不支持的文件类型: {file_type}',
                    'type': 'invalid_request_error'
                }
            }), 400
        
        # 保存文件
        filepath = file_processor.save_uploaded_file(file)
        
        if not filepath:
            return jsonify({
                'error': {
                    'message': '文件保存失败',
                    'type': 'internal_error'
                }
            }), 500
        
        # 获取文件信息
        file_info = file_processor.get_file_info(filepath)
        
        return jsonify({
            'status': 'success',
            'file': file_info
        })
    
    except Exception as e:
        return jsonify({
            'error': {
                'message': str(e),
                'type': 'internal_error'
            }
        }), 500


@app.route('/v1/chat/completions/with-file', methods=['POST'])
def chat_completions_with_file():
    """
    带文件的聊天补全接口
    支持图像和多模态对话
    """
    try:
        # 支持multipart/form-data和application/json两种格式
        
        if request.content_type and 'multipart/form-data' in request.content_type:
            # 处理文件上传格式
            model_name = request.form.get('model')
            temperature = float(request.form.get('temperature', 0.7))
            max_tokens = int(request.form.get('max_tokens')) if request.form.get('max_tokens') else None
            stream = request.form.get('stream', 'false').lower() == 'true'
            
            message = request.form.get('message', '')
            file_type = request.form.get('file_type', 'image')
            
            # 构建消息
            messages = []
            
            # 如果有文件
            if 'file' in request.files:
                file = request.files['file']
                
                if file and file.filename:
                    # 保存文件
                    filepath = file_processor.save_uploaded_file(file)
                    
                    if filepath:
                        file_info = file_processor.get_file_info(filepath)
                        
                        if file_info.get('is_image'):
                            # 构建多模态消息
                            base64_data = file_processor.file_to_base64(filepath)
                            messages.append({
                                'role': 'user',
                                'content': [
                                    {'type': 'text', 'text': message or '请描述这张图片'},
                                    {'type': 'image_url', 'image_url': {'url': base64_data}}
                                ]
                            })
                        else:
                            # 文本文件
                            doc_content = file_processor.prepare_document_for_chat(filepath)
                            messages.append({
                                'role': 'user',
                                'content': f"{message}\n\n{doc_content}"
                            })
            
            if not messages:
                messages.append({
                    'role': 'user',
                    'content': message
                })
        
        else:
            # 处理JSON格式
            data = request.get_json()
            
            model_name = data.get('model')
            temperature = data.get('temperature', 0.7)
            max_tokens = data.get('max_tokens')
            stream = data.get('stream', False)
            
            messages = data.get('messages', [])
        
        # 流式输出
        if stream:
            return Response(
                stream_with_context(generate_stream(
                    messages=messages,
                    model_name=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens
                )),
                mimetype='text/event-stream'
            )
        else:
            # 非流式输出
            response = model_manager.chat_completion(
                messages=messages,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': {
                'message': str(e),
                'type': 'internal_error'
            }
        }), 500


def main():
    """主函数"""
    # 交互式配置
    print("\n" + "=" * 50)
    print("Anthropic格式AI代理服务器")
    print("=" * 50)
    
    config_info = interactive_setup()
    
    # 保存配置
    create_config(config_info)
    
    # 初始化模型管理器
    model_manager = ModelManager('config.yaml')
    
    # 更新全局变量
    global current_vendor, current_model
    current_vendor = config_info['vendor']
    current_model = config_info['model']
    
    # 确认配置
    print("\n" + "=" * 50)
    print("✓ 切换成功！")
    print(f"当前模型厂商: {current_vendor}")
    print(f"当前模型: {current_model}")
    print("=" * 50)
    print("\n喜欢关注python学霸公众号\n")
    
    # 启动服务
    host = '0.0.0.0'
    port = 5000
    
    print(f"服务已启动: http://{host}:{port}")
    print(f"Claude Code配置:")
    print(f"  ANTHROPIC_BASE_URL=http://{host}:{port}")
    print(f"  ANTHROPIC_API_KEY={config_info['api_key']}\n")
    
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    main()
