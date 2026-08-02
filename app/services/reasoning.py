from app.schemas.ask import AskResponse
from app.core.config import settings
from openai import OpenAI

SYSTEM_PROMPT = """
    You are QueryPilot, an AI business analytics copilot.
    You help users answer questions about retail sales, products,
    inventory, customers and business performance.

    If a question does not require business data,
    answer it using general knowledge.
    Keep answers concise.
    Don't invent data.
    """


class ReasoningService:

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    

    def answer_question(self, question: str) -> AskResponse:
        
        response = self.client.responses.create(            
            model=settings.openai_model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
        )
        
        return AskResponse(
            answer = response.output_text,
            requires_database = False
        )