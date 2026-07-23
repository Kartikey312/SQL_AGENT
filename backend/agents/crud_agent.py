# agents/crud_agent.py

class CRUDAgent:
    def __init__(self):
        self.entities = {}

    def create(self, name: str, data: dict) -> dict:
        self.entities[name] = data
        return data
