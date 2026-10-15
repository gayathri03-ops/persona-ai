from .memory_manager import (
    start_memory_system,
    remember,
    get_user_memory
)


start_memory_system()


user_id = "gayathri"


remember(
    user_id,
    "User is learning AI/ML.",
    memory_type="education",
    importance=3
)


remember(
    user_id,
    "User is an ECE student.",
    memory_type="education",
    importance=3
)


remember(
    user_id,
    "User is learning Python.",
    memory_type="skill",
    importance=2
)


memories = get_user_memory(user_id)


print("\nNani's memories:\n")

for memory in memories:

    print(
        f"- {memory['memory']} "
        f"[{memory['type']}]"
    )