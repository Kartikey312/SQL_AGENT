# services/summarizer.py

from backend.services.llm import LLMService


class Summarizer:
    def __init__(self):
        self.llm = LLMService()

    def summarize(self, text: str) -> str:
        prompt = (
            "Summarize the following database search result into a concise, readable answer:\n\n"
            f"{text}"
        )
        return self.llm.generate(prompt)
