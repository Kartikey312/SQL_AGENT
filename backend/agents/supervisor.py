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
        generated_sql = self.sql_generator.generate(user_request, schema_summary)
        is_valid = self.validator.validate(generated_sql)
        execution_result = (
            self.sql_executor.search(user_request)
            if is_valid
            else {"error": "SQL validation failed."}
        )

        natural_answer = self.summarizer.summarize(
            f"User request: {user_request}\n"
            f"Generated SQL: {generated_sql}\n"
            f"Validation: {is_valid}\n"
            f"Execution result: {execution_result}"
        )

        return {
            "request": user_request,
            "schema_summary": schema_summary,
            "generated_sql": generated_sql,
            "is_valid": is_valid,
            "execution_result": execution_result,
            "natural_answer": natural_answer,
        }
