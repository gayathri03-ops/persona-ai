from .database import initialize_database

from .memory_store import (
    save_memory,
    get_memories,
    search_memories
)


def start_memory_system():

    initialize_database()


def remember(
    user_id,
    memory,
    memory_type="general",
    importance=1
):

    return save_memory(
        user_id=user_id,
        memory=memory,
        memory_type=memory_type,
        importance=importance
    )


def get_user_memory(user_id):

    memories = get_memories(user_id)


    return [
        {
            "id": row["id"],
            "memory": row["memory"],
            "type": row["memory_type"],
            "importance": row["importance"],
            "created_at": row["created_at"]
        }

        for row in memories
    ]


def find_memory(
    user_id,
    keyword
):

    memories = search_memories(
        user_id,
        keyword
    )


    return [
        {
            "id": row["id"],
            "memory": row["memory"],
            "type": row["memory_type"],
            "importance": row["importance"]
        }

        for row in memories
    ]