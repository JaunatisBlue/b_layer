import json
from typing import Dict

class EventWriter:
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.file = None

    def __enter__(self):
        self.file = open(self.output_path, 'a', encoding='utf-8')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def write(self, semantic_event: Dict):
        self.file.write(json.dumps(semantic_event, ensure_ascii=False) + '\n')
        self.file.flush()
