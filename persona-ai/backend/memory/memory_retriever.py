from .memory_manager import get_user_memory


def retrieve_memories(user_id, limit=5):
    """
    Retrieve the most important memories
    stored for the user.
    """

    memories = get_user_memory(user_id)

    # Keep only the top `limit` memories
    memories = memories[:limit]

    return memories


def format_memories_for_prompt(memories):
    """
    Convert memory dictionaries into text
    that can be given to the LLM.
    """

    if not memories:
        return ""

    lines = []

    for item in memories:

        lines.append(
            f"- {item['memory']}"
        )

    return "\n".join(lines)