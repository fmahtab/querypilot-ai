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
CLASSIFIER_PROMPT = """
    You are a classifier.
    Determine whether the user's question requires RetailStar internal database.
    Reply with ONLY one word:
    YES
    or
    NO
    Do not explain your answer.
    """


class ReasoningService:

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def _requires_database(self, question: str) -> bool:
        
        response = self.client.responses.create(
            model = settings.openai_model,
            input = [
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": question}
            ]
        )

        return response.output_text.strip().upper() == "YES"


    def answer_question(self, question: str) -> AskResponse:
        requires_database = self._requires_database(question)


        if requires_database:
            return AskResponse(
                answer = "This question requires RetailStar business data. Database querying has not been implemented yet.",
                requires_database = True
            )

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