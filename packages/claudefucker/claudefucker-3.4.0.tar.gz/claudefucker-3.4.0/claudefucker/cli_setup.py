#!/usr/bin/env python3
"""
多模型AI工具 - 交互式配置CLI
用于选择厂商、模型并配置API Key
"""
import os
import sys
import subprocess
from colorama import init, Fore, Style, Back

# 初始化colorama
init(autoreset=True)

# 厂商和模型配置（最新、可靠）
VENDORS_MODELS = {
    '1': {
        'name': 'OpenAI',
        'env_prefix': 'OPENAI',
        'default_base_url': 'https://api.openai.com/v1',
        'models': [
            ('1', 'gpt-4o', 'GPT-4o（最新最强）'),
            ('2', 'gpt-4o-mini', 'GPT-4o Mini（快速经济）'),
            ('3', 'gpt-4-turbo', 'GPT-4 Turbo'),
            ('4', 'gpt-4', 'GPT-4'),
            ('5', 'gpt-3.5-turbo', 'GPT-3.5 Turbo（经典）'),
        ]
    },
    '2': {
        'name': '豆包（火山引擎）',
        'env_prefix': 'DOUBAO',
        'default_base_url': 'https://ark.cn-beijing.volces.com/api/v3',
        'models': [
            ('1', 'doubao-pro-256k-250120', 'Doubao Pro 256K（最新）'),
            ('2', 'doubao-pro-32k-250528', 'Doubao Pro 32K V2'),
            ('3', 'doubao-pro-4k-250528', 'Doubao Pro 4K V2'),
            ('4', 'doubao-lite-32k-250528', 'Doubao Lite 32K'),
            ('5', 'doubao-lite-4k-250528', 'Doubao Lite 4K'),
            ('6', 'doubao-pro-4k-241515', 'Doubao Pro 4K V1'),
        ]
    },
    '3': {
        'name': '智谱AI（GLM）',
        'env_prefix': 'ZHIPU',
        'default_base_url': 'https://open.bigmodel.cn/api/paas/v4',
        'models': [
            ('1', 'glm-4.7-preview', 'GLM-4.7 Preview（最新）'),
            ('2', 'glm-4.5', 'GLM-4.5'),
            ('3', 'glm-4', 'GLM-4（推荐）'),
            ('4', 'glm-4-plus', 'GLM-4 Plus'),
            ('5', 'glm-4-air', 'GLM-4 Air'),
            ('6', 'glm-4-flash', 'GLM-4 Flash（快速）'),
            ('7', 'glm-4-long', 'GLM-4 Long（长上下文）'),
            ('8', 'glm-3-turbo', 'GLM-3 Turbo（经济）'),
        ]
    },
    '4': {
        'name': '通义千问（阿里云）',
        'env_prefix': 'QWEN',
        'default_base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'models': [
            ('1', 'qwen-max-latest', 'Qwen Max Latest（最新）'),
            ('2', 'qwen-plus-latest', 'Qwen Plus Latest'),
            ('3', 'qwen-turbo-latest', 'Qwen Turbo Latest'),
            ('4', 'qwen-max', 'Qwen Max（最强）'),
            ('5', 'qwen-plus', 'Qwen Plus（推荐）'),
            ('6', 'qwen-turbo', 'Qwen Turbo（快速）'),
            ('7', 'qwen-long', 'Qwen Long（长上下文128K）'),
            ('8', 'qwen-vl-max-latest', 'Qwen VL Max（视觉）'),
            ('9', 'qwen-vl-plus', 'Qwen VL Plus（视觉）'),
        ]
    },
    '5': {
        'name': 'Gemini（Google）',
        'env_prefix': 'GEMINI',
        'default_base_url': 'https://generativelanguage.googleapis.com/v1beta',
        'models': [
            ('1', 'gemini-2.5-pro-exp', 'Gemini 2.5 Pro Experimental（最新）'),
            ('2', 'gemini-2.5-flash-exp', 'Gemini 2.5 Flash Experimental'),
            ('3', 'gemini-2.0-flash-exp', 'Gemini 2.0 Flash Experimental'),
            ('4', 'gemini-1.5-pro', 'Gemini 1.5 Pro（稳定）'),
            ('5', 'gemini-1.5-flash', 'Gemini 1.5 Flash（快速）'),
            ('6', 'gemini-1.5-flash-8b', 'Gemini 1.5 Flash 8B（极速）'),
            ('7', 'gemini-pro', 'Gemini Pro'),
            ('8', 'gemini-flash', 'Gemini Flash'),
        ]
    },
    '6': {
        'name': '文心一言（百度）',
        'env_prefix': 'ERNIE',
        'default_base_url': 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat',
        'models': [
            ('1', 'ernie-4.0-8k', 'ERNIE 4.0 8K（最新）'),
            ('2', 'ernie-4.0-turbo-8k', 'ERNIE 4.0 Turbo 8K'),
            ('3', 'ernie-4.0-128k', 'ERNIE 4.0 128K（长上下文）'),
            ('4', 'ernie-3.5-8k', 'ERNIE 3.5 8K'),
            ('5', 'ernie-3.5-128k', 'ERNIE 3.5 128K'),
            ('6', 'ernie-speed-8k', 'ERNIE Speed 8K'),
            ('7', 'ernie-speed-128k', 'ERNIE Speed 128K'),
            ('8', 'ernie-tiny-8k', 'ERNIE Tiny 8K（极速）'),
        ]
    },
    '7': {
        'name': '讯飞星火',
        'env_prefix': 'SPARK',
        'default_base_url': 'https://spark-api.xf-yun.com/v4.0/chat',
        'models': [
            ('1', 'spark-4.0-ultra', 'Spark 4.0 Ultra（最新最强）'),
            ('2', 'spark-max', 'Spark Max'),
            ('3', 'spark-4.0', 'Spark 4.0'),
            ('4', 'spark-pro-128k', 'Spark Pro 128K'),
            ('5', 'spark-pro', 'Spark Pro'),
            ('6', 'spark-lite', 'Spark Lite（快速）'),
            ('7', 'spark-3.5-max', 'Spark 3.5 Max'),
        ]
    },
    '8': {
        'name': 'Kimi（月之暗面）',
        'env_prefix': 'KIMI',
        'default_base_url': 'https://api.moonshot.cn/v1',
        'models': [
            ('1', 'moonshot-v1-128k', 'Moonshot V1 128K（最新）'),
            ('2', 'moonshot-v1-32k', 'Moonshot V1 32K（推荐）'),
            ('3', 'moonshot-v1-8k', 'Moonshot V1 8K'),
            ('4', 'moonshot-v1-8k-vision', 'Moonshot V1 8K Vision（视觉）'),
        ]
    },
    '9': {
        'name': 'Claude（Anthropic）',
        'env_prefix': 'ANTHROPIC',
        'default_base_url': 'https://api.anthropic.com/v1',
        'models': [
            ('1', 'claude-3-7-sonnet-20250219', 'Claude 3.7 Sonnet（最新）'),
            ('2', 'claude-3-5-sonnet-20241022', 'Claude 3.5 Sonnet（推荐）'),
            ('3', 'claude-3-5-haiku-20241022', 'Claude 3.5 Haiku（快速）'),
            ('4', 'claude-3-opus-20240229', 'Claude 3 Opus（最强）'),
            ('5', 'claude-3-sonnet-20240229', 'Claude 3 Sonnet'),
            ('6', 'claude-3-haiku-20240307', 'Claude 3 Haiku（极速）'),
        ]
    },
    '10': {
        'name': 'NVIDIA NIM',
        'env_prefix': 'NVIDIA',
        'default_base_url': 'https://integrate.api.nvidia.com/v1',
        'models': [
            ('1', 'zhipuai/glm-4.7', 'GLM-4.7（智谱AI）'),
            ('2', 'minimax/MiniMax-M2.1', 'MiniMax M2.1'),
            ('3', 'meta/llama-3.3-70b-instruct', 'Llama 3.3 70B（最新）'),
            ('4', 'meta/llama-3.1-405b-instruct', 'Llama 3.1 405B'),
            ('5', 'meta/llama-3.1-70b-instruct', 'Llama 3.1 70B（推荐）'),
            ('6', 'meta/llama-3.1-8b-instruct', 'Llama 3.1 8B（快速）'),
            ('7', 'mistralai/mistral-large@2407', 'Mistral Large'),
            ('8', 'mistralai/mixtral-8x7b-instruct-v0.1', 'Mixtral 8x7B'),
            ('9', 'google/gemma-2-27b-it', 'Gemma 2 27B'),
            ('10', 'nvidia/llama-3.1-nemotron-70b-instruct', 'Llama 3.1 Nemotron 70B'),
            ('11', 'snowflake/arctic', 'Arctic'),
            ('12', 'meta/codellama-70b', 'Code Llama 70B（代码）'),
            ('13', 'meta/llama-2-70b-chat', 'Llama 2 70B'),
            ('14', 'databricks/dbrx-instruct', 'DBRX Instruct'),
        ]
    },
    '11': {
        'name': 'Ollama（本地）',
        'env_prefix': 'OLLAMA',
        'default_base_url': 'http://localhost:11434/v1',
        'models': [
            ('1', 'llama3.2', 'Llama 3.2（最新）'),
            ('2', 'llama3.1', 'Llama 3.1'),
            ('3', 'llama3', 'Llama 3（推荐）'),
            ('4', 'mistral', 'Mistral'),
            ('5', 'gemma2', 'Gemma 2'),
            ('6', 'qwen2.5', 'Qwen 2.5'),
            ('7', 'deepseek-coder-v2', 'DeepSeek Coder V2（代码）'),
            ('8', 'codellama', 'Code Llama（代码）'),
        ]
    },
    '12': {
        'name': 'MiniMax',
        'env_prefix': 'MINIMAX',
        'default_base_url': 'https://api.minimax.chat/v1',
        'models': [
            ('1', 'abab6.5s-chat', 'MiniMax 6.5s Chat（最新）'),
            ('2', 'abab6.5-chat', 'MiniMax 6.5 Chat'),
            ('3', 'abab5.5s-chat', 'MiniMax 5.5s Chat（快速）'),
            ('4', 'abab5.5-chat', 'MiniMax 5.5 Chat'),
        ]
    },
    '13': {
        'name': '零一万物（Yi）',
        'env_prefix': 'YI',
        'default_base_url': 'https://api.lingyiwanwu.com/v1',
        'models': [
            ('1', 'yi-lightning', 'Yi Lightning（最新极速）'),
            ('2', 'yi-large-turbo', 'Yi Large Turbo'),
            ('3', 'yi-large', 'Yi Large（推荐）'),
            ('4', 'yi-medium', 'Yi Medium'),
            ('5', 'yi-spark', 'Yi Spark（快速）'),
            ('6', 'yi-vl-plus', 'Yi VL Plus（视觉）'),
        ]
    },
    '14': {
        'name': 'DeepSeek（深度求索）',
        'env_prefix': 'DEEPSEEK',
        'default_base_url': 'https://api.deepseek.com/v1',
        'models': [
            ('1', 'deepseek-chat', 'DeepSeek Chat（最新）'),
            ('2', 'deepseek-coder', 'DeepSeek Coder（代码）'),
            ('3', 'deepseek-reasoner', 'DeepSeek Reasoner（推理）'),
        ]
    },
}


