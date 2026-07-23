# agents/sql_agent.py

import re


class SQLGenerator:
    def __init__(self):
        pass

    def generate(self, prompt: str, schema_summary: str) -> str:
        terms = [term for term in re.findall(r"\w+", prompt) if len(term) > 2]
        return (
            f"SEARCH DATABASE FOR: {' '.join(terms)}\n"
            f"Schema summary:\n{schema_summary}"
        )
