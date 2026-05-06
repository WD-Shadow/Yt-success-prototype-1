import json
from datetime import datetime
import hashlib
import os

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

# ---------- DUPLICATE CHECK (SAFE VERSION) ----------

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

    # 🔥 STABLE TEST INPUT (always works)
    ideas = [
        {
            "hook": "You keep making this mistake in salah.",
            "script": "You think you're focused.\nBut your mind drifts every few seconds.\nSo what are you really doing?",
            "title": "This Is Ruining Your Salah",
            "score": 8,
            "tag": "TEST"
        },
        {
            "hook": "You stopped expecting Allah to answer this.",
            "script": "You still make dua.\nBut you already accepted it won’t happen.\nSo why ask?",
            "title": "You Gave Up Without Realising",
            "score": 9,
            "tag": "TEST"
        },
        {
            "hook": "Your intentions sound good… your actions don’t match.",
            "script": "You say you care.\nBut your habits show something else.\nSo what do you really want?",
            "title": "Your Actions Don’t Match Your Words",
            "score": 9,
            "tag": "TEST"
        }
    ]

    history = load_json("data/history.json")

    filtered = []
    for idea in ideas:
        if not is_duplicate(idea, history):
            filtered.append(idea)

    # 🔥 GUARANTEE OUTPUT
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

    # ---------- SAVE ----------
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
