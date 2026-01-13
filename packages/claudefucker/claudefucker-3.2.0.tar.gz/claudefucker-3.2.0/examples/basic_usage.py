#!/usr/bin/env python3
"""
claudefucker 基础使用示例

演示如何使用claudefucker进行基本的API调用
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:5000"
API_KEY = "your-api-key"  # 替换为你的API Key


def chat_completion(messages, model="claude-3-5-sonnet-20241022", stream=False):
    """
    创建聊天完成

    Args:
        messages: 消息列表
        model: 模型名称
        stream: 是否使用流式输出

    Returns:
        API响应
    """
    url = f"{BASE_URL}/v1/messages"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    data = {
        "model": model,
        "max_tokens": 1024,
        "messages": messages
    }

    if stream:
        data["stream"] = True

    try:
        response = requests.post(url, headers=headers, json=data, stream=stream)

        if response.status_code == 200:
            if stream:
                # 流式输出
                for line in response.iter_lines():
                    if line:
                        print(line.decode('utf-8'))
            else:
                # 非流式输出
                result = response.json()
                return result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    # 示例1：简单对话
    print("=== 示例1：简单对话 ===")
    messages = [
        {"role": "user", "content": "你好！请介绍一下你自己。"}
    ]

    result = chat_completion(messages)
    if result:
        print(f"回复: {result}")

    # 示例2：多轮对话
    print("\n=== 示例2：多轮对话 ===")
    messages = [
        {"role": "user", "content": "什么是人工智能？"},
        {"role": "assistant", "content": "人工智能是计算机科学的一个分支..."},
        {"role": "user", "content": "那机器学习呢？"}
    ]

    result = chat_completion(messages)
    if result:
        print(f"回复: {result}")

    # 示例3：流式输出
    print("\n=== 示例3：流式输出 ===")
    messages = [
        {"role": "user", "content": "请写一首关于春天的诗"}
    ]

    chat_completion(messages, stream=True)
