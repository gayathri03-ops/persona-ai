import os

from dotenv import load_dotenv
from google import genai

from backend.character.prompt_builder import build_system_prompt


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set in .env"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=api_key
)


# ============================================================
# NANI MODEL
# ============================================================

MODELS = [
    "gemini-flash-latest",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.7-flash"
]
# ============================================================
# ASK NANI
# ============================================================

def ask_nani(user_message):

    system_prompt = build_system_prompt()

    last_error = None

    for model in MODELS:

        try:

            response = client.models.generate_content(
                model=model,
                contents=user_message,
                config={
                    "system_instruction": system_prompt
                }
            )

            if response.text:
                return response.text.strip()

        except Exception as error:

            last_error = error

            # Don't disturb the user-facing chat.
            # Silently move to the next model.
            continue


    # Only show the technical error if ALL models fail.
    print(
        f"\nAll Nani models failed: {last_error}"
    )

    return "wait da 😭"


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\nNani AI started! "
        "Type 'exit' to stop.\n"
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


        reply = ask_nani(
            user_message
        )


        print(
            f"\nNani: {reply}\n"
        )