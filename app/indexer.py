import re
from typing import Dict, List, Set

class LogIndexer:
    def __init__(self):
        self.logs: Dict[int, dict] = {}
        self.inverted_index: Dict[str, Set[int]] = {}
        self.counter = 0

    def _tokenize(self, text: str) -> Set[str]:
        return set(re.findall(r'\w+', text.lower()))

    def add_log(self, level: str, service: str, message: str) -> int:
        self.counter += 1
        log_id = self.counter
        
        log_data = {
            "id": log_id,
            "level": level.upper(),
            "service": service.lower(),
            "message": message
        }
        self.logs[log_id] = log_data

        tokens = self._tokenize(f"{level} {service} {message}")
        for token in tokens:
            if token not in self.inverted_index:
                self.inverted_index[token] = set()
            self.inverted_index[token].add(log_id)

        return log_id

    def search(self, query: str) -> List[dict]:
        tokens = self._tokenize(query)
        if not tokens:
            return []

        matching_ids = None
        for token in tokens:
            ids = self.inverted_index.get(token, set())
            if matching_ids is None:
                matching_ids = set(ids)
            else:
                matching_ids.intersection_update(ids)

        if not matching_ids:
            return []

        return [self.logs[log_id] for log_id in sorted(matching_ids, reverse=True)]

engine = LogIndexer()