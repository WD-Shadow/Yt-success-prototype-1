import json
from datetime import datetime
import hashlib
import os
import random

# ---------- SETUP ----------

def ensure_dirs():
    os.makedirs("output", exist_ok=True)
    os.makedirs("data", exist_ok=True)

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

# ---------- UTILS ----------

def normalize(text):
    return text.lower().strip()

def hash_text(text):
    return hashlib.md5(normalize(text).encode()).hexdigest()

def is_duplicate(idea, history):
    new_title = normalize(idea["title"])
    new_hook = normalize(idea["hook"])

    for entry in history:
        if normalize(entry.get("title", "")) == new_title and \
           normalize(entry.get("hook", "")) == new_hook:
            return True
    return False

# ---------- LOCAL IDEA ENGINE ----------

hooks_bank = [
    "You already gave up on this dua.",
    "Your salah looks fine… but something’s off.",
    "You keep delaying what you know is wrong.",
    "You say you want change… but do nothing.",
    "You’re doing this sin like it’s normal.",
    "You don’t even realise you’re doing this.",
    "You’re not struggling… you’re avoiding.",
    "You know this is wrong… but continue.",
    "You think it’s small… it’s not.",
    "You stopped caring without noticing."
]

scripts_bank = [
    "You tell yourself it's fine.\nBut you keep repeating it.\nSo what changed?",
    "You know the problem.\nYou just don’t fix it.\nWhy?",
    "You feel something’s wrong.\nBut ignore it.\nAgain.",
    "You delay it.\nAgain.\nAnd again.\nSo when does it stop?",
    "You act like it’s small.\nBut it’s consistent.\nThat’s the problem."
]

titles_bank = [
    "You Already Gave Up On This",
    "Something Is Wrong With This",
    "You Keep Ignoring This",
    "This Is Your Real Problem",
    "You’re Not Fixing This",
    "You Know This Is Wrong",
    "This Isn’t As Small As You Think"
]

def generate_local_ideas(n=10):
    ideas = []

    for _ in range(n):
        hook = random.choice(hooks_bank)
        script = random.choice(scripts_bank)
        title = random.choice(titles_bank)

        ideas.append({
            "hook": hook,
            "script": script,
            "title": title,
            "score": random.randint(6, 9),
            "tag": "LOCAL"
        })

    return ideas

# ---------- MAIN ----------

def generate():
    print("RUNNING LOCAL GENERATOR...")

    ensure_dirs()
    timestamp = str(datetime.now())

    history = load_json("data/history.json")

    ideas = generate_local_ideas(15)

    filtered = []
    for idea in ideas:
        if not is_duplicate(idea, history):
            filtered.append(idea)

    if len(filtered) == 0:
        filtered = ideas[:5]

    final = filtered[:5]

    # ---------- OUTPUT ----------
    output_text = f"Generated: {timestamp}\n\n"

    for i, idea in enumerate(final, 1):
        output_text += f"""Idea {i}:
Hook: {idea['hook']}
Script: {idea['script']}
Title: {idea['title']}
Score: {idea['score']}
Tag: {idea['tag']}

"""

    save_output(output_text)

    # ---------- SAVE ----------
    for idea in final:
        history.append({
            "id": hash_text(idea["title"] + timestamp),
            "timestamp": timestamp,
            "hook": idea["hook"],
            "script": idea["script"],
            "title": idea["title"],
            "score": idea["score"],
            "tag": idea["tag"]
        })

    save_json("data/history.json", history)

    print(f"Saved {len(final)} ideas.")

# ---------- RUN ----------

if __name__ == "__main__":
    generate()
