from fastapi import FastAPI
from app.api.health import health_router
from app.api.ask import router
from app.api.evals import evals_router


app = FastAPI(
    title="QueryPilot AI",
    description="An AI-powered business analytics platform.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(router)
app.include_router(evals_router)

@app.get("/")
def read_root() -> dict[str,str]:
    return {
        "message": "Welcome to QueryPilot AI"
    }

