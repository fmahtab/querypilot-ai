from typing import Literal

from pydantic import BaseModel


class ExtractedMemory(BaseModel):
    memory_key: Literal[
        "role",
        "experience_level",
    ]
    memory_value: str


class MemoryExtractionResult(BaseModel):
    memories: list[ExtractedMemory]