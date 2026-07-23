from urllib.parse import quote_plus
from sqlalchemy import create_engine
import os

DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_INSTANCE = os.getenv("DB_INSTANCE")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if DB_INSTANCE and DB_PORT:
    server_value = f"tcp:{DB_SERVER}\\{DB_INSTANCE},{DB_PORT}"
elif DB_INSTANCE:
    server_value = f"tcp:{DB_SERVER}\\{DB_INSTANCE}"
elif DB_PORT:
    server_value = f"tcp:{DB_SERVER},{DB_PORT}"
else:
    server_value = DB_SERVER

connection_string = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={server_value};"
    f"DATABASE={DB_DATABASE};"
    f"UID={DB_USERNAME};"
    f"PWD={DB_PASSWORD};"
    "TrustServerCertificate=yes;"
)

DATABASE_URL = (
    "mssql+pyodbc:///?odbc_connect=" + quote_plus(connection_string)
)

engine = create_engine(DATABASE_URL)
