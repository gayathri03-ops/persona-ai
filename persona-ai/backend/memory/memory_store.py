from .database import get_connection


def save_memory(
    user_id,
    memory,
    memory_type="general",
    importance=1
):

    connection = get_connection()

    cursor = connection.cursor()


    # Check whether the same memory already exists
    cursor.execute(
        """
        SELECT id
        FROM memories
        WHERE user_id = ?
        AND LOWER(memory) = LOWER(?)
        """,
        (
            user_id,
            memory
        )
    )


    existing = cursor.fetchone()


    # Duplicate found
    if existing:

        connection.close()

        return False


    # Save new memory
    cursor.execute(
        """
        INSERT INTO memories
        (
            user_id,
            memory,
            memory_type,
            importance
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            memory,
            memory_type,
            importance
        )
    )


    connection.commit()

    connection.close()

    return True


def get_memories(user_id):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM memories
        WHERE user_id = ?
        ORDER BY importance DESC, created_at DESC
        """,
        (user_id,)
    )


    rows = cursor.fetchall()

    connection.close()

    return rows


def search_memories(
    user_id,
    keyword
):

    connection = get_connection()

    cursor = connection.cursor()


    keyword = f"%{keyword}%"


    cursor.execute(
        """
        SELECT *
        FROM memories
        WHERE user_id = ?
        AND memory LIKE ?
        ORDER BY importance DESC, created_at DESC
        """,
        (
            user_id,
            keyword
        )
    )


    rows = cursor.fetchall()

    connection.close()

    return rows


def delete_memory(memory_id):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM memories
        WHERE id = ?
        """,
        (memory_id,)
    )


    connection.commit()

    connection.close()