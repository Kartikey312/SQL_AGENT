import sys
from pathlib import Path

from pydantic import BaseModel
from sqlalchemy import text

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, Response

from backend.agents.supervisor import Supervisor
from backend.agents.sql_agent import SQLGenerator
from backend.services.summarizer import Summarizer
from backend.tools.schema_tool import SchemaTool
from backend.tools.sql_tool import SQLTool
from backend.tools.validator_tool import ValidatorTool
from backend.database.connection import engine

app = FastAPI(
    title="AI SQL Agent",
    version="1.0.0",
    description="A database-aware chatbot backend with LLM-enhanced responses."
)

supervisor = Supervisor(
    schema_tool=SchemaTool(),
    sql_generator=SQLGenerator(),
    validator=ValidatorTool(),
    sql_executor=SQLTool(),
    summarizer=Summarizer(),
)


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {
        "message": "AI SQL Agent is running.",
        "endpoints": ["/health", "/chat"],
        "usage": "POST /chat with JSON body {\"prompt\": \"your question\"}"
    }
 
@app.get("/health")
def health(response: Response):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "db": "connected"}
    except Exception as exc:
        response.status_code = 503
        return {"status": "unhealthy", "db_error": str(exc)}


@app.post("/chat")
def chat(request: ChatRequest):
    return supervisor.run(request.prompt)
