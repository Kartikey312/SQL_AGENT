# agents/sql_agent.py

class SQLAgent:
    def __init__(self):
        self.name = "sql_agent"

    def run(self, query: str) -> str:
        return f"Executing SQL: {query}"
