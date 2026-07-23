# agents/sql_agent.py

from backend.services.llm import LLMService


class SQLGenerator:
    def __init__(self, llm_service: LLMService | None = None):
        self.llm = llm_service or LLMService()

    def generate(self, prompt: str, schema_summary: str) -> str:
        generation_prompt = (
            f"Generate a SQL statement for the following request:\n\n{prompt}\n\n"
            f"Use this schema information:\n{schema_summary}"
        )
        return self.llm.generate(generation_prompt)
