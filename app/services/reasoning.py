from app.schemas.ask import AskResponse

class ReasoningService:

    def answer_question(self, question: str)->AskResponse:
        return AskResponse(
            answer = "This is a test response",
            requires_database = False
        )