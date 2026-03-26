import json

with open('../events/B.jsonl', 'r', encoding='utf-8') as f:
    events = [json.loads(line) for line in f]

total = len(events)
success = sum(1 for e in events if e['summary'] != '事件聚合')
failed = total - success

print(f"总事件: {total}")
print(f"LLM成功: {success}")
print(f"LLM失败: {failed}")
print(f"成功率: {success/total*100:.1f}%")

print("\n成功的摘要示例:")
for i, e in enumerate(events):
    if e['summary'] != '事件聚合':
        print(f"{i+1}. {e['summary']}")
        if i >= 4:
            break
