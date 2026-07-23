# agents/supervisor.py

from backend.agents.sql_agent import SQLGenerator
from backend.services.summarizer import Summarizer
from backend.tools.schema_tool import SchemaTool
from backend.tools.sql_tool import SQLTool
from backend.tools.validator_tool import ValidatorTool


class Supervisor:
    def __init__(
        self,
        schema_tool: SchemaTool,
        sql_generator: SQLGenerator,
        validator: ValidatorTool,
        sql_executor: SQLTool,
        summarizer: Summarizer,
    ):
        self.schema_tool = schema_tool
        self.sql_generator = sql_generator
        self.validator = validator
        self.sql_executor = sql_executor
        self.summarizer = summarizer

    def run(self, user_request: str) -> dict:
        schema_summary = self.schema_tool.inspect()
        plan = self.sql_generator.interpret(user_request, schema_summary)
        action = plan.get("action", "answer")
        query = plan.get("query", user_request).strip()

        if action == "describe":
            tool_result = self.schema_tool.inspect()
        elif action == "execute":
            if not self.validator.validate(query):
                tool_result = {
                    "error": "SQL validation failed. Please provide a valid SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, or DROP statement."
                }
            else:
                tool_result = self.sql_executor.execute(query)
        elif action == "search":
            tool_result = self.sql_executor.search(query)
        else:
            answer = self.summarizer.llm.generate(
                f"Answer the following user request. Use the database schema only if it is relevant.\n\nSchema:\n{schema_summary}\n\nUser request:\n{user_request}"
            )
            tool_result = {"answer": answer}

        if action == "answer":
            natural_answer = tool_result.get("answer")
        else:
            natural_answer = self.summarizer.summarize(
                {
                    "request": user_request,
                    "action": action,
                    "query": query,
                    "tool_result": tool_result,
                    "schema_summary": schema_summary,
                }
            )

        return {
            "request": user_request,
            "action": action,
            "query": query,
            "tool_result": tool_result,
            "schema_summary": schema_summary,
            "natural_answer": natural_answer,
        }
