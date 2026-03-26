import json
import numpy as np
from typing import Dict, List, Optional

class IdentityTracker:
    def __init__(self, db_path: str, threshold: float = 0.75):
        self.db_path = db_path
        self.threshold = threshold
        self.persons: Dict[str, Dict] = {}
        self.next_alias_id = 0

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def match_or_create(self, embedding: List[float]) -> str:
        embedding_array = np.array(embedding)

        best_match = None
        best_score = 0.0

        for alias_id, person in self.persons.items():
            score = self._cosine_similarity(embedding_array, person['face_embedding_mean'])
            if score > best_score:
                best_score = score
                best_match = alias_id

        if best_score > self.threshold:
            # Update existing person
            person = self.persons[best_match]
            count = person['face_embedding_count']
            person['face_embedding_mean'] = (person['face_embedding_mean'] * count + embedding_array) / (count + 1)
            person['face_embedding_count'] = count + 1
            return best_match
        else:
            # Create new person
            alias_id = f"alias_{chr(65 + self.next_alias_id)}"
            self.next_alias_id += 1
            self.persons[alias_id] = {
                'face_embedding_mean': embedding_array,
                'face_embedding_count': 1,
                'voice_embedding_mean': None,
                'voice_embedding_count': 0
            }
            return alias_id
