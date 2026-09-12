class LogIndexer:
    def __init__(self):
        self.storage = []

    def add_log(self, log_id: str, message: str, level: str):
        log_entry = {
            "id": log_id,
            "message": message,
            "level": level
        }
        self.storage.append(log_entry)
        return log_entry

    def search(self, query: str):
        query_lower = query.lower()
        return [
            log for log in self.storage 
            if query_lower in log["message"].lower() or query_lower in log["level"].lower()
        ]

# Instantiate the shared object for imports
indexer = LogIndexer()
