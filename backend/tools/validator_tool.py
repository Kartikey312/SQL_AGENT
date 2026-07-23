# tools/validator_tool.py

class ValidatorTool:
    def validate(self, sql: str) -> bool:
        normalized = sql.strip()
        return bool(normalized) and normalized.lower().startswith(("select", "insert", "update", "delete", "create", "alter", "drop"))
