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

# ---------- IDEA COMPONENTS ----------

situations = [
    "you keep delaying something important",
    "you’re not focused in salah",
    "you’ve stopped expecting your dua to work",
    "you’re repeating the same sin",
    "you feel stuck but don’t change anything",
    "you know what’s wrong but ignore it",
]

twists = [
    "but you pretend it’s not a problem",
    "but your actions show something else",
    "but deep down you already gave up",
    "but you keep justifying it",
    "but nothing is actually changing",
]

endings = [
    "So what are you really doing?",
    "So what do you actually want?",
    "So why does this keep happening?",
    "So when does it stop?",
]

titles = [
    "This Is Your Real Problem",
    "You’re Not Being Honest About This",
    "This Is Why Nothing Changes",
    "You Keep Ignoring This",
    "This Is Where You’re Going Wrong",
]

# ---------- GENERATION ENGINE ----------

def build_idea():
    situation = random.choice(situations)
    twist = random.choice(twists)
    ending = random.choice(endings)

    hook = f"{situation.capitalize()}..."

    script = f"{situation.capitalize()}.\n{twist}.\n{ending}"

    title = random.choice(titles)

    return {
        "hook": hook,
        "script": script,
        "title": title,
        "score": random.randint(7, 9),
        "tag": "STRUCTURED"
    }

def generate_ideas(n=15):
    return [build_idea() for _ in range(n)]

# ---------- MAIN ----------

def generate():
    print("RUNNING STRUCTURED GENERATOR...")

    ensure_dirs()
    timestamp = str(datetime.now())

    ideas = generate_ideas(15)

    # keep top 5
    final = ideas[:5]

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
    history = load_json("data/history.json")

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
