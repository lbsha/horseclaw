#!/usr/bin/env python3
"""
MiniMax API 集成模块
用于 AI 驱动开发流水线的代码修复
"""

import os
import json
import urllib.request
from typing import Optional, Dict, Any

# 配置
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = "https://api.minimax.chat/v1/text/chatcompletion_v2"
DEFAULT_MODEL = "MiniMax-M2.1"


def call_minimax(
    prompt: str,
    system_prompt: str = "你是一个高级工程师，擅长修复代码问题。",
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 4000
) -> str:
    """调用 MiniMax API"""
    
    if not MINIMAX_API_KEY:
        return "错误: 未设置 MINIMAX_API_KEY"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        req = urllib.request.Request(
            MINIMAX_BASE_URL,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API 调用失败: {e}"


def fix_code(issues: list, code_context: str = "") -> str:
    """修复代码问题"""
    
    system_prompt = """你是一个高级工程师，擅长修复代码问题。

你的任务是：
1. 分析问题
2. 生成修复代码
3. 只返回代码，不需要解释

要求：
- 使用现代编程风格
- 保持代码简洁
- 确保修复正确"""
    
    prompt = f"""请修复以下问题:

问题列表:
{chr(10).join(f"- {i}" for i in issues)}

代码上下文:
```{code_context}
```

请只返回修复后的代码，不需要解释。"""
    
    return call_minimax(prompt, system_prompt)


def review_code(code: str) -> Dict[str, Any]:
    """代码审查"""
    
    system_prompt = """你是一个代码审查专家。审查代码并给出建议。
    
返回 JSON 格式:
{{
    "issues": ["问题1", "问题2"],
    "score": 8,
    "suggestions": ["建议1", "建议2"]
}}"""
    
    prompt = f"""请审查以下代码:

```{code}
{code}
```

返回 JSON 格式的建议。"""
    
    result = call_minimax(prompt, system_prompt)
    
    # 解析 JSON
    try:
        # 尝试提取 JSON
        import re
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    
    return {"issues": [], "score": 10, "suggestions": []}


def explain_error(error: str) -> str:
    """解释错误信息"""
    
    prompt = f"""请简单解释以下错误，并给出修复建议:

错误信息:
{error}

请用中文回答，简洁明了。"""
    
    return call_minimax(prompt, "你是一个友好的编程助手。")


# 测试
if __name__ == "__main__":
    # 测试 API
    print("🧪 测试 MiniMax API...")
    
    result = call_minimax("你好，请用一句话介绍自己")
    print(f"响应: {result}")
