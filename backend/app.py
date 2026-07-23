from fastapi import FastAPI

app = FastAPI(
    title="AI SQL Agent",
    version="1.0.0",
    description="ChatGPT for SQL Server"
)


@app.get("/")
def home():
    return {
        "message": "AI SQL Agent is running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
