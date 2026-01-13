# claudefucker

Anthropic格式AI代理服务器 - 将Claude Code的Anthropic格式请求转换为各厂商格式

## 安装

```bash
pip install claudefucker
```

## 使用

### 启动服务

```bash
claudefuck
```

### Claude Code 配置

启动后按照提示选择：
1. 选择AI厂商（14个主流厂商）
2. 选择模型
3. 输入API Key

启动成功后，配置Claude Code：

```
ANTHROPIC_BASE_URL=http://0.0.0.0:5000
ANTHROPIC_API_KEY=<你的API Key>
```

## 支持的厂商

- OpenAI (GPT系列)
- 豆包（火山引擎）
- 智谱AI（GLM系列）
- 通义千问（阿里云）
- Gemini（Google）
- 文心一言（百度）
- 讯飞星火
- Kimi（月之暗面）
- Claude（Anthropic）
- NVIDIA NIM
- Ollama（本地）
- MiniMax
- 零一万物（Yi）
- DeepSeek

## 特性

- 统一API接口，兼容Anthropic格式
- 支持14个主流AI厂商
- 自动识别API Key所属厂商
- 支持流式和非流式输出
- 支持手动输入模型名称
- 共支持106个模型

## 开发

喜欢关注python学霸公众号

## License

MIT
