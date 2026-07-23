# tools/sql_tool.py

import re
from sqlalchemy import inspect, text

from backend.database.connection import engine


class SQLTool:
    def execute(self, sql: str):
        with engine.connect() as conn:
            try:
                result = conn.execute(text(sql))
                if result.returns_rows:
                    rows = [dict(row._mapping) for row in result]
                    return {"rows": rows}
                conn.commit()
                return {"rowcount": result.rowcount}
            except Exception as exc:
                return {"error": str(exc)}

    def search(self, prompt: str, limit: int = 50):
        terms = [term for term in re.findall(r"\w+", prompt) if len(term) > 2]
        if not terms:
            return {"error": "No searchable terms found in prompt."}

        inspector = inspect(engine)
        matches = []

        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            searchable_columns = [
                column["name"]
                for column in columns
                if any(
                    kind in str(column["type"]).upper()
                    for kind in ("CHAR", "TEXT", "VARCHAR", "NVARCHAR")
                )
            ]

            if not searchable_columns:
                continue

            conditions = []
            params = {}
            param_index = 0
            for column_name in searchable_columns:
                for term in terms:
                    key = f"p{param_index}"
                    conditions.append(f"{column_name} LIKE :{key}")
                    params[key] = f"%{term}%"
                    param_index += 1

            query = f"SELECT * FROM {table_name} WHERE {' OR '.join(conditions)}"

            try:
                with engine.connect() as conn:
                    result = conn.execute(text(query), params)
                    rows = [dict(row._mapping) for row in result.fetchmany(limit)]
                    if rows:
                        matches.append({"table": table_name, "rows": rows})
            except Exception:
                continue

        return {"matches": matches}
