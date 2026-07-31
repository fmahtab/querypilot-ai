from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length = 3,
        max_length = 255, 
        description= "Business question to answer using retail sales data.",
        examples=["Which products generated the highest revenue last quarter?",
        "Which stores have low inventory?"]
    )

class AskResponse(BaseModel):
        answer: str
        requires_database: bool
