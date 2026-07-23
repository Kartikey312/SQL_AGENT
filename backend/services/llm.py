# services/llm.py

import os

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class LLMService:
    def __init__(self, model: str = "gemini-1.0"):
        self.model = model
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and genai is not None:
            genai.configure(api_key=api_key)
            self.enabled = True
        else:
            self.enabled = False

    def generate(self, prompt: str) -> str:
        if not self.enabled:
            return (
                "LLM not configured. Set GOOGLE_API_KEY in .env to enable better responses.\n\n"
                f"Prompt:\n{prompt}"
            )

        try:
            response = genai.generate_text(model=self.model, text=prompt)
            if hasattr(response, "text"):
                return response.text
            if isinstance(response, dict):
                return response.get("output", str(response))
            return str(response)
        except Exception as exc:
            return f"LLM generation failed: {exc}\nPrompt:\n{prompt}"
