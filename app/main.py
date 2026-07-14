from fastapi import FastAPI
from app.api.health import health_router



app = FastAPI(
    title="QueryPilot AI",
    description="An AI-powered business analytics platform.",
    version="0.1.0",
)

app.include_router(health_router)

@app.get("/")
def read_root() -> dict[str,str]:
    return {
        "message": "Welcome to QueryPilot AI"
    }