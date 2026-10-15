import json
from pathlib import Path


CHARACTER_FILE = Path(__file__).parent / "character.json"


def load_character():
    with open(CHARACTER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


character = load_character()


# if __name__ == "__main__":
#     print("Character loaded successfully!")
#     print("Name:", character["identity"]["name"])
#     print("Age:", character["identity"]["age"])
#     print("City:", character["identity"]["city"])
#     print("Occupation:", character["identity"]["occupation"])

if __name__ == "__main__":
    print("Name:", character["identity"]["name"])

    print("\nPersonality:")
    for trait in character["personality"]["traits"]:
        print("-", trait)

    print("\nTechnical Skills:")
    for skill in character["technical_profile"]["strong_areas"]:
        print("-", skill)

    print("\nLanguages:")
    for language in character["languages"]["fluent"]:
        print("-", language)