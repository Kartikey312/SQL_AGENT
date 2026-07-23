# tools/schema_tool.py

from backend.models.table_model import Table


class SchemaTool:
    def inspect(self, tables: list[Table], procedures: list[dict]) -> str:
        parts = []
        if tables:
            parts.append("Tables:")
            for table in tables:
                columns = ", ".join([col.name for col in table.columns])
                parts.append(f"- {table.table_name}: {columns}")

        if procedures:
            parts.append("Procedures:")
            for proc in procedures:
                parts.append(f"- {proc.get('procedure_name')}: {proc.get('signature')}")

        return "\n".join(parts) if parts else "No schema loaded."
