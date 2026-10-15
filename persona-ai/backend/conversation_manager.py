from backend.llm_client import ask_nani
from backend.memory.memory_retriever import retrieve_memories
from backend.memory.memory_extractor import process_memory


USER_ID = "gayathri"


def build_memory_context(user_id):

    memories = retrieve_memories(
        user_id=user_id,
        limit=5
    )

    if not memories:
        return ""

    memory_lines = []

    for item in memories:
        memory_lines.append(
            f"- {item['memory']}"
        )

    return "\n".join(memory_lines)


def chat(user_message):

    memory_context = build_memory_context(
        USER_ID
    )

    if memory_context:

        enhanced_message = f"""
Here are some things you remember about the user:

{memory_context}

Use these memories naturally when relevant.
Do not mention that you have a memory database.
Do not list the memories unless the user asks.

Current user message:

{user_message}
"""

    else:

        enhanced_message = user_message

    reply = ask_nani(
        enhanced_message
    )

    process_memory(
        user_id=USER_ID,
        user_message=user_message
    )

    return reply


if __name__ == "__main__":

    print(
        "\nNani AI started! Type 'exit' to stop.\n"
    )

    while True:

        user_message = input(
            "You: "
        )

        if user_message.lower() == "exit":

            print(
                "\nNani: okay da deii 😂"
            )

            break

        try:

            reply = chat(
                user_message
            )

            print(
                f"\nNani: {reply}\n"
            )

        except Exception as error:

            print(
                f"\nError: {error}\n"
            )