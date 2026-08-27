from fastapi import APIRouter

from app.schemas.ask import AskRequest, AskResponse
from app.services.reasoning import ReasoningService

router = APIRouter()

service = ReasoningService()

@router.post("/ask", response_model=AskResponse)
def ask_question(ask_request: AskRequest) -> AskResponse:
    return service.answer_question(
        ask_request.question,
        history=[
            message.model_dump()
            for message in ask_request.history
        ],
    )
    return service.answer_question(ask_request.question)
