import json
from datetime import datetime

# ---------- JSON HELPERS ----------

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_output(text):
    with open("output/results.txt", "w", encoding="utf-8") as f:
        f.write(text)

# ---------- DUPLICATE CHECK ----------

def is_duplicate(new_title, history):
    for entry in history:
        if entry.get("title") == new_title:
            return True
    return False

# ---------- MAIN GENERATOR ----------

def generate():
    timestamp = str(datetime.now())

    # ⚠️ Placeholder ideas (Codex will replace this later)
    ideas = [
        {
            "hook": "You think your dua won’t be accepted…",
            "script": "You still ask… but deep down you’ve already given up.\nSo what changed?\nYour situation… or your belief?",
            "title": "You Already Gave Up On This Dua?",
            "score": 8,
            "tag": "HIGH CURIOSITY"
        },
        {
            "hook": "You pray… but is it even accepted?",
            "script": "You stand there… say the words…\nbut your heart isn’t there.\nSo what are you really doing?",
            "title": "Is Your Salah Even Being Accepted?",
            "score": 9,
            "tag": "HIGH GUILT TRIGGER"
        }
    ]

    # Save readable output
    output_text = f"Generated: {timestamp}\n\n"
    for i, idea in enumerate(ideas, 1):
        output_text += f"""Idea {i}:
Hook: {idea['hook']}
Script: {idea['script']}
Title: {idea['title']}
Score: {idea['score']}
Tag: {idea['tag']}

"""

    save_output(output_text)

    # Load history
    history = load_json("data/history.json")

    # Add each idea separately (no duplicates)
    for idea in ideas:
        if not is_duplicate(idea["title"], history):
            history.append({
                "timestamp": timestamp,
                "hook": idea["hook"],
                "script": idea["script"],
                "title": idea["title"],
                "score": idea["score"],
                "tag": idea["tag"]
            })

    # Save updated history
    save_json("data/history.json", history)

    print("Saved ideas individually + avoided duplicates")

if __name__ == "__main__":
    generate()
