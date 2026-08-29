from app.services.memory_extractor import MemoryExtractor


extractor = MemoryExtractor()

test_messages = [
    "I'm a new inventory manager at RetailStar.",
    "I work as a store manager.",
    "I have several years of experience in inventory management.",
    "What is BOPIS?",
    "What is considered low inventory?",
]


for message in test_messages:
    result = extractor.extract(message)

    print(f"\nMessage: {message}")

    if result.memories:
        for memory in result.memories:
            print(
                f"  {memory.memory_key} = {memory.memory_value}"
            )
    else:
        print("  No memory extracted")
        