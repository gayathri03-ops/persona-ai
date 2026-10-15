from .database import initialize_database

from .memory_extractor import process_memory


# ============================================================
# START
# ============================================================

print(
    "\nStarting memory extractor test...\n"
)


# Create database/table
initialize_database()


# User ID
user_id = "gayathri"


# ============================================================
# TEST MESSAGES
# ============================================================

messages = [

    "I'm an ECE student and I'm learning AI and ML.",

    "I really like GenAI projects.",

    "bro today the weather is terrible 😂",

    "My goal is to get a core company placement.",

    "I like building IoT projects."

]


# ============================================================
# PROCESS EACH MESSAGE
# ============================================================

for message in messages:

    print(
        f"User: {message}"
    )


    process_memory(

        user_id=user_id,

        user_message=message

    )


    print(
        "-" * 60
    )