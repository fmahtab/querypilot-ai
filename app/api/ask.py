from fastapi import APIRouter

from app.schemas.ask import AskRequest, AskResponse
from app.services.reasoning import ReasoningService
from app.services.memory import get_user_memory_context, process_user_memory

router = APIRouter()

service = ReasoningService()

@router.post("/ask", response_model=AskResponse)
def ask_question(ask_request: AskRequest) -> AskResponse:
    user_id = "demo-user"

    process_user_memory(
        user_id=user_id,
        message=ask_request.question,
    )

    memory_context = get_user_memory_context(user_id)
    print(memory_context)
    return service.answer_question(
        ask_request.question,
        history=[
            message.model_dump()
            for message in ask_request.history
        ],
        memory_context=memory_context,
    )
