import json
import requests

with open('config.json', 'r') as f:
    config = json.load(f)

print("测试LLM API调用...")
print(f"API URL: {config['llm_api_url']}")
print(f"Model: {config['model']}")

test_prompt = """当前上下文：
- 场景：会议室
- 人物：alias_A

事件序列：
- 2026-03-18T17:03:35: 检测到alias_A的人脸

请生成JSON格式输出：
{"summary": "一句话描述", "dialogue_act": "request/promise/complaint/greeting/status_update/unknown"}"""

try:
    response = requests.post(
        config['llm_api_url'],
        headers={
            'Authorization': f'Bearer {config["llm_api_key"]}',
            'Content-Type': 'application/json'
        },
        json={
            'model': config['model'],
            'messages': [{'role': 'user', 'content': test_prompt}],
            'temperature': config['temperature'],
            'max_tokens': config['max_tokens']
        },
        timeout=config['timeout']
    )

    print(f"\n状态码: {response.status_code}")
    print(f"响应: {response.text[:500]}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n解析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")

except Exception as e:
    print(f"\n错误: {e}")
