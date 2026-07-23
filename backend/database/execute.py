# database/execute.py

from backend.database.connection import SessionLocal


def execute_query(sql: str) -> list:
    """Execute a raw SQL query and return the result rows."""
    with SessionLocal() as session:
        result = session.execute(sql)
        return result.fetchall()
