# tools/schema_tool.py

from sqlalchemy import inspect

from backend.database.connection import engine
from backend.models.table_model import Table


class SchemaTool:
    def inspect(self, tables: list[Table] | None = None, procedures: list[dict] | None = None) -> str:
        if tables or procedures:
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

            return "\n".join(parts)

        return self.inspect_db()

    def inspect_db(self) -> str:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if not tables:
            return "No tables found in the database."

        parts = ["Database tables:"]
        for table_name in tables:
            columns = inspector.get_columns(table_name)
            column_names = ", ".join([col["name"] for col in columns])
            parts.append(f"- {table_name}: {column_names}")

        return "\n".join(parts)
