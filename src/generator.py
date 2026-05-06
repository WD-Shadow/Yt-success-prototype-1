def generate():
    timestamp = str(datetime.now())

    # 🔥 HARD TEST DATA (guarantees output)
    ideas = [
        {
            "hook": "You stopped expecting your dua to work.",
            "script": "You still raise your hands.\nBut deep down… you already decided it won’t happen.\nSo why keep asking?",
            "title": "You Gave Up On This Dua Without Noticing",
            "score": 9,
            "tag": "TEST"
        },
        {
            "hook": "Your salah looks fine… but something is missing.",
            "script": "You stand.\nYou recite.\nBut your mind is somewhere else.\nSo what are you really offering?",
            "title": "Your Salah Isn’t What You Think",
            "score": 8,
            "tag": "TEST"
        },
        {
            "hook": "You say you want Jannah… but your actions disagree.",
            "script": "You know what to fix.\nYou just delay it.\nAgain and again.\nSo what do you really want?",
            "title": "Your Actions Don’t Match Your Goal",
            "score": 9,
            "tag": "TEST"
        }
    ]

    history = load_json("data/history.json")

    filtered = []
    for idea in ideas:
        if not is_duplicate_or_similar(idea, history):
            filtered.append(idea)

    # 🔥 GUARANTEE OUTPUT
    if len(filtered) == 0:
        filtered = ideas

    final_ideas = filtered[:5]

    # ---------- OUTPUT ----------
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

    # ---------- SAVE ----------
    added = 0
    for idea in final_ideas:
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

    print(f"Saved {added} ideas (baseline mode)")
