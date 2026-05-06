import json
from datetime import datetime
import hashlib
import os

# ---------- FILE HELPERS ----------

def ensure_dirs():
    os.makedirs("output", exist_ok=True)
    os.makedirs("data", exist_ok=True)

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

# ---------- DUPLICATE CHECK ----------

def is_duplicate(new_idea, history):
    new_title = normalize(new_idea["title"])
    new_hook = normalize(new_idea["hook"])

    for entry in history:
        if normalize(entry.get("title", "")) == new_title and \
           normalize(entry.get("hook", "")) == new_hook:
            return True

    return False

# ---------- GENERATION ----------

def generate():
    print("RUNNING GENERATOR...")

    ensure_dirs()
    timestamp = str(datetime.now())

    # 🔥 HARD-CODED TEST IDEAS (guaranteed output)
    ideas = [
        {
            "hook": "You stopped expecting your dua to work.",
            "script": "You still raise your hands.\nBut deep down… you already gave up.\nSo why keep asking?",
            "title": "You Gave Up On This Dua Without Noticing",
            "score": 9,
            "tag": "TEST"
        },
        {
            "hook": "Your salah looks fine… but something is missing.",
            "script": "You stand.\nYou recite.\nBut your mind drifts away.\nSo what are you really doing?",
            "title": "Your Salah Isn’t What You Think",
            "score": 8,
            "tag": "TEST"
        },
        {
            "hook": "You say you want Jannah… but your actions disagree.",
            "script": "You know what to fix.\nBut you delay it.\nAgain and again.\nSo what do you actually want?",
            "title": "Your Actions Don’t Match Your Goal",
            "score": 9,
            "tag": "TEST"
        }
    ]

    history = load_json("data/history.json")

    # ---------- FILTER ----------
    filtered = []

    for idea in ideas:
        if not is_duplicate(idea, history):
            filtered.append(idea)

    # ---------- GUARANTEE OUTPUT ----------
    if len(filtered) == 0:
        filtered = ideas

    # ---------- OUTPUT ----------
    output_text = f"Generated: {timestamp}\n\n"

    for i, idea in enumerate(filtered, 1):
        output_text += f"""Idea {i}:
Hook: {idea['hook']}
Script: {idea['script']}
Title: {idea['title']}
Score: {idea['score']}
Tag: {idea['tag']}

"""

    save_output(output_text)

    # ---------- SAVE HISTORY ----------
    for idea in filtered:
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

    print(f"Saved {len(filtered)} ideas successfully.")

# ---------- RUN ----------

if __name__ == "__main__":
    generate()
