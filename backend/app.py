import sys
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, File, HTTPException, UploadFile

from backend.agents.supervisor import Supervisor
from backend.agents.sql_agent import SQLGenerator
from backend.services.summarizer import Summarizer
from backend.tools.schema_tool import SchemaTool
from backend.tools.sql_tool import SQLTool
from backend.tools.validator_tool import ValidatorTool

app = FastAPI(
    title="AI SQL Agent",
    version="1.0.0",
    description="ChatGPT for SQL Server"
)

supervisor = Supervisor(
    schema_tool=SchemaTool(),
    sql_generator=SQLGenerator(),
    validator=ValidatorTool(),
    sql_executor=SQLTool(),
    summarizer=Summarizer(),
)

@app.post("/chat")
def chat(request: dict):
    prompt = request.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    return supervisor.run(prompt)
