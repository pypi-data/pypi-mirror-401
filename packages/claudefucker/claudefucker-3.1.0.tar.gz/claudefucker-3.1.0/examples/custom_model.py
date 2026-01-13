#!/usr/bin/env python3
"""
claudefucker 自定义模型示例

演示如何使用自定义模型名称
"""

import requests
import json


def use_custom_model(model_name, messages):
    """
    使用自定义模型进行对话

    Args:
        model_name: 自定义模型名称（格式: custom:模型名称 或 manual:模型名称）
        messages: 消息列表

    Returns:
        API响应
    """
    url = "http://localhost:5000/v1/messages"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": "your-api-key"  # 替换为你的API Key
    }

    data = {
        "model": model_name,
        "max_tokens": 1024,
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    # 示例1：使用custom:前缀
    print("=== 示例1：使用custom:前缀 ===")
    messages = [
        {"role": "user", "content": "你好！"}
    ]

    # 使用OpenAI的GPT-4模型
    result = use_custom_model("custom:openai/gpt-4-turbo-preview", messages)
    if result:
        print(f"回复: {result}")

    # 示例2：使用manual:前缀
    print("\n=== 示例2：使用manual:前缀 ===")

    # 使用DeepSeek模型
    result = use_custom_model("manual:deepseek-chat", messages)
    if result:
        print(f"回复: {result}")

    # 示例3：使用自定义的本地模型
    print("\n=== 示例3：使用自定义的本地模型 ===")

    # 假设你在Ollama中有一个自定义模型
    result = use_custom_model("manual:ollama/my-custom-model", messages)
    if result:
        print(f"回复: {result}")

    print("\n提示：使用自定义模型时，请确保：")
    print("1. 模型名称格式正确（custom: 或 manual: 前缀）")
    print("2. 你有对应厂商的API访问权限")
    print("3. API Key有效且有足够额度")
