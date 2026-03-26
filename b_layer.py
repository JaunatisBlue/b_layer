import json
import uuid
from datetime import datetime
from event_reader import EventReader
from event_writer import EventWriter
from identity_tracker import IdentityTracker
from context_manager import ContextManager
from event_aggregator import EventAggregator
from semantic_generator import SemanticGenerator

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    tracker = IdentityTracker('person_cache.db', config['identity']['face_similarity_threshold'])
    context_mgr = ContextManager()
    aggregator = EventAggregator(config)
    generator = SemanticGenerator(config)

    event_count = 0
    semantic_count = 0

    with EventReader('../events/A.jsonl') as reader, EventWriter('../events/B.jsonl') as writer:
        while True:
            event = reader.read_next()
            if event is None:
                break

            event_count += 1
            print(f"处理事件 {event_count}: {event['event_type']}")

            context_mgr.update(event)

            if event['event_type'] == 'face_detection':
                embedding = event['payload']['face_embedding']['vector']
                alias_id = tracker.match_or_create(embedding)
                event['resolved_alias'] = alias_id

            aggregator.add_event(event)

            if aggregator.should_trigger():
                window_events = aggregator.window
                context = context_mgr.get_context()

                llm_result = generator.generate(window_events, context)

                # Build semantic event
                first_event = window_events[0]
                last_event = window_events[-1]

                primary_alias = None
                primary_embedding = None
                for e in window_events:
                    if 'resolved_alias' in e:
                        primary_alias = e['resolved_alias']
                        if e['event_type'] == 'face_detection':
                            primary_embedding = e['payload']['face_embedding']['vector']
                        break

                semantic_event = {
                    'semantic_event_id': str(uuid.uuid4()),
                    'temp_alias_id': primary_alias,
                    'face_embedding': primary_embedding,
                    'voice_embedding': None,
                    'time': {
                        'start_ts': first_event['time']['start_ts'],
                        'end_ts': last_event['time']['end_ts']
                    },
                    'semantic_type': 'conversation_act',
                    'summary': llm_result['summary'],
                    'slots': {
                        'platform_hint': 'offline',
                        'ui_thread_hint': None,
                        'dialogue_act': llm_result['dialogue_act']
                    }
                }

                writer.write(semantic_event)
                semantic_count += 1
                aggregator.window = []
                aggregator.window_persons = set()

    print(f"\n完成！共处理 {event_count} 个A层事件, 生成 {semantic_count} 个B层事件")

if __name__ == '__main__':
    main()
