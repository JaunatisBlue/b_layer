import json
from typing import Dict

class EventReader:
    def __init__(self, input_path: str):
        self.input_path = input_path
        self.file = None

    def __enter__(self):
        self.file = open(self.input_path, 'r', encoding='utf-8')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def read_next(self) -> Dict:
        while True:
            line = self.file.readline()
            if not line:
                return None
            try:
                return json.loads(line.strip())
            except json.JSONDecodeError:
                print(f"警告: 跳过格式错误的行")
                continue
