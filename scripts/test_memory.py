from app.services.memory import (
    get_user_memories,
    process_user_memory,
)

user_id = "memory-test-user"

message = "What is BOPIS."

saved_memories = process_user_memory(
    user_id=user_id,
    message=message,
)

print("\nSaved memories:")

for memory in saved_memories:
    print(memory.memory_key, "=", memory.memory_value)


print("\nMemories from PostgreSQL:")

memories = get_user_memories(user_id)

for memory in memories:
    print(memory.memory_key, "=", memory.memory_value)
