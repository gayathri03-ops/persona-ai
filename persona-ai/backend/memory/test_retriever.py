from .database import initialize_database
from .memory_retriever import retrieve_memories


initialize_database()


user_id = "gayathri"


print("\nRetrieving memories...\n")


memories = retrieve_memories(
    user_id=user_id,
    limit=5
)


if not memories:

    print("No memories found.")

else:

    for memory in memories:

        print(
            f"- {memory['memory']}"
        )