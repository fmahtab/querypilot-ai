from fastapi import APIRouter

health_router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@health_router.get("")
def health_check() -> dict[str,str]:
    return {"status": "healthy"}