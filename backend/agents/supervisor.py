# agents/supervisor.py

class Supervisor:
    def __init__(self):
        self.agents = []

    def register(self, agent) -> None:
        self.agents.append(agent)
