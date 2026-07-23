# agents/history_agent.py

class HistoryAgent:
    def __init__(self):
        self.history = []

    def add_entry(self, entry: str) -> None:
        self.history.append(entry)
