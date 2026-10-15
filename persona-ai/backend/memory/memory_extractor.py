import json
import time
import os

from google import genai
from dotenv import load_dotenv

from .memory_manager import remember


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)


# Try models in this order
MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite"
]

# ============================================================
# MEMORY EXTRACTION PROMPT
# ============================================================

MEMORY_EXTRACTION_PROMPT = """
You are a memory extraction system.

Your job is NOT to reply to the user.

Your job is to decide whether the user's message contains
stable information that would be useful in future conversations.

Remember useful long-term information such as:

- name
- education
- career
- skills
- goals
- interests
- hobbies
- preferences
- important habits
- important relationships
- long-term projects

Do NOT remember:

- greetings
- casual jokes
- temporary moods
- weather
- random daily events
- ordinary conversation
- irrelevant information

Never invent information.

Return ONLY valid JSON.

If useful memory exists:

{
    "should_remember": true,
    "memory": "short factual statement",
    "memory_type": "goal",
    "importance": 3
}

If it is not useful:

{
    "should_remember": false,
    "memory": "",
    "memory_type": "general",
    "importance": 0
}

Allowed memory_type values:

identity
education
skill
goal
interest
preference
relationship
habit
project
general

Importance:

1 = low
2 = medium
3 = high
"""


# ============================================================
# EXTRACT MEMORY
# ============================================================

def extract_memory(user_message):

    last_error = None

    for model in MODELS:

        print(f"\nTrying memory model: {model}")

        for attempt in range(2):

            try:

                config = {
                    "system_instruction": MEMORY_EXTRACTION_PROMPT,
                    "response_mime_type": "application/json"
                }

                if hasattr(client, "chats") and hasattr(client.chats, "create"):
                    chat = client.chats.create(
                        model=model,
                        config=config
                    )
                    response = chat.send_message(user_message)
                else:
                    response = client.models.generate_content(
                        model=model,
                        contents=user_message,
                        config=config
                    )

                if not response.text:

                    return {
                        "should_remember": False,
                        "memory": "",
                        "memory_type": "general",
                        "importance": 0
                    }

                result = json.loads(response.text)

                return result

            except Exception as error:

                last_error = error

                print(
                    f"Memory model {model} failed "
                    f"(attempt {attempt + 1}/2): {error}"
                )

                if attempt < 1:
                    time.sleep(2)

        print(
            f"Trying next memory model..."
        )


    print(
        f"\nAll memory models failed."
        f"\nLast error: {last_error}"
    )

    return {
        "should_remember": False,
        "memory": "",
        "memory_type": "general",
        "importance": 0
    }


# ============================================================
# PROCESS MEMORY
# ============================================================

def process_memory(
    user_id,
    user_message
):

    result = extract_memory(
        user_message
    )

    if not result.get(
        "should_remember",
        False
    ):
        return False

    memory = result.get(
        "memory",
        ""
    ).strip()

    if not memory:
        return False

    memory_type = result.get(
        "memory_type",
        "general"
    )

    importance = result.get(
        "importance",
        1
    )

    saved = remember(
        user_id=user_id,
        memory=memory,
        memory_type=memory_type,
        importance=importance
    )

    if saved:

        print(
            f"\n[Memory saved] {memory}"
        )

    else:

        print(
            f"\n[Memory already exists] {memory}"
        )

    return saved