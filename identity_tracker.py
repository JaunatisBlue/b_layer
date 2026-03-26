import json
import numpy as np
from typing import Dict, List, Optional

class IdentityTracker:
    def __init__(self, db_path: str, threshold: float = 0.75):
        self.db_path = db_path
        self.face_threshold = threshold
        self.voice_threshold = 0.70
        self.persons: Dict[str, Dict] = {}
        self.next_alias_id = 0

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def match_or_create(self, embedding: List[float], modality: str) -> str:
        embedding_array = np.array(embedding)
        best_match = None
        best_score = 0.0
        threshold = self.face_threshold if modality == 'face' else self.voice_threshold

        for alias_id, person in self.persons.items():
            if modality == 'face' and person['face_embedding_mean'] is not None:
                score = self._cosine_similarity(embedding_array, person['face_embedding_mean'])
            elif modality == 'voice' and person['voice_embedding_mean'] is not None:
                score = self._cosine_similarity(embedding_array, person['voice_embedding_mean'])
            else:
                continue

            if score > best_score:
                best_score = score
                best_match = alias_id

        if best_score > threshold:
            self._update_person(best_match, embedding_array, modality)
            return best_match
        else:
            return self._create_person(embedding_array, modality)

    def _update_person(self, alias_id: str, embedding: np.ndarray, modality: str):
        person = self.persons[alias_id]
        if modality == 'face':
            count = person['face_embedding_count']
            if person['face_embedding_mean'] is not None:
                person['face_embedding_mean'] = (person['face_embedding_mean'] * count + embedding) / (count + 1)
            else:
                person['face_embedding_mean'] = embedding
            person['face_embedding_count'] = count + 1
        else:
            count = person['voice_embedding_count']
            if person['voice_embedding_mean'] is not None:
                person['voice_embedding_mean'] = (person['voice_embedding_mean'] * count + embedding) / (count + 1)
            else:
                person['voice_embedding_mean'] = embedding
            person['voice_embedding_count'] = count + 1

    def _create_person(self, embedding: np.ndarray, modality: str) -> str:
        alias_id = f"alias_{chr(65 + self.next_alias_id)}"
        self.next_alias_id += 1
        self.persons[alias_id] = {
            'face_embedding_mean': embedding if modality == 'face' else None,
            'face_embedding_count': 1 if modality == 'face' else 0,
            'voice_embedding_mean': embedding if modality == 'voice' else None,
            'voice_embedding_count': 1 if modality == 'voice' else 0
        }
        return alias_id
