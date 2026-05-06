import os
from datetime import datetime

def generate():
    print("=== GENERATOR STARTED ===")

    # make sure folders exist
    os.makedirs("output", exist_ok=True)

    timestamp = str(datetime.now())

    ideas = [
        "You stopped expecting your dua to work.",
        "Your salah looks fine… but something’s missing.",
        "You keep delaying what you know is wrong.",
        "You say you want change… but do nothing.",
        "You’re doing this sin like it’s normal."
    ]

    output_text = f"Generated: {timestamp}\n\n"

    for i, idea in enumerate(ideas, 1):
        output_text += f"Idea {i}: {idea}\n\n"

    with open("output/results.txt", "w", encoding="utf-8") as f:
        f.write(output_text)

    print("=== FILE WRITTEN ===")
    print("Saved 5 ideas.")

if __name__ == "__main__":
    generate()
