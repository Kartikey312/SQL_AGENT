from urllib.parse import quote_plus
from sqlalchemy import create_engine
import os

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_DATABASE')};"
    f"UID={os.getenv('DB_USERNAME')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "TrustServerCertificate=yes;"
)

DATABASE_URL = (
    "mssql+pyodbc:///?odbc_connect=" + quote_plus(connection_string)
)

engine = create_engine(DATABASE_URL)