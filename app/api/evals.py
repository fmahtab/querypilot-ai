from fastapi import APIRouter

from app.services.evals.runner import run_evals


evals_router = APIRouter()


@evals_router.post("/evals")
def run_evaluation_suite():
    return run_evals()