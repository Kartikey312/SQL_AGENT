# services/summarizer.py

from backend.services.llm import LLMService


class Summarizer:
    def __init__(self):
        self.llm = LLMService()

    def summarize(self, payload: dict) -> str:
        prompt = (
            "You are an AI assistant. Summarize the following result into a concise, user-friendly answer:\n\n"
            f"User request: {payload.get('request')}\n"
            f"Action: {payload.get('action')}\n"
            f"Query: {payload.get('query')}\n"
            f"Schema summary: {payload.get('schema_summary')}\n"
            f"Result: {payload.get('tool_result')}\n"
        )

        if not self.llm.enabled:
            result = payload.get("tool_result")
            return (
                f"LLM is not configured. Here is the raw response for your request:\n\n"
                f"Request: {payload.get('request')}\n"
                f"Action: {payload.get('action')}\n"
                f"Query: {payload.get('query')}\n"
                f"Result: {result}"
            )

        return self.llm.generate(prompt)