def print_header():
    """打印标题"""
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{' ' * 12}多模型AI工具配置{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")


def print_vendors():
    """打印厂商列表"""
    print(f"{Fore.YELLOW}请选择AI厂商：{Style.RESET_ALL}")
    for key, vendor in VENDORS_MODELS.items():
        print(f"  {Fore.GREEN}{key}.{Style.RESET_ALL} {vendor['name']}")
    print()


def print_models(vendor_key):
    """打印模型列表"""
    vendor = VENDORS_MODELS[vendor_key]
    print(f"\n{Fore.YELLOW}请选择 {vendor['name']} 的模型：{Style.RESET_ALL}")
    for key, model_id, model_name in vendor['models']:
        print(f"  {Fore.GREEN}{key}.{Style.RESET_ALL} {model_id}")
    print(f"  {Fore.GREEN}0.{Style.RESET_ALL} 手动输入模型名")
    print()


def print_success(message):
    """打印成功信息"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message):
    """打印错误信息"""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_info(message):
    """打印信息"""
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def print_warning(message):
    """打印警告"""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def get_user_input(prompt, options=None, allow_custom=False, password=False):
    """获取用户输入"""
    while True:
        try:
            import getpass
            if password:
                user_input = getpass.getpass(prompt)
            else:
                user_input = input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()
            
            if not user_input:
                print_error("输入不能为空！")
                continue
            
            if options and user_input in options:
                return user_input
            
            if options and not allow_custom:
                print_error(f"无效输入，请选择：{', '.join(options)}")
                continue
            
            return user_input
        except KeyboardInterrupt:
            print(f"\n\n{Fore.RED}操作已取消{Style.RESET_ALL}")
            sys.exit(0)
        except EOFError:
            print(f"\n\n{Fore.RED}输入结束{Style.RESET_ALL}")
            sys.exit(0)


def detect_shell_config():
    """检测shell配置文件"""
    shell = os.environ.get('SHELL', '')
    
    if 'zsh' in shell:
        return os.path.expanduser('~/.zshrc'), 'zsh'
    elif 'bash' in shell:
        return os.path.expanduser('~/.bashrc'), 'bash'
    else:
        # 默认返回bashrc
        return os.path.expanduser('~/.bashrc'), 'bash'


def write_to_shell_config(base_url, api_key, env_prefix, shell_config_path):
    """写入shell配置文件"""
    # 检查是否已经存在配置
    export_commands = []
    
    # 读取现有配置
    existing_content = ""
    if os.path.exists(shell_config_path):
        try:
            with open(shell_config_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        except Exception as e:
            print_warning(f"读取 {shell_config_path} 失败：{e}")
            return False
    
    # 检查并删除旧的配置
    lines = existing_content.split('\n')
    new_lines = []
    skip_next = False
    
    for line in lines:
        if skip_next:
            skip_next = False
            continue
        
        if f'{env_prefix}_BASE_URL' in line or f'{env_prefix}_API_KEY' in line:
            skip_next = True
            continue
        
        new_lines.append(line)
    
    # 生成新的export命令
    export_commands = [
        f"\n# 多模型AI工具配置 - {env_prefix}",
        f"export {env_prefix}_BASE_URL={base_url}",
        f"export {env_prefix}_API_KEY={api_key}",
    ]
    
    # 写入文件
    try:
        with open(shell_config_path, 'a', encoding='utf-8') as f:
            f.write('\n'.join(export_commands) + '\n')
        return True
    except Exception as e:
        print_warning(f"写入 {shell_config_path} 失败：{e}")
        return False


def write_to_env_file(base_url, api_key, env_prefix):
    """写入.env文件"""
    env_file = os.path.join(os.getcwd(), '.env')
    
    # 读取现有内容
    existing_content = ""
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        except Exception as e:
            print_warning(f"读取 .env 文件失败：{e}")
    
    # 删除旧的配置
    lines = existing_content.split('\n')
    new_lines = []
    
    for line in lines:
        if line.startswith(f'{env_prefix}_BASE_URL=') or line.startswith(f'{env_prefix}_API_KEY='):
            continue
        new_lines.append(line)
    
    # 添加新配置
    new_lines.extend([
        f"{env_prefix}_BASE_URL={base_url}",
        f"{env_prefix}_API_KEY={api_key}",
    ])
    
    # 写入文件
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines) + '\n')
        return True
    except Exception as e:
        print_warning(f"写入 .env 文件失败：{e}")
        return False


def validate_api_key(api_key, vendor_key):
    """简单的API Key验证"""
    if not api_key or len(api_key) < 10:
        print_warning("API Key长度似乎过短，请确认是否正确")
        return False
    
    vendor = VENDORS_MODELS[vendor_key]
    
    # 厂商特定的验证
    if vendor['env_prefix'] == 'OPENAI':
        if not api_key.startswith('sk-'):
            print_warning("OpenAI API Key通常以 'sk-' 开头")
            return False
    
    elif vendor['env_prefix'] == 'ZHIPU':
        if '.' not in api_key:
            print_warning("智谱AI API Key格式应该包含点号分隔")
            return False
    
    elif vendor['env_prefix'] == 'ANTHROPIC':
        if not api_key.startswith('sk-ant-'):
            print_warning("Claude API Key通常以 'sk-ant-' 开头")
            return False
    
    return True


def main():
    """主函数"""
    print_header()
    
    # 第一步：选择厂商
    print_vendors()
    vendor_options = list(VENDORS_MODELS.keys())
    vendor_key = get_user_input("请输入厂商编号（1-14）: ", vendor_options)
    
    vendor = VENDORS_MODELS[vendor_key]
    vendor_name = vendor['name']
    env_prefix = vendor['env_prefix']
    default_base_url = vendor['default_base_url']
    
    # 第二步：选择模型
    print_models(vendor_key)
    model_options = [m[0] for m in vendor['models']]
    model_key = get_user_input(f"请选择模型编号（1-{len(model_options)}）: ", model_options)
    
    selected_model = None
    for key, model_id, model_name in vendor['models']:
        if key == model_key:
            selected_model = model_id
            break
    
    # 第三步：输入API Key
    print(f"\n{Fore.YELLOW}请输入 {vendor_name} 的 API Key:{Style.RESET_ALL}\n")
    api_key = input(f"{env_prefix}_API_KEY: ").strip()
    
    while not api_key:
        print_error("API Key不能为空！")
        api_key = input(f"{env_prefix}_API_KEY: ").strip()
    
    # 验证API Key
    if not validate_api_key(api_key, vendor_key):
        confirm = get_user_input("API Key可能不正确，是否继续？(y/n): ", ['y', 'n', 'Y', 'N'])
        if confirm.lower() != 'y':
            print_error("配置已取消")
            return
    
    # 第四步：确认配置
    print("\n" + "=" * 50)
    print(f"{Fore.CYAN}当前模型厂商:{Style.RESET_ALL} {vendor_name}")
    print(f"{Fore.CYAN}当前模型:{Style.RESET_ALL} {selected_model}")
    print("=" * 50 + "\n")
    
    confirm = get_user_input("确认以上配置？(y/n): ", ['y', 'n', 'Y', 'N'])
    
    if confirm.lower() != 'y':
        print_error("配置已取消")
        return
    
    # 第五步：写入配置
    print(f"\n正在写入配置...\n")
    
    success_count = 0
    
    # 写入.env文件
    if write_to_env_file(default_base_url, api_key, env_prefix):
        print_success("已写入 .env 文件")
        success_count += 1
    
    # 写入shell配置文件
    shell_config_path, shell_type = detect_shell_config()
    if write_to_shell_config(default_base_url, api_key, env_prefix, shell_config_path):
        print_success(f"已写入 {shell_config_path}")
        success_count += 1
    
    # 写入config.yaml
    config_content = f"""# 多模型AI工具配置文件
# 由交互式配置工具生成

# 统一API Key
api_key: "{api_key}"

# 默认模型
model: "{selected_model}"

# 服务配置
server:
  host: "0.0.0.0"
  port: 5000
  debug: false
"""
    
    try:
        with open('config.yaml', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print_success("已写入 config.yaml")
        success_count += 1
    except Exception as e:
        print_warning(f"写入 config.yaml 失败：{e}")
    
    # 完成
    print("\n" + "=" * 50)
    if success_count == 3:
        print(f"{Fore.GREEN}✓ 切换成功！{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}✓ 切换成功，但有 {3 - success_count} 个文件写入失败{Style.RESET_ALL}")
    print("=" * 50)

    print(f"\n{Fore.CYAN}喜欢关注python学霸公众号{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}启动服务命令:{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}python main.py{Style.RESET_ALL}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}操作已取消{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{Fore.RED}发生错误：{str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
