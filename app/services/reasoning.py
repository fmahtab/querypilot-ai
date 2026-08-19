from app.schemas.ask import AskResponse
from app.core.config import settings
from openai import OpenAI

from app.services.rag.retrieval import retrieve_retailstar_docs

SYSTEM_PROMPT = """
    You are QueryPilot, an AI business analytics copilot.
    You help users answer questions about retail sales, products,
    inventory, customers and business performance.

    If a question does not require business data,
    answer it using general knowledge.
    Keep answers concise.
    Don't invent data.
    """

RAG_SYSTEM_PROMPT = """
    You are QueryPilot, an AI business analytics copilot.
    
    Answer the user's question using only the RetailStar context provided to you.
    Do not invent or infer information that is not supported by the provided context.
    If provided context doesn't contains enough information to answer the question, 
    say that the information is not available in the RetailStar knowledge base.
    Keep answers concise.
    """

CLASSIFIER_PROMPT = """
    You are a classifier.
    Classify the user's question into one of the following categories:
    - RetailStar internal database if it needs live/structured business data
    like RetailStar-specific policies, definitions, terminology, company information, procedures,
    or questions about concepts that are defined in RetailStar documentation,
    even if the user does not explicitly say "RetailStar".
    - RetailStar Knowledge Base if the answer should come from RetailStar documents
    like policies, definitions, company overview, terminology, procedures
    - General knowledge if it is not RetailStar-specific
    like general technical/business knowledge.
    Here are some example classification:
    "What is considered low inventory?" → KNOWLEDGE_BASE
    "What is BOPIS?" → KNOWLEDGE_BASE
    "Can I return opened acrylic paint?" → KNOWLEDGE_BASE
    "Can I return cut-to-order fabric?" → KNOWLEDGE_BASE
    "What is considered low inventory?" → KNOWLEDGE_BASE

    "What is FastAPI?" → GENERAL
    "What is cosine similarity?" → GENERAL
    Reply with ONLY one word:
    - DATABASE
    - KNOWLEDGE_BASE
    - GENERAL
    Do not explain your answer.
    """

    


class ReasoningService:

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def _classify_question(self, question: str) -> str:
        
        response = self.client.responses.create(
            model = settings.openai_model,
            input = [
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": question}
            ]
        )

        return response.output_text.strip().upper()


    def answer_question(self, question: str) -> AskResponse:
        question_type = self._classify_question(question)

        if question_type == "DATABASE":
            return AskResponse(
                answer = "This question requires RetailStar business data. Database querying has not been implemented yet.",
                requires_database = True
            )

        if question_type == "KNOWLEDGE_BASE":
            top_k = 3
            result = retrieve_retailstar_docs(
                question,
                top_k=top_k,
                db=None,
            )

            context = "\n\n---\n\n".join(
                [chunk.content for chunk in result.chunks]
                )
            
         
            rag_input = f"""
            context:
            {context}
            
            question:
            {question}
            """
            
            response = self.client.responses.create(            
                model=settings.openai_model,
                input=[
                    {"role": "system", "content": RAG_SYSTEM_PROMPT},
                    {"role": "user", "content": rag_input}
                ],
            )
        
            return AskResponse(
                answer = response.output_text,
                requires_database = False
            )

        if question_type == "GENERAL":
        
            
         
        
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