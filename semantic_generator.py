import json
import requests
from typing import List, Dict

class SemanticGenerator:
    def __init__(self, config: Dict):
        self.api_url = config['llm_api_url']
        self.api_key = config['llm_api_key']
        self.model = config['model']
        self.temperature = config['temperature']
        self.max_tokens = config['max_tokens']
        self.timeout = config['timeout']

    def generate(self, window_events: List[Dict], context: Dict) -> Dict:
        if not self.api_url or not self.api_key:
            return {
                'summary': '事件聚合',
                'dialogue_act': 'unknown'
            }

        prompt = self._build_prompt(window_events, context)

        for attempt in range(3):
            try:
                response = requests.post(
                    self.api_url,
                    headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                    json={'model': self.model, 'messages': [{'role': 'user', 'content': prompt}],
                          'temperature': self.temperature, 'max_tokens': self.max_tokens},
                    timeout=self.timeout
                )

                if response.status_code != 200:
                    print(f"API错误 {response.status_code}: {response.text[:200]}")
                    raise Exception(f"API returned {response.status_code}")

                result = response.json()
                message = result['choices'][0]['message']
                content = message.get('content') or message.get('reasoning_content', '')

                # Extract JSON from markdown code block
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()

                return json.loads(content)
            except Exception as e:
                print(f"LLM调用失败 (尝试 {attempt+1}/3): {str(e)[:100]}")
                if attempt == 2:
                    return {'summary': '事件聚合', 'dialogue_act': 'unknown'}

        return {'summary': '事件聚合', 'dialogue_act': 'unknown'}

    def _build_prompt(self, events: List[Dict], context: Dict) -> str:
        event_desc = []
        for e in events:
            ts = e['time']['start_ts']
            if e['event_type'] == 'face_detection' and 'resolved_alias' in e:
                event_desc.append(f"- {ts}: 检测到{e['resolved_alias']}的人脸")
            elif e['event_type'] == 'speech_segment':
                event_desc.append(f"- {ts}: 语音活动")

        return f"""当前上下文：
- 场景：{context['scene_label']}
- 人物：{', '.join(context['active_persons'])}

事件序列：
{chr(10).join(event_desc)}

请生成JSON格式输出：
{{"summary": "一句话描述", "dialogue_act": "request/promise/complaint/greeting/status_update/unknown"}}"""
