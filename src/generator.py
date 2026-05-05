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
    new_title = normalize(new_idea["title"])
    new_hook = normalize(new_idea["hook"])

    for entry in history:
        old_title = normalize(entry.get("title", ""))
        old_hook = normalize(entry.get("hook", ""))

        # exact match
        if new_title == old_title or new_hook == old_hook:
            return True

        # loose similarity
        if new_title in old_title or old_title in new_title:
            return True

    return False

# ---------- GENERATION ----------

def generate():
    timestamp = str(datetime.now())

    # ⚠️ Placeholder (Codex will overwrite this with real AI output)
    ideas = [
        {
            "hook": f"Hook variation {i}",
            "script": f"Script variation {i}",
            "title": f"Title variation {i}",
            "score": 5 + (i % 5),  # simulate scores 5–9
            "tag": "AUTO"
        }
        for i in range(20)  # 🔥 generate 20 ideas
    ]

    # ---------- LOAD HISTORY ----------
    history = load_json("data/history.json")

    # ---------- FILTER ----------
    filtered = []

    for idea in ideas:
        if not is_duplicate_or_similar(idea, history):
            filtered.append(idea)

    # ---------- FALLBACK ----------
    if len(filtered) == 0:
        filtered = ideas[:3]

    # ---------- SORT BY SCORE ----------
    filtered.sort(key=lambda x: x["score"], reverse=True)

    # ---------- PICK TOP ----------
    final_ideas = filtered[:5]

    # ---------- OUTPUT BUILD ----------
    output_text = f"Generated: {timestamp}\n\n"

    for i, idea in enumerate(final_ideas, 1):
        output_text += f"""Idea {i}:
Hook: {idea['hook']}
Script: {idea['script']}
Title: {idea['title']}
Score: {idea['score']}
Tag: {idea['tag']}

"""

    save_output(output_text)

    # ---------- SAVE TO HISTORY ----------
    added = 0

    for idea in final_ideas:
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
        "ideas_after_filter": len(filtered),
        "ideas_saved": added
    })

    save_json("data/run_log.json", log)

    print(f"Generated {len(ideas)} → Saved {added} ideas")

# ---------- RUN ----------

if __name__ == "__main__":
    generate()
