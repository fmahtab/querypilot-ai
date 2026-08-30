from app.services.memory_extractor import MemoryExtractor

extractor = MemoryExtractor()

result = extractor.extract(
    "I'm a new inventory manager at RetailStar."
)

print(result)