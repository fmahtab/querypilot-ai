from openai import OpenAI

from app.core.config import settings
from app.schemas.memory import MemoryExtractionResult


MEMORY_EXTRACTION_PROMPT = """
You identify stable user information that is useful to remember
across future QueryPilot sessions.

Only extract these memory types:
- role: the user's ongoing job role
- experience_level: the user's ongoing experience level

Rules:
- Only extract information the user states about themselves.
- Only extract information likely to remain useful in future sessions.
- Do not store ordinary questions.
- Do not store RetailStar policies, definitions, or business facts.
- Do not infer facts that the user did not clearly state.
- If there is nothing worth remembering, return an empty memories list.
"""

class MemoryExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def extract(self, message: str) -> MemoryExtractionResult:

        response = self.client.responses.parse(
            model=settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": MEMORY_EXTRACTION_PROMPT,
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            text_format=MemoryExtractionResult,
        )

        return response.output_parsed