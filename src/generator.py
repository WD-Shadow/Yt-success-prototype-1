import json
from datetime import datetime
import hashlib

# ---------- FILE HELPERS ----------

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

# ---------- NORMALISATION ----------

def normalize(text):
    return text.lower().strip()

def hash_text(text):
    return hashlib.md5(normalize(text).encode()).hexdigest()

# ---------- DUPLICATE + SIMILARITY ----------

def is_duplicate_or_similar(new_idea, history):
    new_title_hash = hash_text(new_idea["title"])
    new_hook_hash = hash_text(new_idea["hook"])

    for entry in history:
        if hash_text(entry.get("title", "")) == new_title_hash:
            return True
        if hash_text(entry.get("hook", "")) == new_hook_hash:
            return True

    return False

# ---------- GENERATION ----------

def generate():
    timestamp = str(datetime.now())

    # ⚠️ Placeholder (Codex will overwrite this later)
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

    # ---------- OUTPUT BUILD ----------

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

    # ---------- HISTORY UPDATE ----------

    history = load_json("data/history.json")
    added = 0

    for idea in ideas:
        if not is_duplicate_or_similar(idea, history):
            history.append({
                "id": hash_text(idea["title"] + timestamp),
                "timestamp": timestamp,
                "hook": idea["hook"],
                "script": idea["script"],
                "title": idea["title"],
                "score": idea["score"],
                "tag": idea["tag"]
            })
            added += 1

    save_json("data/history.json", history)

    # ---------- RUN LOG ----------

    log = load_json("data/run_log.json")

    log.append({
        "timestamp": timestamp,
        "ideas_generated": len(ideas),
        "ideas_saved": added
    })

    save_json("data/run_log.json", log)

    print(f"Saved {added} new ideas (duplicates filtered)")

if __name__ == "__main__":
    generate()
