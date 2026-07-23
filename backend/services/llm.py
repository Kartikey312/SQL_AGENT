# services/llm.py

import os

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import openai
except ImportError:
    openai = None


class LLMService:
    def __init__(self, model: str | None = None):
        self.google_model = model or os.getenv("GOOGLE_MODEL", "gemini-1.0")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        self.google_enabled = False
        self.openai_enabled = False

        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key and genai is not None:
            genai.configure(api_key=google_key)
            self.google_enabled = True

        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai is not None:
            openai.api_key = openai_key
            self.openai_enabled = True

        self.enabled = self.google_enabled or self.openai_enabled

    def generate(self, prompt: str) -> str:
        if self.google_enabled:
            try:
                response = genai.generate_text(model=self.google_model, prompt=prompt)
                if hasattr(response, "text"):
                    return response.text
                if isinstance(response, dict):
                    return response.get("output", str(response))
                return str(response)
            except Exception as exc:
                return f"LLM generation failed with Google Gemini: {exc}\nPrompt:\n{prompt}"

        if self.openai_enabled:
            try:
                completion = openai.ChatCompletion.create(
                    model=self.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=750,
                )
                if completion.choices:
                    return completion.choices[0].message.get("content", "")
                return str(completion)
            except Exception as exc:
                return f"LLM generation failed with OpenAI: {exc}\nPrompt:\n{prompt}"

        return (
            "LLM not configured. Set GOOGLE_API_KEY or OPENAI_API_KEY in .env to enable better responses.\n\n"
            f"Prompt:\n{prompt}"
        )
