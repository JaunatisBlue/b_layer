import json

print("B层输出统计：\n")

with open('../events/B.jsonl', 'r') as f:
    events = [json.loads(line) for line in f]

print(f"总事件数: {len(events)}")

aliases = set()
with_embedding = 0
for e in events:
    if e['temp_alias_id']:
        aliases.add(e['temp_alias_id'])
    if e['face_embedding']:
        with_embedding += 1

print(f"识别人物数: {len(aliases)}")
print(f"人物列表: {sorted(aliases)}")
print(f"包含embedding的事件: {with_embedding}/{len(events)}")

print("\n示例事件：")
for i, e in enumerate(events[:3]):
    print(f"\n事件{i+1}:")
    print(f"  人物: {e['temp_alias_id']}")
    print(f"  时间: {e['time']['start_ts'][:19]} - {e['time']['end_ts'][11:19]}")
    print(f"  摘要: {e['summary']}")
    print(f"  行为: {e['slots']['dialogue_act']}")
