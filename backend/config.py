import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    db_server = os.getenv("DB_SERVER")
    db_database = os.getenv("DB_DATABASE")
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

    if db_server and db_database and db_username and db_password:
        driver = db_driver.replace(" ", "+")
        DATABASE_URL = (
            f"mssql+pyodbc://{db_username}:{db_password}@{db_server}/{db_database}"
            f"?driver={driver}"
        )

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./test.db"
