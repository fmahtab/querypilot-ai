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
    - RetailStar internal database if the question requires structured or changing business data related to RetailStar such as
        - sales amount
        - inventory levels
        - customer records
        - employee records
        - store performance
        - product data
        - financial metrics
        - order count
    
    - Choose KNOWLEDGE_BASE for relatively static company facts or documented business rules, even if the user does not explicitly mention RetailStar such as
        - policies
        - definitions
        - company history
        - company overview
        - founding information
        - terminology
        - procedures
    - General knowledge if it is not RetailStar-specific
    like general technical/business knowledge.
    Here are some example classification:
    "What is BOPIS?" → KNOWLEDGE_BASE
    "Can I return opened acrylic paint?" → KNOWLEDGE_BASE
    "Can I return cut-to-order fabric?" → KNOWLEDGE_BASE
    "What is considered low inventory?" → KNOWLEDGE_BASE

    "What is FastAPI?" → GENERAL
    "What is cosine similarity?" → GENERAL

    "Which store had the highest sales last month?" → DATABASE
    "Which products are currently out of stock?" → DATABASE

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
            sources_set = {
                chunk.source_file for chunk in result.chunks
            }
            sources = list(sources_set)
         
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
                requires_database = False,
                sources = sources
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