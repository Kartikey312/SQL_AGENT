# agents/sql_agent.py

import json
import re

from backend.services.llm import LLMService


class SQLGenerator:
    def __init__(self, llm_service: LLMService | None = None):
        self.llm = llm_service or LLMService()

    def interpret(self, prompt: str, schema_summary: str) -> dict:
        plan_prompt = (
            "You are an AI assistant that decides whether a user request should be answered with a database action or a direct response. "
            "The available actions are:\n"
            "- search: look for matching records across text columns\n"
            "- execute: run a SQL command directly\n"
            "- describe: return database schema details\n"
            "- answer: answer the user request directly with natural language\n"
            "Return only valid JSON with keys: action, query. "
            "Use describe for schema questions, execute for explicit SQL commands, search for data lookups, and answer for general questions or conversational requests. "
            f"Schema summary:\n{schema_summary}\n"
            f"User request:\n{prompt}\n"
        )

        raw_output = self.llm.generate(plan_prompt)
        plan = self._parse_plan(raw_output)
        if plan:
            return plan

        action = self._guess_action(prompt)
        return {
            "action": action,
            "query": prompt,
        }

    def _parse_plan(self, text: str) -> dict | None:
        try:
            json_start = text.index("{")
            json_text = text[json_start:]
            plan = json.loads(json_text)
            if "action" in plan and "query" in plan:
                return plan
        except Exception:
            return None
        return None

    def _guess_action(self, prompt: str) -> str:
        lower = prompt.lower()
        if any(keyword in lower for keyword in ["schema", "table", "columns", "describe", "structure", "schema details"]):
            return "describe"
        if prompt.strip().lower().startswith(("select", "insert", "update", "delete", "create", "alter", "drop", "truncate", "merge")):
            return "execute"
        if any(keyword in lower for keyword in ["find", "search", "show", "list", "where", "count", "matching", "records", "rows"]):
            return "search"
        return "answer"
