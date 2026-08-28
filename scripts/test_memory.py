from app.services.memory import (
    get_user_memories,
    save_user_memory
)

save_user_memory(
    user_id="demo-user",
    memory_key="role",
    memory_value="inventory_manager",
)

memories = get_user_memories("demo-user")

print(f"Found {len(memories)} memories")

for memory in memories:
    print(
        memory.memory_key,
        "=",
        memory.memory_value,
    )

