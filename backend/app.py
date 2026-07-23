import sys
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, File, HTTPException, UploadFile

from backend.models.table_model import Table
from backend.parser.sp_parser import extract_procedures
from backend.parser.table_parser import extract_tables
from backend.agents.supervisor import Supervisor
from backend.agents.sql_agent import SQLGenerator
from backend.services.summarizer import Summarizer
from backend.tools.schema_tool import SchemaTool
from backend.tools.sql_tool import SQLTool
from backend.tools.validator_tool import ValidatorTool

UPLOAD_FOLDER = Path(__file__).resolve().parent / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="AI SQL Agent",
    version="1.0.0",
    description="ChatGPT for SQL Server"
)

parsed_tables: List[Table] = []
parsed_procedures: List[dict] = []

supervisor = Supervisor(
    schema_tool=SchemaTool(),
    sql_generator=SQLGenerator(),
    validator=ValidatorTool(),
    sql_executor=SQLTool(),
    summarizer=Summarizer(),
)


@app.get("/")
def home():
    return {"message": "AI SQL Agent is running 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload-schema")
async def upload_schema(schema: UploadFile = File(...)):
    if schema.content_type not in {"application/sql", "text/plain", "application/octet-stream"}:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    contents = await schema.read()
    try:
        sql_text = contents.decode("utf-8")
    except UnicodeDecodeError:
        sql_text = contents.decode("latin-1")

    saved_path = UPLOAD_FOLDER / schema.filename
    saved_path.write_text(sql_text, encoding="utf-8")

    tables = extract_tables(sql_text)
    procedures = extract_procedures(sql_text)

    parsed_tables.clear()
    parsed_tables.extend(tables)

    parsed_procedures.clear()
    parsed_procedures.extend(procedures)

    return {
        "filename": schema.filename,
        "tables": len(tables),
        "procedures": len(procedures),
        "saved_path": str(saved_path)
    }


@app.get("/tables")
def get_tables():
    return [table.model_dump() for table in parsed_tables]


@app.get("/procedures")
def get_procedures():
    return parsed_procedures


@app.get("/relationships")
def get_relationships():
    relationships = []
    for table in parsed_tables:
        for fk in table.foreign_keys:
            relationships.append(
                {
                    "table": table.table_name,
                    "column": fk.column,
                    "reference_table": fk.reference_table,
                    "reference_column": fk.reference_column,
                }
            )
    return relationships


@app.post("/chat")
def chat(request: dict):
    prompt = request.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    return supervisor.run(prompt, parsed_tables, parsed_procedures)
