from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.user_memory import UserMemory

from app.services.memory_extractor import MemoryExtractor

def get_user_memories(
    user_id: str,
    db: Session | None = None
) -> list[UserMemory]:

    owns_session = db is None
    session = db or SessionLocal()

    try:
        statement = select(UserMemory).where(
            UserMemory.user_id == user_id
        )
        memories = session.scalars(statement).all()
        return list(memories)

    finally:
        if owns_session:
            session.close()

def save_user_memory(
    user_id: str,
    memory_key: str,
    memory_value: str,
    db: Session | None = None
) -> UserMemory:

    owns_session = db is None
    session = db or SessionLocal()

    try:
        statement = select(UserMemory).where(
            UserMemory.user_id == user_id,
            UserMemory.memory_key == memory_key,
        )

        memory = session.scalar(statement)

        if memory:
            memory.memory_value = memory_value
        else:
            memory = UserMemory(
                user_id=user_id,
                memory_key=memory_key,
                memory_value=memory_value,
            )
            session.add(memory)

        session.commit()
        session.refresh(memory)

        return memory

    finally:
        if owns_session:
            session.close()
    

def process_user_memory(
    user_id: str,
    message: str,
    db: Session | None = None,
) -> list[UserMemory]:

    extractor = MemoryExtractor()
    result = extractor.extract(message)

    saved_memories = []

    for extracted_memory in result.memories:
        memory = save_user_memory(
            user_id=user_id,
            memory_key=extracted_memory.memory_key,
            memory_value=extracted_memory.memory_value,
            db=db,
        )

        saved_memories.append(memory)

    return saved_memories


def get_user_memory_context(
    user_id: str,
    db: Session | None = None,
) -> str:

    memories = get_user_memories(
        user_id=user_id,
        db=db,
    )

    if not memories:
        return ""

    return "\n".join(
        f"{memory.memory_key}: {memory.memory_value}"
        for memory in memories
    )