from app.services.reasoning import ReasoningService


def main():
    service = ReasoningService()

    history = [
        {
            "role": "user",
            "content": "What is considered low inventory?",
        },
        {
            "role": "assistant",
            "content": (
                "Low inventory is when the on-hand quantity is below "
                "the minimum threshold but above zero."
            ),
        },
    ]

    question = "What happens when a SKU hits that status?"

    result = service._contextualize_question(
        question,
        history,
    )

    print("Original question:")
    print(question)

    print("\nContextualized question:")
    print(result)

if __name__ == "__main__":
    main()