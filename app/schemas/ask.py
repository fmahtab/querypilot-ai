from pydantic import BaseModel, Field

class ConversationMessage(BaseModel):
    role: str
    content: str
    
class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length = 3,
        max_length = 255, 
        description= "Business question to answer using retail sales data.",
        examples=["Which products generated the highest revenue last quarter?",
        "Which stores have low inventory?"]
    )
    history: list[ConversationMessage] = Field(default_factory=list)

class AskResponse(BaseModel):
        answer: str
        requires_database: bool
        sources: list[str] = Field(default_factory=list)
