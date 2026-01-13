#!/usr/bin/env python3
"""
claudefucker 文件上传示例

演示如何使用claudefucker上传和处理文件
"""

import requests
import base64
from pathlib import Path


def upload_file_and_chat(image_path, prompt, model="claude-3-5-sonnet-20241022"):
    """
    上传图片并进行对话

    Args:
        image_path: 图片文件路径
        prompt: 用户提示词
        model: 模型名称

    Returns:
        API响应
    """
    url = "http://localhost:5000/v1/messages"

    headers = {
        "x-api-key": "your-api-key"  # 替换为你的API Key
    }

    # 读取图片并转换为base64
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # 构建消息
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    data = {
        "model": model,
        "max_tokens": 1024,
        "messages": messages
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            files={
                'file': (Path(image_path).name, open(image_path, 'rb')),
                'data': (None, json.dumps(data), 'application/json')
            }
        )

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Exception: {e}")


def upload_document_and_chat(doc_path, prompt, model="claude-3-5-sonnet-20241022"):
    """
    上传文档并进行对话

    Args:
        doc_path: 文档文件路径
        prompt: 用户提示词
        model: 模型名称

    Returns:
        API响应
    """
    url = "http://localhost:5000/v1/messages"

    headers = {
        "x-api-key": "your-api-key"  # 替换为你的API Key
    }

    # 构建消息
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    data = {
        "model": model,
        "max_tokens": 1024,
        "messages": messages
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            files={
                'file': (Path(doc_path).name, open(doc_path, 'rb')),
                'data': (None, json.dumps(data), 'application/json')
            }
        )

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    # 示例1：上传图片
    print("=== 示例1：图片识别 ===")
    image_path = "example.jpg"  # 替换为你的图片路径

    if Path(image_path).exists():
        result = upload_file_and_chat(
            image_path,
            "请描述这张图片的内容"
        )
        if result:
            print(f"回复: {result}")
    else:
        print(f"图片文件 {image_path} 不存在")

    # 示例2：上传文档
    print("\n=== 示例2：文档分析 ===")
    doc_path = "document.pdf"  # 替换为你的文档路径

    if Path(doc_path).exists():
        result = upload_document_and_chat(
            doc_path,
            "请总结这个文档的主要内容"
        )
        if result:
            print(f"回复: {result}")
    else:
        print(f"文档文件 {doc_path} 不存在")
